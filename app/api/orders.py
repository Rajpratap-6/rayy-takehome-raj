from fastapi import APIRouter, HTTPException

from app.models import ApplyDiscountRequest, Order
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


@router.post("/{order_id}/apply-discount", response_model=Order)
async def apply_discount(order_id: str, body: ApplyDiscountRequest) -> Order:
    try:
        return await orders_service.apply_discount(order_id, body.code)
    except orders_service.OrderNotFound:
        raise HTTPException(status_code=404, detail="order not found")
    except orders_service.DiscountCodeInvalid:
        raise HTTPException(status_code=400, detail="invalid discount code")
    except orders_service.DiscountCodeExpired:
        raise HTTPException(status_code=400, detail="discount code expired")
    except orders_service.DiscountAlreadyApplied:
        raise HTTPException(status_code=409, detail="discount already applied")
