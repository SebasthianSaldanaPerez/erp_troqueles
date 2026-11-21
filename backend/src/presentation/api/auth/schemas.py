from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CurrentUserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    status: str