from fastapi import APIRouter, HTTPException, status, UploadFile
from api.dependecies import db_connection
from api.admin.dependencies import IsSuperAdmin, IsAdmin
from sqlalchemy import select, func, insert
from database.models import Parent, Staff
from api.auth.models import User
from api.auth.schemas import *
from api.admin.schemas import *
import uuid


admin = APIRouter()


@admin.patch(
    "/edit-rights/{user_id}",
    response_model=UserAdminResponse
)
async def assign_admin(
    super_admin: IsSuperAdmin,
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
    
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
        
    await db.commit()
    await db.refresh(user)
    
    message = f"Пользователь {user.username} назначен админом" if user.is_admin else f"Пользователь {user.username} снят с админа"
    
    return UserAdminResponse(
        message=message,
        user=UserAdminPublic.model_validate(user)
    )
    
    

@admin.post(
    path='/add-parent',
)
async def add_parent(
    admin: IsAdmin,
    db: db_connection,
    parent_data: ParentCreate
):
    new_parent = Parent(
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        family_name=parent_data.family_name,
        phone_number=parent_data.phone_number,
        document_id=parent_data.document_id
    )
    db.add(new_parent)
    await db.commit()
    await db.refresh(new_parent)
    
    return new_parent


@admin.post(
    path='/add-staff'
)
async def add_staff(
    # admin: IsAdmin,
    db: db_connection,
    parent_data: StaffBase,
    # upload_file: UploadFile
):
    new_staff = Staff(
        family_name=parent_data.family_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        profile_picture='.jpg', #modify
        staff_type=parent_data.staff_type,
        birth_date=parent_data.birth_date,
        salary=parent_data.salary,
    )
    db.add(new_staff)
    await db.commit()
    await db.refresh(new_staff)
    
    return new_staff