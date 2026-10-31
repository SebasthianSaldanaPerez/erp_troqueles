from uuid import uuid4

import pytest

from src.shared.domain.value_objects.email import Email
from src.users.application.errors import UserNotFoundError
from src.users.application.get_user.handler import GetUserHandler
from src.users.application.get_user.query import GetUserQuery
from src.users.domain.user import User
from tests.fakes.in_memory_user_repository import InMemoryUserRepository


def test_get_user():
    repository = InMemoryUserRepository()

    user = User(
        name="Admin",
        email=Email("admin@empresa.com"),
        password_hash="fake-hash",
    )
    repository.save(user)

    handler = GetUserHandler(repository)

    result = handler.execute(
        GetUserQuery(user_id=user.id)
    )

    assert result.id == user.id
    assert result.email.value == "admin@empresa.com"


def test_get_user_raises_error_when_not_found():
    handler = GetUserHandler(
        InMemoryUserRepository()
    )

    with pytest.raises(UserNotFoundError):
        handler.execute(
            GetUserQuery(user_id=uuid4())
        )