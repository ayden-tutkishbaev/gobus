from src.database.core import Base
import uuid
from datetime import date, datetime
from src.parents.enum import PaymentType, TariffType
from src.database.tools import tashkent_now

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Date, Boolean, Enum, Float, Table, Column, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class School(Base):
    __tablename__ = 'schools'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(260), nullable=False)
    address: Mapped[str] = mapped_column(String(260), nullable=False)
    geo_latitude: Mapped[float] = mapped_column(Float, nullable=False)
    geo_longitude: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)

    kids: Mapped[list["Kid"]] = relationship(back_populates='school')
    teachers: Mapped[list["Teacher"]] = relationship(back_populates='school')
    

class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    last_name: Mapped[str] = mapped_column(String(260), nullable=False)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(90), nullable=False)
    school_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schools.id"), index=True, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    kids: Mapped[list["Kid"]] = relationship(back_populates='teacher')
    school: Mapped["School"] = relationship(back_populates="teachers")
    # TODO: REL, M2M