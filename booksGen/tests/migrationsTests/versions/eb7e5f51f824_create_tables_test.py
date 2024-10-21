"""create tables_test

Revision ID: eb7e5f51f824
Revises: 
Create Date: 2024-10-20 13:13:35.555717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb7e5f51f824'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=30), nullable=False),
    sa.Column('create_all', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('namebook', sa.String(length=100), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('yearbook', sa.Integer(), nullable=False),
    sa.Column('edition', sa.Integer(), nullable=False),
    sa.Column('genere', sa.Enum('romance', 'fantasy', 'mystery', 'horror', 'thriller', 'sci_fi', 'crime', 'classics', 'adventure', 'manga', name='bookgenere'), nullable=False),
    sa.Column('ISBN', sa.Integer(), nullable=False),
    sa.Column('editionPublisher', sa.String(length=500), nullable=False),
    sa.Column('summary', sa.String(length=400), nullable=False),
    sa.Column('pageNum', sa.Integer(), nullable=False),
    sa.Column('language', sa.String(length=5), nullable=False),
    sa.Column('state', sa.Enum('added', 'start', 'read', 'not_read', name='bookstate'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    op.drop_table('users')
    # ### end Alembic commands ###
