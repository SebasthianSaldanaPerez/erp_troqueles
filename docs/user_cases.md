# Customers

- CreateCustomer
- UpdateCustomer
- DeactivateCustomer
- ReactivateCustomer
- GetCustomer
- ListCustomers

## CreateCustomer

Entry:

business_name
trade_name?
rfc?
contact_name?
phone?
email?
address?
notes?

## DeactivateCustomer

ACTIVE → INACTIVE

# Suppliers

- CreateSupplier
- UpdateSupplier
- DeactivateSupplier
- ReactivateSupplier
- GetSupplier
- ListSuppliers

# Quotations

- CreateQuotation
- GetQuotation
- ListQuotations

- AddQuotationItem
- UpdateQuotationItem
- RemoveQuotationItem

- SendQuotation
- AcceptQuotation
- RejectQuotation
- CancelQuotation

- GenerateQuotationPdf
- ConvertQuotationToOrder

## CreateQuotation

customer_id
tax_rate
currency
notes?
valid_until?

## AddQuotationItem

quotation_id
description
quantity
unit_price

## SendQuotation

DRAFT → SENT

## AcceptQuotation

SENT → ACCEPTED

## RejectQuotation

SENT → REJECTED

## CancelQuotation

DRAFT → CANCELLED
SENT  → CANCELLED

## ConvertQuotationToOrder

1. Buscar Quotation
2. Validar que esté ACCEPTED
3. Crear Order
4. Copiar conceptos
5. Asociar CustomerId
6. Asociar OriginQuotationId
7. Guardar Order

## Orders

- GetOrder
- ListOrders

- CreateOrder
- ReviseOrder

- StartOrder
- DeliverOrder
- CancelOrder

- GetOrderRevisionHistory
- GetOrderProfitability

## ReviseOrder

Load Order
   ↓
Apply Changes
   ↓
Validate
   ↓
Generate Revision Snapshot
   ↓
Save Order
   ↓
Save OrderRevision

## Order STatus

StartOrder
DeliverOrder
CancelOrder

# Expenses

- RegisterExpense
- UpdateExpense
- CancelExpense
- GetExpense
- ListExpensesByOrder

Entry:

order_id
description
amount
category
supplier_id?
expense_date
notes?

# Invoices

- RegisterInvoice
- UpdateInvoice
- CancelInvoice
- GetInvoice
- ListInvoicesByOrder

# Documents

- UploadOrderDocument
- UploadExpenseDocument
- UploadInvoiceDocument
- UploadQuotationDocument

- DownloadDocument
- ArchiveDocument

## UploadInvoiceDocument

1. Validar que Invoice existe
2. Validar archivo
3. Subir a Object Storage
4. Crear Document metadata
5. Asociarlo con Invoice

# Users

- Login
- GetCurrentUser
- ChangePassword

- CreateUser
- UpdateUser
- DeactivateUser
- ChangeUserRole
- ListUsers

# Audit

ReviseOrder
      │
      ├── guarda OrderRevision
      └── registra AuditEvent