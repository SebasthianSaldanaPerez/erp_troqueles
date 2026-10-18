import re
from dataclasses import dataclass
from src.customers.domain.errors import InvalidRFCError


@dataclass(frozen=True)
class RFC:
    value: str

    def __post_init__(self):
        normalized_rfc = self.value.strip().upper()

        if not normalized_rfc:
            raise InvalidRFCError("RFC cannot be empty")

        pattern = r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$"

        if not re.match(pattern, normalized_rfc):
            raise InvalidRFCError("Invalid RFC format")

        object.__setattr__(self, "value", normalized_rfc)