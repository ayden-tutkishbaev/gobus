from __future__ import annotations

from src.database.core import Base
import uuid
from datetime import date, datetime
from src.parents.enum import PaymentType, TariffType
from src.database.tools import tashkent_now, tashkent_today
from src.database.associations import parent_kid, parent_contract

from sqlalchemy import DateTime, ForeignKey, String, Date, Boolean, Enum, Float, Table, Column, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Parent(Base):
    __tablename__ = 'parents'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    last_name: Mapped[str] = mapped_column(String(260), nullable=False)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(90), nullable=False)
    document_id: Mapped[str | None] = mapped_column(String(90), nullable=True)  
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)

    home_address: Mapped[str] = mapped_column(String(260), nullable=False)
    
    kids: Mapped[list["Kid"]] = relationship(secondary=parent_kid, back_populates='parents')
    contracts: Mapped[list["Contract"]] = relationship(secondary=parent_contract, back_populates='parents')
    


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    parent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("parents.id"), nullable=False, index=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False, default=tashkent_today)
    signed_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[date] = mapped_column(Date, nullable=False, default=tashkent_today, onupdate=tashkent_today)
    expires_at: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_payment: Mapped[date] = mapped_column(Date, nullable=False)
    type_of_payment: Mapped[PaymentType] = mapped_column(Enum(PaymentType))
    tariff: Mapped[TariffType] = mapped_column(Enum(TariffType))
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    document_url: Mapped[str | None] = mapped_column(String(400), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    kids: Mapped[list["Kid"]] = relationship(back_populates='contract')   
    parents: Mapped[list["Parent"]] = relationship(secondary=parent_contract, back_populates='contracts')
    