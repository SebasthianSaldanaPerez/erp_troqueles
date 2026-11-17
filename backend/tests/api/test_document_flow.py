from fastapi.testclient import TestClient

from tests.api.conftest import temp_file_storage

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
            "description": "Document API Test",
            "quantity": 1,
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

def test_admin_can_upload_document(
    client: TestClient,
    admin_headers,
    admin_user,
    customer,
    temp_file_storage,
):
    order_id = create_order_from_quotation(
        client,
        admin_headers,
        customer,
    )

    response = client.post(
        f"/orders/{order_id}/documents",
        data={
            "document_type": "TECHNICAL_DRAWING",
        },
        files={
            "file": (
                "plano.txt",
                b"document test content",
                "text/plain",
            )
        },
        headers=admin_headers,
    )

    assert response.status_code == 201

    document_id = response.json()["id"]

    metadata_response = client.get(
        f"/documents/{document_id}",
        headers=admin_headers,
    )

    assert metadata_response.status_code == 200

    document = metadata_response.json()

    assert document["order_id"] == order_id
    assert document["filename"] == "plano.txt"
    assert document["mime_type"] == "text/plain"

    assert document["uploaded_by"] == str(
        admin_user["id"]
    )

def test_viewer_cannot_upload_document(
    client: TestClient,
    admin_headers,
    viewer_headers,
    customer,
    temp_file_storage,
):
    order_id = create_order_from_quotation(
        client,
        admin_headers,
        customer,
    )

    response = client.post(
        f"/orders/{order_id}/documents",
        data={
            "document_type": "TECHNICAL_DRAWING",
        },
        files={
            "file": (
                "forbidden.txt",
                b"viewer should not upload this",
                "text/plain",
            )
        },
        headers=viewer_headers,
    )

    assert response.status_code == 403

def test_viewer_can_list_documents(
    client: TestClient,
    admin_headers,
    viewer_headers,
    customer,
    temp_file_storage,
):
    order_id = create_order_from_quotation(
        client,
        admin_headers,
        customer,
    )

    upload_response = client.post(
        f"/orders/{order_id}/documents",
        data={
            "document_type": "TECHNICAL_DRAWING",
        },
        files={
            "file": (
                "viewer-visible.txt",
                b"visible document",
                "text/plain",
            )
        },
        headers=admin_headers,
    )

    assert upload_response.status_code == 201

    response = client.get(
        f"/orders/{order_id}/documents",
        headers=viewer_headers,
    )

    assert response.status_code == 200

    documents = response.json()

    assert len(documents) == 1
    assert documents[0]["filename"] == "viewer-visible.txt"

def test_viewer_can_view_document_but_cannot_archive(
    client: TestClient,
    admin_headers,
    viewer_headers,
    customer,
    temp_file_storage,
):
    order_id = create_order_from_quotation(
        client,
        admin_headers,
        customer,
    )

    upload_response = client.post(
        f"/orders/{order_id}/documents",
        data={
            "document_type": "TECHNICAL_DRAWING",
        },
        files={
            "file": (
                "archive-test.txt",
                b"archive test",
                "text/plain",
            )
        },
        headers=admin_headers,
    )

    document_id = upload_response.json()["id"]

    get_response = client.get(
        f"/documents/{document_id}",
        headers=viewer_headers,
    )

    assert get_response.status_code == 200

    archive_response = client.patch(
        f"/documents/{document_id}/archive",
        headers=viewer_headers,
    )

    assert archive_response.status_code == 403

def test_admin_can_archive_document(
    client: TestClient,
    admin_headers,
    customer,
    temp_file_storage,
):
    order_id = create_order_from_quotation(
        client,
        admin_headers,
        customer,
    )

    upload_response = client.post(
        f"/orders/{order_id}/documents",
        data={
            "document_type": "TECHNICAL_DRAWING",
        },
        files={
            "file": (
                "archive-admin.txt",
                b"archive me",
                "text/plain",
            )
        },
        headers=admin_headers,
    )

    document_id = upload_response.json()["id"]

    archive_response = client.patch(
        f"/documents/{document_id}/archive",
        headers=admin_headers,
    )

    assert archive_response.status_code == 204

    metadata_response = client.get(
        f"/documents/{document_id}",
        headers=admin_headers,
    )

    assert metadata_response.status_code == 200
    assert metadata_response.json()["status"] == "ARCHIVED"

