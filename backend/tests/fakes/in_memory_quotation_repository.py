from src.quotations.domain.quotation import Quotation
from src.quotations.domain.quotation_repository import QuotationRepository


class InMemoryQuotationRepository(QuotationRepository):

    def __init__(self):
        self.quotations = []

    def save(self, quotation: Quotation) -> None:
        for index, existing_quotation in enumerate(self.quotations):
            if existing_quotation.id == quotation.id:
                self.quotations[index] = quotation
                return

        self.quotations.append(quotation)

    def get_by_id(self, quotation_id):
        for quotation in self.quotations:
            if quotation.id == quotation_id:
                return quotation

        return None

    def list_all(self) -> list[Quotation]:
        return list(self.quotations)