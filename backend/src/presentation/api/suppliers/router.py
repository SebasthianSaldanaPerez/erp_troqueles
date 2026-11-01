from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.presentation.api.dependencies import (
    get_db,
    get_supplier_repository,
)
from src.presentation.api.suppliers.mappers import supplier_to_response
from src.presentation.api.suppliers.schemas import (
    ChangeSupplierAddressRequest,
    ChangeSupplierContactNameRequest,
    ChangeSupplierEmailRequest,
    ChangeSupplierNotesRequest,
    ChangeSupplierPhoneRequest,
    ChangeSupplierRFCRequest,
    CreateSupplierRequest,
    CreateSupplierResponse,
    RenameSupplierRequest,
    SupplierResponse,
)
from src.shared.domain.errors import (
    InvalidAddressError,
    InvalidEmailError,
    InvalidPhoneError,
    InvalidRFCError,
)
from src.suppliers.application.change_supplier_address.command import (
    ChangeSupplierAddressCommand,
)
from src.suppliers.application.change_supplier_address.handler import (
    ChangeSupplierAddressHandler,
)
from src.suppliers.application.change_supplier_contact_name.command import (
    ChangeSupplierContactNameCommand,
)
from src.suppliers.application.change_supplier_contact_name.handler import (
    ChangeSupplierContactNameHandler,
)
from src.suppliers.application.change_supplier_email.command import (
    ChangeSupplierEmailCommand,
)
from src.suppliers.application.change_supplier_email.handler import (
    ChangeSupplierEmailHandler,
)
from src.suppliers.application.change_supplier_notes.command import (
    ChangeSupplierNotesCommand,
)
from src.suppliers.application.change_supplier_notes.handler import (
    ChangeSupplierNotesHandler,
)
from src.suppliers.application.change_supplier_phone.command import (
    ChangeSupplierPhoneCommand,
)
from src.suppliers.application.change_supplier_phone.handler import (
    ChangeSupplierPhoneHandler,
)
from src.suppliers.application.change_supplier_rfc.command import (
    ChangeSupplierRFCCommand,
)
from src.suppliers.application.change_supplier_rfc.handler import (
    ChangeSupplierRFCHandler,
)
from src.suppliers.application.create_supplier.command import (
    CreateSupplierCommand,
)
from src.suppliers.application.create_supplier.handler import (
    CreateSupplierHandler,
)
from src.suppliers.application.deactivate_supplier.command import (
    DeactivateSupplierCommand,
)
from src.suppliers.application.deactivate_supplier.handler import (
    DeactivateSupplierHandler,
)
from src.suppliers.application.errors import SupplierNotFoundError
from src.suppliers.application.get_supplier.handler import (
    GetSupplierHandler,
)
from src.suppliers.application.get_supplier.query import (
    GetSupplierQuery,
)
from src.suppliers.application.list_suppliers.handler import (
    ListSuppliersHandler,
)
from src.suppliers.application.list_suppliers.query import (
    ListSuppliersQuery,
)
from src.suppliers.application.reactivate_supplier.command import (
    ReactivateSupplierCommand,
)
from src.suppliers.application.reactivate_supplier.handler import (
    ReactivateSupplierHandler,
)
from src.suppliers.application.rename_supplier.command import (
    RenameSupplierCommand,
)
from src.suppliers.application.rename_supplier.handler import (
    RenameSupplierHandler,
)
from src.suppliers.infrastructure.sqlalchemy_supplier_repository import (
    SQLAlchemySupplierRepository,
)


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


