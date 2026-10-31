from uuid import uuid4
import pytest
from src.users.application.errors import UserNotFoundError
from src.shared.domain.value_objects.email import Email
from src.users.application.reactivate_user.command import ReactivateUserCommand
from src.users.application.reactivate_user.handler import ReactivateUserHandler
from src.users.domain.user import User, UserStatus
from tests.fakes.in_memory_user_repository import InMemoryUserRepository


def test_reactivate_user():
    repository = InMemoryUserRepository()

    user = User(
        name="Admin",
        email=Email("admin@empresa.com"),
        password_hash="fake-hash",
    )
    user.deactivate()

    repository.save(user)

    handler = ReactivateUserHandler(repository)

    handler.execute(
        ReactivateUserCommand(user_id=user.id)
    )

    saved_user = repository.get_by_id(user.id)

    assert saved_user is not None
    assert saved_user.status == UserStatus.ACTIVE

def test_reactivate_user_raises_error_when_not_found():
    handler = ReactivateUserHandler(
        InMemoryUserRepository()
    )

    with pytest.raises(UserNotFoundError):
        handler.execute(
            ReactivateUserCommand(user_id=uuid4())
        )