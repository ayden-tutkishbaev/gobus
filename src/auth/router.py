from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select, func

from src.admin.permissions import require_role
from src.core.security import (
    hash_password,
    verify_password,
    create_access_token, 
    verify_access_token, 
    oauth2_scheme
)

from src.auth.schemas import UserCreate, UserPrivate, UserPublic, Token
from src.auth.models import User
from src.auth.enum import Role
from src.config import config

from typing import Annotated

from datetime import timedelta

from src.database.tools import tashkent_now
from src.dependencies import db_connection

import uuid


user = APIRouter()


@user.post(path="/create",
          response_model=UserPrivate,
          status_code=status.HTTP_201_CREATED,
          dependencies=[Depends(require_role("superadmin"))]
)
async def create_user(user: UserCreate, db: db_connection):
    result = await db.execute(
        select(User).where(User.username == user.username),
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists!"
        )
        
    new_user = User(
        username=user.username.lower(),
        phone_number=user.phone_number,
        password_hashed=hash_password(user.password),
        role=user.role,
    )    

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@user.post(path="/token", response_model=Token,
                     dependencies=[Depends(require_role("superadmin"))])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_connection,
):
    result = await db.execute(
            select(User).where(func.lower(User.username) == form_data.username.lower(),
        ),
    )
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.password_hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password!",
            headers={'WWW-Authenticate': "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=config.access_token_lifetime)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    
    user.last_login = tashkent_now()
    await db.commit()

    return Token(access_token=access_token, token_type="bearer")


@user.get(path="/me", response_model=UserPrivate, 
        dependencies=[Depends(require_role("superadmin"))])
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: db_connection
):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid/expired token!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    try:
        user_id_uuid = uuid.UUID(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid/expired token!",
            headers={"WWW-Authenticate": "Bearer"},
        )        
        
    result = await db.execute(
        select(User).where(User.id == user_id_uuid)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@user.get(path="/{user_id}", response_model=UserPublic,
                    dependencies=[Depends(require_role("superadmin"))])
async def get_user(user_id: uuid.UUID, db: db_connection):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found!")
    
    
@user.patch(path="/{user_id}/deactivate",
          dependencies=[Depends(require_role("superadmin"))])
async def deactivate_user(user_id: uuid.UUID, db: db_connection):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")  
    if user.role == Role.SUPERADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Cannot deactivate superadmin")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User has already been deactivated")
        
    user.is_active = False
    await db.commit()
    return {"detail": "User has been deactivated"}