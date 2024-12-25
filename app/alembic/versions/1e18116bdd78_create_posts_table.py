"""create posts table

Revision ID: 1e18116bdd78
Revises: 
Create Date: 2024-12-24 15:26:29.248505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e18116bdd78'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    schema='davicki')
    pass


def downgrade() -> None:
    op.drop_table('posts', schema='davicki')
    pass
