import uuid

from pydantic import Field
from src.schema import AppBaseModel

from datetime import date, datetime
from typing import Optional

    
    
class KidBase(AppBaseModel):
    last_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    date_of_birth: date
    home_address: str
    
    
    
class KidCreate(KidBase):
    phone_number: Optional[str] = None
    school_id: Optional[uuid.UUID] = None
    route_id: Optional[uuid.UUID] = None
    contract_id: Optional[uuid.UUID] = None
    teacher_id: Optional[uuid.UUID] = None
    
    parents: list[uuid.UUID]
    
    
class KidUpdate(AppBaseModel):
    last_name: str | None = Field(None, min_length=1, max_length=260)
    first_name: str | None = Field(None, min_length=1, max_length=260)
    middle_name: str | None = Field(None, min_length=1, max_length=260)
    phone_number: str | None = None
    home_address: str | None = None
    
    school_id: uuid.UUID | None = None
    route_id: uuid.UUID | None = None
    contract_id: uuid.UUID | None = None
    teacher_id: uuid.UUID | None = None
    
    date_of_birth: date | None = None
    
    parents: list[uuid.UUID] | None = None
    is_active: bool | None = None
    
    
class SchoolModel(AppBaseModel):
    id: uuid.UUID
    name: str
    
    
class TeacherModel(AppBaseModel):
    id: uuid.UUID
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str


class ContractModel(AppBaseModel):
    id: uuid.UUID
    signed_at: date
    expires_at: date
    is_active: bool

    

class RouteModel(AppBaseModel):
    id: uuid.UUID
    name: str
    estimated_duration_minutes: int


class ParentModel(AppBaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    phone_number: str | None
    


class KidsListResponse(KidBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    profile_photo_url: str | None = None
    phone_number: str | None

    school_id: uuid.UUID | None = None      
    route_id: uuid.UUID | None = None      
      
    parents: list[ParentModel] = []


class KidResponse(AppBaseModel):
    id: uuid.UUID
    created_at: datetime
    profile_photo_url: str | None = None
    phone_number: str | None
    is_active: bool
    
    school: SchoolModel | None = None
    route: RouteModel | None = None
    contract: ContractModel | None = None
    teacher: TeacherModel | None = None
    parents: list[ParentModel] = []
    
    
    