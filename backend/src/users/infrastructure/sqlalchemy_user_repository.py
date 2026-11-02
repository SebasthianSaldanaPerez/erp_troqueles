from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.infrastructure.database.models.user_model import UserModel
from src.shared.domain.value_objects.email import Email
from src.users.domain.user import (
    User,
    UserRole,
    UserStatus,
)
from src.users.domain.user_repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: Session):
        self._session = session

    def save(self, user: User) -> None:
        model = self._session.get(
            UserModel,
            user.id,
        )

        if model is None:
            model = UserModel(
                id=user.id,
                name=user.name,
                email=user.email.value,
                password_hash=user.password_hash,
                role=user.role.value,
                status=user.status.value,
            )

            self._session.add(model)
            return

        model.name = user.name
        model.email = user.email.value
        model.password_hash = user.password_hash
        model.role = user.role.value
        model.status = user.status.value

    def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        model = self._session.get(
            UserModel,
            user_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        statement = select(UserModel).where(
            UserModel.email == email.strip().lower()
        )

        model = self._session.scalars(
            statement
        ).first()

        if model is None:
            return None

        return self._to_domain(model)

    def list_all(self) -> list[User]:
        statement = select(UserModel)

        models = self._session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: UserModel,
    ) -> User:
        return User(
            user_id=model.id,
            name=model.name,
            email=Email(model.email),
            password_hash=model.password_hash,
            role=UserRole(model.role),
            status=UserStatus(model.status),
        )