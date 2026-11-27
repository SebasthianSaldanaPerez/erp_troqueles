import { apiRequest } from "../../api/apiClient";

import type {
  Quotation,
} from "./types";


export async function getQuotations(): Promise<Quotation[]> {
  const response = await apiRequest(
    "/quotations",
  );

  if (!response.ok) {
    throw new Error(
      "No se pudieron cargar las cotizaciones",
    );
  }

  return response.json();
}

export type CreateQuotationData = {
  customer_id: string;
  tax_rate: number;
  currency: string;
};


export async function createQuotation(
  data: CreateQuotationData,
): Promise<string> {
  const response = await apiRequest(
    "/quotations",
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
      "No se pudo crear la cotización",
    );
  }

  const result = await response.json();

  return result.id;
}

export type CreateQuotationItemData = {
  description: string;
  quantity: number;
  unit_price: number;
  currency: string;
};


export async function addQuotationItem(
  quotationId: string,
  data: CreateQuotationItemData,
): Promise<void> {
  const response = await apiRequest(
    `/quotations/${quotationId}/items`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        description: data.description,
        quantity: data.quantity,
        unit_price: data.unit_price,
        currency: data.currency,
      }),
    },
  );

  if (!response.ok) {
    const detail =
      await response.text();

    throw new Error(
      `No se pudo agregar uno de los conceptos: ${detail}`,
    );
  }
}

export async function getQuotation(
  quotationId: string,
): Promise<Quotation> {
  const response = await apiRequest(
    `/quotations/${quotationId}`,
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo cargar la cotización",
    );
  }

  return response.json();
}

export type UpdateQuotationItemData = {
  description: string;
  quantity: number;
  unit_price: number;
  currency: string;
};


export async function updateQuotationItem(
  quotationId: string,
  itemId: string,
  data: UpdateQuotationItemData,
): Promise<void> {
  const response = await apiRequest(
    `/quotations/${quotationId}/items/${itemId}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type":
          "application/json",
      },
      body: JSON.stringify(data),
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo actualizar el concepto",
    );
  }
}

export async function sendQuotation(
  quotationId: string,
): Promise<void> {
  const response = await apiRequest(
    `/quotations/${quotationId}/send`,
    {
      method: "PATCH",
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo enviar la cotización",
    );
  }
}

export async function removeQuotationItem(
  quotationId: string,
  itemId: string,
): Promise<void> {
  const response = await apiRequest(
    `/quotations/${quotationId}/items/${itemId}`,
    {
      method: "DELETE",
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo eliminar el concepto",
    );
  }
}

export async function acceptQuotation(
  quotationId: string,
): Promise<void> {
  const response = await apiRequest(
    `/quotations/${quotationId}/accept`,
    {
      method: "PATCH",
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo aceptar la cotización",
    );
  }
}


export async function rejectQuotation(
  quotationId: string,
): Promise<void> {
  const response = await apiRequest(
    `/quotations/${quotationId}/reject`,
    {
      method: "PATCH",
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo rechazar la cotización",
    );
  }
}


export async function cancelQuotation(
  quotationId: string,
): Promise<void> {
  const response = await apiRequest(
    `/quotations/${quotationId}/cancel`,
    {
      method: "PATCH",
    },
  );

  if (!response.ok) {
    throw new Error(
      "No se pudo cancelar la cotización",
    );
  }
}

export async function reopenQuotation(
  quotationId: string,
): Promise<void> {
  const response = await apiRequest(
    `/quotations/${quotationId}/reopen`,
    {
      method: "PATCH",
    },
  );

  if (!response.ok) {
    const detail =
      await response.text();

    throw new Error(
      `No se pudo reabrir la cotización: ${detail}`,
    );
  }
}

export async function convertQuotationToOrder(
  quotationId: string,
): Promise<string> {
  const response = await apiRequest(
    `/quotations/${quotationId}/convert-to-order`,
    {
      method: "POST",
    },
  );

  if (!response.ok) {
    const detail = await response.text();

    throw new Error(
      `No se pudo convertir la cotización: ${detail}`,
    );
  }

  const data: { order_id: string } =
    await response.json();

  return data.order_id;
}

export async function getQuotationOrderId(
  quotationId: string,
): Promise<string | null> {
  const response = await apiRequest(
    `/quotations/${quotationId}/order`,
    {
      method: "GET",
    },
  );

  if (!response.ok) {
    const detail = await response.text();

    throw new Error(
      `No se pudo consultar la orden: ${detail}`,
    );
  }

  const data: {
    order_id: string | null;
  } = await response.json();

  return data.order_id;
}