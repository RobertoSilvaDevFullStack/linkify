import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, List

try:
    import bcrypt
    from passlib.context import CryptContext
    from passlib.hash import bcrypt as passlib_bcrypt
    from fastapi import FastAPI, HTTPException, Depends, Request, Form, status
    from fastapi.responses import HTMLResponse, RedirectResponse
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.middleware.sessions import SessionMiddleware
    from jose import JWTError, jwt
    from pydantic import BaseModel, EmailStr
    from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine, Text
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, Session, relationship
    from sqlalchemy.sql import func
    import httpx
    import string
    import random
except ImportError as e:
    print(f"⚠️ Erro ao importar dependências: {e}")
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    app = FastAPI()
    
    @app.get("/")
    def fallback_root():
        return {"error": "Dependências não instaladas", "message": "Instale as dependências do requirements.txt"}
    
    handler = app
    exit()

# Configurações
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-for-vercel')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup com fallback para Vercel
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("⚠️ DATABASE_URL não configurada. Usando modo demo.")
    DATABASE_URL = 'sqlite:///./linkify_demo.db'

# Converter postgres:// para postgresql:// se necessário
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Configurar engine com tratamento de erro
try:
    if DATABASE_URL.startswith('postgresql://'):
        engine = create_engine(DATABASE_URL)
        print("✅ PostgreSQL configurado")
    else:
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        print("✅ SQLite configurado")
except Exception as e:
    print(f"⚠️ Erro na configuração do banco: {e}")
    DATABASE_URL = 'sqlite:///./linkify_fallback.db'
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(title="Linkify", description="Encurtador de URLs profissional")

# Session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:8000", 
        "http://127.0.0.1:8000",
        "https://*.vercel.app",
        "https://linkify-rho.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Templates com fallback
try:
    templates = Jinja2Templates(directory="frontend/templates")
    # Static files
    app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
except Exception as e:
    print(f"⚠️ Templates/Static não encontrados: {e}")
    templates = None

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    oauth_provider = Column(String, nullable=True)
    oauth_id = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    
    links = relationship("Link", back_populates="owner")

class Link(Base):
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_code = Column(String, unique=True, index=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    owner = relationship("User", back_populates="links")

# Criar tabelas
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
except Exception as e:
    print(f"⚠️ Database initialization error: {e}")

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class LinkCreate(BaseModel):
    original_url: str
    custom_code: Optional[str] = None
    expires_at: Optional[datetime] = None

class LinkResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class StatsResponse(BaseModel):
    total_links: int
    total_clicks: int
    active_links: int

# Utility functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuração de hash de senha
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
except:
    # Fallback para bcrypt direto
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def generate_short_code() -> str:
    return secrets.token_urlsafe(6)

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if templates:
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except:
            pass
    
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Linkify - Encurtador de URLs</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: rgba(255,255,255,0.95);
                color: #333;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                max-width: 600px;
            }
            h1 { color: #667eea; }
            .status { 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 10px; 
                margin: 20px 0; 
            }
            .btn {
                background: #667eea;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                margin: 5px;
                text-decoration: none;
                display: inline-block;
            }
            .form-group {
                margin: 15px 0;
                text-align: left;
            }
            input {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 5px;
            }
            .result {
                background: #e8f5e8;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
                word-break: break-all;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔗 Linkify</h1>
            <p><strong>Encurtador de URLs Profissional</strong></p>
            
            <div class="status">
                <h3>Status do Sistema</h3>
                <p>✅ FastAPI: Ativo</p>
                <p>✅ Vercel: Funcionando</p>
                <p>✅ API: Respondendo</p>
                <p>✅ Database: Configurado</p>
            </div>
            
            <form id="linkForm" onsubmit="createLink(event)">
                <div class="form-group">
                    <label>URL para encurtar:</label>
                    <input type="url" id="originalUrl" placeholder="https://exemplo.com/url-muito-longa" required>
                </div>
                <div class="form-group">
                    <label>Código personalizado (opcional):</label>
                    <input type="text" id="customCode" placeholder="meulink">
                </div>
                <button type="submit" class="btn">Encurtar URL</button>
            </form>
            
            <div id="result" class="result" style="display:none;"></div>
            
            <div>
                <a href="/health" class="btn">Health Check</a>
                <a href="/docs" class="btn">API Docs</a>
                <a href="/dashboard" class="btn">Dashboard</a>
            </div>
        </div>
        
        <script>
        async function createLink(event) {
            event.preventDefault();
            const originalUrl = document.getElementById('originalUrl').value;
            const customCode = document.getElementById('customCode').value;
            
            try {
                const formData = new FormData();
                formData.append('original_url', originalUrl);
                if (customCode) formData.append('custom_code', customCode);
                
                const response = await fetch('/api/links/demo', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('result').innerHTML = `
                        <h4>✅ Link criado com sucesso!</h4>
                        <p><strong>URL Original:</strong> ${data.original_url}</p>
                        <p><strong>Link Encurtado:</strong> <a href="${data.short_url}" target="_blank">${data.short_url}</a></p>
                        <p><strong>Código:</strong> ${data.short_code}</p>
                    `;
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('linkForm').reset();
                } else {
                    throw new Error(data.detail || 'Erro ao criar link');
                }
            } catch (error) {
                document.getElementById('result').innerHTML = `
                    <h4>❌ Erro</h4>
                    <p>${error.message}</p>
                `;
                document.getElementById('result').style.display = 'block';
            }
        }
        </script>
    </body>
    </html>
    """, status_code=200)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if templates:
        try:
            return templates.TemplateResponse("dashboard.html", {"request": request})
        except:
            pass
    return HTMLResponse("<h1>Dashboard em desenvolvimento</h1><a href='/'>Voltar</a>")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if templates:
        try:
            return templates.TemplateResponse("login.html", {"request": request})
        except:
            pass
    return HTMLResponse("<h1>Login em desenvolvimento</h1><a href='/'>Voltar</a>")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Linkify API funcionando no Vercel",
        "version": "2.0.0",
        "database": "connected" if DATABASE_URL else "not configured",
        "timestamp": datetime.utcnow().isoformat()
    }

# API Routes
@app.post("/api/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar se usuário já existe
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email ou username já cadastrado")
    
    # Criar novo usuário
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login", response_model=Token)
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/links", response_model=LinkResponse)
def create_link(link: LinkCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verificar se código personalizado já existe
    if link.custom_code:
        existing = db.query(Link).filter(Link.short_code == link.custom_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Código personalizado já existe")
        short_code = link.custom_code
    else:
        # Gerar código único
        while True:
            short_code = generate_short_code()
            existing = db.query(Link).filter(Link.short_code == short_code).first()
            if not existing:
                break
    
    db_link = Link(
        original_url=link.original_url,
        short_code=short_code,
        expires_at=link.expires_at,
        owner_id=current_user.id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

@app.post("/api/links/demo")
def create_demo_link(original_url: str = Form(...), custom_code: Optional[str] = Form(None), db: Session = Depends(get_db)):
    # Versão demo sem autenticação
    if custom_code:
        existing = db.query(Link).filter(Link.short_code == custom_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Código personalizado já existe")
        short_code = custom_code
    else:
        while True:
            short_code = generate_short_code()
            existing = db.query(Link).filter(Link.short_code == short_code).first()
            if not existing:
                break
    
    db_link = Link(
        original_url=original_url,
        short_code=short_code,
        owner_id=None  # Demo sem usuário
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Retornar com URL completa
    base_url = "https://linkify-rho.vercel.app"  # Ajuste para seu domínio
    return {
        "id": db_link.id,
        "original_url": db_link.original_url,
        "short_code": db_link.short_code,
        "short_url": f"{base_url}/{db_link.short_code}",
        "clicks": db_link.clicks,
        "created_at": db_link.created_at,
        "is_active": db_link.is_active
    }

@app.get("/api/links", response_model=list[LinkResponse])
def get_links(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    links = db.query(Link).filter(Link.owner_id == current_user.id).all()
    return links

@app.delete("/api/links/{link_id}")
def delete_link(link_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.id == link_id, Link.owner_id == current_user.id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")
    db.delete(link)
    db.commit()
    return {"message": "Link deletado com sucesso"}

@app.get("/api/stats", response_model=StatsResponse)
def get_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_links = db.query(Link).filter(Link.owner_id == current_user.id)
    total_links = user_links.count()
    total_clicks = sum(link.clicks for link in user_links.all())
    active_links = user_links.filter(Link.is_active == True).count()
    
    return StatsResponse(
        total_links=total_links,
        total_clicks=total_clicks,
        active_links=active_links
    )

@app.get("/{short_code}")
def redirect_link(short_code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code, Link.is_active == True).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link não encontrado")
    
    # Verificar se expirou
    if link.expires_at and datetime.utcnow() > link.expires_at:
        raise HTTPException(status_code=410, detail="Link expirado")
    
    # Incrementar contador de cliques
    link.clicks += 1
    db.commit()
    
    return RedirectResponse(url=link.original_url, status_code=302)

# Handler direto para Vercel
handler = app
