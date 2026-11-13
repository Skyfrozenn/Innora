"""Сделал поле отелей title уникальным

Revision ID: f95fa5eb8b1f
Revises: ac47ebdcd99c
Create Date: 2026-11-14 01:44:31.390411

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f95fa5eb8b1f"
down_revision: Union[str, Sequence[str], None] = "ac47ebdcd99c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "hotels", ["title"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "hotels", type_="unique")

