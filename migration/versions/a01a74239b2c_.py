"""empty message

Revision ID: a01a74239b2c
Revises: 7f731eb40f40
Create Date: 2026-05-06 23:43:55.766288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a01a74239b2c'
down_revision: Union[str, Sequence[str], None] = '7f731eb40f40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
