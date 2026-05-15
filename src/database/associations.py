from sqlalchemy import Table, Column, ForeignKey
from src.database.core import Base


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