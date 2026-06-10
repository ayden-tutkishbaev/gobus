import uuid

from PIL import UnidentifiedImageError
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from starlette.concurrency import run_in_threadpool
from src.auth.enum import Role
from src.config import config
from src.admin.image_utils import delete_profile_image, process_image
from src.admin.permissions import require_role
from src.admin.schemas.transport import TransportResponse, TransportUpdate, TransportCreate
from src.dependencies import db_connection
from sqlalchemy import select
from src.routes.models import Transport
from src.routes.enum import Status
from sqlalchemy.orm import selectinload
from src.auth.services import http_bearer


admin_transport = APIRouter(
    dependencies=[
        Depends(http_bearer),
        Depends(require_role(Role.SUPERADMIN, Role.ADMIN)), 
    ],
    prefix="/transport"
)


@admin_transport.post(
    path='',
)
async def add_transport(
    db: db_connection,
    parent_data: TransportCreate,
):
    
    new_transport = Transport(
        unique_transport_id=parent_data.unique_transport_id,
        model=parent_data.model,
        capacity=parent_data.capacity,
        status=parent_data.status
    )
    
    db.add(new_transport)
    await db.commit()
    await db.refresh(new_transport)
    
    return new_transport


@admin_transport.patch(
    path='/{transport_id}/photo',
)
async def add_transport_picture(
    db: db_connection,
    transport_id: uuid.UUID,
    uploaded_file: UploadFile
):
    content = await uploaded_file.read()
    
    if len(content) > config.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is too large"
        )
        
    query = await db.execute(select(Transport).where(Transport.id == transport_id))
    chosen_transport = query.scalars().first()
    
    if not chosen_transport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transport not found")
    
    try:
        new_filename = await run_in_threadpool(process_image, "transport", content, False)
    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file."
        ) from error
        
    old_filename = chosen_transport.photo_url
    
    chosen_transport.photo_url = f"transport/{new_filename}"

    await db.commit()
    await db.refresh(chosen_transport)

    if chosen_transport.photo_url:
        delete_profile_image(old_filename)

    return chosen_transport


@admin_transport.get(
    path="",
    response_model=list[TransportResponse],
)
async def get_all_transports(
    db: db_connection,
    limit: int = 20,
    offset: int = 0
):
    result = await db.execute(select(Transport).where(Transport.status == Status.ACTIVE).limit(limit).offset(offset))
    return result.scalars().all()


@admin_transport.get(
    path="/{transport_id}",
    response_model=TransportResponse,
)
async def get_transport(
    db: db_connection,
    transport_id: uuid.UUID
):
    result = await db.execute(select(Transport).where(Transport.id == transport_id))
    transport = result.scalars().first()
    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transport not found"
        )
    return transport


@admin_transport.patch(
    path="/{transport_id}",
)
async def edit_transport(
    db: db_connection,
    data_edited: TransportUpdate, 
    transport_id: uuid.UUID
):
    query = await db.execute(select(Transport).where(Transport.id == transport_id))
    transport = query.scalars().first()
    
    if not transport:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Transport not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(transport, field, value)
        
    await db.commit()
    await db.refresh(transport)
    return transport


@admin_transport.patch(
    path="/{transport_id}/deactivate",
)
async def deactivate_transport(
    db: db_connection,
    transport_id: uuid.UUID
):
    result = await db.execute(select(Transport).where(Transport.id == transport_id))
    transport = result.scalars().first()
    
    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            path="Transport not found"
        )
    transport.is_active = False
    await db.commit()
    return {"detail": "Transport has been transport"}