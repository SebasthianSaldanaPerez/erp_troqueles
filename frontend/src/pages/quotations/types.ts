export type QuotationStatus =
  | "DRAFT"
  | "SENT"
  | "ACCEPTED"
  | "REJECTED"
  | "CANCELLED";


export type QuotationItem = {
  id: string;
  description: string;
  quantity: number;
  unit_price: string;
  currency: string;
  total: string;
};


export type Quotation = {
  id: string;
  customer_id: string;
  status: QuotationStatus;
  tax_rate: string;
  currency: string;
  items: QuotationItem[];
  subtotal: string;
  tax: string;
  total: string;
};