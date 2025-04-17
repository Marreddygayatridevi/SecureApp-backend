"""add is_active column to users

Revision ID: ebe2fcd83b32
Revises: 
Create Date: 2025-04-15 17:53:16.906089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebe2fcd83b32'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default='1'))

def downgrade() -> None:
    op.drop_column('users', 'is_active')

