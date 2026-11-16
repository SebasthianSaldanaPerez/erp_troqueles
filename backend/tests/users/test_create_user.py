import pytest

from tests.fakes.fake_password_hasher import FakePasswordHasher
from src.users.application.create_user.command import CreateUserCommand
from src.users.application.create_user.handler import CreateUserHandler
from src.users.application.errors import UserEmailAlreadyExistsError
from src.users.domain.user import UserRole
from tests.fakes.in_memory_user_repository import InMemoryUserRepository


def test_create_user():
    repository = InMemoryUserRepository()
    handler = CreateUserHandler(
    repository=repository,
    password_hasher=FakePasswordHasher(),
)

    user_id = handler.execute(
        CreateUserCommand(
            name="Admin User",
            email="admin@empresa.com",
            password="super-secret",
            role=UserRole.ADMIN,
        )
    )

    saved_user = repository.get_by_id(user_id)

    assert saved_user is not None
    assert saved_user.name == "Admin User"
    assert saved_user.email.value == "admin@empresa.com"
    assert saved_user.role == UserRole.ADMIN
    assert saved_user.password_hash == "hashed-super-secret"


def test_create_user_normalizes_email():
    repository = InMemoryUserRepository()
    handler = CreateUserHandler(
    repository=repository,
    password_hasher=FakePasswordHasher(),
)

    user_id = handler.execute(
        CreateUserCommand(
            name="Admin User",
            email="  ADMIN@EMPRESA.COM  ",
            password="super-secret",
        )
    )

    saved_user = repository.get_by_id(user_id)

    assert saved_user is not None
    assert saved_user.email.value == "admin@empresa.com"
    assert saved_user.password_hash == "hashed-super-secret"


def test_create_user_cannot_use_duplicate_email():
    repository = InMemoryUserRepository()
    handler = CreateUserHandler(
    repository=repository,
    password_hasher=FakePasswordHasher(),
)

    handler.execute(
        CreateUserCommand(
            name="First User",
            email="admin@empresa.com",
            password="super-secret",
        )
    )

    with pytest.raises(UserEmailAlreadyExistsError):
        handler.execute(
            CreateUserCommand(
                name="Second User",
                email="ADMIN@EMPRESA.COM",
                password="super-secret",
            )
        )