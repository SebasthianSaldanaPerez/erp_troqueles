from uuid import uuid4

import pytest

from src.users.infrastructure.jwt_token_service import (
    JWTTokenService,
)


def test_jwt_token_service_creates_and_decodes_token():
    service = JWTTokenService()

    user_id = uuid4()

    token = service.create_access_token(
        user_id
    )

    decoded_user_id = service.decode_access_token(
        token
    )

    assert decoded_user_id == user_id

def test_jwt_token_service_rejects_invalid_token():
    service = JWTTokenService()

    with pytest.raises(ValueError):
        service.decode_access_token(
            "esto-no-es-un-jwt"
        )