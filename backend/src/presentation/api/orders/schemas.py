from decimal import Decimal

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


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

class ReviseOrderRequest(BaseModel):
    item_id: UUID
    description: str
    quantity: int
    unit_price: Decimal
    currency: str = "MXN"
    reason: str
    user_id: UUID


class OrderRevisionResponse(BaseModel):
    id: str
    order_id: str
    revision_number: int
    snapshot: dict
    reason: str
    created_by: str
    created_at: datetime