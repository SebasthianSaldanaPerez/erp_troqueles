from uuid import uuid4

import pytest

from src.shared.domain.value_objects.email import Email
from src.users.application.deactivate_user.command import DeactivateUserCommand
from src.users.application.deactivate_user.handler import DeactivateUserHandler
from src.users.application.errors import UserNotFoundError
from src.users.domain.user import User, UserStatus
from tests.fakes.in_memory_user_repository import InMemoryUserRepository


def test_deactivate_user():
    repository = InMemoryUserRepository()

    user = User(
        name="Admin",
        email=Email("admin@empresa.com"),
        password_hash="fake-hash",
    )
    repository.save(user)

    handler = DeactivateUserHandler(repository)

    handler.execute(
        DeactivateUserCommand(user_id=user.id)
    )

    saved_user = repository.get_by_id(user.id)

    assert saved_user is not None
    assert saved_user.status == UserStatus.INACTIVE


def test_deactivate_user_raises_error_when_not_found():
    handler = DeactivateUserHandler(
        InMemoryUserRepository()
    )

    with pytest.raises(UserNotFoundError):
        handler.execute(
            DeactivateUserCommand(user_id=uuid4())
        )