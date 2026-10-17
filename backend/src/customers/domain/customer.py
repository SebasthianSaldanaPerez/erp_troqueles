from enum import Enum
from uuid import UUID, uuid4


class CustomerStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Customer:
    def __init__(self,business_name: str,customer_id: UUID | None = None, status: CustomerStatus = CustomerStatus.ACTIVE,):
        if not business_name or not business_name.strip():
            raise ValueError("Business name is required")

        self._id = customer_id or uuid4()
        self._business_name = business_name.strip()
        self._status = status

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def business_name(self) -> str:
        return self._business_name

    @property
    def status(self) -> CustomerStatus:
        return self._status

    def rename(self, new_business_name: str) -> None:
        self._business_name = self._validate_business_name(new_business_name)

    def deactivate(self) -> None:
        self._status = CustomerStatus.INACTIVE

    def reactivate(self) -> None:
        self._status = CustomerStatus.ACTIVE

    @staticmethod
    def _validate_business_name(business_name: str) -> str:
        if not business_name or not business_name.strip():
            raise ValueError("Business name is required")

        return business_name.strip()