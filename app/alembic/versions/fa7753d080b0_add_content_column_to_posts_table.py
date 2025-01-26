"""add_content_column_to_posts_table

Revision ID: fa7753d080b0
Revises: 3db9c0567e2f
Create Date: 2025-01-25 20:28:46.022697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa7753d080b0'
down_revision: Union[str, None] = '3db9c0567e2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

myschema:str = 'davicki'

def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False), schema=myschema)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content', schema=myschema)
    pass
