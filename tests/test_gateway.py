import hashlib
import hmac
import json

import pytest

from app.gateway import SIGNATURE_HEADER, StubGateway
from app.repositories import discount_codes


def test_webhook_is_signed_and_delivered_twice():
    gateway = StubGateway(webhook_secret="whsec_test")
    payment = gateway.create_payment("ord_x", 12345)
    deliveries = gateway.deliveries(payment)
    assert len(deliveries) == 2
    headers, body = deliveries[0]
    expected = hmac.new(b"whsec_test", body, hashlib.sha256).hexdigest()
    assert headers[SIGNATURE_HEADER] == expected
    assert json.loads(body) == {
        "event": "payment.succeeded",
        "payment_id": payment["payment_id"],
        "order_id": "ord_x",
        "amount_paise": 12345,
    }
    assert deliveries[0][1] == deliveries[1][1]


def test_gateway_refuses_non_integer_amount():
    with pytest.raises(TypeError):
        StubGateway().create_payment("ord_x", 123.45)


def test_discount_codes_load():
    codes = discount_codes.all_codes()
    assert codes
    for code in codes:
        assert code.partner_share_bps + code.rayy_share_bps == 10000
    assert discount_codes.get_by_code("NOT_A_CODE") is None
