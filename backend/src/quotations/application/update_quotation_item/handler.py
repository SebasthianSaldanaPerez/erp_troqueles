from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.domain.quotation_repository import QuotationRepository
from src.shared.domain.value_objects.money import Money

from .command import UpdateQuotationItemCommand


class UpdateQuotationItemHandler:

    def __init__(self, repository: QuotationRepository):
        self._repository = repository

    def execute(self, command: UpdateQuotationItemCommand) -> None:
        quotation = self._repository.get_by_id(command.quotation_id)

        if quotation is None:
            raise QuotationNotFoundError(
                f"Quotation {command.quotation_id} was not found"
            )

        unit_price = Money(
            amount=command.unit_price,
            currency=command.currency,
        )

        quotation.update_item(
            item_id=command.item_id,
            description=command.description,
            quantity=command.quantity,
            unit_price=unit_price,
        )

        self._repository.save(quotation)