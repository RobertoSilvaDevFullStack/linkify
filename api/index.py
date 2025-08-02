"""
Entrada principal para Vercel - Versão de produção
"""
import os
import sys

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    # Importar a aplicação principal
    from main import app
    print("✅ Aplicação principal importada com sucesso!")
    
except Exception as e:
    print(f"❌ Erro ao importar main.py: {e}")
    
    # Fallback - criar aplicação básica
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    
    app = FastAPI(title="Linkify")
    
    @app.get("/", response_class=HTMLResponse)
    def fallback():
        return """
        <html>
            <head><title>Linkify - Carregando</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>🔗 Linkify</h1>
                <p>Aplicação está inicializando...</p>
                <p>Aguarde um momento.</p>
            </body>
        </html>
        """
    
    @app.get("/health")
    def health():
        return {"status": "fallback_mode", "error": str(e)}

# Handler para Vercel
def handler(event, context):
    return app

# Export da aplicação  
__all__ = ["app", "handler"]
