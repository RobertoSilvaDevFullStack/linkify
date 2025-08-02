# =============================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS - VERSÃO SQLITE
# =============================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from typing import Dict

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do banco SQLite
DATABASE_URL = "sqlite:///./linkify.db"

# Engine do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Cache em memória (substitui Redis temporariamente)
memory_cache: Dict[str, str] = {}

def get_db():
    """
    Dependency para obter sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_cache():
    """
    Dependency para obter cache (substitui Redis)
    """
    return memory_cache

def create_tables():
    """
    Cria todas as tabelas no banco de dados
    """
    from models import Base
    Base.metadata.create_all(bind=engine)

# Configurações gerais
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production-make-it-very-long-and-random")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
LINK_EXPIRY_DAYS = int(os.getenv("LINK_EXPIRY_DAYS", "30"))
SHORT_URL_LENGTH = int(os.getenv("SHORT_URL_LENGTH", "6"))
