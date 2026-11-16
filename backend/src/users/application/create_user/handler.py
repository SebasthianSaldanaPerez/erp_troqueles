from uuid import UUID

from src.shared.domain.value_objects.email import Email
from src.users.application.errors import UserEmailAlreadyExistsError
from src.users.application.password_hasher import PasswordHasher
from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository

from .command import CreateUserCommand


class CreateUserHandler:

    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._repository = repository
        self._password_hasher = password_hasher

    def execute(
        self,
        command: CreateUserCommand,
    ) -> UUID:
        email = Email(command.email)

        existing_user = self._repository.get_by_email(
            email.value
        )

        if existing_user is not None:
            raise UserEmailAlreadyExistsError(
                f"User with email {email.value} already exists"
            )

        password_hash = self._password_hasher.hash(
            command.password
        )

        user = User(
            name=command.name,
            email=email,
            password_hash=password_hash,
            role=command.role,
        )

        self._repository.save(user)

        return user.id