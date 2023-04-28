"""add content column to posts table

Revision ID: 35d3c243101a
Revises: fe6fb0e2d505
Create Date: 2023-04-28 21:19:53.806595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35d3c243101a'
down_revision = 'fe6fb0e2d505'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
