"""add_property_fields

Revision ID: 83f7e1666aaf
Revises: eeca96ef9b91
Create Date: 2026-07-09 16:22:04.789970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = '83f7e1666aaf'
down_revision: Union[str, None] = 'eeca96ef9b91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   
    op.add_column('properties', sa.Column('purpose', sa.String(length=50), nullable=True))
    op.add_column('properties', sa.Column('parking', sa.Boolean(), nullable=True))
    op.add_column('properties', sa.Column('furnishing_status', sa.String(length=50), nullable=True))



def downgrade() -> None:
    
    op.drop_column('properties', 'furnishing_status')
    op.drop_column('properties', 'parking')
    op.drop_column('properties', 'purpose')
   
