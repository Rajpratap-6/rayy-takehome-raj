"""Load seed/orders.json into the ``orders`` collection.

Run with ``python -m app.seed``. Safe to run more than once: orders are
replaced by id, so re-seeding resets them to their initial state.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

from app.db import ORDERS, get_db

SEED_DIR = Path(__file__).resolve().parents[1] / "seed"


def load_orders() -> list[dict]:
    raw = json.loads((SEED_DIR / "orders.json").read_text())
    docs = []
    for row in raw["orders"]:
        doc = dict(row)
        doc["_id"] = doc.pop("order_id")
        doc["created_at"] = datetime.fromisoformat(doc["created_at"])
        docs.append(doc)
    return docs


async def seed(db=None) -> int:
    db = db if db is not None else get_db()
    docs = load_orders()
    for doc in docs:
        await db[ORDERS].replace_one({"_id": doc["_id"]}, doc, upsert=True)
    return len(docs)


if __name__ == "__main__":
    count = asyncio.run(seed())
    print(f"seeded {count} orders")
