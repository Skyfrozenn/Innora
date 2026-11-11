"""Добавил таблицу отелей

Revision ID: 477135dbee72
Revises:
Create Date: 2026-11-08 02:16:59.520957

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "477135dbee72"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("hotels")
    
