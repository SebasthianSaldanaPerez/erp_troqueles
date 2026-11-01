from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.infrastructure.database.models.quotation_model import (
    QuotationItemModel,
    QuotationModel,
)
from src.quotations.domain.quotation import (
    Quotation,
    QuotationStatus,
)
from src.quotations.domain.quotation_item import QuotationItem
from src.quotations.domain.quotation_repository import QuotationRepository
from src.shared.domain.value_objects.money import Money
from src.shared.domain.value_objects.tax_rate import TaxRate


class SQLAlchemyQuotationRepository(QuotationRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, quotation: Quotation) -> None:
        model = self._session.get(
            QuotationModel,
            quotation.id,
        )

        if model is None:
            model = QuotationModel(
                id=quotation.id,
                customer_id=quotation.customer_id,
                status=quotation.status.value,
                tax_rate=quotation.tax_rate.value,
                currency=quotation.currency,
            )

            model.items = [
                QuotationItemModel(
                    id=item.id,
                    quotation_id=quotation.id,
                    description=item.description,
                    quantity=item.quantity,
                    unit_price=item.unit_price.amount,
                    currency=item.unit_price.currency,
                )
                for item in quotation.items
            ]

            self._session.add(model)
            return

        model.customer_id = quotation.customer_id
        model.status = quotation.status.value
        model.tax_rate = quotation.tax_rate.value
        model.currency = quotation.currency

        model.items = [
            QuotationItemModel(
                id=item.id,
                quotation_id=quotation.id,
                description=item.description,
                quantity=item.quantity,
                unit_price=item.unit_price.amount,
                currency=item.unit_price.currency,
            )
            for item in quotation.items
        ]

    def get_by_id(
        self,
        quotation_id: UUID,
    ) -> Quotation | None:
        statement = (
            select(QuotationModel)
            .options(
                selectinload(QuotationModel.items)
            )
            .where(QuotationModel.id == quotation_id)
        )

        model = self._session.scalars(
            statement
        ).first()

        if model is None:
            return None

        return self._to_domain(model)

    def list_all(self) -> list[Quotation]:
        statement = (
            select(QuotationModel)
            .options(
                selectinload(QuotationModel.items)
            )
        )

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: QuotationModel,
    ) -> Quotation:
        items = [
            QuotationItem(
                item_id=item_model.id,
                description=item_model.description,
                quantity=item_model.quantity,
                unit_price=Money(
                    amount=item_model.unit_price,
                    currency=item_model.currency,
                ),
            )
            for item_model in model.items
        ]

        return Quotation.rehydrate(
            quotation_id=model.id,
            customer_id=model.customer_id,
            tax_rate=TaxRate(model.tax_rate),
            currency=model.currency,
            status=QuotationStatus(model.status),
            items=items,
        )