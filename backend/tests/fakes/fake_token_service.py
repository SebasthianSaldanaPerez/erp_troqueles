from uuid import UUID

from src.users.application.token_service import TokenService


class FakeTokenService(TokenService):

    def create_access_token(
        self,
        user_id: UUID,
    ) -> str:
        return f"token-{user_id}"

    def decode_access_token(
        self,
        token: str,
    ) -> UUID:
        prefix = "token-"

        if not token.startswith(prefix):
            raise ValueError("Invalid token")

        return UUID(
            token.removeprefix(prefix)
        )