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
