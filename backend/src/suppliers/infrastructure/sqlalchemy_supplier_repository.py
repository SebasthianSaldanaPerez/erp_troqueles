from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models.supplier_model import SupplierModel
from src.shared.domain.value_objects.address import Address
from src.shared.domain.value_objects.email import Email
from src.shared.domain.value_objects.phone import Phone
from src.shared.domain.value_objects.rfc import RFC
from src.suppliers.domain.supplier import Supplier, SupplierStatus
from src.suppliers.domain.supplier_repository import SupplierRepository


class SQLAlchemySupplierRepository(SupplierRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, supplier: Supplier) -> None:
        model = self._session.get(
            SupplierModel,
            supplier.id,
        )

        if model is None:
            model = SupplierModel(
                id=supplier.id,
                name=supplier.name,
                status=supplier.status.value,
                email=supplier.email.value if supplier.email else None,
                rfc=supplier.rfc.value if supplier.rfc else None,
                phone=supplier.phone.value if supplier.phone else None,
                contact_name=supplier.contact_name,
                notes=supplier.notes,
                address_street=(
                    supplier.address.street
                    if supplier.address
                    else None
                ),
                address_exterior_number=(
                    supplier.address.exterior_number
                    if supplier.address
                    else None
                ),
                address_interior_number=(
                    supplier.address.interior_number
                    if supplier.address
                    else None
                ),
                address_neighborhood=(
                    supplier.address.neighborhood
                    if supplier.address
                    else None
                ),
                address_city=(
                    supplier.address.city
                    if supplier.address
                    else None
                ),
                address_state=(
                    supplier.address.state
                    if supplier.address
                    else None
                ),
                address_postal_code=(
                    supplier.address.postal_code
                    if supplier.address
                    else None
                ),
                address_country=(
                    supplier.address.country
                    if supplier.address
                    else None
                ),
            )

            self._session.add(model)
            return

        model.name = supplier.name
        model.status = supplier.status.value
        model.email = supplier.email.value if supplier.email else None
        model.rfc = supplier.rfc.value if supplier.rfc else None
        model.phone = supplier.phone.value if supplier.phone else None
        model.contact_name = supplier.contact_name
        model.notes = supplier.notes

        if supplier.address:
            model.address_street = supplier.address.street
            model.address_exterior_number = supplier.address.exterior_number
            model.address_interior_number = supplier.address.interior_number
            model.address_neighborhood = supplier.address.neighborhood
            model.address_city = supplier.address.city
            model.address_state = supplier.address.state
            model.address_postal_code = supplier.address.postal_code
            model.address_country = supplier.address.country
        else:
            model.address_street = None
            model.address_exterior_number = None
            model.address_interior_number = None
            model.address_neighborhood = None
            model.address_city = None
            model.address_state = None
            model.address_postal_code = None
            model.address_country = None

    def get_by_id(
        self,
        supplier_id: UUID,
    ) -> Supplier | None:
        model = self._session.get(
            SupplierModel,
            supplier_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_all(self) -> list[Supplier]:
        statement = select(SupplierModel)

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: SupplierModel,
    ) -> Supplier:
        address = None

        if model.address_street:
            address = Address(
                street=model.address_street,
                exterior_number=model.address_exterior_number,
                interior_number=model.address_interior_number,
                neighborhood=model.address_neighborhood,
                city=model.address_city,
                state=model.address_state,
                postal_code=model.address_postal_code,
                country=model.address_country,
            )

        return Supplier(
            supplier_id=model.id,
            name=model.name,
            status=SupplierStatus(model.status),
            email=Email(model.email) if model.email else None,
            rfc=RFC(model.rfc) if model.rfc else None,
            phone=Phone(model.phone) if model.phone else None,
            address=address,
            contact_name=model.contact_name,
            notes=model.notes,
        )