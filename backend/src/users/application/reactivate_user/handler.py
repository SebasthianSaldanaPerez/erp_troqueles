from src.users.application.errors import UserNotFoundError
from src.users.domain.user_repository import UserRepository

from .command import ReactivateUserCommand


class ReactivateUserHandler:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, command: ReactivateUserCommand) -> None:
        user = self._repository.get_by_id(command.user_id)

        if user is None:
            raise UserNotFoundError(
                f"User {command.user_id} was not found"
            )

        user.reactivate()

        self._repository.save(user)