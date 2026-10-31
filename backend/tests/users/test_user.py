import pytest

from src.shared.domain.value_objects.email import Email
from src.users.domain.user import (
    User,
    UserRole,
    UserStatus,
)


def create_user(
    role: UserRole = UserRole.VIEWER,
) -> User:
    return User(
        name="Admin User",
        email=Email("admin@empresa.com"),
        password_hash="fake-hash",
        role=role,
    )


def test_user_is_created_active():
    user = create_user()

    assert user.id is not None
    assert user.name == "Admin User"
    assert user.email.value == "admin@empresa.com"
    assert user.role == UserRole.VIEWER
    assert user.status == UserStatus.ACTIVE


def test_user_requires_name():
    with pytest.raises(ValueError):
        User(
            name="",
            email=Email("admin@empresa.com"),
            password_hash="fake-hash",
        )


def test_user_requires_password_hash():
    with pytest.raises(ValueError):
        User(
            name="Admin User",
            email=Email("admin@empresa.com"),
            password_hash="",
        )


def test_user_can_be_deactivated():
    user = create_user()

    user.deactivate()

    assert user.status == UserStatus.INACTIVE


def test_user_can_be_reactivated():
    user = create_user()
    user.deactivate()

    user.reactivate()

    assert user.status == UserStatus.ACTIVE


def test_user_can_change_role():
    user = create_user()

    user.change_role(UserRole.ADMIN)

    assert user.role == UserRole.ADMIN