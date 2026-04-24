from pydantic import BaseModel, Field, ConfigDict
from api.auth.schemas import UserPublic
from datetime import datetime, date
from database.enum import Role


class UserUpdate(BaseModel):
    is_admin: bool = Field(description="Выдать права администратора")
    
    
class UserAdminPublic(UserPublic):
    is_admin: bool    
    
    
class UserAdminResponse(BaseModel):
    message: str
    user: UserAdminPublic
    
    
    
class ParentBase(BaseModel):
    family_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: str = Field(min_length=1, max_length=90)
    

class ParentCreate(ParentBase):
    id: int
    registered_at: datetime
    document_id: str = Field(min_length=5, max_length=90)
    
    
class StaffBase(BaseModel):
    family_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: str = Field(min_length=1, max_length=90)
    profile_picture: str
    staff_type: Role
    birth_date: date
    salary: int = Field(ge=0)

    