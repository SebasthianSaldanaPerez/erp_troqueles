from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.customers.infrastructure.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)
from src.infrastructure.database.session import SessionLocal
from src.suppliers.infrastructure.sqlalchemy_supplier_repository import (
    SQLAlchemySupplierRepository,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_customer_repository(
    db: Session = Depends(get_db),
) -> SQLAlchemyCustomerRepository:
    return SQLAlchemyCustomerRepository(db)

def get_supplier_repository(
    db: Session = Depends(get_db),
) -> SQLAlchemySupplierRepository:
    return SQLAlchemySupplierRepository(db)