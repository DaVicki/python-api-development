"""create_posts_table

Revision ID: 3db9c0567e2f
Revises: 
Create Date: 2025-01-25 20:26:58.116395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3db9c0567e2f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


myschema:str = 'davicki'

def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False), schema=myschema)
    pass


def downgrade() -> None:
    op.drop_table('posts', schema=myschema)
    pass
