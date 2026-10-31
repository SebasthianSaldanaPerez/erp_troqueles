import pytest

from src.users.application.create_user.command import CreateUserCommand
from src.users.application.create_user.handler import CreateUserHandler
from src.users.application.errors import UserEmailAlreadyExistsError
from src.users.domain.user import UserRole
from tests.fakes.in_memory_user_repository import InMemoryUserRepository


def test_create_user():
    repository = InMemoryUserRepository()
    handler = CreateUserHandler(repository)

    user_id = handler.execute(
        CreateUserCommand(
            name="Admin User",
            email="admin@empresa.com",
            password_hash="fake-hash",
            role=UserRole.ADMIN,
        )
    )

    saved_user = repository.get_by_id(user_id)

    assert saved_user is not None
    assert saved_user.name == "Admin User"
    assert saved_user.email.value == "admin@empresa.com"
    assert saved_user.role == UserRole.ADMIN


def test_create_user_normalizes_email():
    repository = InMemoryUserRepository()
    handler = CreateUserHandler(repository)

    user_id = handler.execute(
        CreateUserCommand(
            name="Admin User",
            email="  ADMIN@EMPRESA.COM  ",
            password_hash="fake-hash",
        )
    )

    saved_user = repository.get_by_id(user_id)

    assert saved_user is not None
    assert saved_user.email.value == "admin@empresa.com"


def test_create_user_cannot_use_duplicate_email():
    repository = InMemoryUserRepository()
    handler = CreateUserHandler(repository)

    handler.execute(
        CreateUserCommand(
            name="First User",
            email="admin@empresa.com",
            password_hash="fake-hash",
        )
    )

    with pytest.raises(UserEmailAlreadyExistsError):
        handler.execute(
            CreateUserCommand(
                name="Second User",
                email="ADMIN@EMPRESA.COM",
                password_hash="another-hash",
            )
        )