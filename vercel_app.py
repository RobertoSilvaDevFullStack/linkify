"""
Configuração específica para Vercel
"""
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import app
except ImportError as e:
    print(f"Erro na importação: {e}")
    # Fallback para uma app básica
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    def health_check():
        return {"status": "error", "message": "Failed to import main app"}

# Export para Vercel
vercel_app = app
