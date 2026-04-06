from __future__ import annotations

import uuid
from database.core import Base
from datetime import UTC, datetime, date, time
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Date, Boolean, Enum, Float, Table, Column, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.options import Status, TariffType, PaymentType, Role


def tashkent_now():
    return datetime.now(ZoneInfo("Asia/Tashkent"))


parent_kid = Table(
    'parent_kid', Base.metadata,
    Column('parent_id', ForeignKey('parents.id'), primary_key=True),
    Column('kid_id', ForeignKey('kids.id'), primary_key=True),
)

parent_contract = Table(
    'parent_contract', Base.metadata,
    Column('parent_id', ForeignKey('parents.id'), primary_key=True),
    Column('contract_id', ForeignKey('contracts.id'), primary_key=True),
)


class Kid(Base):
    __tablename__ = 'kids'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)

    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    family_name: Mapped[str] = mapped_column(String(260), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(400), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(90), nullable=True)
    home_address: Mapped[str] = mapped_column(String(260), nullable=False)

    school: Mapped[int] = mapped_column(ForeignKey('schools.id'), nullable=False, index=True)
    contract: Mapped[int] = mapped_column(ForeignKey('contracts.id'), nullable=False, index=True)
    driver: Mapped[int] = mapped_column(ForeignKey('staff.id'), nullable=False, index=True)
    transport: Mapped[int] = mapped_column(ForeignKey('transport.id'), nullable=False, index=True)
    babysitter: Mapped[int] = mapped_column(ForeignKey('staff.id'), nullable=False, index=True)
    teacher: Mapped[int | None] = mapped_column(ForeignKey('teachers.id'), nullable=True, index=True)

    birth_date: Mapped[date] = mapped_column(Date)
    active: Mapped[bool] = mapped_column(Boolean)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now, nullable=False)
    
    parents: Mapped[list[Parent]] = relationship(secondary=parent_kid, back_populates='kids')
    
    rel_school: Mapped[School] = relationship(back_populates='children')
    rel_contract: Mapped[Contract] = relationship(back_populates='kids')
    rel_driver: Mapped[Staff] = relationship(back_populates='kids_rel', foreign_keys=[driver])
    rel_transport: Mapped[Transport] = relationship(back_populates='kids_rel')
    rel_babysitter: Mapped[Staff] = relationship(back_populates='kids_rel_b', foreign_keys=[babysitter])
    rel_teacher: Mapped[Teacher] = relationship(back_populates='kids')


class Staff(Base):
    __tablename__ = 'staff'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    family_name: Mapped[str] = mapped_column(String(260), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(400), nullable=False)
    staff_type: Mapped[Role] = mapped_column(Enum(Role))
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(90), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)

    transport_rel_driver: Mapped[list[Transport]] = relationship(back_populates='rel_driver', foreign_keys='Transport.driver')
    transport_rel_babysitter: Mapped[list[Transport]] = relationship(back_populates='rel_babysitter', foreign_keys='Transport.babysitter')
    violations: Mapped[list[Violation]] = relationship(back_populates='rel_recipient')

    kids_rel: Mapped[list[Kid]] = relationship(back_populates='rel_driver', foreign_keys='Kid.driver')
    kids_rel_b: Mapped[list[Kid]] = relationship(back_populates='rel_babysitter', foreign_keys='Kid.babysitter')


class Parent(Base):
    __tablename__ = 'parents'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    family_name: Mapped[str] = mapped_column(String(260), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(90), nullable=True)
    document_id: Mapped[str | None] = mapped_column(String(90), nullable=True)

    active: Mapped[bool] = mapped_column(Boolean)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)

    kids: Mapped[list[Kid]] = relationship(secondary=parent_kid, back_populates='parents')
    contracts_rel: Mapped[list[Contract]] = relationship(secondary=parent_contract, back_populates='parents')


class Transport(Base):
    __tablename__ = 'transport'

    id:  Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    unique_transport_id: Mapped[str] = mapped_column(String(90), nullable=False)
    transport_picture: Mapped[str] = mapped_column(String(400), nullable=False)
    driver: Mapped[int] = mapped_column(ForeignKey('staff.id'), index=True, nullable=False)
    babysitter: Mapped[int] = mapped_column(ForeignKey('staff.id'), index=True, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)

    rel_driver: Mapped[Staff] = relationship(back_populates='transport_rel_driver', foreign_keys=[driver])
    rel_babysitter: Mapped[Staff] = relationship(back_populates='transport_rel_babysitter', foreign_keys=[babysitter])

    kids_rel: Mapped[list[Kid]] = relationship(back_populates='rel_transport')


class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_payment: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_end: Mapped[date] = mapped_column(Date, nullable=False)
    type_of_payment: Mapped[PaymentType] = mapped_column(Enum(PaymentType))
    tariff: Mapped[TariffType] = mapped_column(Enum(TariffType))
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    document: Mapped[str] = mapped_column(String(400), nullable=False)

    kids: Mapped[list[Kid]] = relationship(back_populates='rel_contract')
    parents: Mapped[list[Parent]] = relationship(secondary=parent_contract, back_populates='contracts_rel')


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    family_name: Mapped[str] = mapped_column(String(260), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(90), nullable=False)
    school: Mapped[int] = mapped_column(ForeignKey('schools.id'), nullable=False, index=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    active: Mapped[bool] = mapped_column(Boolean)

    rel_school: Mapped[School] = relationship(back_populates='teachers')
    kids: Mapped[list[Kid]] = relationship(back_populates='rel_teacher')


class School(Base):
    __tablename__ = 'schools'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(260), nullable=False)

    children: Mapped[list[Kid]] = relationship(back_populates='rel_school')
    teachers: Mapped[list[Teacher]] = relationship(back_populates='rel_school')


class Violation(Base):
    __tablename__ = 'violations'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    recipient: Mapped[int] = mapped_column(ForeignKey('staff.id'), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    nature: Mapped[str] = mapped_column(String(260), nullable=False)
    outcome: Mapped[str] = mapped_column(String(260), nullable=False)

    rel_recipient: Mapped[Staff] = relationship(back_populates='violations')
    
    
class Admin():
    __tablename__ = 'admin'
    
    
    
    
    
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)