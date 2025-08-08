#!/usr/bin/env python3
"""
Script de setup para Linkify
Detecta o ambiente e instala as dependências corretas
"""
import os
import sys
import subprocess
import platform

def run_command(command, description=""):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso")
            return True
        else:
            print(f"❌ {description} - Erro:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False

def main():
    print("🚀 Setup do Linkify")
    print("=" * 50)
    
    # Detectar sistema operacional
    system = platform.system()
    print(f"💻 Sistema: {system}")
    
    # Atualizar pip
    run_command("pip install --upgrade pip", "Atualizando pip")
    
    # Instalar dependências básicas
    basic_deps = [
        "fastapi==0.104.1",
        "uvicorn==0.24.0", 
        "sqlalchemy==2.0.23",
        "bcrypt==4.1.1",
        "python-jose[cryptography]==3.3.0",
        "python-multipart==0.0.6",
        "jinja2==3.1.2",
        "authlib==1.3.0",
        "requests-oauthlib==1.3.1",
        "httpx==0.25.2",
        "python-dotenv==1.0.0",
        "starlette==0.27.0",
        "itsdangerous==2.1.2",
        "supabase==2.3.4"
    ]
    
    print("\n📦 Instalando dependências básicas...")
    for dep in basic_deps:
        run_command(f"pip install {dep}", f"Instalando {dep.split('==')[0]}")
    
    # Tentar instalar PostgreSQL driver
    print("\n🗄️  Configurando driver PostgreSQL...")
    if system == "Windows":
        # Windows - tentar psycopg2-binary primeiro, depois psycopg2
        if not run_command("pip install psycopg2-binary==2.9.9", "Instalando psycopg2-binary"):
            if not run_command("pip install psycopg2==2.9.9", "Instalando psycopg2"):
                print("⚠️  PostgreSQL driver não instalado. Usando SQLite para desenvolvimento.")
    else:
        # Linux/Mac
        run_command("pip install psycopg2-binary==2.9.9", "Instalando psycopg2-binary")
    
    # Criar .env se não existir
    if not os.path.exists('.env'):
        print("\n📝 Criando arquivo .env...")
        try:
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Arquivo .env criado. Configure suas variáveis!")
        except Exception as e:
            print(f"❌ Erro ao criar .env: {e}")
    
    print("\n🎉 Setup concluído!")
    print("\n📋 Próximos passos:")
    print("1. Configure o arquivo .env com suas credenciais")
    print("2. Execute: python main.py")
    print("3. Acesse: http://localhost:8001")
    
    print("\n🔗 Links úteis:")
    print("- Supabase: https://supabase.com")
    print("- Documentação: README.md")
    print("- Setup Supabase: SUPABASE_SETUP.md")

if __name__ == "__main__":
    main()
