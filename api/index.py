"""
Entrada principal para Vercel - Versão robusta
"""
import os
import sys

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

print(f"📍 Current directory: {current_dir}")
print(f"📁 Parent directory: {parent_dir}")
print(f"🐍 Python path: {sys.path}")

# Tentar importar aplicação principal
try:
    print("🔄 Tentando importar aplicação principal...")
    from simple_app import app
    print("✅ Aplicação importada com sucesso!")
    
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    print("🔄 Criando aplicação de fallback...")
    
    from fastapi import FastAPI
    app = FastAPI(title="Linkify Fallback")
    
    @app.get("/")
    def fallback():
        return {
            "status": "fallback_mode",
            "error": str(e),
            "message": "Aplicação em modo de emergência",
            "python_path": sys.path,
            "current_dir": current_dir
        }

# Handler para Vercel
def handler(event, context):
    return app

# Export da aplicação
__all__ = ["app", "handler"]

# Para teste local
if __name__ == "__main__":
    print("🧪 Teste local da aplicação Vercel")
    print(f"App type: {type(app)}")
    print("✅ Aplicação carregada com sucesso!")
