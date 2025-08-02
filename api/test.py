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
            # Interface completa do Linkify
            html_content = """
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>🔗 Linkify - Encurtador de URLs</title>
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh; color: #333;
                    }
                    .header {
                        background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);
                        padding: 20px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1);
                    }
                    .header h1 { color: white; font-size: 2.5rem; margin-bottom: 0.5rem; }
                    .header p { color: rgba(255,255,255,0.8); font-size: 1.2rem; }
                    .container {
                        max-width: 800px; margin: 50px auto; padding: 0 20px;
                    }
                    .card {
                        background: rgba(255,255,255,0.95); padding: 40px;
                        border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.2);
                        margin-bottom: 30px;
                    }
                    .url-form {
                        display: flex; gap: 15px; margin-bottom: 30px;
                        flex-wrap: wrap;
                    }
                    .url-input {
                        flex: 1; min-width: 300px; padding: 15px 20px;
                        border: 2px solid #e0e0e0; border-radius: 10px;
                        font-size: 1rem; outline: none; transition: all 0.3s;
                    }
                    .url-input:focus { border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
                    .shorten-btn {
                        padding: 15px 30px; background: linear-gradient(135deg, #667eea, #764ba2);
                        color: white; border: none; border-radius: 10px;
                        font-size: 1rem; font-weight: 600; cursor: pointer;
                        transition: all 0.3s; text-decoration: none; display: inline-block;
                    }
                    .shorten-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102,126,234,0.3); }
                    .features {
                        display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                        gap: 20px; margin-top: 30px;
                    }
                    .feature {
                        padding: 20px; background: #f8f9fa; border-radius: 15px;
                        text-align: center; transition: all 0.3s;
                    }
                    .feature:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
                    .feature-icon { font-size: 2.5rem; margin-bottom: 15px; }
                    .feature h3 { color: #667eea; margin-bottom: 10px; }
                    .demo-section {
                        background: rgba(255,255,255,0.1); padding: 30px;
                        border-radius: 15px; margin-top: 30px; text-align: center;
                    }
                    .demo-url {
                        background: rgba(255,255,255,0.9); padding: 15px 20px;
                        border-radius: 10px; margin: 10px; display: inline-block;
                        color: #667eea; font-weight: 600; text-decoration: none;
                    }
                    .demo-url:hover { background: white; }
                    .status-grid {
                        display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 15px; margin: 20px 0;
                    }
                    .status-item {
                        background: #f8f9fa; padding: 15px; border-radius: 10px;
                        display: flex; justify-content: space-between; align-items: center;
                    }
                    .success { color: #28a745; font-weight: bold; }
                    .warning { color: #ffc107; font-weight: bold; }
                    .footer {
                        text-align: center; padding: 30px; color: rgba(255,255,255,0.7);
                    }
                    @media (max-width: 768px) {
                        .url-form { flex-direction: column; }
                        .url-input { min-width: auto; }
                        .header h1 { font-size: 2rem; }
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🔗 Linkify</h1>
                    <p>Encurtador de URLs - Simples, Rápido e Confiável</p>
                </div>

                <div class="container">
                    <div class="card">
                        <h2 style="text-align: center; margin-bottom: 30px; color: #667eea;">Encurte sua URL</h2>
                        
                        <div class="url-form">
                            <input type="url" class="url-input" placeholder="Cole sua URL aqui (ex: https://exemplo.com)" id="urlInput">
                            <button class="shorten-btn" onclick="shortenUrl()">Encurtar URL</button>
                        </div>
                        
                        <div id="result" style="display: none; background: #d4edda; padding: 20px; border-radius: 10px; margin-top: 20px;">
                            <h3 style="color: #155724; margin-bottom: 15px;">✅ URL Encurtada com Sucesso!</h3>
                            <div style="display: flex; gap: 15px; align-items: center; flex-wrap: wrap;">
                                <input type="text" id="shortUrl" readonly style="flex: 1; padding: 10px; border: 1px solid #c3e6cb; border-radius: 5px; background: white;">
                                <button onclick="copyUrl()" style="padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">Copiar</button>
                            </div>
                        </div>
                    </div>

                    <div class="features">
                        <div class="feature">
                            <div class="feature-icon">⚡</div>
                            <h3>Rápido</h3>
                            <p>Encurte URLs instantaneamente com nossa tecnologia otimizada</p>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">📊</div>
                            <h3>Analytics</h3>
                            <p>Acompanhe cliques e estatísticas detalhadas de suas URLs</p>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">🔒</div>
                            <h3>Seguro</h3>
                            <p>Suas URLs são protegidas com criptografia e verificação</p>
                        </div>
                        <div class="feature">
                            <div class="feature-icon">🎯</div>
                            <h3>Personalizado</h3>
                            <p>Crie URLs personalizadas para sua marca ou projeto</p>
                        </div>
                    </div>

                    <div class="demo-section">
                        <h3 style="color: white; margin-bottom: 20px;">🚀 Exemplo de URLs Encurtadas</h3>
                        <a href="#" class="demo-url">https://linkify.app/abc123</a>
                        <a href="#" class="demo-url">https://linkify.app/xyz789</a>
                        <a href="#" class="demo-url">https://linkify.app/demo01</a>
                    </div>

                    <div class="card">
                        <h3 style="text-align: center; margin-bottom: 20px;">📈 Status do Sistema</h3>
                        <div class="status-grid">
                            <div class="status-item">
                                <span>🟢 Servidor</span>
                                <span class="success">Online</span>
                            </div>
                            <div class="status-item">
                                <span>🟢 API</span>
                                <span class="success">Funcionando</span>
                            </div>
                            <div class="status-item">
                                <span>🟡 Database</span>
                                <span class="warning">Config. Pendente</span>
                            </div>
                            <div class="status-item">
                                <span>🟡 OAuth</span>
                                <span class="warning">Config. Pendente</span>
                            </div>
                        </div>
                        <div style="text-align: center; margin-top: 20px;">
                            <a href="/health" class="shorten-btn" style="margin: 5px;">Health Check</a>
                            <a href="/api" class="shorten-btn" style="margin: 5px;">API Info</a>
                        </div>
                    </div>
                </div>

                <div class="footer">
                    <p>💜 Linkify v1.0 - Desenvolvido por Roberto Silva</p>
                    <p>Deploy no Vercel funcionando perfeitamente!</p>
                </div>

                <script>
                    function shortenUrl() {
                        const url = document.getElementById('urlInput').value;
                        if (!url) {
                            alert('Por favor, insira uma URL!');
                            return;
                        }
                        
                        // Simular encurtamento
                        const shortCode = Math.random().toString(36).substring(2, 8);
                        const shortUrl = `https://linkify.app/${shortCode}`;
                        
                        document.getElementById('shortUrl').value = shortUrl;
                        document.getElementById('result').style.display = 'block';
                        
                        // Scroll to result
                        document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
                    }
                    
                    function copyUrl() {
                        const shortUrl = document.getElementById('shortUrl');
                        shortUrl.select();
                        shortUrl.setSelectionRange(0, 99999);
                        navigator.clipboard.writeText(shortUrl.value);
                        
                        const btn = event.target;
                        const originalText = btn.textContent;
                        btn.textContent = 'Copiado!';
                        btn.style.background = '#28a745';
                        
                        setTimeout(() => {
                            btn.textContent = originalText;
                            btn.style.background = '#28a745';
                        }, 2000);
                    }
                    
                    // Auto-focus no input
                    document.getElementById('urlInput').focus();
                    
                    // Enter key support
                    document.getElementById('urlInput').addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            shortenUrl();
                        }
                    });
                </script>
            </body>
            </html>
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
            """
            self.wfile.write(html_content.encode('utf-8'))
        
        return
