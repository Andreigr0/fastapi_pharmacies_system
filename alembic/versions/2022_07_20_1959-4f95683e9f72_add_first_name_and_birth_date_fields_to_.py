"""add first name and birth date fields to user

Revision ID: 4f95683e9f72
Revises: 46499c4818d7
Create Date: 2022-07-20 19:59:28.521284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f95683e9f72'
down_revision = '46499c4818d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('birth_date', sa.TIMESTAMP(), nullable=True))
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('users', 'birth_date')
    op.drop_column('users', 'first_name')
    # ### end Alembic commands ###
