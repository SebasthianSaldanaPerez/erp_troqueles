from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.domain.quotation_repository import QuotationRepository

from .command import SendQuotationCommand


class SendQuotationHandler:

    def __init__(self, repository: QuotationRepository):
        self._repository = repository

    def execute(self, command: SendQuotationCommand) -> None:
        quotation = self._repository.get_by_id(command.quotation_id)

        if quotation is None:
            raise QuotationNotFoundError(
                f"Quotation {command.quotation_id} was not found"
            )

        quotation.send()

        self._repository.save(quotation)