from fastapi.testclient import TestClient
from decimal import Decimal



def test_quotations_requires_authentication(
    client: TestClient,
):
    response = client.get(
        "/quotations"
    )

    assert response.status_code == 401

def test_viewer_can_list_quotations_but_cannot_create(
    client: TestClient,
    viewer_headers,
    customer,
):
    list_response = client.get(
        "/quotations",
        headers=viewer_headers,
    )

    assert list_response.status_code == 200

    create_response = client.post(
        "/quotations",
        json={
            "customer_id": str(customer.id),
            "tax_rate": 16,
            "currency": "MXN",
        },
        headers=viewer_headers,
    )

    assert create_response.status_code == 403

def test_admin_can_complete_quotation_flow(
    client: TestClient,
    admin_headers,
    customer,
):
    create_response = client.post(
        "/quotations",
        json={
            "customer_id": str(customer.id),
            "tax_rate": 16,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    assert create_response.status_code == 201

    quotation_id = create_response.json()["id"]

    add_item_response = client.post(
        f"/quotations/{quotation_id}/items",
        json={
            "description": "Troquel API Test",
            "quantity": 2,
            "unit_price": 1000,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    assert add_item_response.status_code == 201

    get_response = client.get(
        f"/quotations/{quotation_id}",
        headers=admin_headers,
    )

    assert get_response.status_code == 200

    quotation = get_response.json()

    assert quotation["status"] == "DRAFT"
    assert Decimal(str(quotation["subtotal"])) == Decimal("2000.00")
    assert Decimal(str(quotation["total"])) == Decimal("2320.00")

    send_response = client.patch(
        f"/quotations/{quotation_id}/send",
        headers=admin_headers,
    )

    assert send_response.status_code == 204

    accept_response = client.patch(
        f"/quotations/{quotation_id}/accept",
        headers=admin_headers,
    )

    assert accept_response.status_code == 204

    final_response = client.get(
        f"/quotations/{quotation_id}",
        headers=admin_headers,
    )

    assert final_response.status_code == 200

    quotation = final_response.json()

    assert quotation["status"] == "ACCEPTED"