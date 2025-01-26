"""add_foreign_key_to_posts_table

Revision ID: 4b9ba1f1471b
Revises: 6b22cfc2a9d4
Create Date: 2025-01-25 20:30:48.704716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b9ba1f1471b'
down_revision: Union[str, None] = '6b22cfc2a9d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

myschema:str = 'davicki'

def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False), schema=myschema)
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE", source_schema=myschema, referent_schema=myschema)
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts", schema=myschema)
    op.drop_column('posts', 'owner_id', schema=myschema)
    pass
