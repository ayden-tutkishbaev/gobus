from __future__ import annotations

import uuid
from database.core import Base
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Date, Boolean, Enum, Float, Table, Column, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.options import Role
    

def tashkent_now():
    return datetime.now(ZoneInfo("Asia/Tashkent"))



class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    date_joined: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role))
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    username: Mapped[str] = mapped_column(String(260), nullable=False)
    first_name: Mapped[str] = mapped_column(String(260), nullable=True)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=True)
    family_name: Mapped[str] = mapped_column(String(260), nullable=True)