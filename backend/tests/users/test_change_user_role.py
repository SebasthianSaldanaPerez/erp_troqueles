from uuid import uuid4

import pytest

from src.users.application.errors import UserNotFoundError
from src.shared.domain.value_objects.email import Email
from src.users.application.change_user_role.command import ChangeUserRoleCommand
from src.users.application.change_user_role.handler import ChangeUserRoleHandler
from src.users.domain.user import User, UserRole
from tests.fakes.in_memory_user_repository import InMemoryUserRepository


def test_change_user_role():
    repository = InMemoryUserRepository()

    user = User(
        name="Operator",
        email=Email("operator@empresa.com"),
        password_hash="fake-hash",
    )
    repository.save(user)

    handler = ChangeUserRoleHandler(repository)

    handler.execute(
        ChangeUserRoleCommand(
            user_id=user.id,
            new_role=UserRole.ADMIN,
        )
    )

    saved_user = repository.get_by_id(user.id)

    assert saved_user is not None
    assert saved_user.role == UserRole.ADMIN

def test_change_user_role_raises_error_when_not_found():
    handler = ChangeUserRoleHandler(
        InMemoryUserRepository()
    )

    with pytest.raises(UserNotFoundError):
        handler.execute(
            ChangeUserRoleCommand(user_id=uuid4(), new_role=UserRole.ADMIN)
        )