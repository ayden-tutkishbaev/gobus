from fastapi import APIRouter, HTTPException, status, Depends
from src.auth.enum import Role
from src.auth.schemas import AdminCreate, ChangePassword, StaffModel, UserCreate, UserSchema
from src.auth.security import hash_password
from src.dependencies import db_connection
from sqlalchemy import select
from src.auth.models import User
from src.admin.schemas.users import UserUpdate
from src.admin.permissions import require_role
import uuid

from src.auth.services import http_bearer
from sqlalchemy.orm import selectinload


superadmin = APIRouter(
    dependencies=[
        Depends(http_bearer),
        Depends(require_role(Role.SUPERADMIN)), 
    ],
    prefix="/superadmin", 
    tags=['Superadmin']
)


@superadmin.post(path="/admins/create",
          response_model=UserSchema,
          status_code=status.HTTP_201_CREATED
)
async def create_admin(user: AdminCreate, db: db_connection):
    result = await db.execute(
        select(User).where(User.username == user.username),
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
        
    new_user = User(
        username=user.username.lower(),
        phone_number=user.phone_number,
        password_hashed=hash_password(user.password),
        role=Role.ADMIN,
    )    

    db.add(new_user)
    await db.flush()
    new_user_id = new_user.id
    await db.commit()

    result = await db.execute(
        select(User)
        .options(selectinload(User.staff))
        .where(User.id == new_user_id)
    )
    user_db = result.scalar()

    return UserSchema(
        id=user_db.id,
        username=user_db.username,
        role=user_db.role,
        phone_number=user_db.phone_number,
        is_active=user_db.is_active,
        staff=StaffModel.model_validate(user_db.staff) if user_db.staff else None,
        logged_in_at=None,
    )



    
    
@superadmin.get(
    path="/admins"
)
async def get_all_admins(    
    db: db_connection,
    limit: int = 20,
    offset: int = 0
):
    result = await db.execute(select(User).where(User.role == Role.ADMIN).limit(limit).offset(offset))
    return result.scalars().all()


@superadmin.get(
    path="/admins/{admin_id}",
)
async def get_admin(
    admin_id: uuid.UUID,
    db: db_connection
):
    result = await db.execute(select(User).where(User.id == admin_id))
    admin = result.scalars().first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    return admin


@superadmin.patch(path="/{user_id}/change-password")
async def change_user_password(
    user_id: uuid.UUID, 
    db: db_connection, 
    data: ChangePassword
):
    query = await db.execute(select(User).where(User.id == user_id))
    user = query.scalars().first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    
    update_data = data.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    user.password_hashed = hash_password(data.new_password)
        
    await db.commit()
    return {"detail": "Password changed successfully!"}


    
@superadmin.patch(path="/{user_id}/deactivate")
async def deactivate_admin(user_id: uuid.UUID, db: db_connection):
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