"""add_user_table

Revision ID: 6b22cfc2a9d4
Revises: fa7753d080b0
Create Date: 2025-01-25 20:29:46.173104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b22cfc2a9d4'
down_revision: Union[str, None] = 'fa7753d080b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

myschema:str = 'davicki'

def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    schema=myschema
                    )
    pass


def downgrade() -> None:
    op.drop_table('users', schema=myschema)
    pass
