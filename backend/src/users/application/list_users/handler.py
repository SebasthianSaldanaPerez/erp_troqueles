from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository

from .query import ListUsersQuery


class ListUsersHandler:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: ListUsersQuery,
    ) -> list[User]:
        return self._repository.list_all()