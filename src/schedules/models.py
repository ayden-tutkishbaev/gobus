from src.database.core import Base
import uuid
import datetime
from src.database.tools import tashkent_now

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Date, Boolean, Enum, Float, Table, Time, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schedules.enum import RouteStatus


class Schedule(Base):
    __tablename__ = 'schedules'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                    default=uuid.uuid4)
    route_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("routes.id"), index=True, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    departure_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    status: Mapped[RouteStatus] = mapped_column(Enum(RouteStatus), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now, onupdate=tashkent_now)
    
    route: Mapped["Route"] = relationship(back_populates='schedules')
    attendance_records: Mapped[list["Attendance"]] = relationship(back_populates='schedule')