"""setnull_on_del_focus

Revision ID: ffe8d61cff53
Revises: 2203b9a0f3dd
Create Date: 2024-11-04 19:05:12.777478

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'ffe8d61cff53'
down_revision = '2203b9a0f3dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_focus_id_fkey', 'users', type_='foreignkey')
    op.create_foreign_key(None, 'users', 'users', ['focus_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.create_foreign_key('users_focus_id_fkey', 'users', 'users', ['focus_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###