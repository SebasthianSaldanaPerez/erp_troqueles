from enum import Enum
from uuid import UUID, uuid4

from src.suppliers.domain.errors import InvalidSupplierNameError


class SupplierStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Supplier:
    def __init__(
        self,
        name: str,
        supplier_id: UUID | None = None,
        status: SupplierStatus = SupplierStatus.ACTIVE,
    ):
        self._id = supplier_id or uuid4()
        self._name = self._validate_name(name)
        self._status = status

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> SupplierStatus:
        return self._status

    def rename(self, new_name: str) -> None:
        self._name = self._validate_name(new_name)

    def deactivate(self) -> None:
        self._status = SupplierStatus.INACTIVE

    def reactivate(self) -> None:
        self._status = SupplierStatus.ACTIVE

    @staticmethod
    def _validate_name(name: str) -> str:
        if not name or not name.strip():
            raise InvalidSupplierNameError("Supplier name is required")

        return name.strip()