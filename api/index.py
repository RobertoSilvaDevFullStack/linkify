from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def read_root():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Linkify - Funcionando!</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 50px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: rgba(255,255,255,0.95);
                color: #333;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                max-width: 500px;
            }
            h1 { color: #667eea; }
            .status { 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 10px; 
                margin: 20px 0; 
            }
            .btn {
                background: #667eea;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                margin: 5px;
                text-decoration: none;
                display: inline-block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔗 Linkify</h1>
            <p><strong>Deploy no Vercel: FUNCIONANDO! ✅</strong></p>
            
            <div class="status">
                <h3>Status do Sistema</h3>
                <p>✅ FastAPI: Ativo</p>
                <p>✅ Vercel: Funcionando</p>
                <p>✅ API: Respondendo</p>
                <p>⚠️ Database: Precisa configurar</p>
                <p>⚠️ OAuth: Precisa configurar</p>
            </div>
            
            <div>
                <a href="/health" class="btn">Health Check</a>
                <a href="/docs" class="btn">API Docs</a>
            </div>
            
            <p><small>Versão simplificada funcionando. Configure DATABASE_URL para versão completa.</small></p>
        </div>
    </body>
    </html>
    """, status_code=200)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Linkify API funcionando no Vercel",
        "version": "1.0.0",
        "timestamp": "2025-08-02"
    }

@app.get("/test")
def test_endpoint():
    return {"message": "Teste OK - API respondendo corretamente!"}

# Handler direto para Vercel
handler = app
