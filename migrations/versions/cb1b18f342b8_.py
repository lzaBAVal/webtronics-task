"""empty message

Revision ID: cb1b18f342b8
Revises: 7562329621b7
Create Date: 2023-01-12 01:05:48.209012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb1b18f342b8'
down_revision = '7562329621b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
