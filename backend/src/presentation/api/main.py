from fastapi import FastAPI

from src.presentation.api.customers.router import router as customers_router
from src.presentation.api.suppliers.router import router as suppliers_router
from src.presentation.api.quotations.router import router as quotations_router
from src.presentation.api.orders.router import router as orders_router
from src.presentation.api.expenses.router import router as expenses_router
from src.presentation.api.invoices.router import router as invoices_router
from src.presentation.api.documents.router import router as documents_router
from src.presentation.api.auth.router import router as auth_router
from src.presentation.api.users.router import router as users_router
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.logging_config import configure_logging
import logging

from fastapi import Request
from fastapi.responses import JSONResponse


configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Troqueles ERP API",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers_router)
app.include_router(suppliers_router)
app.include_router(quotations_router)
app.include_router(orders_router)
app.include_router(expenses_router)
app.include_router(invoices_router)
app.include_router(documents_router)
app.include_router(auth_router)
app.include_router(users_router)

@app.get(
    "/health",
    tags=["Health"],
)
def health_check():
    return {
        "status": "ok",
    }

@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled exception while processing %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )