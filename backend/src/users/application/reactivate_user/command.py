from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ReactivateUserCommand:
    user_id: UUID