from src.database.core import Base
import uuid
from datetime import date, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Date, Boolean, Enum, Float, Table, Column, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.attendance.enum import KidStatus


class Attendance(Base):
    __tablename__ = 'attendance'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                default=uuid.uuid4)
    schedule_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("schedules.id"), index=True, nullable=False)
    kid_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("kids.id"), index=True, nullable=False)
    status: Mapped[KidStatus] = mapped_column(Enum(KidStatus), nullable=False)
    marked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    babysitter_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("staff.id"), index=True, nullable=False)
    note: Mapped[str | None] = mapped_column(String(300), nullable=True)
    
    schedule: Mapped["Schedule"] = relationship(back_populates='attendance_records')
    marked_by: Mapped["Staff"] = relationship(back_populates='attendance_records')
    
    
