import os
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError

from src.users.application.token_service import TokenService


load_dotenv()


class JWTTokenService(TokenService):

    def __init__(self):
        self._secret_key = os.getenv("JWT_SECRET_KEY")
        self._algorithm = os.getenv(
            "JWT_ALGORITHM",
            "HS256",
        )
        self._expire_minutes = int(
            os.getenv(
                "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
                "30",
            )
        )

        if not self._secret_key:
            raise RuntimeError(
                "JWT_SECRET_KEY environment variable is required"
            )

    def create_access_token(
        self,
        user_id: UUID,
    ) -> str:
        expires_at = datetime.now(UTC) + timedelta(
            minutes=self._expire_minutes
        )

        payload = {
            "sub": str(user_id),
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            self._secret_key,
            algorithm=self._algorithm,
        )

    def decode_access_token(
        self,
        token: str,
    ) -> UUID:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )

            subject = payload.get("sub")

            if subject is None:
                raise ValueError(
                    "Token subject is missing"
                )

            return UUID(subject)

        except (
            InvalidTokenError,
            ValueError,
        ) as error:
            raise ValueError(
                "Invalid or expired access token"
            ) from error