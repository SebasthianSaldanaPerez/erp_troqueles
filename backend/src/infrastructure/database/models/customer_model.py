from uuid import UUID

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base


class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
    )

    business_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    rfc: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    contact_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    address_street: Mapped[str | None] = mapped_column(
    String(255),
    nullable=True,
    )

    address_exterior_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    address_interior_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    address_neighborhood: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address_city: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address_state: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    address_postal_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    address_country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )