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