from src.users.application.errors import UserNotFoundError
from src.users.domain.user_repository import UserRepository

from .command import DeactivateUserCommand


class DeactivateUserHandler:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, command: DeactivateUserCommand) -> None:
        user = self._repository.get_by_id(command.user_id)

        if user is None:
            raise UserNotFoundError(
                f"User {command.user_id} was not found"
            )

        user.deactivate()

        self._repository.save(user)