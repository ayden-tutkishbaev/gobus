from src.schema import AppBaseModel
from src.schedules.enum import RouteStatus

import datetime
import uuid


class RouteModel(AppBaseModel):
    id: uuid.UUID
    name: str
    estimated_duration_minutes: int


class ScheduleBase(AppBaseModel):
    route_id: uuid.UUID
    date: datetime.date
    departure_time: datetime.time
    

class ScheduleCreate(ScheduleBase):
    status: RouteStatus = RouteStatus.PLANNED
    
    
class ScheduleUpdate(AppBaseModel):
    route_id: uuid.UUID | None = None
    date: datetime.date | None = None
    departure_time: datetime.time | None = None
    status: RouteStatus | None = None
    

class SchedulesListResponse(AppBaseModel):
    id: uuid.UUID
    route_id: uuid.UUID
    date: datetime.date
    departure_time: datetime.time
    status: RouteStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    

class ScheduleResponse(AppBaseModel):
    id: uuid.UUID
    route: RouteModel
    date: datetime.date
    departure_time: datetime.time
    status: RouteStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    