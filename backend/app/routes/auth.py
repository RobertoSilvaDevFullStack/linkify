# =============================================================================
# ROTAS PARA AUTENTICAÇÃO DE USUÁRIOS
# =============================================================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db, ACCESS_TOKEN_EXPIRE_MINUTES
from models import User
from schemas import UserCreate, User as UserSchema, Token, MessageResponse
from auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token,
    get_current_user
)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=MessageResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário
    """
    # Verifica se username já existe
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Verifica se email já existe
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Cria novo usuário
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return MessageResponse(
        success=True,
        message="User registered successfully"
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login do usuário e geração de token JWT
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retorna informações do usuário atual
    """
    return current_user

@router.get("/verify-token")
async def verify_token_endpoint(current_user: User = Depends(get_current_user)):
    """
    Verifica se o token é válido
    """
    return MessageResponse(
        success=True,
        message=f"Token is valid for user: {current_user.username}"
    )
