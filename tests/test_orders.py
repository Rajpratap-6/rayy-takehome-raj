import json
from pathlib import Path

SEED = json.loads((Path(__file__).resolve().parents[1] / "seed" / "orders.json").read_text())


async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_get_seeded_order(client):
    expected = SEED["orders"][0]
    response = await client.get(f"/orders/{expected['order_id']}")
    assert response.status_code == 200
    body = response.json()
    assert body["order_id"] == expected["order_id"]
    assert body["subtotal_paise"] == expected["subtotal_paise"]
    assert body["total_paise"] == expected["subtotal_paise"]
    assert body["status"] == "pending"


async def test_unknown_order_is_404(client):
    response = await client.get("/orders/ord_does_not_exist")
    assert response.status_code == 404


async def test_list_orders_returns_all_seeded(client):
    response = await client.get("/orders")
    assert response.status_code == 200
    assert {o["order_id"] for o in response.json()} == {o["order_id"] for o in SEED["orders"]}


async def test_seed_subtotals_match_items():
    for order in SEED["orders"]:
        items_total = sum(i["unit_price_paise"] * i["quantity"] for i in order["items"])
        assert order["subtotal_paise"] == items_total
        assert isinstance(order["subtotal_paise"], int)


async def test_apply_discount_calculates_percentage_and_funding(client):
    response = await client.post(
        "/orders/ord_a_1001/apply-discount",
        json={"code": "PARTNER15"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["subtotal_paise"] == 19999
    assert body["total_paise"] == 17000
    assert body["discount"] == {
        "code": "PARTNER15",
        "percent_off_bps": 1500,
        "cap_paise": 50000,
        "amount_paise": 2999,
        "partner_share_bps": 7000,
        "rayy_share_bps": 3000,
        "partner_amount_paise": 2099,
        "rayy_amount_paise": 900,
    }


async def test_apply_discount_respects_cap(client):
    response = await client.post(
        "/orders/ord_a_1002/apply-discount",
        json={"code": "MEGA50"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["discount"]["amount_paise"] == 6000
    assert body["total_paise"] == 13999


async def test_apply_discount_rejects_invalid_and_expired_codes(client):
    invalid = await client.post(
        "/orders/ord_a_1003/apply-discount",
        json={"code": "NOT_A_CODE"},
    )
    expired = await client.post(
        "/orders/ord_a_1003/apply-discount",
        json={"code": "LASTWEEK20"},
    )

    assert invalid.status_code == 400
    assert invalid.json() == {"detail": "invalid discount code"}
    assert expired.status_code == 400
    assert expired.json() == {"detail": "discount code expired"}


async def test_apply_discount_rejects_second_code(client):
    first = await client.post(
        "/orders/ord_a_1004/apply-discount",
        json={"code": "PARTNER15"},
    )
    second = await client.post(
        "/orders/ord_a_1004/apply-discount",
        json={"code": "WELCOME10"},
    )

    assert first.status_code == 200
    assert second.status_code == 409
    assert second.json() == {"detail": "discount already applied"}
