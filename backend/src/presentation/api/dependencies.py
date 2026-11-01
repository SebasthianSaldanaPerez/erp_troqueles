from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.customers.infrastructure.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)
from src.infrastructure.database.session import SessionLocal


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