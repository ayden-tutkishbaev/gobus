import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from src.admin.permissions import require_role
from src.admin.schemas.parents import ParentCreate, ParentUpdate, ParentResponse
from src.auth.enum import Role
from src.dependencies import db_connection
from sqlalchemy import select
from src.parents.models import Parent
from src.auth.services import http_bearer


admin_parent = APIRouter(
    dependencies=[
        Depends(http_bearer),
        Depends(require_role(Role.SUPERADMIN, Role.ADMIN)), 
    ],
    prefix="/parents"
)


@admin_parent.post(
    path='',
)
async def add_parent(
    db: db_connection,
    parent_data: ParentCreate
):
    new_parent = Parent(
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        last_name=parent_data.last_name,
        phone_number=parent_data.phone_number,
        document_id=parent_data.document_id,
        home_address=parent_data.home_address,
    )
    db.add(new_parent)
    await db.commit()
    await db.refresh(new_parent)
    
    return new_parent


@admin_parent.get(
    path="",
    response_model=list[ParentResponse],
)
async def get_all_parents(
    db: db_connection,
    limit: int = 20,
    offset: int = 0
):
    result = await db.execute(select(Parent).where(Parent.is_active).limit(limit).offset(offset))
    return result.scalars().all()


@admin_parent.get(
    path="/{parent_id}",
    response_model=ParentResponse,
)
async def get_parent(
    parent_id: uuid.UUID,
    db: db_connection
):
    result = await db.execute(select(Parent).where(Parent.id == parent_id))
    parent = result.scalars().first()
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent not found"
        )
    return parent


@admin_parent.patch(
    path="/{parent_id}",
)
async def edit_parents(
    db: db_connection,
    data_edited: ParentUpdate, 
    parent_id: uuid.UUID
):
    query = await db.execute(select(Parent).where(Parent.id == parent_id))
    parent = query.scalars().first()
    
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Parent not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(parent, field, value)
        
    await db.commit()
    await db.refresh(parent)
    return parent


@admin_parent.patch(
    path="/{parent_id}/deactivate",
)
async def deactivate_parent(
    db: db_connection,
    parent_id: uuid.UUID
):
    result = await db.execute(select(Parent).where(Parent.id == parent_id))
    parent = result.scalars().first()
    
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            path="Parent not found"
        )
    parent.is_active = False
    await db.commit()
    return {"detail": "Parent has been deactivated"}