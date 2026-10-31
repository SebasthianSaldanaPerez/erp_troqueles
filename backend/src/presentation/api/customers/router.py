from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.customers.application.create_customer.command import (
    CreateCustomerCommand,
)
from src.customers.application.create_customer.handler import (
    CreateCustomerHandler,
)
from src.customers.infrastructure.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)
from src.presentation.api.customers.schemas import (
    AddressResponse,
    CreateCustomerRequest,
    CreateCustomerResponse,
    CustomerResponse,
)
from src.presentation.api.dependencies import get_db

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from src.customers.application.errors import CustomerNotFoundError
from src.customers.application.get_customer.handler import GetCustomerHandler
from src.customers.application.get_customer.query import GetCustomerQuery
from src.customers.application.list_customers.handler import (
    ListCustomersHandler,
)
from src.customers.application.list_customers.query import (
    ListCustomersQuery,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=CreateCustomerResponse,
    status_code=201,
)
def create_customer(
    request: CreateCustomerRequest,
    db: Session = Depends(get_db),
) -> CreateCustomerResponse:
    repository = SQLAlchemyCustomerRepository(db)

    handler = CreateCustomerHandler(repository)

    command = CreateCustomerCommand(
    business_name=request.business_name,
    email=request.email,
    rfc=request.rfc,
    phone=request.phone,

    address_street=(
        request.address.street
        if request.address
        else None
    ),
    address_exterior_number=(
        request.address.exterior_number
        if request.address
        else None
    ),
    address_interior_number=(
        request.address.interior_number
        if request.address
        else None
    ),
    address_neighborhood=(
        request.address.neighborhood
        if request.address
        else None
    ),
    address_city=(
        request.address.city
        if request.address
        else None
    ),
    address_state=(
        request.address.state
        if request.address
        else None
    ),
    address_postal_code=(
        request.address.postal_code
        if request.address
        else None
    ),
    address_country=(
        request.address.country
        if request.address
        else None
    ),

    contact_name=request.contact_name,
    notes=request.notes,
)
    customer_id = handler.execute(command)

    db.commit()

    return CreateCustomerResponse(
        id=str(customer_id),
    )



@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
) -> CustomerResponse:
    repository = SQLAlchemyCustomerRepository(db)
    handler = GetCustomerHandler(repository)

    try:
        customer = handler.execute(
            GetCustomerQuery(
                customer_id=customer_id,
            )
        )
    except CustomerNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    return CustomerResponse(
        id=str(customer.id),
        business_name=customer.business_name,
        status=customer.status.value,
        email=customer.email.value if customer.email else None,
        rfc=customer.rfc.value if customer.rfc else None,
        phone=customer.phone.value if customer.phone else None,
        contact_name=customer.contact_name,
        notes=customer.notes,
        address=(
        AddressResponse(
            street=customer.address.street,
            exterior_number=customer.address.exterior_number,
            interior_number=customer.address.interior_number,
            neighborhood=customer.address.neighborhood,
            city=customer.address.city,
            state=customer.address.state,
            postal_code=customer.address.postal_code,
            country=customer.address.country,
        )
        if customer.address
        else None
    ),
    )

@router.get(
    "",
    response_model=list[CustomerResponse],
)
def list_customers(
    db: Session = Depends(get_db),
) -> list[CustomerResponse]:
    repository = SQLAlchemyCustomerRepository(db)
    handler = ListCustomersHandler(repository)

    customers = handler.execute(
        ListCustomersQuery()
    )

    return [
        CustomerResponse(
            id=str(customer.id),
            business_name=customer.business_name,
            status=customer.status.value,
            email=customer.email.value if customer.email else None,
            rfc=customer.rfc.value if customer.rfc else None,
            phone=customer.phone.value if customer.phone else None,
            contact_name=customer.contact_name,
            notes=customer.notes,
            address=(
            AddressResponse(
                street=customer.address.street,
                exterior_number=customer.address.exterior_number,
                interior_number=customer.address.interior_number,
                neighborhood=customer.address.neighborhood,
                city=customer.address.city,
                state=customer.address.state,
                postal_code=customer.address.postal_code,
                country=customer.address.country,
            )
            if customer.address
            else None
        ),
        )
        for customer in customers
    ]