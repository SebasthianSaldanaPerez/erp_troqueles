from src.orders.domain.order import Order
from src.presentation.api.orders.schemas import (
    OrderItemResponse,
    OrderResponse,
)


def order_to_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=str(order.id),
        customer_id=str(order.customer_id),
        origin_quotation_id=(
            str(order.origin_quotation_id)
            if order.origin_quotation_id
            else None
        ),
        status=order.status.value,
        billing_status=order.billing_status.value,
        currency=order.currency,
        tax_rate=order.tax_rate.value,
        revision_number=order.revision_number,
        items=[
            OrderItemResponse(
                id=str(item.id),
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price.amount,
                currency=item.unit_price.currency,
                total=item.total.amount,
            )
            for item in order.items
        ],
        subtotal=order.subtotal.amount,
        tax=order.tax.amount,
        total=order.total.amount,
    )