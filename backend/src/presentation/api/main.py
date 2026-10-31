from fastapi import FastAPI

from src.presentation.api.customers.router import router as customers_router


app = FastAPI(
    title="Troqueles ERP API",
    version="0.1.0",
)

app.include_router(customers_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}