from fastapi.testclient import TestClient

from tests.api.conftest import admin_headers


def test_customers_requires_authentication(
    client: TestClient,
):
    response = client.get(
        "/customers"
    )

    assert response.status_code == 401

def test_authenticated_admin_can_list_customers(
    client: TestClient,
    admin_headers,
):
    list_response = client.get(
        "/customers",
        headers=admin_headers,
    )

    assert list_response.status_code == 200

def test_viewer_can_list_customers_but_cannot_rename(
    client: TestClient,
    viewer_headers,
    customer,
):
    list_response = client.get(
        "/customers",
        headers=viewer_headers,
    )

    assert list_response.status_code == 200

    rename_response = client.patch(
        f"/customers/{customer.id}/name",
        json={
            "new_business_name": "Unauthorized Rename",
        },
        headers=viewer_headers,
    )

    assert rename_response.status_code == 403

def test_admin_can_rename_customer(
    client: TestClient,
    admin_headers,
    customer,
):
    response = client.patch(
        f"/customers/{customer.id}/name",
        json={
            "new_business_name": "Renamed by Admin",
        },
        headers=admin_headers,
    )

    assert response.status_code == 204