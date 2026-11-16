from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.presentation.api.dependencies import get_user_repository
from src.users.domain.user import User, UserStatus
from src.users.infrastructure.jwt_token_service import JWTTokenService
from src.users.infrastructure.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from collections.abc import Callable

from src.users.domain.user import (
    User,
    UserRole,
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: SQLAlchemyUserRepository = Depends(
        get_user_repository
    ),
) -> User:
    token_service = JWTTokenService()

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        user_id = token_service.decode_access_token(
            token
        )

    except ValueError as error:
        raise credentials_exception from error

    user = repository.get_by_id(
        user_id
    )

    if user is None:
        raise credentials_exception

    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    return user

def require_roles(
    *allowed_roles: UserRole,
) -> Callable:
    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return dependency