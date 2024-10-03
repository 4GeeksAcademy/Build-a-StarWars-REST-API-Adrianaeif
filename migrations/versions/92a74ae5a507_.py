"""empty message

Revision ID: 92a74ae5a507
Revises: 4830d815dd97
Create Date: 2024-10-02 13:45:03.209729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92a74ae5a507'
down_revision = '4830d815dd97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('character_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('favorite_character_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorite_planet_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorite_user_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.create_foreign_key(None, 'planet', ['planet_id'], ['id'])
        batch_op.create_foreign_key(None, 'character', ['character_id'], ['id'])
        batch_op.drop_column('user')
        batch_op.drop_column('character')
        batch_op.drop_column('planet')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('character', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorite_user_fkey', 'user', ['user'], ['id'])
        batch_op.create_foreign_key('favorite_planet_fkey', 'planet', ['planet'], ['id'])
        batch_op.create_foreign_key('favorite_character_fkey', 'character', ['character'], ['id'])
        batch_op.drop_column('planet_id')
        batch_op.drop_column('character_id')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###