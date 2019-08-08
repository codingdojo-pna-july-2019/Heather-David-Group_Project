"""empty message

Revision ID: 05aeaa4e9609
Revises: 
Create Date: 2019-08-07 18:47:24.739800

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05aeaa4e9609'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('events_flag_karaoke', sa.Boolean(), nullable=True),
    sa.Column('events_flag_trivia', sa.Boolean(), nullable=True),
    sa.Column('events_flag_billiards', sa.Boolean(), nullable=True),
    sa.Column('events_flag_football', sa.Boolean(), nullable=True),
    sa.Column('events_flag_potluck', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('date_updated', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('beers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brewery_name', sa.String(length=255), nullable=True),
    sa.Column('beer_name', sa.String(length=255), nullable=True),
    sa.Column('beer_type', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('abv', sa.Numeric(precision=2, scale=1), nullable=True),
    sa.Column('ibu', sa.Integer(), nullable=True),
    sa.Column('nitro_flag', sa.Boolean(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('date_updated', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['admins.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('foods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('date_updated', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['admins.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('liquors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('liquor_type', sa.Text(), nullable=True),
    sa.Column('proof', sa.Numeric(precision=3), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('date_updated', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['admins.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('liquors')
    op.drop_table('foods')
    op.drop_table('beers')
    op.drop_table('admins')
    op.drop_table('users')
    # ### end Alembic commands ###