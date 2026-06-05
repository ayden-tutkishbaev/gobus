from src.database.core import Base
import uuid
from datetime import datetime
from src.auth.enum import Role
from src.database.tools import tashkent_now

from sqlalchemy import DateTime, LargeBinary, String, Boolean, Enum, UUID
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    phone_number: Mapped[str] = mapped_column(String(90), nullable=False)
    password_hashed: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now, nullable=True)
    
    # created_by_UUID: Mapped[] # TODO: THINK 
    
    
    