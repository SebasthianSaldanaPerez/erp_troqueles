import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from dotenv import load_dotenv
from src.infrastructure.database.session import SessionLocal
from src.users.application.create_user.command import CreateUserCommand
from src.users.application.create_user.handler import CreateUserHandler
from src.users.domain.user import UserRole
from src.users.infrastructure.argon2_password_hasher import (
    Argon2PasswordHasher,
)
from pathlib import Path

from src.documents.infrastructure.local_file_storage import (
    LocalFileStorage,
)
from src.presentation.api.dependencies import get_file_storage
from src.users.infrastructure.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.database.models.user_model import UserModel
from src.customers.domain.customer import Customer
from src.customers.infrastructure.sqlalchemy_customer_repository import (
    SQLAlchemyCustomerRepository,
)
from src.infrastructure.database.models.customer_model import CustomerModel

load_dotenv()

TEST_DATABASE_URL = os.getenv(
    "DATABASE_TEST_URL"
)

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "DATABASE_TEST_URL environment variable is required"
    )


# IMPORTANTE:
# esto debe ocurrir ANTES de importar la aplicación.
os.environ["DATABASE_URL"] = TEST_DATABASE_URL


from src.presentation.api.main import app  # noqa: E402

def login(
    client: TestClient,
    email: str,
    password: str,
) -> str:
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
    }

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def admin_user():
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        handler = CreateUserHandler(
            repository=repository,
            password_hasher=Argon2PasswordHasher(),
        )

        user_id = handler.execute(
            CreateUserCommand(
                name="API Test Admin",
                email="api-admin@test.local",
                password="Admin123!",
                role=UserRole.ADMIN,
            )
        )

        session.commit()

        yield {
            "id": user_id,
            "email": "api-admin@test.local",
            "password": "Admin123!",
        }

    finally:
        session.rollback()

        user = repository.get_by_email(
            "api-admin@test.local"
        )

        if user is not None:
            model = session.get(
                UserModel,
                user.id,
            )

            if model is not None:
                session.delete(model)
                session.commit()

        session.close()

@pytest.fixture
def viewer_user():
    session = SessionLocal()

    try:
        repository = SQLAlchemyUserRepository(session)

        handler = CreateUserHandler(
            repository=repository,
            password_hasher=Argon2PasswordHasher(),
        )

        user_id = handler.execute(
            CreateUserCommand(
                name="API Test Viewer",
                email="api-viewer@test.local",
                password="Viewer123!",
                role=UserRole.VIEWER,
            )
        )

        session.commit()

        yield {
            "id": user_id,
            "email": "api-viewer@test.local",
            "password": "Viewer123!",
        }

    finally:
        session.rollback()

        user = repository.get_by_email(
            "api-viewer@test.local"
        )

        if user is not None:
            model = session.get(
                UserModel,
                user.id,
            )

            if model is not None:
                session.delete(model)
                session.commit()

        session.close()

@pytest.fixture
def admin_headers(
    client: TestClient,
    admin_user,
) -> dict[str, str]:
    token = login(
        client,
        admin_user["email"],
        admin_user["password"],
    )

    return auth_headers(token)


@pytest.fixture
def viewer_headers(
    client: TestClient,
    viewer_user,
) -> dict[str, str]:
    token = login(
        client,
        viewer_user["email"],
        viewer_user["password"],
    )

    return auth_headers(token)


@pytest.fixture
def customer():
    session = SessionLocal()

    try:
        repository = SQLAlchemyCustomerRepository(session)

        customer = Customer(
            business_name="Quotation API Customer",
        )

        repository.save(customer)
        session.commit()

        yield customer

    finally:
        session.close()

@pytest.fixture(autouse=True)
def clean_database():
    yield

    session = SessionLocal()

    try:
        session.execute(
            text(
                """
                DELETE FROM invoices;
                DELETE FROM expenses;
                DELETE FROM order_revisions;
                DELETE FROM documents;
                DELETE FROM order_items;
                DELETE FROM orders;
                DELETE FROM quotation_items;
                DELETE FROM quotations;
                DELETE FROM suppliers;
                DELETE FROM customers;
                DELETE FROM users;
                """
            )
        )

        session.commit()

    finally:
        session.close()

@pytest.fixture
def temp_file_storage(
    tmp_path: Path,
):
    storage = LocalFileStorage(
        base_path=str(tmp_path)
    )

    app.dependency_overrides[
        get_file_storage
    ] = lambda: storage

    yield storage

    app.dependency_overrides.pop(
        get_file_storage,
        None,
    )