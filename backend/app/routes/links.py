# =============================================================================
# ROTAS PARA GERENCIAMENTO DE LINKS
# =============================================================================

from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db, get_redis, LINK_EXPIRY_DAYS, SHORT_URL_LENGTH
from ..models import User, Link
from ..schemas import (
    LinkCreate, 
    Link as LinkSchema, 
    LinkCreateResponse,
    LinkListResponse,
    MessageResponse,
    UserStatsResponse
)
from ..auth import get_current_user, normalize_url, is_valid_url

router = APIRouter(tags=["links"])

@router.post("/shorten", response_model=LinkCreateResponse)
async def create_short_link(
    link_data: LinkCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis_client = Depends(get_redis)
):
    """
    Cria um link encurtado
    """
    # Normaliza e valida a URL
    original_url = normalize_url(str(link_data.original_url))
    
    if not is_valid_url(original_url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL format"
        )
    
    # Gera slug único
    max_attempts = 10
    for _ in range(max_attempts):
        short_slug = Link.generate_short_slug(SHORT_URL_LENGTH)
        
        # Verifica se slug já existe no banco
        if not db.query(Link).filter(Link.short_slug == short_slug).first():
            break
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not generate unique short URL"
        )
    
    # Cria o link no banco
    expiration_date = datetime.utcnow() + timedelta(days=LINK_EXPIRY_DAYS)
    db_link = Link(
        original_url=original_url,
        short_slug=short_slug,
        user_id=current_user.id,
        expiration_date=expiration_date
    )
    
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    # Armazena no Redis para acesso rápido
    redis_key = f"link:{short_slug}"
    redis_client.setex(
        redis_key,
        int(timedelta(days=LINK_EXPIRY_DAYS).total_seconds()),
        original_url
    )
    
    # Constrói URL completa
    base_url = f"{request.url.scheme}://{request.url.netloc}"
    short_url = f"{base_url}/{short_slug}"
    
    return LinkCreateResponse(
        success=True,
        message="Link shortened successfully",
        link=LinkSchema.from_orm(db_link),
        short_url=short_url
    )

@router.get("/{short_slug}")
async def redirect_to_original(
    short_slug: str,
    db: Session = Depends(get_db),
    redis_client = Depends(get_redis)
):
    """
    Redireciona para a URL original
    """
    # Primeiro tenta buscar no Redis (cache)
    redis_key = f"link:{short_slug}"
    original_url = redis_client.get(redis_key)
    
    if original_url:
        # Incrementa contador de cliques (assíncrono)
        db_link = db.query(Link).filter(Link.short_slug == short_slug).first()
        if db_link:
            db_link.clicks_count += 1
            db.commit()
        
        return RedirectResponse(url=original_url, status_code=307)
    
    # Se não encontrou no Redis, busca no banco
    db_link = db.query(Link).filter(Link.short_slug == short_slug).first()
    
    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found"
        )
    
    # Verifica se o link expirou
    if datetime.utcnow() > db_link.expiration_date:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This short URL has expired"
        )
    
    # Incrementa contador de cliques
    db_link.clicks_count += 1
    db.commit()
    
    # Recoloca no Redis
    redis_client.setex(
        redis_key,
        int((db_link.expiration_date - datetime.utcnow()).total_seconds()),
        db_link.original_url
    )
    
    return RedirectResponse(url=db_link.original_url, status_code=307)

@router.get("/user/links", response_model=LinkListResponse)
async def get_user_links(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna todos os links do usuário atual
    """
    links = db.query(Link).filter(
        Link.user_id == current_user.id
    ).order_by(desc(Link.creation_date)).all()
    
    return LinkListResponse(
        success=True,
        links=links,
        total=len(links)
    )

@router.delete("/user/links/{link_id}", response_model=MessageResponse)
async def delete_link(
    link_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis_client = Depends(get_redis)
):
    """
    Deleta um link do usuário
    """
    db_link = db.query(Link).filter(
        Link.id == link_id,
        Link.user_id == current_user.id
    ).first()
    
    if not db_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    # Remove do Redis
    redis_key = f"link:{db_link.short_slug}"
    redis_client.delete(redis_key)
    
    # Remove do banco
    db.delete(db_link)
    db.commit()
    
    return MessageResponse(
        success=True,
        message="Link deleted successfully"
    )

@router.get("/user/stats", response_model=UserStatsResponse)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna estatísticas do usuário
    """
    links = db.query(Link).filter(Link.user_id == current_user.id).all()
    
    total_links = len(links)
    total_clicks = sum(link.clicks_count for link in links)
    active_links = len([link for link in links if datetime.utcnow() <= link.expiration_date])
    expired_links = total_links - active_links
    
    return UserStatsResponse(
        total_links=total_links,
        total_clicks=total_clicks,
        active_links=active_links,
        expired_links=expired_links
    )
