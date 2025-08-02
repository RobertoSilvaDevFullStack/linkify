# =============================================================================
# MODELOS DO BANCO DE DADOS - SQLAlchemy
# =============================================================================

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import secrets
import string

Base = declarative_base()

class User(Base):
    """
    Modelo para usuários do sistema
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento com links
    links = relationship("Link", back_populates="owner", cascade="all, delete-orphan")

class Link(Base):
    """
    Modelo para links encurtados
    """
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(Text, nullable=False)
    short_slug = Column(String(10), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime, nullable=False)
    clicks_count = Column(Integer, default=0)  # Bonus: contador de cliques
    
    # Relacionamento com usuário
    owner = relationship("User", back_populates="links")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'expiration_date' not in kwargs:
            # Define expiração para 30 dias por padrão
            self.expiration_date = datetime.utcnow() + timedelta(days=30)
    
    @staticmethod
    def generate_short_slug(length=6):
        """Gera um slug único para o link encurtado"""
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
