from database.core import Base
import uuid
from datetime import datetime
from database.enum import Role
from database.tools import tashkent_now

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Date, Boolean, Enum, Float, Table, Column, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    date_joined: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superadmin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    username: Mapped[str] = mapped_column(String(260), nullable=False)