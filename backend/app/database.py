# =============================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# =============================================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import redis
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do banco PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://linkify:linkify123@localhost:5432/linkify_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Engine do SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Conexão Redis
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def get_db():
    """
    Dependency para obter sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    """
    Dependency para obter cliente Redis
    """
    return redis_client

def create_tables():
    """
    Cria todas as tabelas no banco de dados
    """
    from models import Base
    Base.metadata.create_all(bind=engine)

# Configurações gerais
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
LINK_EXPIRY_DAYS = int(os.getenv("LINK_EXPIRY_DAYS", "30"))
SHORT_URL_LENGTH = int(os.getenv("SHORT_URL_LENGTH", "6"))
