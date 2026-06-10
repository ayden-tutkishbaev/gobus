from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
import uuid
from src.auth.enum import UserRole, Role
from src.schema import AppBaseModel
from src.staff.enum import StaffRole


class UserBase(AppBaseModel):
    username: str = Field(min_length=1, max_length=50)
    phone_number: str
    
    
class UserCreate(UserBase):
    password: str = Field(min_length=1)
    role: UserRole
    
    
class AdminCreate(UserBase):
    password: str = Field(min_length=1)


class StaffModel(AppBaseModel):
    id: uuid.UUID
    last_name: str 
    first_name: str 
    middle_name: str 
    # phone_number: str 
    staff_type: StaffRole
    profile_photo_url: str | None = None
    is_active: bool
    registered_at: datetime
    
    

class UserSchema(AppBaseModel):
    id: uuid.UUID
    username: str
    role: Role
    phone_number: str
    is_active: bool
    staff: StaffModel | None = None  
    logged_in_at: int | None = None 
    
    
class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    
    
class ChangePassword(BaseModel):
    new_password: str = Field(min_length=1)