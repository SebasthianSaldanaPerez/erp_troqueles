from decimal import Decimal

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: str
    description: str
    quantity: int
    unit_price: Decimal
    currency: str
    total: Decimal


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    origin_quotation_id: str | None
    status: str
    billing_status: str
    currency: str
    tax_rate: Decimal
    revision_number: int
    items: list[OrderItemResponse]
    subtotal: Decimal
    tax: Decimal
    total: Decimal

class OrderProfitabilityResponse(BaseModel):
    revenue: Decimal
    expenses: Decimal
    profit: Decimal
    margin: Decimal
    currency: str