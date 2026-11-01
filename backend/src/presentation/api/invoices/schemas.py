from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class RegisterInvoiceRequest(BaseModel):
    folio: str
    invoice_date: date
    total: Decimal
    currency: str = "MXN"


class RegisterInvoiceResponse(BaseModel):
    id: str


class InvoiceResponse(BaseModel):
    id: str
    order_id: str
    folio: str
    invoice_date: date
    total: Decimal
    currency: str
    status: str