"""auto_vote

Revision ID: a1cc31a09ff8
Revises: 2c17a80c31d5
Create Date: 2025-01-25 20:32:44.503198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1cc31a09ff8'
down_revision: Union[str, None] = '2c17a80c31d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


myschema:str = 'davicki'
def upgrade() -> None:
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], [f'{myschema}.posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], [f'{myschema}.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id'),
    schema=myschema
    )


def downgrade() -> None:
    op.drop_table('votes', schema=myschema)
    pass
