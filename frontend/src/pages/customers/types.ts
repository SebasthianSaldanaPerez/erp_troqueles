export type CustomerStatus =
  | "ACTIVE"
  | "INACTIVE";

export type CustomerAddress = {
  street: string | null;
  exterior_number: string | null;
  interior_number: string | null;
  neighborhood: string | null;
  city: string | null;
  state: string | null;
  postal_code: string | null;
  country: string | null;
};

export type Customer = {
  id: string;
  business_name: string;
  status: CustomerStatus;
  email: string | null;
  rfc: string | null;
  phone: string | null;
  contact_name: string | null;
  notes: string | null;
  address: CustomerAddress | null;
};