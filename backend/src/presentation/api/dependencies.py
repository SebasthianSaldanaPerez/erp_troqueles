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
from src.quotations.infrastructure.sqlalchemy_quotation_repository import (
    SQLAlchemyQuotationRepository,
)
from src.orders.infrastructure.sqlalchemy_order_repository import (
    SQLAlchemyOrderRepository,
)
from src.expenses.infrastructure.sqlalchemy_expense_repository import (
    SQLAlchemyExpenseRepository,
)
from src.invoices.infrastructure.sqlalchemy_invoice_repository import (
    SQLAlchemyInvoiceRepository,
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

def get_quotation_repository(
    db: Session = Depends(get_db),
) -> SQLAlchemyQuotationRepository:
    return SQLAlchemyQuotationRepository(db)

def get_order_repository(
    db: Session = Depends(get_db),
) -> SQLAlchemyOrderRepository:
    return SQLAlchemyOrderRepository(db)

def get_expense_repository(
    db: Session = Depends(get_db),
) -> SQLAlchemyExpenseRepository:
    return SQLAlchemyExpenseRepository(db)

def get_invoice_repository(
    db: Session = Depends(get_db),
) -> SQLAlchemyInvoiceRepository:
    return SQLAlchemyInvoiceRepository(db)