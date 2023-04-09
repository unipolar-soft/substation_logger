"""add prefix column to substation

Revision ID: f4652ecf6d39
Revises: 
Create Date: 2023-04-09 11:27:05.112825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4652ecf6d39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('substation', sa.Column('prefix', sa.String(length=100), nullable=True))


def downgrade() -> None:
    op.drop_column('substation', 'prefix')
