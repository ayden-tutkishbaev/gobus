import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from src.admin.permissions import require_role
from src.admin.schemas.schedules import ScheduleUpdate, ScheduleCreate, ScheduleResponse, SchedulesListResponse
from src.auth.enum import Role
from src.dependencies import db_connection
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.schedules.models import Schedule
from src.auth.services import http_bearer


admin_schedule = APIRouter(
    dependencies=[
        Depends(http_bearer),
        Depends(require_role(Role.SUPERADMIN, Role.ADMIN)), 
    ]
)


@admin_schedule.post(
    path='/schedules',
)
async def add_schedule(
    db: db_connection,
    parent_data: ScheduleCreate,
):
    new_schedule = Schedule(
        route_id=parent_data.route_id,
        date=parent_data.date,
        departure_time=parent_data.departure_time,
        status=parent_data.status
    )
    
    db.add(new_schedule)
    await db.commit()
    await db.refresh(new_schedule)
    
    return new_schedule

    
@admin_schedule.get(
    path="/schedules",
    response_model=list[SchedulesListResponse],
)
async def get_all_schedules(
    db: db_connection,
    limit: int = 20,
    offset: int = 0
):
    result = await db.execute(select(Schedule).limit(limit).offset(offset))
    return result.scalars().all()


@admin_schedule.get(
    path="/schedules/{schedule_id}",
    response_model=ScheduleResponse,
)
async def get_schedules(
    schedule_id: uuid.UUID,
    db: db_connection
):
    result = await db.execute(select(Schedule).options(selectinload(Schedule.route)).where(Schedule.id == schedule_id))
    schedule = result.scalars().first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    return schedule   
    
    
@admin_schedule.patch(
    path="/schedules/{schedule_id}",
)
async def edit_schedule(
    db: db_connection,
    data_edited: ScheduleUpdate, 
    schedule_id: uuid.UUID
):
    query = await db.execute(select(Schedule).where(Schedule.id == schedule_id))
    schedule = query.scalars().first()
    
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Schedule not found')
    
    update_data = data_edited.model_dump(exclude_unset=True)
   
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No field to update")
   
    for field, value in update_data.items():
        setattr(schedule, field, value)
        
    await db.commit()
    await db.refresh(schedule)
    return schedule
