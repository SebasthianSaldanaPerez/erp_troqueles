from fastapi import FastAPI

from src.presentation.api.customers.router import router as customers_router
from src.presentation.api.suppliers.router import router as suppliers_router
from src.presentation.api.quotations.router import router as quotations_router
from src.presentation.api.orders.router import router as orders_router
from src.presentation.api.expenses.router import router as expenses_router
from src.presentation.api.invoices.router import router as invoices_router


app = FastAPI(
    title="Troqueles ERP API",
    version="0.1.0",
)

app.include_router(customers_router)
app.include_router(suppliers_router)
app.include_router(quotations_router)
app.include_router(orders_router)
app.include_router(expenses_router)
app.include_router(invoices_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}