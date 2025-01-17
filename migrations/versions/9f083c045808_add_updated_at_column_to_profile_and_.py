"""Add updated_at column to profile and thought tables

Revision ID: 9f083c045808
Revises: 
Create Date: 2025-01-16 19:17:33.383420

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9f083c045808'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Sadece thought tablosuna updated_at sütunu ekleniyor
    op.add_column('thought', sa.Column('updated_at', sa.DateTime(), nullable=True))

def downgrade():
    # Sadece thought tablosundan updated_at sütunu siliniyor
    op.drop_column('thought', 'updated_at')

