from pydantic import BaseModel

from src.users.domain.user import UserRole


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole


class CreateUserResponse(BaseModel):
    id: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    status: str