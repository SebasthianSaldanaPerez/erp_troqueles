from src.users.domain.user import User
from src.users.domain.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self.users = []

    def save(self, user: User) -> None:
        for index, existing_user in enumerate(self.users):
            if existing_user.id == user.id:
                self.users[index] = user
                return

        self.users.append(user)

    def get_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user

        return None

    def get_by_email(self, email: str):
        normalized_email = email.strip().lower()

        for user in self.users:
            if user.email.value == normalized_email:
                return user

        return None

    def list_all(self) -> list[User]:
        return list(self.users)