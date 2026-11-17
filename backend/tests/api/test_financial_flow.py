from decimal import Decimal

from fastapi.testclient import TestClient

def create_order_from_quotation(
    client: TestClient,
    admin_headers,
    customer,
) -> str:
    quotation_response = client.post(
        "/quotations",
        json={
            "customer_id": str(customer.id),
            "tax_rate": 16,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    assert quotation_response.status_code == 201

    quotation_id = quotation_response.json()["id"]

    item_response = client.post(
        f"/quotations/{quotation_id}/items",
        json={
            "description": "Troquel Financial API Test",
            "quantity": 3,
            "unit_price": 1000,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    assert item_response.status_code == 201

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

    convert_response = client.post(
        f"/quotations/{quotation_id}/convert-to-order",
        headers=admin_headers,
    )

    assert convert_response.status_code == 201

    return convert_response.json()["order_id"]

def test_admin_can_register_expense_and_profitability_is_recalculated(
    client: TestClient,
    admin_headers,
    customer,
):
    order_id = create_order_from_quotation(
        client,
        admin_headers,
        customer,
    )

    initial_response = client.get(
        f"/orders/{order_id}/profitability",
        headers=admin_headers,
    )

    assert initial_response.status_code == 200

    initial = initial_response.json()

    assert Decimal(
        str(initial["revenue"])
    ) == Decimal("3480.00")

    assert Decimal(
        str(initial["expenses"])
    ) == Decimal("0")

    expense_response = client.post(
        f"/orders/{order_id}/expenses",
        json={
            "description": "Material de prueba",
            "amount": 1000,
            "currency": "MXN",
            "category": "MATERIAL",
            "expense_date": "2026-11-16",
            "supplier_id": None,
            "notes": "API financial test",
        },
        headers=admin_headers,
    )

    assert expense_response.status_code == 201

    profitability_response = client.get(
        f"/orders/{order_id}/profitability",
        headers=admin_headers,
    )

    assert profitability_response.status_code == 200

    profitability = profitability_response.json()

    assert Decimal(
        str(profitability["revenue"])
    ) == Decimal("3480.00")

    assert Decimal(
        str(profitability["expenses"])
    ) == Decimal("1000.00")

    assert Decimal(
        str(profitability["profit"])
    ) == Decimal("2480.00")

    assert Decimal(
        str(profitability["margin"])
    ) == Decimal("71.26")

def test_admin_can_complete_invoice_and_payment_flow(
    client: TestClient,
    admin_headers,
    customer,
):
    order_id = create_order_from_quotation(
        client,
        admin_headers,
        customer,
    )

    first_invoice_response = client.post(
        f"/orders/{order_id}/invoices",
        json={
            "folio": "FAC-API-001",
            "invoice_date": "2026-11-16",
            "total": 1000,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    assert first_invoice_response.status_code == 201

    partial_order_response = client.get(
        f"/orders/{order_id}",
        headers=admin_headers,
    )

    assert partial_order_response.status_code == 200

    assert (
        partial_order_response.json()["billing_status"]
        == "PARTIALLY_INVOICED"
    )

    second_invoice_response = client.post(
        f"/orders/{order_id}/invoices",
        json={
            "folio": "FAC-API-002",
            "invoice_date": "2026-11-16",
            "total": 2480,
            "currency": "MXN",
        },
        headers=admin_headers,
    )

    assert second_invoice_response.status_code == 201

    full_order_response = client.get(
        f"/orders/{order_id}",
        headers=admin_headers,
    )

    assert full_order_response.status_code == 200

    assert (
        full_order_response.json()["billing_status"]
        == "FULLY_INVOICED"
    )

    paid_response = client.patch(
        f"/orders/{order_id}/paid",
        headers=admin_headers,
    )

    assert paid_response.status_code == 204

    final_order_response = client.get(
        f"/orders/{order_id}",
        headers=admin_headers,
    )

    assert final_order_response.status_code == 200

    assert (
        final_order_response.json()["billing_status"]
        == "PAID"
    )

def test_viewer_cannot_register_expense_or_invoice(
    client: TestClient,
    admin_headers,
    viewer_headers,
    customer,
):
    order_id = create_order_from_quotation(
        client,
        admin_headers,
        customer,
    )

    expense_response = client.post(
        f"/orders/{order_id}/expenses",
        json={
            "description": "Unauthorized expense",
            "amount": 500,
            "currency": "MXN",
            "category": "MATERIAL",
            "expense_date": "2026-11-16",
            "supplier_id": None,
            "notes": None,
        },
        headers=viewer_headers,
    )

    assert expense_response.status_code == 403

    invoice_response = client.post(
        f"/orders/{order_id}/invoices",
        json={
            "folio": "FAC-NOPE",
            "invoice_date": "2026-11-16",
            "total": 500,
            "currency": "MXN",
        },
        headers=viewer_headers,
    )

    assert invoice_response.status_code == 403