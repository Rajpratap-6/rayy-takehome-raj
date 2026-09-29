from fastapi import FastAPI

from app.api import health, orders

app = FastAPI(title="RAYY take-home")

app.include_router(health.router)
app.include_router(orders.router)
