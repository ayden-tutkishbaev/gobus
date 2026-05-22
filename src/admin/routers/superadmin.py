from fastapi import APIRouter, HTTPException, status, Depends
from src.dependencies import db_connection
from sqlalchemy import select
from src.auth.models import User
from src.admin.schemas.users import UserUpdate
from src.admin.permissions import require_role
import uuid


superadmin = APIRouter()


@superadmin.patch(
    "/edit-rights/{user_id}",
    dependencies=[Depends(require_role("superadmin"))]
)
async def assign_admin(
    user_id: uuid.UUID,
    user_data: UserUpdate,
    db: db_connection
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
        
    if user_data.role == 'superadmin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot assign superadmin"
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
        
    await db.commit()
    await db.refresh(user)
        
    return user