"""add content column

Revision ID: ce30d4dcb6c6
Revises: 1e18116bdd78
Create Date: 2024-12-24 15:56:55.034593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce30d4dcb6c6'
down_revision: Union[str, None] = '1e18116bdd78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False), schema='davicki')
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content', schema='davicki')
    pass
