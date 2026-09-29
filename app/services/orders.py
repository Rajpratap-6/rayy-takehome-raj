"""Order business rules. No HTTP here; routes call into this module."""

from app.models import Order
from app.repositories import orders as orders_repo


class OrderNotFound(Exception):
    pass


async def get_order(order_id: str) -> Order:
    doc = await orders_repo.get(order_id)
    if doc is None:
        raise OrderNotFound(order_id)
    return Order(**doc)


async def list_orders(limit: int = 50) -> list[Order]:
    return [Order(**doc) for doc in await orders_repo.list_recent(limit)]
