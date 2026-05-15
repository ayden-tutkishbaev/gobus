import uuid

from pydantic import BaseModel, Field

from src.auth.schemas import UserPublic
from datetime import date
from src.auth.enum import Role
from src.routes.enum import Status
from src.parents.enum import TariffType, PaymentType
from typing import Optional
from src.staff.enum import StaffRole


class UserUpdate(BaseModel):
    role: Role = Field(description="Выдать права администратора")
    
    
class UserAdminPublic(UserPublic):
    role: Role    
    
    
class UserAdminResponse(BaseModel):
    message: str
    user: UserAdminPublic
    
    
    
class ParentBase(BaseModel):
    last_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: str
    

class ParentCreate(ParentBase):
    document_id: str = Field(min_length=5, max_length=90)
    home_address: str
    
    
class ParentUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    document_id: Optional[str] = None
    active: Optional[bool] = None
    
    
class StaffBase(BaseModel):
    last_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: str
    staff_type: StaffRole
    date_of_birth: date
    salary: int = Field(ge=0)
    
    
class StaffUpdate(BaseModel):
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    middle_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    phone_number: Optional[str] = None
    staff_type: Optional[StaffRole] = None
    date_of_birth: Optional[date] = None
    salary: Optional[int] = Field(default=None, ge=0)
    
    
class TransportBase(BaseModel):
    unique_transport_id: str = Field(min_length=1, max_length=90)
    model: str
    capacity: int
    status: Status
    
    
class TransportUpdate(BaseModel):
    unique_transport_id: str = Field(default=None, min_length=1, max_length=90)
    model: Optional[str] = None
    capacity: Optional[str] = None
    status: Optional[Status] = None
    
    
class ContractBase(BaseModel):
    parent_id: uuid.UUID
    signed_at: date
    date_of_payment: date
    expires_at: date
    type_of_payment: PaymentType
    tariff: TariffType
    cost: float = Field(ge=0)
    
    
class ContractUpdate(BaseModel):
    signed_at: Optional[date] = None
    date_of_payment: Optional[date] = None
    expires_at: Optional[date] = None
    type_of_payment: Optional[PaymentType] = None
    tariff: Optional[TariffType] = None
    cost: Optional[float] = None
        
    
class SchoolBase(BaseModel):
    name: str = Field(min_length=1, max_length=260)
    address: str
    geo_latitude: float
    geo_longitude: float  
    
    
class SchoolUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    address: Optional[str] = None
    geo_latitude: Optional[float] = None
    geo_longitude: Optional[float] = None  
    
    
class TeacherBase(BaseModel):
    last_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: str
    school: uuid.UUID  
    
    
class TeacherUpdate(BaseModel):
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    middle_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    phone_number: Optional[str] = None
    school: Optional[uuid.UUID] = None
    
    
class KidBase(BaseModel):
    last_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: Optional[str] = None
    home_address: str
    date_of_birth: date
    
    school_id: Optional[uuid.UUID] = None
    route_id: Optional[uuid.UUID] = None
    contract_id: Optional[uuid.UUID] = None
    teacher_id: Optional[uuid.UUID] = None
    
    
    parents: list[uuid.UUID]
    
    
class KidUpdate(BaseModel):
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    middle_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    phone_number: Optional[str] = None
    home_address: Optional[str] = None
    
    school_id: Optional[uuid.UUID] = None
    route_id: Optional[uuid.UUID] = None
    contract_id: Optional[uuid.UUID] = None
    teacher_id: Optional[uuid.UUID] = None
    
    date_of_birth: Optional[date] = None
    
    parents: Optional[list[uuid.UUID]] = None
    is_active: Optional[bool] = None
    
    # PROFILE PIC, ACTIVITY - TBD
    
    
class RouteBase(BaseModel):
    name: str
    estimated_duration_minutes: int
    
    driver_id: uuid.UUID
    babysitter_id: uuid.UUID
    transport_id: uuid.UUID
    
    
class RouteUpdate(BaseModel):
    name: Optional[str] = None
    estimated_duration_minutes: Optional[int] = None
    
    driver_id: Optional[uuid.UUID] = None
    babysitter_id: Optional[uuid.UUID] = None
    transport_id: Optional[uuid.UUID] = None