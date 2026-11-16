from uuid import UUID

import pytest

from src.shared.domain.value_objects.email import Email
from src.users.application.errors import (
    InactiveUserError,
    InvalidCredentialsError,
)
from src.users.application.login_user.command import (
    LoginUserCommand,
)
from src.users.application.login_user.handler import (
    LoginUserHandler,
)
from src.users.domain.user import User
from tests.fakes.fake_password_hasher import FakePasswordHasher
from tests.fakes.fake_token_service import FakeTokenService
from tests.fakes.in_memory_user_repository import (
    InMemoryUserRepository,
)


def create_user(
    repository: InMemoryUserRepository,
) -> User:
    user = User(
        name="Admin User",
        email=Email("admin@empresa.com"),
        password_hash="hashed-super-secret",
    )

    repository.save(user)

    return user


def test_login_user():
    repository = InMemoryUserRepository()
    user = create_user(repository)

    handler = LoginUserHandler(
        repository=repository,
        password_hasher=FakePasswordHasher(),
        token_service=FakeTokenService(),
    )

    token = handler.execute(
        LoginUserCommand(
            email="admin@empresa.com",
            password="super-secret",
        )
    )

    assert token == f"token-{user.id}"


def test_login_rejects_wrong_password():
    repository = InMemoryUserRepository()
    create_user(repository)

    handler = LoginUserHandler(
        repository=repository,
        password_hasher=FakePasswordHasher(),
        token_service=FakeTokenService(),
    )

    with pytest.raises(InvalidCredentialsError):
        handler.execute(
            LoginUserCommand(
                email="admin@empresa.com",
                password="wrong-password",
            )
        )


def test_login_rejects_unknown_email():
    handler = LoginUserHandler(
        repository=InMemoryUserRepository(),
        password_hasher=FakePasswordHasher(),
        token_service=FakeTokenService(),
    )

    with pytest.raises(InvalidCredentialsError):
        handler.execute(
            LoginUserCommand(
                email="unknown@empresa.com",
                password="super-secret",
            )
        )


def test_login_rejects_inactive_user():
    repository = InMemoryUserRepository()

    user = create_user(repository)
    user.deactivate()

    handler = LoginUserHandler(
        repository=repository,
        password_hasher=FakePasswordHasher(),
        token_service=FakeTokenService(),
    )

    with pytest.raises(InactiveUserError):
        handler.execute(
            LoginUserCommand(
                email="admin@empresa.com",
                password="super-secret",
            )
        )