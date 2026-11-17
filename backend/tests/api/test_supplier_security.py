from fastapi.testclient import TestClient


def test_suppliers_requires_authentication(
    client: TestClient,
):
    response = client.get(
        "/suppliers"
    )

    assert response.status_code == 401


def test_viewer_can_list_suppliers(
    client: TestClient,
    viewer_headers,
):
    response = client.get(
        "/suppliers",
        headers=viewer_headers,
    )

    assert response.status_code == 200


def test_viewer_cannot_create_supplier(
    client: TestClient,
    viewer_headers,
):
    response = client.post(
        "/suppliers",
        json={
            "name": "API Test Supplier",
            "email": "supplier@test.local",
            "rfc": "ABC010203XYZ",
            "phone": "4491234567",
            "contact_name": "Supplier Contact",
            "notes": "API test",
        },
        headers=viewer_headers,
    )

    assert response.status_code == 403


def test_admin_can_create_supplier(
    client: TestClient,
    admin_headers,
):
    response = client.post(
        "/suppliers",
        json={
            "name": "API Admin Supplier",
            "email": "admin-supplier@test.local",
            "rfc": "ABC010203XYZ",
            "phone": "4491234567",
            "contact_name": "Admin Contact",
            "notes": "API test supplier",
        },
        headers=admin_headers,
    )

    assert response.status_code == 201