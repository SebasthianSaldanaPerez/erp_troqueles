from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.presentation.api.dependencies import (
    get_user_repository,
)
from src.presentation.api.auth.schemas import (
    TokenResponse,
)
from src.users.application.errors import (
    InactiveUserError,
    InvalidCredentialsError,
)
from src.users.application.login_user.command import (
    LoginUserCommand,
)
from src.users.application.login_user.handler import (
    LoginUserHandler,
)
from src.users.infrastructure.argon2_password_hasher import (
    Argon2PasswordHasher,
)
from src.users.infrastructure.jwt_token_service import (
    JWTTokenService,
)
from src.users.infrastructure.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from fastapi.security import OAuth2PasswordRequestForm
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repository: SQLAlchemyUserRepository = Depends(
        get_user_repository
    ),
) -> TokenResponse:
    handler = LoginUserHandler(
        repository=repository,
        password_hasher=Argon2PasswordHasher(),
        token_service=JWTTokenService(),
    )

    try:
        token = handler.execute(
            LoginUserCommand(
                email=form_data.username,
                password=form_data.password,
            )
        )

        logger.info(
            "Successful login for user email=%s",
            form_data.username,
        )

    except InvalidCredentialsError as error:
        logger.warning(
            "Failed login attempt for email=%s",
            form_data.username,
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        ) from error

    except InactiveUserError as error:
        logger.warning(
            "Login attempt for inactive user email=%s",
            form_data.username,
        )

        raise HTTPException(
            status_code=403,
            detail="User is inactive",
        ) from error

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )