"""create user table

Revision ID: e47836b8a4df
Revises: edc825660b77
Create Date: 2023-05-26 15:29:50.677090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e47836b8a4df'
down_revision = 'edc825660b77'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_id', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_on', sa.DateTime(), nullable=True),
    sa.Column('is_logged_in', sa.Boolean(), server_default='False', nullable=False),
    sa.ForeignKeyConstraint(['email_id'], ['emails.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
