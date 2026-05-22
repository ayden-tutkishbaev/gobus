from pydantic import Field
from src.auth.enum import UserRole
from src.schema import AppBaseModel


class UserUpdate(AppBaseModel):
    role: UserRole = Field(description="Assign admin rights")