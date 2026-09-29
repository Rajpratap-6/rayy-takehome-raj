from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from app.gateway import SIGNATURE_HEADER, verify_webhook_signature
from app.models import PaymentWebhook
from app.services import orders as orders_service

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/payment")
async def payment_webhook(request: Request) -> dict[str, str]:
    body = await request.body()
    signature = request.headers.get(SIGNATURE_HEADER)
    if signature is None or not verify_webhook_signature(body, signature):
        raise HTTPException(status_code=401, detail="invalid webhook signature")

    try:
        webhook = PaymentWebhook.model_validate_json(body)
    except ValidationError:
        raise HTTPException(status_code=400, detail="invalid webhook payload")

    try:
        await orders_service.record_payment(
            webhook.order_id,
            webhook.payment_id,
            webhook.amount_paise,
        )
    except orders_service.OrderNotFound:
        raise HTTPException(status_code=404, detail="order not found")
    except orders_service.PaymentAmountMismatch:
        raise HTTPException(status_code=409, detail="payment amount does not match order")
    except orders_service.OrderAlreadyPaid:
        raise HTTPException(status_code=409, detail="order already paid")

    return {"status": "ok"}
