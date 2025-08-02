# =============================================================================
# APLICAÇÃO LINKIFY - VERSÃO DEMO (SEM BANCO DE DADOS)
# =============================================================================

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
import os
import string
import secrets
from datetime import datetime
from typing import Dict

# Armazenamento em memória (para demo)
links_storage: Dict[str, dict] = {}
users_storage: Dict[str, dict] = {}

# Cria a aplicação FastAPI
app = FastAPI(
    title="Linkify - URL Shortener (Demo)",
    description="A modern URL shortener - Demo version",
    version="1.0.0-demo",
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
else:
    print(f"⚠️  Static files directory not found: {static_path}")

# Templates Jinja2
if os.path.exists(template_path):
    templates = Jinja2Templates(directory=template_path)
else:
    print(f"⚠️  Templates directory not found: {template_path}")
    templates = None

def generate_short_slug(length=6):
    """Gera um slug único para o link encurtado"""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# =============================================================================
# ROTAS BÁSICAS
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página inicial"""
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return HTMLResponse("""
        <html><head><title>Linkify Demo</title></head>
        <body><h1>🔗 Linkify Demo is Running!</h1>
        <p>Visit <a href="/api/docs">/api/docs</a> for API documentation</p>
        <p>Visit <a href="/health">/health</a> for health check</p>
        </body></html>
        """)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de login"""
    if templates:
        return templates.TemplateResponse("login.html", {"request": request})
    else:
        return HTMLResponse("<h1>Login page - Templates not found</h1>")

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Página de registro"""
    if templates:
        return templates.TemplateResponse("register.html", {"request": request})
    else:
        return HTMLResponse("<h1>Register page - Templates not found</h1>")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard do usuário"""
    if templates:
        return templates.TemplateResponse("dashboard.html", {"request": request})
    else:
        return HTMLResponse("<h1>Dashboard - Templates not found</h1>")

@app.post("/api/shorten")
async def create_short_link_demo(request: Request):
    """Cria um link encurtado (versão demo)"""
    try:
        data = await request.json()
        original_url = data.get("original_url")
        
        if not original_url:
            return {"success": False, "message": "URL is required"}
        
        # Gera slug único
        short_slug = generate_short_slug(6)
        while short_slug in links_storage:
            short_slug = generate_short_slug(6)
        
        # Armazena em memória
        links_storage[short_slug] = {
            "original_url": original_url,
            "created_at": datetime.now().isoformat(),
            "clicks": 0
        }
        
        # Constrói URL completa
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        short_url = f"{base_url}/{short_slug}"
        
        return {
            "success": True,
            "message": "Link shortened successfully",
            "short_url": short_url,
            "original_url": original_url
        }
    
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.get("/{short_slug}")
async def redirect_to_original(short_slug: str):
    """Redireciona para a URL original"""
    if short_slug in links_storage:
        link_data = links_storage[short_slug]
        link_data["clicks"] += 1  # Incrementa contador
        return RedirectResponse(url=link_data["original_url"], status_code=307)
    else:
        return {"error": "Short URL not found"}

@app.get("/api/stats")
async def get_stats():
    """Retorna estatísticas básicas"""
    total_links = len(links_storage)
    total_clicks = sum(link["clicks"] for link in links_storage.values())
    
    return {
        "total_links": total_links,
        "total_clicks": total_clicks,
        "links": list(links_storage.items())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "service": "linkify-demo",
        "version": "1.0.0-demo",
        "total_links": len(links_storage)
    }

# =============================================================================
# STARTUP
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Eventos executados na inicialização da aplicação"""
    print("🚀 Linkify URL Shortener (Demo) is starting up...")
    print("🔗 API Documentation: http://localhost:8000/api/docs")
    print("🌐 Frontend: http://localhost:8000")
    print("📊 Stats: http://localhost:8000/api/stats")
    print("❤️  Health: http://localhost:8000/health")
    print("")
    print("⚠️  DEMO MODE: Data is stored in memory only!")
    print("💾 To use with database, install PostgreSQL and Redis")

if __name__ == "__main__":
    uvicorn.run(
        "demo_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
