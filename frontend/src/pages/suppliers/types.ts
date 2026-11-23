export type SupplierStatus =
  | "ACTIVE"
  | "INACTIVE";

export type SupplierAddress = {
  street: string | null;
  exterior_number: string | null;
  interior_number: string | null;
  neighborhood: string | null;
  city: string | null;
  state: string | null;
  postal_code: string | null;
  country: string | null;
};

export type Supplier = {
  id: string;
  name: string;
  status: SupplierStatus;
  email: string | null;
  rfc: string | null;
  phone: string | null;
  contact_name: string | null;
  notes: string | null;
  address: SupplierAddress | null;
};