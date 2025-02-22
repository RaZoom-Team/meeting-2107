"""cascade_del

Revision ID: 1ccf0b803e3e
Revises: 4122366e8e4f
Create Date: 2024-10-25 17:20:39.684522

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '1ccf0b803e3e'
down_revision = '4122366e8e4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('attachments_user_id_fkey', 'attachments', type_='foreignkey')
    op.create_foreign_key(None, 'attachments', 'users', ['user_id'], ['id'], ondelete='cascade')
    op.drop_constraint('likes_target_id_fkey', 'likes', type_='foreignkey')
    op.drop_constraint('likes_user_id_fkey', 'likes', type_='foreignkey')
    op.create_foreign_key(None, 'likes', 'users', ['user_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'likes', 'users', ['target_id'], ['id'], ondelete='cascade')
    op.drop_constraint('views_user_id_fkey', 'views', type_='foreignkey')
    op.drop_constraint('views_target_id_fkey', 'views', type_='foreignkey')
    op.create_foreign_key(None, 'views', 'users', ['user_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'views', 'users', ['target_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'views', type_='foreignkey')
    op.drop_constraint(None, 'views', type_='foreignkey')
    op.create_foreign_key('views_target_id_fkey', 'views', 'users', ['target_id'], ['id'])
    op.create_foreign_key('views_user_id_fkey', 'views', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'likes', type_='foreignkey')
    op.drop_constraint(None, 'likes', type_='foreignkey')
    op.create_foreign_key('likes_user_id_fkey', 'likes', 'users', ['user_id'], ['id'])
    op.create_foreign_key('likes_target_id_fkey', 'likes', 'users', ['target_id'], ['id'])
    op.drop_constraint(None, 'attachments', type_='foreignkey')
    op.create_foreign_key('attachments_user_id_fkey', 'attachments', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###