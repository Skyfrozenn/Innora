"""Добавил поля is_active, created_at, updated_at для таблицы Юзерс

Revision ID: 619c0b2dcc4e
Revises: f95fa5eb8b1f
Create Date: 2026-11-14 19:16:23.751457

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "619c0b2dcc4e"
down_revision: Union[str, Sequence[str], None] = "f95fa5eb8b1f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False))
    op.add_column(
        "users",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
    op.drop_column("users", "is_active")
    
