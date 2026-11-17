from decimal import Decimal

from fastapi.testclient import TestClient

def test_orders_requires_authentication(
    client: TestClient,
):
    response = client.get(
        "/orders"
    )

    assert response.status_code == 401

def test_viewer_can_list_orders(
    client: TestClient,
    viewer_headers,
):
    response = client.get(
        "/orders",
        headers=viewer_headers,
    )

    assert response.status_code == 200

def test_admin_can_convert_quotation_and_complete_order_flow(
    client: TestClient,
    admin_headers,
    customer,
):
    # 1. Create quotation
    create_quotation_response = client.post(
        "/quotations",
        json={
            "customer_id": str(customer.id),
            "tax_rate": 16,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    assert create_quotation_response.status_code == 201

    quotation_id = create_quotation_response.json()["id"]

    # 2. Add item
    add_item_response = client.post(
        f"/quotations/{quotation_id}/items",
        json={
            "description": "Troquel Order API Test",
            "quantity": 2,
            "unit_price": 1000,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    assert add_item_response.status_code == 201

    # 3. Send quotation
    send_response = client.patch(
        f"/quotations/{quotation_id}/send",
        headers=admin_headers,
    )

    assert send_response.status_code == 204

    # 4. Accept quotation
    accept_response = client.patch(
        f"/quotations/{quotation_id}/accept",
        headers=admin_headers,
    )

    assert accept_response.status_code == 204

    # 5. Convert quotation to order
    convert_response = client.post(
        f"/quotations/{quotation_id}/convert-to-order",
        headers=admin_headers,
    )

    assert convert_response.status_code == 201

    order_id = convert_response.json()["order_id"]

    # 6. Get created order
    get_order_response = client.get(
        f"/orders/{order_id}",
        headers=admin_headers,
    )

    assert get_order_response.status_code == 200

    order = get_order_response.json()

    assert order["status"] == "CREATED"
    assert order["origin_quotation_id"] == quotation_id
    assert order["revision_number"] == 0

    assert Decimal(
        str(order["subtotal"])
    ) == Decimal("2000.00")

    assert Decimal(
        str(order["tax"])
    ) == Decimal("320.00")

    assert Decimal(
        str(order["total"])
    ) == Decimal("2320.00")

    assert len(order["items"]) == 1

    # 7. Start order
    start_response = client.patch(
        f"/orders/{order_id}/start",
        headers=admin_headers,
    )

    assert start_response.status_code == 204

    started_order_response = client.get(
        f"/orders/{order_id}",
        headers=admin_headers,
    )

    assert started_order_response.status_code == 200
    assert (
        started_order_response.json()["status"]
        == "IN_PROGRESS"
    )

    # 8. Deliver order
    deliver_response = client.patch(
        f"/orders/{order_id}/deliver",
        headers=admin_headers,
    )

    assert deliver_response.status_code == 204

    delivered_order_response = client.get(
        f"/orders/{order_id}",
        headers=admin_headers,
    )

    assert delivered_order_response.status_code == 200

    delivered_order = delivered_order_response.json()

    assert delivered_order["status"] == "DELIVERED"

    assert Decimal(
        str(delivered_order["total"])
    ) == Decimal("2320.00")

def test_viewer_cannot_start_order(
    client: TestClient,
    admin_headers,
    viewer_headers,
    customer,
):
    quotation_response = client.post(
        "/quotations",
        json={
            "customer_id": str(customer.id),
            "tax_rate": 16,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    quotation_id = quotation_response.json()["id"]

    client.post(
        f"/quotations/{quotation_id}/items",
        json={
            "description": "Protected Order",
            "quantity": 1,
            "unit_price": 1000,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    client.patch(
        f"/quotations/{quotation_id}/send",
        headers=admin_headers,
    )

    client.patch(
        f"/quotations/{quotation_id}/accept",
        headers=admin_headers,
    )

    convert_response = client.post(
        f"/quotations/{quotation_id}/convert-to-order",
        headers=admin_headers,
    )

    order_id = convert_response.json()["order_id"]

    response = client.patch(
        f"/orders/{order_id}/start",
        headers=viewer_headers,
    )

    assert response.status_code == 403