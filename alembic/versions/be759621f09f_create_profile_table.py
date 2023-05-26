"""create profile table

Revision ID: be759621f09f
Revises: e47836b8a4df
Create Date: 2023-05-26 15:29:52.893379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be759621f09f'
down_revision = 'e47836b8a4df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('phone_number', sa.BigInteger(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('highest_qualification', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    pass


def downgrade() -> None:
    op.drop_table('profiles')
    pass
