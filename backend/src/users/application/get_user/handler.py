from src.users.application.errors import UserNotFoundError
from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository

from .query import GetUserQuery


class GetUserHandler:

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def execute(self, query: GetUserQuery) -> User:
        user = self._repository.get_by_id(query.user_id)

        if user is None:
            raise UserNotFoundError(
                f"User {query.user_id} was not found"
            )

        return user