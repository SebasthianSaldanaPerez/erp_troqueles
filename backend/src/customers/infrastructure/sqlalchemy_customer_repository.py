from uuid import UUID

from sqlalchemy.orm import Session

from src.customers.domain.customer import Customer, CustomerStatus
from src.customers.domain.customer_repository import CustomerRepository
from src.infrastructure.database.models.customer_model import CustomerModel
from src.shared.domain.value_objects.email import Email
from src.shared.domain.value_objects.phone import Phone
from src.shared.domain.value_objects.rfc import RFC
from src.shared.domain.value_objects.address import Address


class SQLAlchemyCustomerRepository(CustomerRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, customer: Customer) -> None:
        model = self._session.get(CustomerModel, customer.id)

        if model is None:
            model = CustomerModel(
                id=customer.id,
                business_name=customer.business_name,
                status=customer.status.value,
                email=customer.email.value if customer.email else None,
                rfc=customer.rfc.value if customer.rfc else None,
                phone=customer.phone.value if customer.phone else None,
                contact_name=customer.contact_name,
                notes=customer.notes,
                address_street=(
                customer.address.street
                if customer.address
                else None
            ),
            address_exterior_number=(
                customer.address.exterior_number
                if customer.address
                else None
            ),
            address_interior_number=(
                customer.address.interior_number
                if customer.address
                else None
            ),
            address_neighborhood=(
                customer.address.neighborhood
                if customer.address
                else None
            ),
            address_city=(
                customer.address.city
                if customer.address
                else None
            ),
            address_state=(
                customer.address.state
                if customer.address
                else None
            ),
            address_postal_code=(
                customer.address.postal_code
                if customer.address
                else None
            ),
            address_country=(
                customer.address.country
                if customer.address
                else None
            ),
            )

            self._session.add(model)

        else:
            model.business_name = customer.business_name
            model.status = customer.status.value
            model.email = customer.email.value if customer.email else None
            model.rfc = customer.rfc.value if customer.rfc else None
            model.phone = customer.phone.value if customer.phone else None
            model.contact_name = customer.contact_name
            model.notes = customer.notes
        if customer.address:
            model.address_street = customer.address.street
            model.address_exterior_number = customer.address.exterior_number
            model.address_interior_number = customer.address.interior_number
            model.address_neighborhood = customer.address.neighborhood
            model.address_city = customer.address.city
            model.address_state = customer.address.state
            model.address_postal_code = customer.address.postal_code
            model.address_country = customer.address.country
        else:
            model.address_street = None
            model.address_exterior_number = None
            model.address_interior_number = None
            model.address_neighborhood = None
            model.address_city = None
            model.address_state = None
            model.address_postal_code = None
            model.address_country = None

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        model = self._session.get(CustomerModel, customer_id)

        if model is None:
            return None

        return self._to_domain(model)

    def list_all(self) -> list[Customer]:
        models = self._session.query(CustomerModel).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(model: CustomerModel) -> Customer:

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

        return Customer(
            customer_id=model.id,
            business_name=model.business_name,
            status=CustomerStatus(model.status),
            email=Email(model.email) if model.email else None,
            rfc=RFC(model.rfc) if model.rfc else None,
            phone=Phone(model.phone) if model.phone else None,
            address=address,
            contact_name=model.contact_name,
            notes=model.notes,
        )