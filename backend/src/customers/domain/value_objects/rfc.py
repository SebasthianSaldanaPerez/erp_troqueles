import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RFC:
    value: str

    def __post_init__(self):
        normalized_rfc = self.value.strip().upper()

        if not normalized_rfc:
            raise ValueError("RFC cannot be empty")

        pattern = r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$"

        if not re.match(pattern, normalized_rfc):
            raise ValueError("Invalid RFC format")

        object.__setattr__(self, "value", normalized_rfc)