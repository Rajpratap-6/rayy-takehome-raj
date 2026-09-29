"""Order business rules. No HTTP here; routes call into this module."""

from datetime import datetime, timezone

from app.models import AppliedDiscount, DiscountCode, Order, Payment
from app.repositories import discount_codes
from app.repositories import orders as orders_repo


class OrderNotFound(Exception):
    pass


class DiscountCodeInvalid(Exception):
    pass


class DiscountCodeExpired(Exception):
    pass


class DiscountAlreadyApplied(Exception):
    pass


class PaymentAmountMismatch(Exception):
    pass


class OrderAlreadyPaid(Exception):
    pass


def calculate_discount(subtotal_paise: int, code: DiscountCode) -> AppliedDiscount:
    amount_paise = min(
        subtotal_paise * code.percent_off_bps // 10000,
        code.cap_paise,
    )
    partner_amount_paise = amount_paise * code.partner_share_bps // 10000
    rayy_amount_paise = amount_paise - partner_amount_paise
    return AppliedDiscount(
        code=code.code,
        percent_off_bps=code.percent_off_bps,
        cap_paise=code.cap_paise,
        amount_paise=amount_paise,
        partner_share_bps=code.partner_share_bps,
        rayy_share_bps=code.rayy_share_bps,
        partner_amount_paise=partner_amount_paise,
        rayy_amount_paise=rayy_amount_paise,
    )


async def get_order(order_id: str) -> Order:
    doc = await orders_repo.get(order_id)
    if doc is None:
        raise OrderNotFound(order_id)
    return Order(**doc)


async def list_orders(limit: int = 50) -> list[Order]:
    return [Order(**doc) for doc in await orders_repo.list_recent(limit)]


async def apply_discount(order_id: str, code_value: str) -> Order:
    order = await get_order(order_id)
    if order.discount is not None:
        raise DiscountAlreadyApplied(order_id)

    code = discount_codes.get_by_code(code_value)
    if code is None:
        raise DiscountCodeInvalid(code_value)
    if code.expires_at <= datetime.now(timezone.utc):
        raise DiscountCodeExpired(code_value)

    discount = calculate_discount(order.subtotal_paise, code)
    updated = await orders_repo.apply_discount(
        order_id,
        discount.model_dump(),
        order.subtotal_paise - discount.amount_paise,
    )
    if updated is None:
        raise DiscountAlreadyApplied(order_id)
    return Order(**updated)


async def record_payment(order_id: str, payment_id: str, amount_paise: int) -> Order:
    order = await get_order(order_id)
    if order.payment is not None:
        if (
            order.payment.payment_id == payment_id
            and order.payment.amount_paise == amount_paise
        ):
            return order
        raise OrderAlreadyPaid(order_id)
    if amount_paise != order.total_paise:
        raise PaymentAmountMismatch(order_id)

    payment = Payment(payment_id=payment_id, amount_paise=amount_paise)
    updated = await orders_repo.mark_paid(order_id, payment.model_dump())
    if updated is not None:
        return Order(**updated)

    current = await get_order(order_id)
    if (
        current.payment is not None
        and current.payment.payment_id == payment_id
        and current.payment.amount_paise == amount_paise
    ):
        return current
    raise OrderAlreadyPaid(order_id)
