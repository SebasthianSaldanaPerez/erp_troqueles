from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.customers.application.change_customer_address.command import (
    ChangeCustomerAddressCommand,
)
from src.customers.application.change_customer_address.handler import (
    ChangeCustomerAddressHandler,
)
from src.customers.application.change_customer_contact_name.command import (
    ChangeCustomerContactNameCommand,
)
from src.customers.application.change_customer_contact_name.handler import (
    ChangeCustomerContactNameHandler,
)
from src.customers.application.change_customer_email.command import (
    ChangeCustomerEmailCommand,
)
from src.customers.application.change_customer_email.handler import (
    ChangeCustomerEmailHandler,
)
from src.customers.application.change_customer_notes.command import (
    ChangeCustomerNotesCommand,
)
from src.customers.application.change_customer_notes.handler import (
    ChangeCustomerNotesHandler,
)
from src.customers.application.change_customer_phone.command import (
    ChangeCustomerPhoneCommand,
)
from src.customers.application.change_customer_phone.handler import (
    ChangeCustomerPhoneHandler,
)
from src.customers.application.change_customer_rfc.command import (
    ChangeCustomerRFCCommand,
)
from src.customers.application.change_customer_rfc.handler import (
    ChangeCustomerRFCHandler,
)
from src.customers.application.create_customer.command import (
    CreateCustomerCommand,
)
from src.customers.application.create_customer.handler import (
    CreateCustomerHandler,
)
from src.customers.application.deactivate_customer.command import (
    DeactivateCustomerCommand,
)
from src.customers.application.deactivate_customer.handler import (
    DeactivateCustomerHandler,
)
from src.customers.application.errors import CustomerNotFoundError
from src.customers.application.get_customer.handler import (
    GetCustomerHandler,
)
from src.customers.application.get_customer.query import (
    GetCustomerQuery,
)
from src.customers.application.list_customers.handler import (
    ListCustomersHandler,
)
from src.customers.application.list_customers.query import (
    ListCustomersQuery,
)
from src.customers.application.reactivate_customer.command import (
    ReactivateCustomerCommand,
)
from src.customers.application.reactivate_customer.handler import (
    ReactivateCustomerHandler,
)
from src.customers.application.rename_customer.command import (
    RenameCustomerCommand,
)
from src.customers.application.rename_customer.handler import (
    RenameCustomerHandler,
)
from src.customers.infrastructure.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)
from src.presentation.api.customers.mappers import customer_to_response
from src.presentation.api.customers.schemas import (
    ChangeCustomerAddressRequest,
    ChangeCustomerContactNameRequest,
    ChangeCustomerEmailRequest,
    ChangeCustomerNotesRequest,
    ChangeCustomerPhoneRequest,
    ChangeCustomerRFCRequest,
    CreateCustomerRequest,
    CreateCustomerResponse,
    CustomerResponse,
    RenameCustomerRequest,
)
from src.presentation.api.dependencies import (
    get_customer_repository,
    get_db,
)
from src.shared.domain.errors import (
    InvalidAddressError,
    InvalidEmailError,
    InvalidPhoneError,
    InvalidRFCError,
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
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> CreateCustomerResponse:
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

    try:
        customer_id = handler.execute(command)
        db.commit()

    except (
        InvalidEmailError,
        InvalidRFCError,
        InvalidPhoneError,
        InvalidAddressError,
    ) as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise

    return CreateCustomerResponse(
        id=str(customer_id),
    )


@router.get(
    "",
    response_model=list[CustomerResponse],
)
def list_customers(
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> list[CustomerResponse]:
    handler = ListCustomersHandler(repository)

    customers = handler.execute(
        ListCustomersQuery()
    )

    return [
        customer_to_response(customer)
        for customer in customers
    ]


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: UUID,
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> CustomerResponse:
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

    return customer_to_response(customer)


@router.patch(
    "/{customer_id}/name",
    status_code=204,
)
def rename_customer(
    customer_id: UUID,
    request: RenameCustomerRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> None:
    handler = RenameCustomerHandler(repository)

    command = RenameCustomerCommand(
        customer_id=customer_id,
        new_business_name=request.new_business_name,
    )

    try:
        handler.execute(command)
        db.commit()

    except CustomerNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{customer_id}/deactivate",
    status_code=204,
)
def deactivate_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> None:
    handler = DeactivateCustomerHandler(repository)

    command = DeactivateCustomerCommand(
        customer_id=customer_id,
    )

    try:
        handler.execute(command)
        db.commit()

    except CustomerNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{customer_id}/reactivate",
    status_code=204,
)
def reactivate_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> None:
    handler = ReactivateCustomerHandler(repository)

    command = ReactivateCustomerCommand(
        customer_id=customer_id,
    )

    try:
        handler.execute(command)
        db.commit()

    except CustomerNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{customer_id}/email",
    status_code=204,
)
def change_customer_email(
    customer_id: UUID,
    request: ChangeCustomerEmailRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> None:
    handler = ChangeCustomerEmailHandler(repository)

    command = ChangeCustomerEmailCommand(
        customer_id=customer_id,
        new_email=request.new_email,
    )

    try:
        handler.execute(command)
        db.commit()

    except CustomerNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    except InvalidEmailError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{customer_id}/rfc",
    status_code=204,
)
def change_customer_rfc(
    customer_id: UUID,
    request: ChangeCustomerRFCRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> None:
    handler = ChangeCustomerRFCHandler(repository)

    command = ChangeCustomerRFCCommand(
        customer_id=customer_id,
        new_rfc=request.new_rfc,
    )

    try:
        handler.execute(command)
        db.commit()

    except CustomerNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    except InvalidRFCError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{customer_id}/phone",
    status_code=204,
)
def change_customer_phone(
    customer_id: UUID,
    request: ChangeCustomerPhoneRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> None:
    handler = ChangeCustomerPhoneHandler(repository)

    command = ChangeCustomerPhoneCommand(
        customer_id=customer_id,
        new_phone=request.new_phone,
    )

    try:
        handler.execute(command)
        db.commit()

    except CustomerNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    except InvalidPhoneError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{customer_id}/address",
    status_code=204,
)
def change_customer_address(
    customer_id: UUID,
    request: ChangeCustomerAddressRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> None:
    handler = ChangeCustomerAddressHandler(repository)

    command = ChangeCustomerAddressCommand(
        customer_id=customer_id,
        street=request.street,
        exterior_number=request.exterior_number,
        interior_number=request.interior_number,
        neighborhood=request.neighborhood,
        city=request.city,
        state=request.state,
        postal_code=request.postal_code,
        country=request.country,
    )

    try:
        handler.execute(command)
        db.commit()

    except CustomerNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    except InvalidAddressError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{customer_id}/contact-name",
    status_code=204,
)
def change_customer_contact_name(
    customer_id: UUID,
    request: ChangeCustomerContactNameRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> None:
    handler = ChangeCustomerContactNameHandler(repository)

    command = ChangeCustomerContactNameCommand(
        customer_id=customer_id,
        new_contact_name=request.new_contact_name,
    )

    try:
        handler.execute(command)
        db.commit()

    except CustomerNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{customer_id}/notes",
    status_code=204,
)
def change_customer_notes(
    customer_id: UUID,
    request: ChangeCustomerNotesRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyCustomerRepository = Depends(
        get_customer_repository
    ),
) -> None:
    handler = ChangeCustomerNotesHandler(repository)

    command = ChangeCustomerNotesCommand(
        customer_id=customer_id,
        new_notes=request.new_notes,
    )

    try:
        handler.execute(command)
        db.commit()

    except CustomerNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        ) from error

    except Exception:
        db.rollback()
        raise