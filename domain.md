# Bounded Context

-Customers
-Suppliers
-Quotations
-Orders
-Expenses
-Invoices
-Documents
-Users / Access
-Audit


# Aggregates principales

## Customer

Customer
├── CustomerId
├── BusinessName
├── TradeName?
├── RFC?
├── ContactName?
├── Phone?
├── Email?
├── Address?
├── Notes?
└── Status

## Supplier

Supplier
├── SupplierId
├── Name
├── RFC?
├── ContactName?
├── Phone?
├── Email?
├── Address?
├── Notes?
└── Status

## Quotation

Quotation
├── QuotationId
├── Folio
├── CustomerId
├── Status
├── TaxRate
├── Currency
├── Notes?
├── ValidUntil?
├── CreatedAt
├── UpdatedAt
│
└── QuotationItem
    ├── ItemId
    ├── Description
    ├── Quantity
    └── UnitPrice

### QuotationItem

line_total = quantity × unit_price

subtotal = Σ line_total

tax = subtotal × tax_rate

total = subtotal + tax

DRAFT
SENT
ACCEPTED
REJECTED
CANCELLED

## Order

Order
├── OrderId
├── Folio
├── CustomerId
├── OriginQuotationId?
├── ProductionStatus
├── CurrentRevisionNumber
├── CreatedAt
├── UpdatedAt
│
└── OrderItem
    ├── ItemId
    ├── Description
    ├── Quantity
    └── UnitPrice

### OrderItem

order_total = Σ(quantity × unit_price)

# Status Order

## Production

CREATED
IN_PROGRESS
DELIVERED
CANCELLED

# Billing

NOT_INVOICED
PARTIALLY_INVOICED
FULLY_INVOICED
PAID

# Order Reviews

OrderRevision
├── RevisionId
├── OrderId
├── RevisionNumber
├── Snapshot
├── Reason
├── CreatedBy
└── CreatedAt

## Expense

Expense
├── ExpenseId
├── OrderId
├── Description
├── Amount
├── Category
├── SupplierId?
├── ExpenseDate
├── Notes?
├── Status
├── CreatedBy
├── CreatedAt
├── CancelledBy?
└── CancelledAt?

### Categories

MATERIAL
OUTSOURCED_SERVICE
TRANSPORT
CONSUMABLE
TOOLING
OTHER

### Status

REGISTERED
CANCELLED

## Invoice

Invoice
├── InvoiceId
├── OrderId
├── Folio
├── InvoiceDate
├── Total
├── Status
├── CreatedBy
└── CreatedAt

## Document

Document
├── DocumentId
├── Filename
├── ObjectKey
├── MimeType
├── Size
├── DocumentType
├── UploadedBy
├── CreatedAt
└── Status

### Document Type

QUOTATION
INVOICE
EXPENSE_RECEIPT
TECHNICAL_DRAWING
ORDER_ATTACHMENT
IMAGE
OTHER

## User

User
├── UserId
├── Name
├── Email
├── PasswordHash
├── Role
├── Status
├── CreatedAt
└── LastLoginAt?

### Role

ADMIN
OPERATOR
VIEWER

## Audit Event

created_by
updated_by
cancelled_by
uploaded_by

### Audit Events

AuditEvent
├── AuditEventId
├── UserId
├── EntityType
├── EntityId
├── Action
├── Metadata
└── Timestamp

# Value Objects

## Money

Money
├── amount
└── currency

## TaxRate

TaxRate
└── percentage

## Address

Address
├── street
├── exterior_number
├── interior_number?
├── neighborhood?
├── city
├── state
├── postal_code
└── country

# Relationships

Customer
   │
   ├───────────────┐
   ▼               ▼
Quotation        Order
   │               │
   │ convert       ├──── OrderRevision
   └──────────────►│
                   │
                   ├──── Expense ─── Supplier
                   │
                   ├──── Invoice
                   │
                   └──── Document

