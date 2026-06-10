import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from src.admin.permissions import require_role
from src.admin.schemas.schools import SchoolCreate, SchoolResponse, SchoolUpdate
from src.auth.enum import Role
from src.dependencies import db_connection
from sqlalchemy import select

from src.schools.models import School
from src.auth.services import http_bearer


admin_school = APIRouter(
    dependencies=[
        Depends(http_bearer),
        Depends(require_role(Role.SUPERADMIN, Role.ADMIN)), 
    ],
    prefix="/schools"
)


@admin_school.post(
    path='',
)
async def add_school(
    db: db_connection,
    parent_data: SchoolCreate,
):
    new_school = School(
        name=parent_data.name,
        address=parent_data.address,
        geo_latitude=parent_data.geo_latitude,
        geo_longitude=parent_data.geo_longitude
    )
    
    db.add(new_school)
    await db.commit()
    await db.refresh(new_school)
    
    return new_school

    
@admin_school.get(
    path="",
    response_model=list[SchoolResponse],
)
async def get_schools(
    db: db_connection,
    limit: int = 20,
    offset: int = 0
):
    result = await db.execute(select(School).where(School.is_active).limit(limit).offset(offset))
    return result.scalars().all()


@admin_school.get(
    path="/{school_id}",
    response_model=SchoolResponse,
)
async def get_school(
    school_id: uuid.UUID,
    db: db_connection
):
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalars().first()
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    return school   
    
    
@admin_school.patch(
    path="/{school_id}",
)
async def edit_school(
    db: db_connection,
    data_edited: SchoolUpdate, 
    school_id: uuid.UUID
):
    query = await db.execute(select(School).where(School.id == school_id))
    school = query.scalars().first()
    
    if not school:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='School not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(school, field, value)
        
    await db.commit()
    await db.refresh(school)
    return school


@admin_school.patch(
    path="/{school_id}/deactivate",
)
async def deactivate_school(
    db: db_connection,
    school_id: uuid.UUID
):
    result = await db.execute(select(School).where(School.id == school_id))
    school = result.scalars().first()
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            path="Parent not found"
        )
    school.is_active = False
    await db.commit()
    return {"detail": "School has been deactivated"}