@router.post(
    "",
    response_model=CreateSupplierResponse,
    status_code=201,
)
def create_supplier(
    request: CreateSupplierRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> CreateSupplierResponse:
    handler = CreateSupplierHandler(repository)

    command = CreateSupplierCommand(
        name=request.name,
        email=request.email,
        rfc=request.rfc,
        phone=request.phone,
        address_street=request.address.street if request.address else None,
        address_exterior_number=(
            request.address.exterior_number if request.address else None
        ),
        address_interior_number=(
            request.address.interior_number if request.address else None
        ),
        address_neighborhood=(
            request.address.neighborhood if request.address else None
        ),
        address_city=request.address.city if request.address else None,
        address_state=request.address.state if request.address else None,
        address_postal_code=(
            request.address.postal_code if request.address else None
        ),
        address_country=request.address.country if request.address else None,
        contact_name=request.contact_name,
        notes=request.notes,
    )

    try:
        supplier_id = handler.execute(command)
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

    return CreateSupplierResponse(
        id=str(supplier_id),
    )


@router.get(
    "",
    response_model=list[SupplierResponse],
)
def list_suppliers(
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> list[SupplierResponse]:
    handler = ListSuppliersHandler(repository)

    suppliers = handler.execute(
        ListSuppliersQuery()
    )

    return [
        supplier_to_response(supplier)
        for supplier in suppliers
    ]


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse,
)
def get_supplier(
    supplier_id: UUID,
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> SupplierResponse:
    handler = GetSupplierHandler(repository)

    try:
        supplier = handler.execute(
            GetSupplierQuery(
                supplier_id=supplier_id,
            )
        )

    except SupplierNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        ) from error

    return supplier_to_response(supplier)


@router.patch(
    "/{supplier_id}/name",
    status_code=204,
)
def rename_supplier(
    supplier_id: UUID,
    request: RenameSupplierRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> None:
    handler = RenameSupplierHandler(repository)

    try:
        handler.execute(
            RenameSupplierCommand(
                supplier_id=supplier_id,
                new_name=request.new_name,
            )
        )
        db.commit()

    except SupplierNotFoundError as error:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{supplier_id}/deactivate",
    status_code=204,
)
def deactivate_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> None:
    handler = DeactivateSupplierHandler(repository)

    try:
        handler.execute(
            DeactivateSupplierCommand(
                supplier_id=supplier_id,
            )
        )
        db.commit()

    except SupplierNotFoundError as error:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{supplier_id}/reactivate",
    status_code=204,
)
def reactivate_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> None:
    handler = ReactivateSupplierHandler(repository)

    try:
        handler.execute(
            ReactivateSupplierCommand(
                supplier_id=supplier_id,
            )
        )
        db.commit()

    except SupplierNotFoundError as error:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{supplier_id}/email",
    status_code=204,
)
def change_supplier_email(
    supplier_id: UUID,
    request: ChangeSupplierEmailRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> None:
    handler = ChangeSupplierEmailHandler(repository)

    try:
        handler.execute(
            ChangeSupplierEmailCommand(
                supplier_id=supplier_id,
                new_email=request.new_email,
            )
        )
        db.commit()

    except SupplierNotFoundError as error:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
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
    "/{supplier_id}/rfc",
    status_code=204,
)
def change_supplier_rfc(
    supplier_id: UUID,
    request: ChangeSupplierRFCRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> None:
    handler = ChangeSupplierRFCHandler(repository)

    try:
        handler.execute(
            ChangeSupplierRFCCommand(
                supplier_id=supplier_id,
                new_rfc=request.new_rfc,
            )
        )
        db.commit()

    except SupplierNotFoundError as error:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
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
    "/{supplier_id}/phone",
    status_code=204,
)
def change_supplier_phone(
    supplier_id: UUID,
    request: ChangeSupplierPhoneRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> None:
    handler = ChangeSupplierPhoneHandler(repository)

    try:
        handler.execute(
            ChangeSupplierPhoneCommand(
                supplier_id=supplier_id,
                new_phone=request.new_phone,
            )
        )
        db.commit()

    except SupplierNotFoundError as error:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
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
    "/{supplier_id}/address",
    status_code=204,
)
def change_supplier_address(
    supplier_id: UUID,
    request: ChangeSupplierAddressRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> None:
    handler = ChangeSupplierAddressHandler(repository)

    try:
        handler.execute(
            ChangeSupplierAddressCommand(
                supplier_id=supplier_id,
                street=request.street,
                exterior_number=request.exterior_number,
                interior_number=request.interior_number,
                neighborhood=request.neighborhood,
                city=request.city,
                state=request.state,
                postal_code=request.postal_code,
                country=request.country,
            )
        )
        db.commit()

    except SupplierNotFoundError as error:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
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
    "/{supplier_id}/contact-name",
    status_code=204,
)
def change_supplier_contact_name(
    supplier_id: UUID,
    request: ChangeSupplierContactNameRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> None:
    handler = ChangeSupplierContactNameHandler(repository)

    try:
        handler.execute(
            ChangeSupplierContactNameCommand(
                supplier_id=supplier_id,
                new_contact_name=request.new_contact_name,
            )
        )
        db.commit()

    except SupplierNotFoundError as error:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        ) from error

    except Exception:
        db.rollback()
        raise


@router.patch(
    "/{supplier_id}/notes",
    status_code=204,
)
def change_supplier_notes(
    supplier_id: UUID,
    request: ChangeSupplierNotesRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemySupplierRepository = Depends(
        get_supplier_repository
    ),
) -> None:
    handler = ChangeSupplierNotesHandler(repository)

    try:
        handler.execute(
            ChangeSupplierNotesCommand(
                supplier_id=supplier_id,
                new_notes=request.new_notes,
            )
        )
        db.commit()

    except SupplierNotFoundError as error:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        ) from error

    except Exception:
        db.rollback()
        raise