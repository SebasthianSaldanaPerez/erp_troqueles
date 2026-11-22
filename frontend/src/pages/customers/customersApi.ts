import { apiRequest } from "../../api/apiClient";
import type { Customer } from "./types";


export type CustomerAddressData = {
  street: string;
  exterior_number: string;
  interior_number: string | null;
  neighborhood: string | null;
  city: string;
  state: string;
  postal_code: string;
  country: string;
};

export type CreateCustomerData = {
  business_name: string;
  email: string | null;
  rfc: string | null;
  phone: string | null;
  contact_name: string | null;
  notes: string | null;
  address: CustomerAddressData | null;
};


export async function getCustomers(): Promise<Customer[]> {
  const response = await apiRequest(
    "/customers",
  );

  if (!response.ok) {
    throw new Error(
      "No se pudieron cargar los clientes",
    );
  }

  return response.json();
}


export async function createCustomer(
  data: CreateCustomerData,
): Promise<string> {
  const response = await apiRequest(
    "/customers",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(data),
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo crear el cliente",
    );
  }

  const result = await response.json();

  return result.id;
}

export async function getCustomer(
  customerId: string,
): Promise<Customer> {
  const response = await apiRequest(
    `/customers/${customerId}`,
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo cargar el cliente",
    );
  }

  return response.json();
}

export async function deactivateCustomer(
  customerId: string,
): Promise<void> {
  const response = await apiRequest(
    `/customers/${customerId}/deactivate`,
    {
      method: "PATCH",
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo desactivar el cliente",
    );
  }
}


export async function reactivateCustomer(
  customerId: string,
): Promise<void> {
  const response = await apiRequest(
    `/customers/${customerId}/reactivate`,
    {
      method: "PATCH",
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo reactivar el cliente",
    );
  }
}

export async function changeCustomerBusinessName(
  customerId: string,
  businessName: string,
): Promise<void> {
  const response = await apiRequest(
    `/customers/${customerId}/name`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        new_business_name: businessName,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo actualizar la razón social",
    );
  }
}


export async function changeCustomerEmail(
  customerId: string,
  email: string | null,
): Promise<void> {
  const response = await apiRequest(
    `/customers/${customerId}/email`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        new_email: email,
      }),
    },
  );

  if (!response.ok) {
    throw new Error("No se pudo actualizar el correo");
  }
}


export async function changeCustomerRfc(
  customerId: string,
  rfc: string | null,
): Promise<void> {
  const response = await apiRequest(
    `/customers/${customerId}/rfc`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        new_rfc: rfc,
      }),
    },
  );

  if (!response.ok) {
    throw new Error("No se pudo actualizar el RFC");
  }
}


export async function changeCustomerPhone(
  customerId: string,
  phone: string | null,
): Promise<void> {
  const response = await apiRequest(
    `/customers/${customerId}/phone`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        new_phone: phone,
      }),
    },
  );

  if (!response.ok) {
    throw new Error("No se pudo actualizar el teléfono");
  }
}


export async function changeCustomerContactName(
  customerId: string,
  contactName: string | null,
): Promise<void> {
  const response = await apiRequest(
    `/customers/${customerId}/contact-name`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        new_contact_name: contactName,
      }),
    },
  );

  if (!response.ok) {
    throw new Error("No se pudo actualizar el contacto");
  }
}


export async function changeCustomerNotes(
  customerId: string,
  notes: string | null,
): Promise<void> {
  const response = await apiRequest(
    `/customers/${customerId}/notes`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        new_notes: notes,
      }),
    },
  );

  if (!response.ok) {
    throw new Error("No se pudieron actualizar las notas");
  }
}

export async function changeCustomerAddress(
  customerId: string,
  address: CustomerAddressData,
): Promise<void> {
  const response = await apiRequest(
    `/customers/${customerId}/address`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(address),
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo actualizar la dirección",
    );
  }
}