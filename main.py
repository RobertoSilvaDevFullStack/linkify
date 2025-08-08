import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from authlib.integrations.starlette_client import OAuth
import httpx
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Importar configuração OAuth
from oauth_config import setup_oauth, OAUTH_CONFIG

# Configurações
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./linkify.db')

# Converter postgres:// para postgresql:// se necessário (Heroku/Railway)
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

print(f"🗄️  Database: {DATABASE_URL.split('@')[0]}@[hidden]" if '@' in DATABASE_URL else f"🗄️  Database: {DATABASE_URL}")

# Configurar engine baseado no tipo de banco
try:
    if DATABASE_URL.startswith('postgresql://'):
        # Tentar importar psycopg2
        try:
            import psycopg2
            engine = create_engine(DATABASE_URL)
            print("✅ PostgreSQL configurado com psycopg2")
        except ImportError:
            print("⚠️  psycopg2 não encontrado. Usando SQLite para desenvolvimento.")
            DATABASE_URL = 'sqlite:///./linkify.db'
            engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        print("✅ SQLite configurado para desenvolvimento")
except Exception as e:
    print(f"⚠️  Erro na configuração do banco: {e}")
    print("🔄 Usando SQLite como fallback")
    DATABASE_URL = 'sqlite:///./linkify.db'
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI app
app = FastAPI(title="Linkify", description="Encurtador de URLs profissional")

# Session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-in-production")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:8000", 
        "http://127.0.0.1:8000",
        "https://*.vercel.app",  # Permite todos os subdomínios do Vercel
        "https://linkify-rho.vercel.app",  # Seu domínio específico (atualize)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar OAuth
oauth = setup_oauth(app)

# Security
security = HTTPBearer()

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# Static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)  # Pode ser null para OAuth
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Campos OAuth
    oauth_provider = Column(String, nullable=True)  # google, github, microsoft, apple
    oauth_id = Column(String, nullable=True)  # ID do usuário no provedor OAuth
    avatar_url = Column(String, nullable=True)  # URL da foto de perfil
    full_name = Column(String, nullable=True)  # Nome completo do usuário
    
    # Relationship
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
    
    # Relationship
    owner = relationship("User", back_populates="links")

# Create tables
Base.metadata.create_all(bind=engine)

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

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth functions
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
        username = payload.get("sub")
        if username is None or not isinstance(username, str):
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def generate_short_code() -> str:
    return secrets.token_urlsafe(6)

# Create test user if not exists
def create_test_user():
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == "testuser").first()
    if not existing_user:
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hash_password("testpass123")
        )
        db.add(test_user)
        db.commit()
        print("✅ Test user created: testuser / testpass123")
    db.close()

# Routes

