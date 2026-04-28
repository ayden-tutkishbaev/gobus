from pydantic import BaseModel, Field, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber

from api.auth.schemas import UserPublic
from datetime import datetime, date
from database.enum import Role, Status, PaymentType, TariffType
from typing import Optional


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
    phone_number: PhoneNumber
    

class ParentCreate(ParentBase):
    document_id: str = Field(min_length=5, max_length=90)
    
    
class ParentUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    family_name: Optional[str] = None
    phone_number: Optional[str] = None
    document_id: Optional[str] = None
    active: Optional[bool] = None
    
    
class StaffBase(BaseModel):
    family_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: PhoneNumber
    staff_type: Role
    birth_date: date
    salary: int = Field(ge=0)
    
    
class StaffUpdate(BaseModel):
    family_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    middle_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    phone_number: Optional[PhoneNumber] = None
    staff_type: Optional[Role] = None
    birth_date: Optional[date] = None
    salary: Optional[int] = Field(default=None, ge=0)
    
    
class TransportBase(BaseModel):
    unique_transport_id: str = Field(min_length=1, max_length=90)
    transport_picture: str
    driver: int
    babysitter: int
    registered_at: date
    status: Status
    
    
class TransportUpdate(BaseModel):
    unique_transport_id: str = Field(default=None, min_length=1, max_length=90)
    transport_picture: Optional[str] = None
    driver: Optional[int] = None
    babysitter: Optional[int] = None
    status: Optional[Status] = None
    
    
class ContractBase(BaseModel):
    date_of_payment: date
    date_of_end: date
    type_of_payment: PaymentType
    tariff: TariffType
    cost: float = Field(ge=0)
    document: str
    
    
class ContractUpdate(BaseModel):
    date_of_payment: Optional[date] = None
    date_of_end: Optional[date] = None
    type_of_payment: Optional[PaymentType] = None
    tariff: Optional[TariffType] = None
    cost: Optional[float] = Field(default=None, ge=0)
    document: Optional[str] = None
    
    
class SchoolBase(BaseModel):
    name: str = Field(min_length=1, max_length=260)
    
    
class SchoolUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    
    
class TeacherBase(BaseModel):
    family_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: PhoneNumber
    school: int    
    
    
class TeacherUpdate(BaseModel):
    family_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    middle_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    phone_number: Optional[PhoneNumber] = None
    school: Optional[int] = None
    
    
class KidBase(BaseModel):
    family_name: str = Field(min_length=1, max_length=260)
    first_name: str = Field(min_length=1, max_length=260)
    middle_name: str = Field(min_length=1, max_length=260)
    phone_number: PhoneNumber
    home_address: str
    
    school: int
    contract: int
    driver: int
    babysitter: int 
    teacher: int
    
    birth_date: date
    
    parents: list[int]
    
    
class KidUpdate(BaseModel):
    family_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    middle_name: Optional[str] = Field(default=None, min_length=1, max_length=260)
    phone_number: Optional[PhoneNumber] = None
    home_address: Optional[str] = None
    
    school: Optional[int] = None
    contract: Optional[int] = None
    driver: Optional[int] = None # TBD
    babysitter: Optional[int] = None # TBD
    teacher: Optional[int] = None
    
    birth_date: Optional[date] = None
    
    parents: Optional[list[int]] = None
    activity: Optional[bool] = None
    
    # PROFILE PIC, ACTIVITY - TBD