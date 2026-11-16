from src.users.application.password_hasher import PasswordHasher


class FakePasswordHasher(PasswordHasher):

    def hash(self, password: str) -> str:
        return f"hashed-{password}"

    def verify(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        return password_hash == f"hashed-{password}"