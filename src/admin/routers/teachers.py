import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from src.admin.permissions import require_role
from src.admin.schemas.teachers import TeacherCreate, TeacherUpdate, TeacherResponse, TeacherListResponse
from src.auth.enum import Role
from src.dependencies import db_connection
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.auth.services import http_bearer

from src.schools.models import Teacher


admin_teacher = APIRouter(
    dependencies=[
        Depends(http_bearer),
        Depends(require_role(Role.SUPERADMIN, Role.ADMIN)), 
    ]
)


@admin_teacher.post(
    path='/teachers',
)
async def add_teacher(
    db: db_connection,
    parent_data: TeacherCreate,
):
    new_teacher = Teacher(
        last_name=parent_data.last_name,
        first_name=parent_data.first_name,
        middle_name=parent_data.middle_name,
        phone_number=parent_data.phone_number,
        school_id=parent_data.school_id,
    )
    
    db.add(new_teacher)
    await db.commit()
    await db.refresh(new_teacher)
    
    return new_teacher


@admin_teacher.patch(
    path="/teachers/{teacher_id}",
)
async def edit_teacher(db: db_connection,
    data_edited: TeacherUpdate, 
    teacher_id: uuid.UUID
):
    query = await db.execute(select(Teacher).where(Teacher.id == teacher_id))
    teacher = query.scalars().first()
    
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Teacher not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(teacher, field, value)
        
    await db.commit()
    await db.refresh(teacher)
    return teacher


@admin_teacher.get(
    path="/teachers",
    response_model=list[TeacherListResponse],
)
async def get_all_teachers(
    db: db_connection,
    limit: int = 20,
    offset: int = 0
):
    result = await db.execute(select(Teacher).where(Teacher.is_active).limit(limit).offset(offset))
    return result.scalars().all()


@admin_teacher.get(
    path="/teachers/{teacher_id}",
    response_model=TeacherResponse,
)
async def get_teacher(
    teacher_id: uuid.UUID,
    db: db_connection
):
    result = await db.execute(select(Teacher).options(selectinload(Teacher.school)).where(Teacher.id == teacher_id))
    teacher = result.scalars().first()
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    return teacher   


@admin_teacher.patch(
    path="/teacher/{teacher_id}/deactivate",
)
async def deactivate_teacher(
    db: db_connection,
    teacher_id: uuid.UUID
):
    result = await db.execute(select(Teacher).where(Teacher.id == teacher_id))
    teacher = result.scalars().first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            path="Teacher not found"
        )
    teacher.is_active = False
    await db.commit()
    return {"detail": "Teacher has been deactivated"}