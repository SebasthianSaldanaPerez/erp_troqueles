import re
from dataclasses import dataclass
from src.customers.domain.errors import InvalidEmailError


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        normalized_email = self.value.strip().lower()

        if not normalized_email:
            raise InvalidEmailError("Email cannot be empty")

        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(pattern, normalized_email):
            raise InvalidEmailError("Invalid email format")

        object.__setattr__(self, "value", normalized_email)