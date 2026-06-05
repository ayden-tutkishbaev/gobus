import uuid

from PIL import UnidentifiedImageError
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from starlette.concurrency import run_in_threadpool
from src.auth.enum import Role
from src.config import config
from src.admin.image_utils import delete_profile_image, process_image
from src.admin.permissions import require_role
from src.admin.schemas.staff import StaffCreate, StaffUpdate, StaffResponse
from src.dependencies import db_connection
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.staff.models import Staff
from src.auth.services import http_bearer


admin_staff = APIRouter(
    dependencies=[
        Depends(http_bearer),
        Depends(require_role(Role.SUPERADMIN, Role.ADMIN)), 
    ]
)


@admin_staff.post(
    path='/staff',
)
async def add_staff(
    db: db_connection,
    parent_data: StaffCreate,
):    
    new_staff = Staff(
        last_name=parent_data.last_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        staff_type=parent_data.staff_type,
        date_of_birth=parent_data.date_of_birth,
        salary=parent_data.salary,
    )
    
    db.add(new_staff)
    await db.commit()
    await db.refresh(new_staff)
    
    return new_staff


@admin_staff.patch(
    path='/staff/{staff_id}/photo',
)
async def add_staff_picture(
    db: db_connection,
    staff_id: uuid.UUID,
    uploaded_file: UploadFile
):
    content = await uploaded_file.read()
    
    if len(content) > config.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large"
        )
        
    query = await db.execute(select(Staff).where(Staff.id == staff_id))
    chosen_staff = query.scalars().first()
    
    if not chosen_staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    
    try:
        new_filename = await run_in_threadpool(process_image, "staff", content)
    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file."
        ) from error
        
    old_filename = chosen_staff.profile_photo_url
    
    chosen_staff.profile_photo_url = f"staff/{new_filename}"
    
    print(new_filename)

    await db.commit()
    await db.refresh(chosen_staff)

    delete_profile_image(old_filename)

    return chosen_staff


@admin_staff.patch(
    path="/staff/{staff_id}",
)
async def edit_staff(
    db: db_connection,
    data_edited: StaffUpdate, 
    staff_id: uuid.UUID
):
    query = await db.execute(select(Staff).where(Staff.id == staff_id))
    staff = query.scalars().first()
    
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Staff member not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(staff, field, value)
        
    await db.commit()
    await db.refresh(staff)
    return staff


@admin_staff.get(
    path="/staff",
    response_model=list[StaffResponse],
)
async def get_all_staff(
    db: db_connection,
    limit: int = 20,
    offset: int = 0
):
    result = await db.execute(select(Staff).where(Staff.is_active).limit(limit).offset(offset))
    return result.scalars().all()


@admin_staff.get(
    path="/staff/{staff_id}",
    response_model=StaffResponse,
)
async def get_staff(
    staff_id: uuid.UUID,
    db: db_connection
):
    result = await db.execute(select(Staff).where(Staff.id == staff_id))
    staff = result.scalars().first()
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff not found"
        )
    return staff   


@admin_staff.patch(
    path="/staff/{staff_id}/deactivate",
)
async def deactivate_staff(
    db: db_connection,
    staff_id: uuid.UUID
):
    result = await db.execute(select(Staff).where(Staff.id == staff_id))
    staff = result.scalars().first()
    
    if not staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            path="Staff not found"
        )
    staff.is_active = False
    await db.commit()
    return {"detail": "Staff has been deactivated"}