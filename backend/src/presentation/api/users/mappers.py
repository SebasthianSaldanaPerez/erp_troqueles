from src.presentation.api.users.schemas import UserResponse
from src.users.domain.user import User


def user_to_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        name=user.name,
        email=user.email.value,
        role=user.role.value,
        status=user.status.value,
    )