"""
Aplicação principal simplificada para Vercel
"""

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Criar app
app = FastAPI(title="Linkify", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000", 
        "https://*.vercel.app",
        "https://linkify-peach.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-for-sessions")

# Templates
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    try:
        return templates.TemplateResponse("login.html", {"request": request})
    except Exception as e:
        return HTMLResponse(f"""
        <html>
            <body>
                <h1>Linkify - Carregando...</h1>
                <p>Aplicação está inicializando. Error: {str(e)}</p>
                <p>Template directory: frontend/templates</p>
            </body>
        </html>
        """)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Linkify is running"}

# Tentativa de importar a aplicação completa
try:
    from main import *
    print("✅ Aplicação completa carregada")
except Exception as e:
    print(f"⚠️  Usando versão simplificada. Erro: {e}")
    
    @app.get("/error")
    async def show_error():
        return {"error": str(e), "message": "Aplicação em modo simplificado"}
