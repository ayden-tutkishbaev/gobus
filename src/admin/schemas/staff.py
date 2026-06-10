import uuid

from src.auth.enum import Role, UserRole
from src.staff.enum import StaffRole
from pydantic import Field
from datetime import date, datetime

from src.schema import AppBaseModel


class StaffBase(AppBaseModel):
    last_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    staff_type: StaffRole
    
    
class StaffCreate(StaffBase):
    phone_number: str = Field(min_length=1, max_length=90)
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1)
    role: UserRole
    date_of_birth: date
    salary: int = Field(ge=0)
        
    
class StaffListResponse(StaffBase):
    id: uuid.UUID
    profile_photo_url: str | None = None
    is_active: bool
    registered_at: datetime
    user_id: uuid.UUID | None = None
    
    
class UserModel(AppBaseModel):
    id: uuid.UUID
    username: str
    role: Role
    phone_number: str

    
class StaffResponse(StaffBase):
    id: uuid.UUID
    profile_photo_url: str | None = None
    is_active: bool
    registered_at: datetime
    user: UserModel | None = None
    
    
class UserUpdate(AppBaseModel):
    phone_number: str | None = None
    username: str | None = Field(None, min_length=3, max_length=50)
    is_active: bool | None = None
    role: UserRole


class StaffUpdate(AppBaseModel):
    last_name: str | None = Field(None, min_length=1, max_length=260)
    first_name: str | None = Field(None, min_length=1, max_length=260)
    middle_name: str | None = Field(None, min_length=1, max_length=260)
    staff_type: StaffRole | None = None
    date_of_birth: date | None = None
    salary: int | None = Field(default=None, ge=0)


class StaffWithUserUpdate(AppBaseModel):
    staff: StaffUpdate | None = None
    user: UserUpdate | None = None
    