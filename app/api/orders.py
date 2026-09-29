from fastapi import APIRouter, HTTPException

from app.models import Order
from app.services import orders as orders_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[Order])
async def list_orders(limit: int = 50) -> list[Order]:
    return await orders_service.list_orders(limit)


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str) -> Order:
    try:
        return await orders_service.get_order(order_id)
    except orders_service.OrderNotFound:
        raise HTTPException(status_code=404, detail="order not found")
