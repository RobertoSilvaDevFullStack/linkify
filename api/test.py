from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        if self.path == '/health':
            response = {
                'status': 'ok',
                'message': 'Linkify API funcionando!',
                'service': 'linkify-vercel'
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/api':
            response = {
                'message': 'API Linkify',
                'endpoints': ['/health', '/', '/api'],
                'status': 'online'
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            # Página principal HTML
            html_content = """
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>🔗 Linkify - Funcionando!</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        margin: 0; padding: 0; min-height: 100vh;
                        display: flex; align-items: center; justify-content: center;
                    }
                    .container {
                        background: rgba(255,255,255,0.95); color: #333;
                        padding: 40px; border-radius: 20px;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
                        text-align: center; max-width: 600px; width: 90%;
                    }
                    h1 { color: #667eea; font-size: 2.5rem; margin-bottom: 1rem; }
                    .status { background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; }
                    .status-item { display: flex; justify-content: space-between; margin: 10px 0; }
                    .success { color: #28a745; font-weight: bold; }
                    .warning { color: #ffc107; font-weight: bold; }
                    .btn {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; padding: 12px 25px; border: none; border-radius: 25px;
                        margin: 10px; text-decoration: none; display: inline-block;
                        transition: all 0.3s; font-weight: bold;
                    }
                    .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
                </style>
            </head>
            <body>
                <div class="container">
                    <div style="font-size: 4rem; margin-bottom: 20px;">🔗</div>
                    <h1>Linkify</h1>
                    <p style="font-size: 1.2rem; margin-bottom: 30px;">
                        <strong>✅ DEPLOY NO VERCEL FUNCIONANDO!</strong>
                    </p>
                    
                    <div class="status">
                        <h3>📊 Status do Sistema</h3>
                        <div class="status-item">
                            <span>🐍 Python Handler</span>
                            <span class="success">✅ Funcionando</span>
                        </div>
                        <div class="status-item">
                            <span>☁️ Vercel Deploy</span>
                            <span class="success">✅ Ativo</span>
                        </div>
                        <div class="status-item">
                            <span>🌐 API Endpoints</span>
                            <span class="success">✅ Respondendo</span>
                        </div>
                        <div class="status-item">
                            <span>🗄️ Database</span>
                            <span class="warning">⏳ Aguardando configuração</span>
                        </div>
                        <div class="status-item">
                            <span>🔐 OAuth</span>
                            <span class="warning">⏳ Aguardando configuração</span>
                        </div>
                    </div>
                    
                    <div style="margin: 30px 0;">
                        <a href="/health" class="btn">🏥 Health Check</a>
                        <a href="/api" class="btn">📡 API Info</a>
                    </div>
                    
                    <div style="background: #e9ecef; padding: 20px; border-radius: 10px; margin-top: 30px;">
                        <h4>🚀 Próximos Passos:</h4>
                        <p style="text-align: left; margin: 10px 0;">
                            1. ✅ <strong>Deploy Base:</strong> Concluído<br>
                            2. ⏳ <strong>Database:</strong> Configurar PostgreSQL no Vercel<br>
                            3. ⏳ <strong>OAuth:</strong> Adicionar credenciais Google/GitHub<br>
                            4. ⏳ <strong>Funcionalidade Completa:</strong> Ativar após configurações
                        </p>
                    </div>
                    
                    <p style="margin-top: 30px; color: #6c757d; font-size: 0.9rem;">
                        🎯 <strong>Linkify v1.0</strong> - Encurtador de URLs Inteligente<br>
                        Desenvolvido por Roberto Silva
                    </p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        
        return
