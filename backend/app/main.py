# =============================================================================
# APLICAÇÃO PRINCIPAL FASTAPI - LINKIFY
# =============================================================================

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

# Importa as rotas
from routes import auth, links
from database import create_tables

# Carrega variáveis de ambiente
load_dotenv()

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
    allow_origins=["*"],  # Em produção, especifique domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta arquivos estáticos
app.mount("/static", StaticFiles(directory="../../frontend/static"), name="static")

# Templates Jinja2
templates = Jinja2Templates(directory="../../frontend/templates")

# Inclui as rotas da API
app.include_router(auth.router, prefix="/api")
app.include_router(links.router, prefix="/api")

# Cria tabelas no banco de dados
create_tables()

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
# EVENTO DE INICIALIZAÇÃO
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Eventos executados na inicialização da aplicação"""
    print("🚀 Linkify URL Shortener is starting up...")
    print("📊 Database tables created successfully")
    print("🔗 API Documentation available at: /api/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos executados no encerramento da aplicação"""
    print("👋 Linkify URL Shortener is shutting down...")

if __name__ == "__main__":
    import uvicorn
    
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )
