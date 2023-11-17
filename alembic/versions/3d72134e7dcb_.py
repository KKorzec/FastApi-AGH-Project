"""empty message

Revision ID: 3d72134e7dcb
Revises: 3fba181f5f93
Create Date: 2022-05-22 16:47:35.528679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d72134e7dcb'
down_revision = '3fba181f5f93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('koszyk',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('data_utworzenia', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['uzytkownicy.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('przemioty_koszyka',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('koszyk_id', sa.Integer(), nullable=True),
    sa.Column('film_id', sa.Integer(), nullable=True),
    sa.Column('data_utworzenia', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['film_id'], ['filmy.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['koszyk_id'], ['koszyk.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('przemioty_koszyka')
    op.drop_table('koszyk')
    # ### end Alembic commands ###
