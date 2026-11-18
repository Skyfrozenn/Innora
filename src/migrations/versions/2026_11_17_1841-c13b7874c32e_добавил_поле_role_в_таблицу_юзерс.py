"""Добавил поле role в таблицу юзерс

Revision ID: c13b7874c32e
Revises: 619c0b2dcc4e
Create Date: 2026-11-17 18:41:04.227555

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c13b7874c32e"
down_revision: Union[str, Sequence[str], None] = "619c0b2dcc4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    user_role = postgresql.ENUM(
        "SUPERUSER",
        "ADMIN",
        "BUYER",
        name="user_role",
    )

    user_role.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            server_default="BUYER",
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "role")

    postgresql.ENUM(
        "SUPERUSER",
        "ADMIN",
        "BUYER",
        name="user_role",
    ).drop(op.get_bind(), checkfirst=True)
