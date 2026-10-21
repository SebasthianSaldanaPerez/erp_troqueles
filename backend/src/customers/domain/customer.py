from enum import Enum
from uuid import UUID, uuid4
from src.shared.domain.value_objects.address import Address
from src.shared.domain.value_objects.email import Email
from src.shared.domain.value_objects.phone import Phone
from src.shared.domain.value_objects.rfc import RFC
from src.customers.domain.errors import InvalidBusinessNameError

class CustomerStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Customer:
    def __init__(self,business_name: str,customer_id: UUID | None = None, status: CustomerStatus = CustomerStatus.ACTIVE, email: Email | None = None, 
                 rfc: RFC | None = None, phone: Phone | None = None, address: Address | None = None, contact_name: str | None = None, notes: str | None = None,):

        self._id = customer_id or uuid4()
        self._business_name = self._validate_business_name(business_name)
        self._status = status
        self._email = email
        self._rfc = rfc
        self._phone = phone
        self._address = address
        self._contact_name = contact_name.strip() if contact_name else None
        self._notes = notes.strip() if notes else None

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def business_name(self) -> str:
        return self._business_name

    @property
    def status(self) -> CustomerStatus:
        return self._status

    @property
    def email(self) -> Email | None:
        return self._email
    
    @property
    def rfc(self) -> RFC | None:
        return self._rfc

    @property
    def phone(self) -> Phone | None:
        return self._phone

    @property
    def address(self) -> Address | None:
        return self._address

    @property
    def contact_name(self) -> str | None:
        return self._contact_name

    @property
    def notes(self) -> str | None:
        return self._notes

    def rename(self, new_business_name: str) -> None:
        self._business_name = self._validate_business_name(new_business_name)

    def change_email(self, new_email: Email) -> None:
        self._email = new_email

    def change_rfc(self, new_rfc: RFC) -> None:
        self._rfc = new_rfc

    def deactivate(self) -> None:
        self._status = CustomerStatus.INACTIVE

    def reactivate(self) -> None:
        self._status = CustomerStatus.ACTIVE


    def change_phone(self, new_phone: Phone) -> None:
        self._phone = new_phone


    def change_address(self, new_address: Address) -> None:
        self._address = new_address


    def change_contact_name(self, new_contact_name: str | None) -> None:
        self._contact_name = (
            new_contact_name.strip()
            if new_contact_name
            else None
        )

    def change_notes(self, new_notes: str | None) -> None:
        self._notes = new_notes.strip() if new_notes else None

    @staticmethod
    def _validate_business_name(business_name: str) -> str:
        if not business_name or not business_name.strip():
            raise InvalidBusinessNameError("Business name is required")

        return business_name.strip()