"""create email table

Revision ID: edc825660b77
Revises: 
Create Date: 2023-05-26 15:29:41.761678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edc825660b77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('emails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_email')
    )
    pass


def downgrade() -> None:
    op.drop_table('emails')
    pass
