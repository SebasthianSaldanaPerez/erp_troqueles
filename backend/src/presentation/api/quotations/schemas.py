from decimal import Decimal

from pydantic import BaseModel


class CreateQuotationRequest(BaseModel):
    customer_id: str
    tax_rate: Decimal
    currency: str = "MXN"


class CreateQuotationResponse(BaseModel):
    id: str


class QuotationItemResponse(BaseModel):
    id: str
    description: str
    quantity: int
    unit_price: Decimal
    currency: str
    total: Decimal


class QuotationResponse(BaseModel):
    id: str
    customer_id: str
    status: str
    tax_rate: Decimal
    currency: str
    items: list[QuotationItemResponse]
    subtotal: Decimal
    tax: Decimal
    total: Decimal

class AddQuotationItemRequest(BaseModel):
    description: str
    quantity: int
    unit_price: Decimal
    currency: str = "MXN"


class UpdateQuotationItemRequest(BaseModel):
    description: str
    quantity: int
    unit_price: Decimal
    currency: str = "MXN"


class QuotationItemCreatedResponse(BaseModel):
    id: str