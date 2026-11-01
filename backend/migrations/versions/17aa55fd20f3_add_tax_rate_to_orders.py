"""add tax rate to orders

Revision ID: 17aa55fd20f3
Revises: 125fdd0165a8
Create Date: 2026-11-01 00:03:34.465837

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "17aa55fd20f3"
down_revision: Union[str, Sequence[str], None] = "125fdd0165a8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "orders",
        sa.Column(
            "tax_rate",
            sa.Numeric(precision=5, scale=2),
            nullable=True,
        ),
    )

    op.execute(
        "UPDATE orders SET tax_rate = 16.00 WHERE tax_rate IS NULL"
    )

    op.alter_column(
        "orders",
        "tax_rate",
        nullable=False,
    )


def downgrade() -> None:
    op.drop_column(
        "orders",
        "tax_rate",
    )