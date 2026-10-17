from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    street: str
    exterior_number: str
    city: str
    state: str
    postal_code: str
    country: str
    interior_number: str | None = None
    neighborhood: str | None = None

    def __post_init__(self):
        if not self.street.strip():
            raise ValueError("Street is required")

        if not self.exterior_number.strip():
            raise ValueError("Exterior number is required")

        if not self.city.strip():
            raise ValueError("City is required")

        if not self.state.strip():
            raise ValueError("State is required")

        if not self.country.strip():
            raise ValueError("Country is required")

        if not self.postal_code.strip():
            raise ValueError("Postal code is required")

        object.__setattr__(self, "street", self.street.strip())
        object.__setattr__(self, "exterior_number", self.exterior_number.strip())
        object.__setattr__(self, "city", self.city.strip())
        object.__setattr__(self, "state", self.state.strip())
        object.__setattr__(self, "postal_code", self.postal_code.strip())
        object.__setattr__(self, "country", self.country.strip())

        if self.interior_number is not None:
            object.__setattr__(
                self,
                "interior_number",
                self.interior_number.strip() or None,
            )

        if self.neighborhood is not None:
            object.__setattr__(
                self,
                "neighborhood",
                self.neighborhood.strip() or None,
            )