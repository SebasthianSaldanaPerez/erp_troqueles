from pwdlib import PasswordHash

from src.users.application.password_hasher import PasswordHasher


class Argon2PasswordHasher(PasswordHasher):

    def __init__(self):
        self._password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        if not password or not password.strip():
            raise ValueError("Password is required")

        return self._password_hash.hash(password)

    def verify(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        return self._password_hash.verify(
            password,
            password_hash,
        )