from dataclasses import dataclass

from src.users.domain.user import UserRole


@dataclass(frozen=True)
class CreateUserCommand:
    name: str
    email: str
    password: str
    role: UserRole = UserRole.VIEWER