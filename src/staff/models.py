from __future__ import annotations

from src.database.core import Base
import uuid
from datetime import date, datetime
from src.staff.enum import StaffRole, ViolationType
from src.database.tools import tashkent_now

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Date, Boolean, Enum, Float, Table, Column, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.routes.models import Route
from src.attendance.models import Attendance


class Staff(Base):
    __tablename__ = 'staff'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    last_name: Mapped[str] = mapped_column(String(260), nullable=False)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    profile_photo_url: Mapped[str] = mapped_column(String(400), nullable=True)
    staff_type: Mapped[StaffRole] = mapped_column(Enum(StaffRole))
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(90), nullable=False) # REMOVE
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)

    driver_routes: Mapped[list[Route]] = relationship(back_populates='driver', foreign_keys="Route.driver_id")
    babysitter_routes: Mapped[list[Route]] = relationship(back_populates='babysitter', foreign_keys="Route.babysitter_id")
    violations: Mapped[list[Violation]] = relationship(back_populates='recipient', foreign_keys="Violation.recipient_id")
    violations_given_to: Mapped[list[Violation]] = relationship(back_populates='recorded_by', foreign_keys="Violation.recorded_by_id")
    attendance_records: Mapped[list[Attendance]] = relationship(back_populates='marked_by')


class Violation(Base):
    __tablename__ = 'violations'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    recipient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("staff.id"), nullable=False, index=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    type: Mapped[ViolationType] = mapped_column(Enum(ViolationType), nullable=False)
    recorded_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("staff.id"), nullable=False, index=True) 
    description: Mapped[str] = mapped_column(String(260), nullable=False)
    
    recipient: Mapped[Staff] = relationship(back_populates='violations', foreign_keys="Violation.recipient_id")
    recorded_by: Mapped[Staff] = relationship(back_populates='violations_given_to', foreign_keys="Violation.recorded_by_id")
    