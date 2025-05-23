"""new 1

Revision ID: ce254ba02d0d
Revises: ba2754255513
Create Date: 2025-05-17 23:10:57.726348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce254ba02d0d'
down_revision: Union[str, None] = 'ba2754255513'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('berths', sa.Column('maintenance_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'berths', 'maintenance_logs', ['maintenance_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'berths', type_='foreignkey')
    op.drop_column('berths', 'maintenance_id')
    # ### end Alembic commands ###
