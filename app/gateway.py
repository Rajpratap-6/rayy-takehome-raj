"""Stub payment-gateway client.

This stands in for the real gateway SDK. It never makes a network call.

Webhooks
--------
When a payment succeeds the gateway POSTs to ``/webhooks/payment`` with a
JSON body::

    {
      "event": "payment.succeeded",
      "payment_id": "pay_...",
      "order_id": "ord_...",
      "amount_paise": 12345
    }

``amount_paise`` is what the customer was actually charged. The raw request
body is signed with HMAC-SHA256 using the shared webhook secret, hex-encoded,
and sent in the ``X-Gateway-Signature`` header.

Delivery is at-least-once. The real gateway occasionally delivers the same
event more than once, sometimes seconds apart; ``deliveries()`` below always
delivers twice so you can see it.
"""

import hashlib
import hmac
import json
import secrets

from app.config import settings

SIGNATURE_HEADER = "X-Gateway-Signature"


class StubGateway:
    def __init__(self, webhook_secret: str | None = None):
        self.webhook_secret = webhook_secret or settings.gateway_webhook_secret

    def create_payment(self, order_id: str, amount_paise: int) -> dict:
        if not isinstance(amount_paise, int):
            raise TypeError("amount_paise must be an int")
        return {
            "payment_id": f"pay_{secrets.token_hex(8)}",
            "order_id": order_id,
            "amount_paise": amount_paise,
            "status": "created",
        }

    def webhook_body(self, payment: dict) -> bytes:
        body = {
            "event": "payment.succeeded",
            "payment_id": payment["payment_id"],
            "order_id": payment["order_id"],
            "amount_paise": payment["amount_paise"],
        }
        return json.dumps(body, separators=(",", ":")).encode()

    def sign(self, body: bytes) -> str:
        return hmac.new(self.webhook_secret.encode(), body, hashlib.sha256).hexdigest()

    def deliveries(self, payment: dict) -> list[tuple[dict, bytes]]:
        """Return the (headers, body) pairs the gateway would POST, in order."""
        body = self.webhook_body(payment)
        headers = {SIGNATURE_HEADER: self.sign(body), "Content-Type": "application/json"}
        return [(headers, body), (dict(headers), body)]
