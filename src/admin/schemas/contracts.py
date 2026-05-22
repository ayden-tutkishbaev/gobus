import uuid

from pydantic import Field

from datetime import date
from src.parents.enum import TariffType, PaymentType
from src.schema import AppBaseModel


class ContractBase(AppBaseModel):
    type_of_payment: PaymentType
    signed_at: date
    date_of_payment: date
    expires_at: date
    tariff: TariffType
    cost: float = Field(ge=0)


class ContractCreate(ContractBase):
    parent_id: uuid.UUID  

    
class ContractUpdate(AppBaseModel):
    signed_at: date | None = None
    date_of_payment: date | None = None
    expires_at: date | None = None
    type_of_payment: PaymentType | None = None
    tariff: TariffType | None = None
    cost: float | None = None
    
    
class ContractsListResponse(ContractBase):    
    id: uuid.UUID
    parent_id: uuid.UUID
    created_at: date
    document_url: str | None = None    
    is_active: bool
    
    
class ParentModel(AppBaseModel):
    id: uuid.UUID
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str
    document_id: str | None = None
    
    
class ContractResponse(ContractBase):    
    id: uuid.UUID
    parent: ParentModel
    created_at: date
    document_url: str | None = None
    is_active: bool
    