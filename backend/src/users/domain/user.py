from enum import Enum
from uuid import UUID, uuid4

from src.shared.domain.value_objects.email import Email


class UserRole(Enum):
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class User:
    def __init__(
        self,
        name: str,
        email: Email,
        password_hash: str,
        role: UserRole = UserRole.VIEWER,
        user_id: UUID | None = None,
        status: UserStatus = UserStatus.ACTIVE,
    ):
        self._id = user_id or uuid4()
        self._name = self._validate_name(name)
        self._email = email
        self._password_hash = self._validate_password_hash(password_hash)
        self._role = role
        self._status = status

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> Email:
        return self._email

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def role(self) -> UserRole:
        return self._role

    @property
    def status(self) -> UserStatus:
        return self._status

    def deactivate(self) -> None:
        self._status = UserStatus.INACTIVE

    def reactivate(self) -> None:
        self._status = UserStatus.ACTIVE

    def change_role(self, new_role: UserRole) -> None:
        self._role = new_role

    @staticmethod
    def _validate_name(name: str) -> str:
        if not name or not name.strip():
            raise ValueError("User name is required")

        return name.strip()

    @staticmethod
    def _validate_password_hash(password_hash: str) -> str:
        if not password_hash or not password_hash.strip():
            raise ValueError("Password hash is required")

        return password_hash.strip()