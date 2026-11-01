from pydantic import BaseModel


class AddressRequest(BaseModel):
    street: str
    exterior_number: str
    interior_number: str | None = None
    neighborhood: str | None = None
    city: str
    state: str
    postal_code: str
    country: str


class AddressResponse(BaseModel):
    street: str
    exterior_number: str
    interior_number: str | None = None
    neighborhood: str | None = None
    city: str
    state: str
    postal_code: str
    country: str


class CreateSupplierRequest(BaseModel):
    name: str
    email: str | None = None
    rfc: str | None = None
    phone: str | None = None
    address: AddressRequest | None = None
    contact_name: str | None = None
    notes: str | None = None


class CreateSupplierResponse(BaseModel):
    id: str


class SupplierResponse(BaseModel):
    id: str
    name: str
    status: str
    email: str | None = None
    rfc: str | None = None
    phone: str | None = None
    address: AddressResponse | None = None
    contact_name: str | None = None
    notes: str | None = None


class RenameSupplierRequest(BaseModel):
    new_name: str


class ChangeSupplierEmailRequest(BaseModel):
    new_email: str


class ChangeSupplierRFCRequest(BaseModel):
    new_rfc: str


class ChangeSupplierPhoneRequest(BaseModel):
    new_phone: str


class ChangeSupplierAddressRequest(BaseModel):
    street: str
    exterior_number: str
    interior_number: str | None = None
    neighborhood: str | None = None
    city: str
    state: str
    postal_code: str
    country: str


class ChangeSupplierContactNameRequest(BaseModel):
    new_contact_name: str | None = None


class ChangeSupplierNotesRequest(BaseModel):
    new_notes: str | None = None