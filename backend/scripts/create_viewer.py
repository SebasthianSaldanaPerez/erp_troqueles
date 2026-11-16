from src.infrastructure.database.session import SessionLocal
from src.users.application.create_user.command import (
    CreateUserCommand,
)
from src.users.application.create_user.handler import (
    CreateUserHandler,
)
from src.users.domain.user import UserRole
from src.users.infrastructure.argon2_password_hasher import (
    Argon2PasswordHasher,
)
from src.users.infrastructure.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


session = SessionLocal()

try:
    repository = SQLAlchemyUserRepository(session)

    handler = CreateUserHandler(
        repository=repository,
        password_hasher=Argon2PasswordHasher(),
    )

    user_id = handler.execute(
        CreateUserCommand(
            name="Viewer",
            email="viewer@troqueles.local",
            password="Viewer123!",
            role=UserRole.VIEWER,
        )
    )

    session.commit()

    print(f"Created viewer: {user_id}")

finally:
    session.close()