# Frontend Routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Página inicial"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard principal"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)  
async def login_page(request: Request):
    """Página de login"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    """Página de analytics"""
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Página de configurações"""
    return templates.TemplateResponse("settings.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    """Página de perfil"""
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/debug", response_class=HTMLResponse)
async def debug_page(request: Request):
    """Página de debug para testar autenticação"""
    return templates.TemplateResponse("debug.html", {"request": request})

# API Routes

# Auth endpoints
@app.post("/api/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Registrar novo usuário"""
    # Check if user exists
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create user
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
    """Login do usuário"""
    user = db.query(User).filter(User.username == username).first()
    hashed_password = getattr(user, 'hashed_password', None) if user else None
    if not user or not hashed_password or not verify_password(password, str(hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.get("/api/user/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Obter perfil do usuário"""
    return current_user

# Link endpoints
@app.post("/api/links", response_model=LinkResponse)
def create_link(link: LinkCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Criar novo link encurtado"""
    # Generate or use custom short code
    if link.custom_code:
        existing_link = db.query(Link).filter(Link.short_code == link.custom_code).first()
        if existing_link:
            raise HTTPException(status_code=400, detail="Custom code already exists")
        short_code = link.custom_code
    else:
        while True:
            short_code = generate_short_code()
            existing_link = db.query(Link).filter(Link.short_code == short_code).first()
            if not existing_link:
                break
    
    # Create link
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
    """Criar link demo para usuários não autenticados (temporário, 1 hora)"""
    # Generate or use custom short code
    if custom_code:
        existing_link = db.query(Link).filter(Link.short_code == custom_code).first()
        if existing_link:
            raise HTTPException(status_code=400, detail="Custom code already exists")
        short_code = custom_code
    else:
        while True:
            short_code = generate_short_code()
            existing_link = db.query(Link).filter(Link.short_code == short_code).first()
            if not existing_link:
                break
    
    # Create temporary link (expires in 1 hour, no owner)
    from datetime import datetime, timedelta
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    db_link = Link(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at,
        owner_id=None  # No owner for demo links
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    return {
        "id": db_link.id,
        "original_url": db_link.original_url,
        "short_code": db_link.short_code,
        "clicks": db_link.clicks,
        "created_at": db_link.created_at.isoformat(),
        "expires_at": db_link.expires_at.isoformat() if db_link.expires_at is not None else None
    }

@app.get("/api/links", response_model=list[LinkResponse])
def get_links(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Obter links do usuário"""
    links = db.query(Link).filter(Link.owner_id == current_user.id).order_by(Link.created_at.desc()).all()
    return links

@app.delete("/api/links/{link_id}")
def delete_link(link_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Deletar link"""
    link = db.query(Link).filter(Link.id == link_id, Link.owner_id == current_user.id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    db.delete(link)
    db.commit()
    return {"message": "Link deleted successfully"}

@app.get("/api/stats", response_model=StatsResponse)
def get_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Obter estatísticas do usuário"""
    total_links = db.query(Link).filter(Link.owner_id == current_user.id).count()
    total_clicks = db.query(Link).filter(Link.owner_id == current_user.id).with_entities(Link.clicks).all()
    total_clicks = sum([click[0] for click in total_clicks])
    active_links = db.query(Link).filter(Link.owner_id == current_user.id, Link.is_active == True).count()
    
    return StatsResponse(
        total_links=total_links,
        total_clicks=total_clicks,
        active_links=active_links
    )

# Redirect endpoint
@app.get("/{short_code}")
def redirect_link(short_code: str, db: Session = Depends(get_db)):
    """Redirecionar link encurtado"""
    link = db.query(Link).filter(Link.short_code == short_code, Link.is_active == True).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # Check if expired
    expires_at = getattr(link, 'expires_at')
    if expires_at is not None and datetime.utcnow() > expires_at:
        raise HTTPException(status_code=410, detail="Link expired")
    
    # Increment clicks using update query
    db.query(Link).filter(Link.id == link.id).update({Link.clicks: Link.clicks + 1})
    db.commit()
    
    return RedirectResponse(url=str(link.original_url), status_code=302)

# ====== ROTAS OAUTH2 ======

@app.get("/auth/{provider}")
async def oauth_login(provider: str, request: Request):
    """Inicia o login OAuth com o provedor especificado"""
    if provider not in ['google', 'github', 'microsoft', 'apple']:
        raise HTTPException(status_code=400, detail="Provedor não suportado")
    
    # Verificar se as credenciais OAuth estão configuradas
    config = OAUTH_CONFIG.get(provider, {})
    client_id = config.get('client_id', '')
    if not client_id or client_id.startswith('seu-'):
        # Redirecionar para login com mensagem de erro
        return RedirectResponse(url="/?error=oauth_not_configured", status_code=302)
    
    try:
        # URL de callback
        redirect_uri = request.url_for('oauth_callback', provider=provider)
        
        # Obter cliente OAuth
        client = oauth.create_client(provider)
        if not client:
            raise HTTPException(status_code=500, detail="Erro na configuração OAuth")
        
        return await client.authorize_redirect(request, redirect_uri)
    
    except Exception as e:
        print(f"Erro OAuth {provider}: {str(e)}")
        return RedirectResponse(url="/?error=oauth_failed", status_code=302)

@app.get("/auth/{provider}/callback")
async def oauth_callback(provider: str, request: Request):
    """Callback OAuth para processar o retorno do provedor"""
    if provider not in ['google', 'github', 'microsoft', 'apple']:
        raise HTTPException(status_code=400, detail="Provedor não suportado")
    
    try:
        # Obter cliente OAuth
        client = oauth.create_client(provider)
        if not client:
            raise HTTPException(status_code=500, detail="Erro na configuração OAuth")
        
        # Obter token do provedor
        token = await client.authorize_access_token(request)
        
        # Obter informações do usuário
        user_info = await get_user_info_from_provider(client, token, provider)
        
        if user_info is None:
            raise HTTPException(status_code=500, detail="Erro ao obter dados do usuário")
        
        # Criar ou encontrar usuário no banco
        db = SessionLocal()
        try:
            user = get_or_create_oauth_user(db, user_info, provider)
            
            # Criar token JWT
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            
            # Redirecionar para dashboard com token
            response = RedirectResponse(url="/dashboard", status_code=302)
            
            # Detectar se está em produção (HTTPS)
            is_production = os.getenv('VERCEL_ENV') == 'production' or request.url.scheme == 'https'
            
            response.set_cookie(
                key="linkify_token",
                value=access_token,
                httponly=True,
                secure=is_production,  # HTTPS em produção
                samesite="lax",
                max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )
            
            return response
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"Erro OAuth {provider}: {str(e)}")
        # Redirecionar para login com erro
        return RedirectResponse(url="/?error=oauth_failed", status_code=302)

async def get_user_info_from_provider(client, token, provider: str) -> Optional[dict]:
    """Obtém informações do usuário do provedor OAuth"""
    try:
        if provider == 'google':
            resp = await client.parse_id_token(token)
            return {
                'id': str(resp['sub']),
                'email': resp['email'],
                'name': resp.get('name', ''),
                'picture': resp.get('picture', ''),
                'username': resp['email'].split('@')[0]
            }
        
        elif provider == 'github':
            # Obter dados do usuário
            user_resp = await client.get('user', token=token)
            user_data = user_resp.json()
            
            # Obter email (pode estar privado)
            email_resp = await client.get('user/emails', token=token)
            emails = email_resp.json()
            primary_email = next((email['email'] for email in emails if email['primary']), user_data.get('email'))
            
            return {
                'id': str(user_data['id']),
                'email': primary_email,
                'name': user_data.get('name', ''),
                'picture': user_data.get('avatar_url', ''),
                'username': user_data.get('login', primary_email.split('@')[0] if primary_email else 'user')
            }
        
        elif provider == 'microsoft':
            resp = await client.parse_id_token(token)
            return {
                'id': str(resp['sub']),
                'email': resp['email'],
                'name': resp.get('name', ''),
                'picture': '',  # Microsoft não fornece foto no token ID
                'username': resp['email'].split('@')[0]
            }
        
        elif provider == 'apple':
            resp = await client.parse_id_token(token)
            return {
                'id': str(resp['sub']),
                'email': resp['email'],
                'name': resp.get('name', ''),
                'picture': '',  # Apple não fornece foto
                'username': resp['email'].split('@')[0]
            }
    
    except Exception as e:
        print(f"Erro ao obter dados do usuário {provider}: {str(e)}")
        return None

def get_or_create_oauth_user(db: Session, user_info: dict, provider: str):
    """Cria ou encontra usuário OAuth no banco de dados"""
    # Procurar usuário existente por OAuth ID ou email
    user = db.query(User).filter(
        (User.oauth_provider == provider) & (User.oauth_id == user_info['id'])
    ).first()
    
    if not user:
        # Procurar por email existente
        user = db.query(User).filter(User.email == user_info['email']).first()
        if user:
            # Atualizar usuário existente com dados OAuth usando update query
            db.query(User).filter(User.id == user.id).update({
                User.oauth_provider: provider,
                User.oauth_id: user_info['id'],
                User.avatar_url: user_info.get('picture', ''),
                User.full_name: user_info.get('name', '')
            })
            db.commit()
            db.refresh(user)
        else:
            # Criar novo usuário
            username = user_info['username']
            counter = 1
            original_username = username
            
            # Garantir username único
            while db.query(User).filter(User.username == username).first():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User(
                username=username,
                email=user_info['email'],
                oauth_provider=provider,
                oauth_id=user_info['id'],
                avatar_url=user_info.get('picture', ''),
                full_name=user_info.get('name', ''),
                is_active=True
            )
            db.add(user)
    
    db.commit()
    db.refresh(user)
    return user

# Inicialização automática do banco em produção
try:
    # Criar tabelas automaticamente
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"⚠️  Database initialization warning: {e}")

if __name__ == "__main__":
    # Create test user
    create_test_user()
    
    # Create frontend directories
    os.makedirs("frontend/templates", exist_ok=True)
    os.makedirs("frontend/static", exist_ok=True)
    
    print("🚀 Starting Linkify server...")
    print("📱 Frontend: http://localhost:8001")
    print("🔧 API Docs: http://localhost:8001/docs")
    print("👤 Test Login: testuser / testpass123")
    
    uvicorn.run(app, host="127.0.0.1", port=8001)
