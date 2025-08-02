# =============================================================================
# APLICAÇÃO PRINCIPAL FASTAPI - LINKIFY (VERSÃO SIMPLIFICADA)
# =============================================================================

import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importações locais
from database import get_db, create_tables, ACCESS_TOKEN_EXPIRE_MINUTES
from models import User, Link
from schemas import UserCreate, Token, MessageResponse, LinkCreate, LinkCreateResponse
from auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token,
    get_current_user,
    normalize_url,
    is_valid_url
)

# Cria a aplicação FastAPI
app = FastAPI(
    title="Linkify - URL Shortener",
    description="A modern URL shortener with user management",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta arquivos estáticos
app.mount("/static", StaticFiles(directory="../../frontend/static"), name="static")

# Templates Jinja2
templates = Jinja2Templates(directory="../../frontend/templates")

# Cria tabelas no banco de dados
try:
    create_tables()
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"⚠️ Database connection issue: {e}")
    print("📝 Make sure PostgreSQL is running and configured properly")

# =============================================================================
# ROTAS DE AUTENTICAÇÃO
# =============================================================================

@app.post("/api/auth/register", response_model=MessageResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    # Verifica se username já existe
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Verifica se email já existe
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Cria novo usuário
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return MessageResponse(success=True, message="User registered successfully")

@app.post("/api/auth/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login do usuário e geração de token JWT"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@app.get("/api/auth/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Retorna informações do usuário atual"""
    return current_user

# =============================================================================
# ROTAS PARA LINKS (SIMPLIFICADAS)
# =============================================================================

@app.post("/api/shorten", response_model=LinkCreateResponse)
async def create_short_link(
    link_data: LinkCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria um link encurtado"""
    # Normaliza e valida a URL
    original_url = normalize_url(str(link_data.original_url))
    
    if not is_valid_url(original_url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL format"
        )
    
    # Gera slug único
    short_slug = Link.generate_short_slug(6)
    
    # Verifica se slug já existe
    while db.query(Link).filter(Link.short_slug == short_slug).first():
        short_slug = Link.generate_short_slug(6)
    
    # Cria o link no banco
    db_link = Link(
        original_url=original_url,
        short_slug=short_slug,
        user_id=current_user.id
    )
    
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Constrói URL completa
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    short_url = f"{base_url}/{short_slug}"
    
    return LinkCreateResponse(
        success=True,
        message="Link shortened successfully",
        short_url=short_url
    )

@app.get("/api/user/links")
async def get_user_links(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna todos os links do usuário atual"""
    links = db.query(Link).filter(Link.user_id == current_user.id).all()
    return {"success": True, "links": links, "total": len(links)}

@app.get("/api/user/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna estatísticas do usuário"""
    links = db.query(Link).filter(Link.user_id == current_user.id).all()
    
    total_links = len(links)
    total_clicks = sum(link.clicks_count for link in links)
    active_links = total_links  # Simplified for now
    expired_links = 0  # Simplified for now
    
    return {
        "total_links": total_links,
        "total_clicks": total_clicks,
        "active_links": active_links,
        "expired_links": expired_links
    }

# =============================================================================
# ROTAS PARA O FRONTEND
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página inicial"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Página de registro"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard do usuário"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "linkify"}

# =============================================================================
# STARTUP
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Eventos executados na inicialização da aplicação"""
    print("🚀 Linkify URL Shortener is starting up...")
    print("🔗 API Documentation available at: http://localhost:8000/api/docs")
    print("🌐 Frontend available at: http://localhost:8000")

if __name__ == "__main__":
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main_simple:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )
