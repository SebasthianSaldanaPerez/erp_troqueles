from src.users.application.errors import (
    InactiveUserError,
    InvalidCredentialsError,
)
from src.users.application.password_hasher import PasswordHasher
from src.users.application.token_service import TokenService
from src.users.domain.user import UserStatus
from src.users.domain.user_repository import UserRepository

from .command import LoginUserCommand


class LoginUserHandler:

    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self._repository = repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    def execute(
        self,
        command: LoginUserCommand,
    ) -> str:
        user = self._repository.get_by_email(
            command.email
        )

        if user is None:
            raise InvalidCredentialsError(
                "Invalid email or password"
            )

        password_is_valid = (
            self._password_hasher.verify(
                command.password,
                user.password_hash,
            )
        )

        if not password_is_valid:
            raise InvalidCredentialsError(
                "Invalid email or password"
            )

        if user.status != UserStatus.ACTIVE:
            raise InactiveUserError(
                "User is inactive"
            )

        return self._token_service.create_access_token(
            user.id
        )