"""add last few columns to post

Revision ID: b71a1388fb0b
Revises: 4ae2c4709b84
Create Date: 2024-12-24 16:53:25.472557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b71a1388fb0b'
down_revision: Union[str, None] = '4ae2c4709b84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default='TRUE'), schema='davicki')
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('NOW()')), schema='davicki')
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published', schema='davicki')
    op.drop_column('posts', 'created_at', schema='davicki')
    pass
