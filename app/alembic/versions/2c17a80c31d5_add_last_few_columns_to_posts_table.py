"""add_last_few_columns_to_posts_table

Revision ID: 2c17a80c31d5
Revises: 4b9ba1f1471b
Create Date: 2025-01-25 20:31:53.109642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c17a80c31d5'
down_revision: Union[str, None] = '4b9ba1f1471b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

myschema:str = 'davicki'

def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'), schema=myschema)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')), schema=myschema)
    pass

def downgrade() -> None:
    op.drop_column('posts', 'published', schema=myschema)
    op.drop_column('posts', 'created_at', schema=myschema)
    pass
