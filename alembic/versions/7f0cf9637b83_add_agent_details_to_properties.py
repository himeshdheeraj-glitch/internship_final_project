"""add_agent_details_to_properties

Revision ID: 7f0cf9637b83
Revises: 83f7e1666aaf
Create Date: 2026-07-10 22:03:24.113599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = '7f0cf9637b83'
down_revision: Union[str, None] = '83f7e1666aaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.add_column('properties', sa.Column('agent_name', sa.String(length=100), nullable=True))
    op.add_column('properties', sa.Column('agent_phone', sa.String(length=20), nullable=True))
    op.add_column('properties', sa.Column('agent_email', sa.String(length=255), nullable=True))
   


def downgrade() -> None:
    
    op.drop_column('properties', 'agent_email')
    op.drop_column('properties', 'agent_phone')
    op.drop_column('properties', 'agent_name')
  
