"""
Entrada para Vercel - Versão serverless otimizada
"""
import os
import sys

# Configurar Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Criar aplicação FastAPI básica para Vercel
try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(title="Linkify", version="1.0.0")
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Templates
    templates = Jinja2Templates(directory=os.path.join(parent_dir, "frontend", "templates"))
    
    @app.get("/", response_class=HTMLResponse)
    async def home_page(request: Request):
        try:
            return templates.TemplateResponse("login.html", {"request": request})
        except Exception as e:
            return HTMLResponse(f"""
            <html>
                <head><title>Linkify</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <h1>🔗 Linkify</h1>
                    <p>Aplicação está funcionando no Vercel!</p>
                    <p><small>Versão simplificada - Configure DATABASE_URL para funcionalidade completa</small></p>
                    <br>
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                        <h3>✅ Status do Deploy</h3>
                        <p>✅ FastAPI: Funcionando</p>
                        <p>✅ Vercel: Ativo</p>
                        <p>⏳ Database: Aguardando configuração</p>
                        <p>⏳ OAuth: Aguardando configuração</p>
                    </div>
                </body>
            </html>
            """)
    
    @app.get("/health")
    async def health_check():
        return {
            "status": "ok",
            "message": "Linkify rodando no Vercel",
            "version": "1.0.0",
            "environment": "production"
        }
        
    @app.get("/test")
    async def test_route():
        return {"message": "Rota de teste funcionando!"}
        
    print("✅ Aplicação Vercel criada com sucesso!")
    
except Exception as e:
    print(f"❌ Erro crítico: {e}")
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    def emergency_fallback():
        return {"error": str(e), "status": "emergency_mode"}

# Export para Vercel
def handler(request):
    return app

# Compatibilidade
__all__ = ["app"]
