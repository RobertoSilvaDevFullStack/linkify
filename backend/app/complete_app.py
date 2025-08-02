# =============================================================================
# APLICAÇÃO PRINCIPAL FASTAPI - LINKIFY COMPLETA
# =============================================================================

import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importações locais
from database_sqlite import get_db, get_cache, create_tables, ACCESS_TOKEN_EXPIRE_MINUTES, LINK_EXPIRY_DAYS, SHORT_URL_LENGTH
from models import User, Link
from schemas import UserCreate, Token, MessageResponse, LinkCreate, LinkCreateResponse, Link as LinkSchema
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
static_path = os.path.abspath("../../frontend/static")
template_path = os.path.abspath("../../frontend/templates")

if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    print(f"✅ Static files mounted from: {static_path}")
else:
    print(f"⚠️  Static files directory not found: {static_path}")

# Templates Jinja2
if os.path.exists(template_path):
    templates = Jinja2Templates(directory=template_path)
    print(f"✅ Templates loaded from: {template_path}")
else:
    print(f"⚠️  Templates directory not found: {template_path}")
    templates = None

# Cria tabelas no banco de dados
try:
    create_tables()
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"⚠️ Database connection issue: {e}")

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
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

@app.get("/api/auth/verify-token")
async def verify_token_endpoint(current_user: User = Depends(get_current_user)):
    """Verifica se o token é válido"""
    return MessageResponse(
        success=True,
        message=f"Token is valid for user: {current_user.username}"
    )

# =============================================================================
# ROTAS PARA LINKS
# =============================================================================

@app.post("/api/shorten", response_model=LinkCreateResponse)
async def create_short_link(
    link_data: LinkCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    cache = Depends(get_cache)
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
    max_attempts = 10
    for _ in range(max_attempts):
        short_slug = Link.generate_short_slug(SHORT_URL_LENGTH)
        
        # Verifica se slug já existe no banco
        if not db.query(Link).filter(Link.short_slug == short_slug).first():
            break
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not generate unique short URL"
        )
    
    # Cria o link no banco
    expiration_date = datetime.utcnow() + timedelta(days=LINK_EXPIRY_DAYS)
    db_link = Link(
        original_url=original_url,
        short_slug=short_slug,
        user_id=current_user.id,
        expiration_date=expiration_date
    )
    
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Armazena no cache para acesso rápido
    cache_key = f"link:{short_slug}"
    cache[cache_key] = original_url
    
    # Constrói URL completa
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    short_url = f"{base_url}/{short_slug}"
    
    return LinkCreateResponse(
        success=True,
        message="Link shortened successfully",
        short_url=short_url
    )

@app.get("/{short_slug}")
async def redirect_to_original(
    short_slug: str,
    db: Session = Depends(get_db),
    cache = Depends(get_cache)
):
    """Redireciona para a URL original"""
    # Primeiro tenta buscar no cache
    cache_key = f"link:{short_slug}"
    original_url = cache.get(cache_key)
    
    if original_url:
        # Incrementa contador de cliques
        db_link = db.query(Link).filter(Link.short_slug == short_slug).first()
        if db_link:
            db_link.clicks_count += 1
            db.commit()
        
        return RedirectResponse(url=original_url, status_code=307)
    
    # Se não encontrou no cache, busca no banco
    db_link = db.query(Link).filter(Link.short_slug == short_slug).first()
    
    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )
    
    # Verifica se o link expirou
    if datetime.utcnow() > db_link.expiration_date:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This short URL has expired"
        )
    
    # Incrementa contador de cliques
    db_link.clicks_count += 1
    db.commit()
    
    # Recoloca no cache
    cache[cache_key] = db_link.original_url
    
    return RedirectResponse(url=db_link.original_url, status_code=307)

@app.get("/api/user/links")
async def get_user_links(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna todos os links do usuário atual"""
    links = db.query(Link).filter(
        Link.user_id == current_user.id
    ).order_by(Link.creation_date.desc()).all()
    
    # Converte para dict para evitar problemas de serialização
    links_data = []
    for link in links:
        links_data.append({
            "id": link.id,
            "original_url": link.original_url,
            "short_slug": link.short_slug,
            "user_id": link.user_id,
            "creation_date": link.creation_date,
            "expiration_date": link.expiration_date,
            "clicks_count": link.clicks_count
        })
    
    return {"success": True, "links": links_data, "total": len(links_data)}

@app.delete("/api/user/links/{link_id}")
async def delete_link(
    link_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    cache = Depends(get_cache)
):
    """Deleta um link do usuário"""
    db_link = db.query(Link).filter(
        Link.id == link_id,
        Link.user_id == current_user.id
    ).first()
    
    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    # Remove do cache
    cache_key = f"link:{db_link.short_slug}"
    cache.pop(cache_key, None)
    
    # Remove do banco
    db.delete(db_link)
    db.commit()
    
    return MessageResponse(
        success=True,
        message="Link deleted successfully"
    )

@app.get("/api/user/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna estatísticas do usuário"""
    links = db.query(Link).filter(Link.user_id == current_user.id).all()
    
    total_links = len(links)
    total_clicks = sum(link.clicks_count for link in links)
    
    # Count active and expired links
    active_links = 0
    expired_links = 0
    now = datetime.utcnow()
    
    for link in links:
        if now <= link.expiration_date:
            active_links += 1
        else:
            expired_links += 1
    
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
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return HTMLResponse("""
        <html><head><title>Linkify</title></head>
        <body>
        <h1>🔗 Linkify URL Shortener</h1>
        <p>Welcome to Linkify! API Documentation: <a href="/api/docs">/api/docs</a></p>
        </body></html>
        """)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login"""
    if templates:
        return templates.TemplateResponse("login.html", {"request": request})
    else:
        return HTMLResponse("<h1>Login - Use API at /api/docs</h1>")

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Página de registro"""
    if templates:
        return templates.TemplateResponse("register.html", {"request": request})
    else:
        return HTMLResponse("<h1>Register - Use API at /api/docs</h1>")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard do usuário"""
    if templates:
        return templates.TemplateResponse("dashboard.html", {"request": request})
    else:
        return HTMLResponse("<h1>Dashboard - Use API at /api/docs</h1>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "linkify",
        "version": "1.0.0-complete",
        "database": "sqlite",
        "cache": "memory"
    }

# =============================================================================
# STARTUP
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Eventos executados na inicialização da aplicação"""
    print("🚀 Linkify URL Shortener (Complete Version) is starting up...")
    print("🔗 API Documentation: http://localhost:8000/api/docs")
    print("🌐 Frontend: http://localhost:8000")
    print("📊 Health Check: http://localhost:8000/health")
    print("")
    print("✅ COMPLETE VERSION with Authentication!")
    print("💾 Database: SQLite (linkify.db)")
    print("🚀 Cache: In-Memory")

if __name__ == "__main__":
    uvicorn.run(
        "complete_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
