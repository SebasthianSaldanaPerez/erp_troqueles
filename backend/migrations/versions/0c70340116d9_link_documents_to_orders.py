"""link documents to orders

Revision ID: 0c70340116d9
Revises: a66113bd78f6
Create Date: 2026-11-01 19:04:03.981166
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0c70340116d9"
down_revision: Union[str, Sequence[str], None] = "a66113bd78f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add column temporarily allowing NULL
    op.add_column(
        "documents",
        sa.Column(
            "order_id",
            sa.UUID(),
            nullable=True,
        ),
    )

    # 2. Recover order_id from:
    # orders/{order_id}/{filename}
    op.execute(
        """
        UPDATE documents
        SET order_id = split_part(object_key, '/', 2)::uuid
        WHERE object_key LIKE 'orders/%/%'
        """
    )

    # 3. Now make it required
    op.alter_column(
        "documents",
        "order_id",
        nullable=False,
    )

    # 4. Create FK with an explicit name
    op.create_foreign_key(
        "fk_documents_order_id_orders",
        "documents",
        "orders",
        ["order_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_documents_order_id_orders",
        "documents",
        type_="foreignkey",
    )

    op.drop_column(
        "documents",
        "order_id",
    )