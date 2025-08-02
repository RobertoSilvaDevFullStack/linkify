# =============================================================================
# ESQUEMAS PYDANTIC PARA VALIDAÇÃO DE DADOS
# =============================================================================

from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime
from typing import Optional, List

# =============================================================================
# ESQUEMAS PARA USUÁRIOS
# =============================================================================

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserInDB(User):
    password_hash: str

# =============================================================================
# ESQUEMAS PARA LINKS
# =============================================================================

class LinkBase(BaseModel):
    original_url: HttpUrl

class LinkCreate(LinkBase):
    pass

class LinkUpdate(BaseModel):
    original_url: Optional[HttpUrl] = None

class Link(LinkBase):
    id: int
    short_slug: str
    user_id: int
    creation_date: datetime
    expiration_date: datetime
    clicks_count: int
    
    class Config:
        from_attributes = True

class LinkInDB(Link):
    pass

class LinkPublic(BaseModel):
    """Schema público para links (sem informações sensíveis)"""
    short_slug: str
    creation_date: datetime
    expiration_date: datetime
    clicks_count: int

# =============================================================================
# ESQUEMAS PARA AUTENTICAÇÃO
# =============================================================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# =============================================================================
# ESQUEMAS PARA RESPOSTAS DA API
# =============================================================================

class LinkCreateResponse(BaseModel):
    """Resposta ao criar um link"""
    success: bool
    message: str
    link: Optional[LinkPublic] = None
    short_url: Optional[str] = None

class LinkListResponse(BaseModel):
    """Resposta para listar links do usuário"""
    success: bool
    links: List[Link]
    total: int

class MessageResponse(BaseModel):
    """Resposta genérica com mensagem"""
    success: bool
    message: str

class UserStatsResponse(BaseModel):
    """Estatísticas do usuário"""
    total_links: int
    total_clicks: int
    active_links: int
    expired_links: int
