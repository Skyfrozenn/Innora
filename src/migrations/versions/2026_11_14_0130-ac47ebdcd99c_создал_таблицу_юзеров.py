"""Создал таблицу юзеров

Revision ID: ac47ebdcd99c
Revises: 556a57a6750b
Create Date: 2026-11-14 01:30:04.141135

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ac47ebdcd99c"
down_revision: Union[str, Sequence[str], None] = "556a57a6750b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("hash_password", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    
