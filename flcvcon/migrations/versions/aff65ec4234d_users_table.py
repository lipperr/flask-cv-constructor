"""users table

Revision ID: aff65ec4234d
Revises: bd0230159852
Create Date: 2022-12-03 12:16:05.719307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aff65ec4234d'
down_revision = 'bd0230159852'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_email')
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.VARCHAR(length=120), nullable=True))
        batch_op.create_index('ix_user_email', ['email'], unique=False)

    # ### end Alembic commands ###
