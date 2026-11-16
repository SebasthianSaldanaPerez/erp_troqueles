from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.presentation.api.dependencies import (
    get_db,
    get_user_repository,
)
from src.presentation.api.security import require_roles
from src.presentation.api.users.mappers import user_to_response
from src.presentation.api.users.schemas import (
    CreateUserRequest,
    CreateUserResponse,
    UserResponse,
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