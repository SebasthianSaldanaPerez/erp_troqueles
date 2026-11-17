from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.presentation.api.dependencies import (
    get_db,
    get_user_repository,
)
from src.presentation.api.security import require_roles
from src.presentation.api.users.mappers import user_to_response
from src.presentation.api.users.schemas import (
    ChangeUserRoleRequest,
    CreateUserRequest,
    CreateUserResponse,
    UserResponse,
)
from uuid import UUID

from src.users.application.change_user_role.command import (
    ChangeUserRoleCommand,
)
from src.users.application.change_user_role.handler import (
    ChangeUserRoleHandler,
)
from src.users.application.deactivate_user.command import (
    DeactivateUserCommand,
)
from src.users.application.deactivate_user.handler import (
    DeactivateUserHandler,
)
from src.users.application.reactivate_user.command import (
    ReactivateUserCommand,
)
from src.users.application.reactivate_user.handler import (
    ReactivateUserHandler,
)
from src.users.application.errors import (
    UserEmailAlreadyExistsError,
    UserNotFoundError,
)
from src.users.application.create_user.command import (
    CreateUserCommand,
)
from src.users.application.create_user.handler import (
    CreateUserHandler,
)
from src.users.application.errors import (
    UserEmailAlreadyExistsError,
)
from src.users.application.list_users.handler import (
    ListUsersHandler,
)
from src.users.application.list_users.query import (
    ListUsersQuery,
)
from src.users.domain.user import User, UserRole
from src.users.infrastructure.argon2_password_hasher import (
    Argon2PasswordHasher,
)
from src.users.infrastructure.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(
    repository: SQLAlchemyUserRepository = Depends(
        get_user_repository
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
) -> list[UserResponse]:
    handler = ListUsersHandler(repository)

    users = handler.execute(
        ListUsersQuery()
    )

    return [
        user_to_response(user)
        for user in users
    ]

@router.post(
    "",
    response_model=CreateUserResponse,
    status_code=201,
)
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyUserRepository = Depends(
        get_user_repository
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
) -> CreateUserResponse:
    handler = CreateUserHandler(
        repository=repository,
        password_hasher=Argon2PasswordHasher(),
    )

    try:
        user_id = handler.execute(
            CreateUserCommand(
                name=request.name,
                email=request.email,
                password=request.password,
                role=request.role,
            )
        )

        db.commit()

    except UserEmailAlreadyExistsError as error:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="User email already exists",
        ) from error

    except ValueError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise

    return CreateUserResponse(
        id=str(user_id),
    )

@router.patch(
    "/{user_id}/deactivate",
    status_code=204,
)
def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyUserRepository = Depends(
        get_user_repository
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
) -> None:
    handler = DeactivateUserHandler(
        repository
    )

    try:
        handler.execute(
            DeactivateUserCommand(
                user_id=user_id,
            )
        )

        db.commit()

    except UserNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="User not found",
        ) from error

    except ValueError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise

@router.patch(
    "/{user_id}/reactivate",
    status_code=204,
)
def reactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    repository: SQLAlchemyUserRepository = Depends(
        get_user_repository
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
) -> None:
    handler = ReactivateUserHandler(
        repository
    )

    try:
        handler.execute(
            ReactivateUserCommand(
                user_id=user_id,
            )
        )

        db.commit()

    except UserNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="User not found",
        ) from error

    except ValueError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise
    
@router.patch(
    "/{user_id}/role",
    status_code=204,
)
def change_user_role(
    user_id: UUID,
    request: ChangeUserRoleRequest,
    db: Session = Depends(get_db),
    repository: SQLAlchemyUserRepository = Depends(
        get_user_repository
    ),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
) -> None:
    handler = ChangeUserRoleHandler(
        repository
    )

    try:
        handler.execute(
            ChangeUserRoleCommand(
                user_id=user_id,
                new_role=request.role,
            )
        )

        db.commit()

    except UserNotFoundError as error:
        db.rollback()

        raise HTTPException(
            status_code=404,
            detail="User not found",
        ) from error

    except ValueError as error:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception:
        db.rollback()
        raise