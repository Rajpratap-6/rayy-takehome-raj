"""Discount code lookup.

Codes are partner configuration, not transactional data, so they are loaded
from ``seed/discount_codes.json`` rather than stored in Mongo. Expiry in the
seed file is relative (``expires_in_days``) so the data stays meaningful
whenever it is loaded.
"""

import json
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path

from app.models import DiscountCode

SEED_FILE = Path(__file__).resolve().parents[2] / "seed" / "discount_codes.json"


@lru_cache(maxsize=1)
def _load() -> dict[str, DiscountCode]:
    raw = json.loads(SEED_FILE.read_text())
    now = datetime.now(timezone.utc)
    codes = {}
    for row in raw["codes"]:
        row = dict(row)
        row["expires_at"] = now + timedelta(days=row.pop("expires_in_days"))
        code = DiscountCode(**row)
        codes[code.code] = code
    return codes


def get_by_code(code: str) -> DiscountCode | None:
    return _load().get(code)


def all_codes() -> list[DiscountCode]:
    return list(_load().values())
