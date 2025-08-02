#!/usr/bin/env python3
"""
Script de preparação para deploy no Vercel
Execute: python setup_production.py
"""

import os
import json
import subprocess
import sys

def create_file_if_not_exists(filepath, content):
    """Cria arquivo se não existir"""
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Criado: {filepath}")
    else:
        print(f"⚠️  Já existe: {filepath}")

def main():
    print("🚀 Preparando Linkify para produção no Vercel...")
    print("=" * 50)
    
    # 1. Verificar se estamos no diretório correto
    if not os.path.exists("main.py"):
        print("❌ Erro: Execute este script no diretório do projeto Linkify")
        sys.exit(1)
    
    # 2. Criar/verificar arquivos necessários
    print("\n📁 Verificando arquivos de deploy...")
    
    # vercel.json
    vercel_config = """{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "./"
  }
}"""
    create_file_if_not_exists("vercel.json", vercel_config)
    
    # api/index.py
    os.makedirs("api", exist_ok=True)
    api_index = """from main import app

# Vercel requer que o app esteja em api/index.py
handler = app"""
    create_file_if_not_exists("api/index.py", api_index)
    
    # requirements.txt
    requirements = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
bcrypt==4.1.1
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
jinja2==3.1.2
authlib==1.3.0
requests-oauthlib==1.3.1
httpx==0.25.2
python-dotenv==1.0.0
starlette==0.27.0
itsdangerous==2.1.2
psycopg2-binary==2.9.9"""
    create_file_if_not_exists("requirements.txt", requirements)
    
    # .env.example
    env_example = """# OAuth Credentials - SUBSTITUA PELOS VALORES REAIS
GOOGLE_CLIENT_ID=seu-google-client-id-real
GOOGLE_CLIENT_SECRET=seu-google-client-secret-real
GITHUB_CLIENT_ID=seu-github-client-id-real
GITHUB_CLIENT_SECRET=seu-github-client-secret-real
MICROSOFT_CLIENT_ID=seu-microsoft-client-id-real
MICROSOFT_CLIENT_SECRET=seu-microsoft-client-secret-real
APPLE_CLIENT_ID=seu-apple-client-id-real
APPLE_CLIENT_SECRET=seu-apple-client-secret-real

# App Security
SECRET_KEY=sua-chave-super-secreta-aqui-256bits

# Database (PostgreSQL para produção)
DATABASE_URL=postgresql://usuario:senha@host:5432/linkify

# Vercel
VERCEL_ENV=production"""
    create_file_if_not_exists(".env.example", env_example)
    
    # .gitignore
    gitignore = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Database
*.db
*.sqlite3

# Environment variables
.env
.env.local
.env.production
.env.staging

# Vercel
.vercel

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Dependencies
node_modules/"""
    create_file_if_not_exists(".gitignore", gitignore)
    
    print("\n🔧 Arquivos de configuração criados!")
    
    # 3. Verificar dependências
    print("\n📦 Verificando instalação do Vercel CLI...")
    try:
        result = subprocess.run(["vercel", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Vercel CLI instalado: {result.stdout.strip()}")
        else:
            print("❌ Vercel CLI não encontrado")
            print("💡 Instale com: npm i -g vercel")
    except FileNotFoundError:
        print("❌ Vercel CLI não encontrado")
        print("💡 Instale com: npm i -g vercel")
    
    # 4. Próximos passos
    print("\n" + "=" * 50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("=" * 50)
    print("1. Configure OAuth nos provedores (veja OAUTH_PRODUCTION.md)")
    print("2. Configure banco PostgreSQL (Neon/Supabase)")
    print("3. Suba código para GitHub")
    print("4. Conecte repositório no Vercel")
    print("5. Configure Environment Variables no Vercel")
    print("6. Deploy: vercel --prod")
    print("\n📚 Guias detalhados:")
    print("   - DEPLOY_VERCEL.md (guia completo)")
    print("   - OAUTH_PRODUCTION.md (configuração OAuth)")
    print("\n🚀 Seu Linkify estará online em breve!")

if __name__ == "__main__":
    main()
