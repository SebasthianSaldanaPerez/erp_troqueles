from src.presentation.api.quotations.schemas import (
    QuotationItemResponse,
    QuotationResponse,
)
from src.quotations.domain.quotation import Quotation


def quotation_to_response(
    quotation: Quotation,
) -> QuotationResponse:
    return QuotationResponse(
        id=str(quotation.id),
        customer_id=str(quotation.customer_id),
        status=quotation.status.value,
        tax_rate=quotation.tax_rate.value,
        currency=quotation.currency,
        items=[
            QuotationItemResponse(
                id=str(item.id),
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price.amount,
                currency=item.unit_price.currency,
                total=item.total.amount,
            )
            for item in quotation.items
        ],
        subtotal=quotation.subtotal.amount,
        tax=quotation.tax.amount,
        total=quotation.total.amount,
    )