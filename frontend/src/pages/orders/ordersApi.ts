import { apiRequest } from "../../api/apiClient";

export interface OrderItem {
  id: string;
  description: string;
  quantity: number;
  unit_price: string;
  currency: string;
  total: string;
}

export interface OrderDetail {
  id: string;
  customer_id: string;
  origin_quotation_id: string | null;
  status: string;
  billing_status: string;
  currency: string;
  tax_rate: string;
  revision_number: number;
  items: OrderItem[];
  subtotal: string;
  tax: string;
  total: string;
}

export interface ReviseOrderRequest {
  item_id: string;
  description: string;
  quantity: number;
  unit_price: string;
  currency: string;
  reason: string;
}

export async function getOrder(
  orderId: string,
): Promise<OrderDetail> {
  const response = await apiRequest(
    `/orders/${orderId}`,
    { method: "GET" },
  );

  if (!response.ok) {
    throw new Error(
      `No se pudo cargar la orden: ${await response.text()}`,
    );
  }

  return response.json();
}

export async function reviseOrder(
  orderId: string,
  data: ReviseOrderRequest,
): Promise<void> {
  const response = await apiRequest(
    `/orders/${orderId}/revision`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    },
  );

  if (!response.ok) {
    throw new Error(
      `No se pudo registrar la revisión: ${await response.text()}`,
    );
  }
}

export interface OrderRevisionSnapshotItem {
  id: string;
  description: string;
  quantity: number;
  unit_price: string | number;
  currency?: string;
}

export interface OrderRevisionSnapshot {
  currency?: string;
  items?: OrderRevisionSnapshotItem[];
  subtotal?: string | number;
  tax?: string | number;
  total?: string | number;
}

export interface OrderRevision {
  id: string;
  order_id: string;
  revision_number: number;
  snapshot: OrderRevisionSnapshot;
  reason: string;
  created_by: string;
  created_at: string;
}

export async function getOrderRevisions(
  orderId: string,
): Promise<OrderRevision[]> {
  const response = await apiRequest(
    `/orders/${orderId}/revisions`,
    {
      method: "GET",
    },
  );

  if (!response.ok) {
    throw new Error(
      `No se pudo cargar el historial: ${await response.text()}`,
    );
  }

  return response.json();
}