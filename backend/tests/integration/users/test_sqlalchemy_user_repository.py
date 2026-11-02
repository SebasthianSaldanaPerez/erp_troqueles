from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.session import SessionLocal
from src.shared.domain.value_objects.email import Email
from src.users.domain.user import (
    User,
    UserRole,
    UserStatus,
)
from src.users.infrastructure.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


def test_sqlalchemy_user_repository_saves_and_gets_user():
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = User(
            name="Admin User",
            email=Email("admin@empresa.com"),
            password_hash="fake-hash",
            role=UserRole.ADMIN,
        )

        repository.save(user)
        session.commit()

        saved_user = repository.get_by_id(user.id)

        assert saved_user is not None
        assert saved_user.id == user.id
        assert saved_user.name == "Admin User"
        assert saved_user.email.value == "admin@empresa.com"
        assert saved_user.password_hash == "fake-hash"
        assert saved_user.role == UserRole.ADMIN
        assert saved_user.status == UserStatus.ACTIVE

    finally:
        session.rollback()

        if "user" in locals():
            model = session.get(
                UserModel,
                user.id,
            )

            if model is not None:
                session.delete(model)
                session.commit()

        session.close()

def test_sqlalchemy_user_repository_gets_user_by_email():
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        user = User(
            name="Operator",
            email=Email("operator@empresa.com"),
            password_hash="fake-hash",
            role=UserRole.OPERATOR,
        )

        repository.save(user)
        session.commit()

        saved_user = repository.get_by_email(
            "operator@empresa.com"
        )

        assert saved_user is not None
        assert saved_user.id == user.id

    finally:
        session.rollback()

        if "user" in locals():
            model = session.get(
                UserModel,
                user.id,
            )

            if model is not None:
                session.delete(model)
                session.commit()

        session.close()