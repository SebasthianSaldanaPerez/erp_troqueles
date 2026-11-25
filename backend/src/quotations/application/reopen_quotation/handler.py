from src.quotations.application.errors import QuotationNotFoundError
from src.quotations.application.reopen_quotation.command import (
    ReopenQuotationCommand,
)
from src.quotations.domain.quotation_repository import (
    QuotationRepository,
)


class ReopenQuotationHandler:
    def __init__(
        self,
        repository: QuotationRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: ReopenQuotationCommand,
    ) -> None:
        quotation = self._repository.get_by_id(
            command.quotation_id
        )

        if quotation is None:
            raise QuotationNotFoundError()

        quotation.reopen()

        self._repository.save(
            quotation
        )