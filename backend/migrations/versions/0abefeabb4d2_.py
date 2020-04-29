"""empty message

Revision ID: 0abefeabb4d2
Revises: cd5c43ade505
Create Date: 2020-04-27 06:17:53.362511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0abefeabb4d2'
down_revision = 'cd5c43ade505'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.drop_column('users', 'user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'name')
    # ### end Alembic commands ###