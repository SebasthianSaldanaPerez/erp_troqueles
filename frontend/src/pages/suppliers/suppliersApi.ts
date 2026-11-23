import { apiRequest } from "../../api/apiClient";
import type { Supplier } from "./types";

export type SupplierAddressData = {
  street: string;
  exterior_number: string;
  interior_number: string | null;
  neighborhood: string | null;
  city: string;
  state: string;
  postal_code: string;
  country: string;
};

export type CreateSupplierData = {
  name: string;
  email: string | null;
  rfc: string | null;
  phone: string | null;
  address: SupplierAddressData | null;
  contact_name: string | null;
  notes: string | null;
};


export async function getSuppliers(): Promise<Supplier[]> {
  const response = await apiRequest(
    "/suppliers",
  );

  if (!response.ok) {
    throw new Error(
      "No se pudieron cargar los proveedores",
    );
  }

  return response.json();
}


export async function getSupplier(
  supplierId: string,
): Promise<Supplier> {
  const response = await apiRequest(
    `/suppliers/${supplierId}`,
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo cargar el proveedor",
    );
  }

  return response.json();
}


export async function createSupplier(
  data: CreateSupplierData,
): Promise<string> {
  const response = await apiRequest(
    "/suppliers",
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
      "No se pudo crear el proveedor",
    );
  }

  const result = await response.json();

  return result.id;
}


export async function renameSupplier(
  supplierId: string,
  name: string,
): Promise<void> {
  const response = await apiRequest(
    `/suppliers/${supplierId}/name`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        new_name: name,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo actualizar el nombre",
    );
  }
}


export async function changeSupplierEmail(
  supplierId: string,
  email: string,
): Promise<void> {
  const response = await apiRequest(
    `/suppliers/${supplierId}/email`,
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
    throw new Error(
      "No se pudo actualizar el correo",
    );
  }
}


export async function changeSupplierRfc(
  supplierId: string,
  rfc: string,
): Promise<void> {
  const response = await apiRequest(
    `/suppliers/${supplierId}/rfc`,
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
    throw new Error(
      "No se pudo actualizar el RFC",
    );
  }
}


export async function changeSupplierPhone(
  supplierId: string,
  phone: string,
): Promise<void> {
  const response = await apiRequest(
    `/suppliers/${supplierId}/phone`,
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
    throw new Error(
      "No se pudo actualizar el teléfono",
    );
  }
}


export async function changeSupplierAddress(
  supplierId: string,
  address: SupplierAddressData,
): Promise<void> {
  const response = await apiRequest(
    `/suppliers/${supplierId}/address`,
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


export async function changeSupplierContactName(
  supplierId: string,
  contactName: string | null,
): Promise<void> {
  const response = await apiRequest(
    `/suppliers/${supplierId}/contact-name`,
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
    throw new Error(
      "No se pudo actualizar el contacto",
    );
  }
}


export async function changeSupplierNotes(
  supplierId: string,
  notes: string | null,
): Promise<void> {
  const response = await apiRequest(
    `/suppliers/${supplierId}/notes`,
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
    throw new Error(
      "No se pudieron actualizar las notas",
    );
  }
}

export async function deactivateSupplier(
  supplierId: string,
): Promise<void> {
  const response = await apiRequest(
    `/suppliers/${supplierId}/deactivate`,
    {
      method: "PATCH",
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo desactivar el proveedor",
    );
  }
}


export async function reactivateSupplier(
  supplierId: string,
): Promise<void> {
  const response = await apiRequest(
    `/suppliers/${supplierId}/reactivate`,
    {
      method: "PATCH",
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo reactivar el proveedor",
    );
  }
}