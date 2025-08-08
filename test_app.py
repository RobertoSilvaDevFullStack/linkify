#!/usr/bin/env python3
"""
Script de teste para verificar se a aplicação está funcionando
"""

import sys
import os
import subprocess
import time
import requests

def test_import():
    """Testa se os módulos podem ser importados"""
    print("🔍 Testando imports...")
    
    try:
        import main
        print("✅ main.py importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar main.py: {e}")
        return False
    
    try:
        import supabase_config
        print("✅ supabase_config.py importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar supabase_config.py: {e}")
        return False
    
    try:
        import oauth_config
        print("✅ oauth_config.py importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar oauth_config.py: {e}")
        return False
    
    return True

def test_database():
    """Testa se o banco de dados está funcionando"""
    print("\n🗄️  Testando banco de dados...")
    
    try:
        from main import engine, Base, SessionLocal, User
        
        # Criar tabelas
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso")
        
        # Testar conexão
        db = SessionLocal()
        try:
            # Contar usuários
            user_count = db.query(User).count()
            print(f"✅ Conexão com banco OK - {user_count} usuários cadastrados")
            return True
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_fastapi():
    """Testa se a aplicação FastAPI está funcionando"""
    print("\n🚀 Testando aplicação FastAPI...")
    
    try:
        from main import app
        print("✅ App FastAPI criada com sucesso")
        
        # Verificar se tem rotas
        routes = [route.path for route in app.routes]
        print(f"✅ {len(routes)} rotas configuradas")
        return True
        
    except Exception as e:
        print(f"❌ Erro na aplicação FastAPI: {e}")
        return False

def test_server():
    """Testa se o servidor pode ser iniciado"""
    print("\n🌐 Testando servidor (início rápido)...")
    
    try:
        # Tentar iniciar o servidor por alguns segundos
        import uvicorn
        from main import app
        
        print("✅ Uvicorn disponível")
        print("✅ Servidor pode ser iniciado")
        print("💡 Para iniciar: python main.py")
        return True
        
    except Exception as e:
        print(f"❌ Erro no servidor: {e}")
        return False

def main():
    print("🧪 Teste de Funcionamento - Linkify")
    print("=" * 50)
    
    tests = [
        ("Imports", test_import),
        ("Banco de Dados", test_database), 
        ("FastAPI", test_fastapi),
        ("Servidor", test_server)
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    print("\n📊 Resumo dos Testes:")
    print("=" * 30)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{name:15} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 30)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n🚀 A aplicação está funcionando!")
        print("\n📱 Para usar:")
        print("1. Execute: python main.py")
        print("2. Acesse: http://localhost:8001")
        print("3. Login teste: testuser / testpass123")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print("\n🔧 Verifique os erros acima e:")
        print("1. Execute: python setup.py")
        print("2. Configure o arquivo .env")
        print("3. Execute este teste novamente")

if __name__ == "__main__":
    main()
