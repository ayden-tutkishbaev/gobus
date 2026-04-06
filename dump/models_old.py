from __future__ import annotations

from core import Base

from datetime import UTC, datetime, date, time
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Date, Boolean, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from options import Status, TariffType, PaymentType, StaffType


def tashkent_now():
    return datetime.now(ZoneInfo("Asia/Tashkent"))


class Kid(Base):
    __tablename__ = 'kids'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    family_name: Mapped[str] = mapped_column(String(260), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(400), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(90), nullable=True)
    home_address: Mapped[str] = mapped_column(String(260), nullable=False)
        
    teacher: Mapped[int] = mapped_column(ForeignKey('teachers.id'), nullable=True, index=True)
    school: Mapped[int] = mapped_column(ForeignKey('schools.id'), nullable=False, index=True) 
    contract: Mapped[int] = mapped_column(ForeignKey('contracts.id'), nullable=False, index=True)
    driver: Mapped[int] = mapped_column(ForeignKey('staff.id'), nullable=False, index=True)
    babysitter: Mapped[int] = mapped_column(ForeignKey('staff.id'), nullable=False, index=True)
    transport: Mapped[int] = mapped_column(ForeignKey('transport.id'), nullable=False, index=True)
    
    birth_date: Mapped[date] = mapped_column(Date)
    active: Mapped[bool] = mapped_column(Boolean)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now, nullable=False)
    
    parents_rel: Mapped[list[Parent]] = relationship(back_populates='kids_rel')
    rel_school: Mapped[School] = relationship(back_populates='children_rel')
    rel_contract: Mapped[Contract] = relationship(back_populates='kids_rel')
    rel_driver: Mapped[Staff] = relationship(back_populates='kids_rel', foreign_keys=[driver])
    rel_babysitter: Mapped[Staff] = relationship(back_populates='kids_rel_b', foreign_keys=[babysitter])
    rel_transport: Mapped[Transport] = relationship(back_populates='kids_rel')
    rel_teacher: Mapped[Teacher] = relationship(back_populates='kids_rel')
    
       
    
class Staff(Base):
    __tablename__ = 'staff'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    family_name: Mapped[str] = mapped_column(String(260), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String(400), nullable=False)
    staff_type: Mapped[StaffType] = mapped_column(Enum(StaffType)) # TBD
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(90), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    
    transport_rel_driver: Mapped[list[Transport]] = relationship(back_populates='rel_driver')      # CONNECTED TO TRANSPORT
    transport_rel_babysitter: Mapped[list[Transport]] = relationship(back_populates='rel_babysitter')  # CONNECTED TO TRANSPORT
    
    violation_rel: Mapped[list[Violation]] = relationship(back_populates='rel_recipient')
    kids_rel: Mapped[list[Kid]] = relationship(back_populates='rel_driver')                 # CONNECTED TO KIDS
    kids_rel_b: Mapped[list[Kid]] = relationship(back_populates='rel_babysitter')           # CONNECTED TO KIDS
    
    
class Parent(Base):
    __tablename__ = 'parents'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    family_name: Mapped[str] = mapped_column(String(260), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(90), nullable=True)
    document_id: Mapped[str | None] = mapped_column(String(90), nullable=True)
    
    kids: ... # M2M?
    
    kids_rel: Mapped[list[Kid]] = relationship(back_populates='rel_parents')
    contracts: ... # M2M?
    
    active: Mapped[bool] = mapped_column(Boolean)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    
    
    
class Transport(Base):
    __tablename__ = 'transport'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    unique_transport_id: Mapped[str] = mapped_column(String(90), nullable=False)
    transport_picture: Mapped[str] = mapped_column(String(400), nullable=False) 
    driver: Mapped[int] = mapped_column(ForeignKey('staff.id'), index=True, nullable=False)
    babysitter: Mapped[int] = mapped_column(ForeignKey('staff.id'), index=True, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False) # TBD
    
    rel_driver: Mapped[Staff] = relationship(back_populates='transport_rel_driver', foreign_keys=[driver])
    rel_babysitter: Mapped[Staff] = relationship(back_populates='transport_rel_babysitter', foreign_keys=[babysitter])
    
    kids_rel: Mapped[list[Kid]] = relationship(back_populates='rel_transport')
    
    
    
class Contract(Base):
    __tablename__ = 'contracts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[date] = mapped_column(Date, nullable=False)
    parents: ... # M2M?      # THINK!
    kids: ... # M2M?       # THINK!
    date_of_payment: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_end: Mapped[date] = mapped_column(Date, nullable=False)
    type_of_payment: Mapped[PaymentType] = mapped_column(Enum(PaymentType)) # TBD
    tariff: Mapped[TariffType] = mapped_column(Enum(TariffType)) # TBD
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    document: Mapped[str] = mapped_column(String(400), nullable=False) 
    
    kids_rel: Mapped[list[Kid]] = relationship(back_populates='rel_contract')
    
    
# POSTPONED
 
    
# class Route(Base):
#     __tablename__ = 'routes'

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#     # start_cord: Mapped[float] = mapped_column(Float, nullable=False)
#     # end_cord: Mapped[float] = mapped_column(Float, nullable=False)
#     start_loc: Mapped[str] = mapped_column(String(400), nullable=False) 
#     end_loc: Mapped[str] = mapped_column(String(400), nullable=False) 
#     duration:  Mapped[str] = mapped_column(String(40), nullable=False) 
#     babysitter: ... # >
#     kids: ... # <REL 
#     transport: ... # >
#     active: Mapped[bool] = mapped_column(Boolean)

    
    
class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    family_name: Mapped[str] = mapped_column(String(260), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(90), nullable=False)
    school: Mapped[int] = mapped_column(ForeignKey('schools.id'), nullable=False, index=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=tashkent_now)
    active: Mapped[bool] = mapped_column(Boolean)
    
    rel_school: Mapped[School] = relationship(back_populates='teacher_rel')
    kids_rel: Mapped[list[Kid]] = relationship(back_populates='rel_teacher')
    


class School(Base):
    __tablename__ = 'schools'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(260), nullable=False)
    
    children_rel: Mapped[list[Kid]] = relationship(back_populates='rel_school')
    teacher_rel: Mapped[list[Teacher]] = relationship(back_populates='rel_school')
    
    
class Violation(Base):
    __tablename__ = 'violations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    recipient: Mapped[int] = mapped_column(ForeignKey('staff.id'), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    nature: Mapped[str] = mapped_column(String(260), nullable=False)
    outcome: Mapped[str] = mapped_column(String(260), nullable=False)
    
    rel_recipient: Mapped[Staff] = relationship(back_populates='violation_rel')