"""add foreign key to post table

Revision ID: 4ae2c4709b84
Revises: 096182535c54
Create Date: 2024-12-24 16:45:09.843974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ae2c4709b84'
down_revision: Union[str, None] = '096182535c54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),
                  nullable=False), schema='davicki')
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE", source_schema='davicki', referent_schema='davicki')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts', schema='davicki')
    op.drop_column('posts', 'owner_id', schema='davicki')
    pass
