from src.database.core import Base
import uuid
from datetime import date, datetime
from src.routes.enum import Status
from src.database.tools import tashkent_now

from sqlalchemy import DateTime, ForeignKey, Integer, String, Boolean, Enum, Float, Table, Column, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

    
class Route(Base):
    __tablename__ = 'routes'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                        default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(240), nullable=False)
    # type (h2s, s2h) - TBD
    estimated_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    driver_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("staff.id"), nullable=True, index=True)
    babysitter_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("staff.id"), nullable=True, index=True)
    transport_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("transport.id"), nullable=True, index=True)
    
    kids: Mapped[list["Kid"]] = relationship(back_populates='route')
    
    driver: Mapped["Staff"] = relationship(back_populates='driver_routes', foreign_keys=[driver_id])
    babysitter: Mapped["Staff"] = relationship(back_populates='babysitter_routes', foreign_keys=[babysitter_id])
    transport: Mapped["Transport"] = relationship(back_populates='routes')
    trips: Mapped[list["Trip"]] = relationship(back_populates='route')
    
    
class Transport(Base):
    __tablename__ = 'transport'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    unique_transport_id: Mapped[str] = mapped_column(String(90), nullable=False)
    photo_url: Mapped[str] = mapped_column(String(400), nullable=True)
    model: Mapped[str] = mapped_column(String(90), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)
    
    routes: Mapped[list["Route"]] = relationship(back_populates='transport')