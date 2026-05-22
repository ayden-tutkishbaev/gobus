import uuid

from src.staff.enum import StaffRole
from pydantic import Field
from datetime import date, datetime

from src.schema import AppBaseModel


class StaffBase(AppBaseModel):
    last_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: str
    staff_type: StaffRole
    
    
class StaffCreate(StaffBase):
    date_of_birth: date
    salary: int = Field(ge=0)
    
    
class StaffResponse(StaffBase):
    id: uuid.UUID
    profile_photo_url: str | None = None
    is_active: bool
    registered_at: datetime
    
    
class StaffUpdate(AppBaseModel):
    last_name: str | None = Field(None, min_length=1, max_length=260)
    first_name: str | None = Field(None, min_length=1, max_length=260)
    middle_name: str | None = Field(None, min_length=1, max_length=260)
    phone_number: str | None = None
    staff_type: StaffRole | None = None
    date_of_birth: date | None = None
    salary: int | None = Field(default=None, ge=0)