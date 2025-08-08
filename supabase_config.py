"""
Configuração do Supabase para Linkify
"""
import os
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

# Client do Supabase (será inicializado quando necessário)
supabase_client = None

def get_supabase_client():
    """
    Retorna o client do Supabase configurado
    Importa supabase apenas quando necessário
    """
    global supabase_client
    if supabase_client is None:
        try:
            from supabase import create_client
            if not SUPABASE_URL or not SUPABASE_KEY:
                raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
            supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except ImportError:
            print("⚠️ Supabase client não instalado. Execute: pip install supabase")
            return None
        except Exception as e:
            print(f"⚠️ Erro ao configurar Supabase: {e}")
            return None
    return supabase_client

def get_supabase_admin_client():
    """
    Retorna o client administrativo do Supabase (com service key)
    """
    try:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_SERVICE_KEY devem estar configurados")
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except ImportError:
        print("⚠️ Supabase client não instalado. Execute: pip install supabase")
        return None
    except Exception as e:
        print(f"⚠️ Erro ao configurar Supabase admin: {e}")
        return None

# Funções utilitárias para autenticação
async def verify_supabase_token(token: str) -> Optional[Any]:
    """
    Verifica um token JWT do Supabase
    """
    try:
        client = get_supabase_client()
        if client is None:
            return None
        response = client.auth.get_user(token)
        return response.user if response.user else None
    except Exception as e:
        print(f"Erro ao verificar token Supabase: {e}")
        return None

async def get_user_by_email(email: str) -> Optional[Any]:
    """
    Busca usuário por email no Supabase
    """
    try:
        client = get_supabase_admin_client()
        if client is None:
            return None
        response = client.auth.admin.list_users()
        for user in response:
            if user.email == email:
                return user
        return None
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
