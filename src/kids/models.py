from src.database.core import Base
import uuid
from datetime import date

from sqlalchemy import ForeignKey, String, Date, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.parents.models import parent_kid


class Kid(Base):
    __tablename__ = 'kids'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True,
                                          default=uuid.uuid4)
    last_name: Mapped[str] = mapped_column(String(260), nullable=False)
    first_name: Mapped[str] = mapped_column(String(260), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(260), nullable=False)
    profile_photo_url: Mapped[str] = mapped_column(String(400), nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    phone_number: Mapped[str | None] = mapped_column(String(90), nullable=True)
    
    school_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("schools.id"), nullable=True, index=True)
    route_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("routes.id"), nullable=True, index=True)
    contract_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("contracts.id"), nullable=True, index=True)
    teacher_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("teachers.id"), nullable=True, index=True)
    
    school: Mapped["School"] = relationship(back_populates='kids')
    route: Mapped["Route"] = relationship(back_populates='kids')
    contract: Mapped["Contract"] = relationship(back_populates='kids')
    teacher: Mapped["Teacher"] = relationship(back_populates='kids')
    
    parents: Mapped[list["Parent"]] = relationship(secondary=parent_kid, back_populates='kids')

    home_address: Mapped[str] = mapped_column(String(260), nullable=False)

# TODO: REL