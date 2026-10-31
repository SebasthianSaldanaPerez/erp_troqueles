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

class CreateCustomerRequest(BaseModel):
    business_name: str
    email: str | None = None
    rfc: str | None = None
    phone: str | None = None
    address: AddressRequest | None = None
    contact_name: str | None = None
    notes: str | None = None


class CreateCustomerResponse(BaseModel):
    id: str


class CustomerResponse(BaseModel):
    id: str
    business_name: str
    status: str
    email: str | None = None
    rfc: str | None = None
    phone: str | None = None
    address: AddressResponse | None = None
    contact_name: str | None = None
    notes: str | None = None