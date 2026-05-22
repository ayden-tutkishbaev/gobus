import uuid

from PIL import UnidentifiedImageError
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from starlette.concurrency import run_in_threadpool
from src.config import config
from src.admin.image_utils import delete_profile_image, process_image
from src.admin.permissions import require_role
from src.admin.schemas.kids import KidCreate, KidUpdate, KidsListResponse, KidResponse
from src.dependencies import db_connection
from sqlalchemy import select
from src.kids.models import Kid
from src.parents.models import Parent
from sqlalchemy.orm import selectinload


admin_kid = APIRouter()


@admin_kid.post(
    path='/kids',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_kid(
    db: db_connection,
    parent_data: KidCreate,
):
    
    new_kid = Kid(
        last_name=parent_data.last_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        home_address=parent_data.home_address,
        school_id=parent_data.school_id,
        route_id=parent_data.route_id,
        contract_id=parent_data.contract_id,
        teacher_id=parent_data.teacher_id,
        date_of_birth=parent_data.date_of_birth,
    )
    
    if parent_data.parents:
        parents = await db.execute(
            select(Parent).where(Parent.id.in_(parent_data.parents))
        )
        new_kid.parents = parents.scalars().all()
    
    db.add(new_kid)
    await db.commit()
    await db.refresh(new_kid)
    
    return new_kid


@admin_kid.patch(
    path='/kids/{kid_id}/photo',
    dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def add_kid_picture(
    db: db_connection,
    kid_id: uuid.UUID,
    uploaded_file: UploadFile
):
    content = await uploaded_file.read()
    
    if len(content) > config.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large"
        )
        
    query = await db.execute(select(Kid).where(Kid.id == kid_id))
    chosen_kid = query.scalars().first()
    
    if not chosen_kid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kid not found"
        )

    try:
        new_filename = await run_in_threadpool(process_image, "kids", content)
    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file."
        ) from error
        
    old_filename = chosen_kid.profile_photo_url
    
    chosen_kid.profile_photo_url = f"kids/{new_filename}"

    await db.commit()
    await db.refresh(chosen_kid)

    if chosen_kid.profile_photo_url:
        delete_profile_image(old_filename)

    return chosen_kid


@admin_kid.patch(path='/kids/{kid_id}',
             dependencies=[Depends(require_role("superadmin", "admin"))]
)
async def update_kid(
    kid_id: uuid.UUID,
    data_edited: KidUpdate,
    db: db_connection,
):
    query = await db.execute(
        select(Kid)
        .options(selectinload(Kid.parents))
        .where(Kid.id == kid_id)
    )
    kid = query.scalars().first()
    if not kid:
        raise HTTPException(status_code=404, detail="Kid not found")

    update_data = data_edited.model_dump(exclude_unset=True, exclude={'parents'})
    for field, value in update_data.items():
        setattr(kid, field, value)

    if 'parents' in data_edited.model_fields_set:
        if data_edited.parents == []:
            kid.parents = []
        else:
            result = await db.execute(
                select(Parent).where(Parent.id.in_(data_edited.parents))
            )
            kid.parents = result.scalars().all()

    await db.commit()
    await db.refresh(kid)
    return kid


@admin_kid.get(path="/kids", 
               response_model=list[KidsListResponse],
                dependencies=[Depends(require_role("superadmin", "admin"))])
async def get_kids(
    db: db_connection, 
    limit: int = 20, 
    offset: int = 0
):
    result = await db.execute(
        select(Kid)
        .options(selectinload(Kid.parents))  
        .where(Kid.is_active == True)
        .limit(limit).offset(offset)
    )
    return result.scalars().all()


@admin_kid.get(path="/kids/{kid_id}", 
               response_model=KidResponse,
               dependencies=[Depends(require_role("superadmin", "admin"))])
async def get_kid(
    kid_id: uuid.UUID, 
    db: db_connection
):
    result = await db.execute(
        select(Kid)
        .options(
            selectinload(Kid.school),
            selectinload(Kid.route),
            selectinload(Kid.contract),
            selectinload(Kid.teacher),
            selectinload(Kid.parents),
        )
        .where(Kid.id == kid_id)
    )
    kid = result.scalar_one_or_none()
    
    if not kid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Kid not found")
        
    return kid