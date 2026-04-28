"""merge heads

Revision ID: 28a77caefa40
Revises: 20f9ef094165, 91e1ec84a5a0
Create Date: 2026-04-26 17:55:03.693966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28a77caefa40'
down_revision: Union[str, Sequence[str], None] = ('20f9ef094165', '91e1ec84a5a0')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
