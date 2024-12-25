"""add user table

Revision ID: 096182535c54
Revises: ce30d4dcb6c6
Create Date: 2024-12-24 16:01:14.676684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '096182535c54'
down_revision: Union[str, None] = 'ce30d4dcb6c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    schema='davicki')
    pass


def downgrade() -> None:
    op.drop_table('users', schema='davicki')
    pass
