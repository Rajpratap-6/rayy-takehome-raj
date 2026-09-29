from app.gateway import StubGateway


async def test_payment_webhook_marks_order_paid_and_records_payment(client):
    gateway = StubGateway(webhook_secret="whsec_test")
    payment = gateway.create_payment("ord_a_1003", 89900)
    headers, body = gateway.deliveries(payment)[0]

    response = await client.post("/webhooks/payment", content=body, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    order = (await client.get("/orders/ord_a_1003")).json()
    assert order["status"] == "paid"
    assert order["payment"] == {
        "payment_id": payment["payment_id"],
        "amount_paise": 89900,
    }


async def test_payment_webhook_rejects_invalid_signature(client):
    gateway = StubGateway(webhook_secret="whsec_test")
    payment = gateway.create_payment("ord_a_1003", 89900)
    headers, body = gateway.deliveries(payment)[0]
    headers["X-Gateway-Signature"] = "invalid"

    response = await client.post("/webhooks/payment", content=body, headers=headers)

    assert response.status_code == 401
    order = (await client.get("/orders/ord_a_1003")).json()
    assert order["status"] == "pending"
    assert order["payment"] is None


async def test_payment_webhook_duplicate_delivery_is_idempotent(client, db):
    gateway = StubGateway(webhook_secret="whsec_test")
    payment = gateway.create_payment("ord_a_1003", 89900)
    deliveries = gateway.deliveries(payment)

    first = await client.post(
        "/webhooks/payment", content=deliveries[0][1], headers=deliveries[0][0]
    )
    second = await client.post(
        "/webhooks/payment", content=deliveries[1][1], headers=deliveries[1][0]
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert await db.orders.count_documents(
        {"payment.payment_id": payment["payment_id"]}
    ) == 1


async def test_payment_webhook_rejects_wrong_amount(client):
    gateway = StubGateway(webhook_secret="whsec_test")
    payment = gateway.create_payment("ord_a_1003", 1)
    headers, body = gateway.deliveries(payment)[0]

    response = await client.post("/webhooks/payment", content=body, headers=headers)

    assert response.status_code == 409
    order = (await client.get("/orders/ord_a_1003")).json()
    assert order["status"] == "pending"
