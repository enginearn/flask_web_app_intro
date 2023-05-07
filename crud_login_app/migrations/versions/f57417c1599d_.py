"""empty message

Revision ID: f57417c1599d
Revises: 2c95233ae3d0
Create Date: 2023-05-06 20:53:20.176870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f57417c1599d'
down_revision = '2c95233ae3d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('login',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Boolean(create_constraint=1),
               existing_nullable=True)
        batch_op.drop_index('ix_users_login')
        batch_op.create_index(batch_op.f('ix_users_login'), ['login'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_login'))
        batch_op.create_index('ix_users_login', ['login'], unique=False)
        batch_op.alter_column('login',
               existing_type=sa.Boolean(create_constraint=1),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###