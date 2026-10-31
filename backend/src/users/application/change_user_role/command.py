from dataclasses import dataclass
from uuid import UUID

from src.users.domain.user import UserRole


@dataclass(frozen=True)
class ChangeUserRoleCommand:
    user_id: UUID
    new_role: UserRole