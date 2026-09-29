import os

# Default to the in-memory Mongo; set MONGO_URL to run against a real one.
os.environ.setdefault("MONGO_URL", "mongomock://localhost")
os.environ.setdefault("MONGO_DB", "rayy_exercise_test")
os.environ.setdefault("GATEWAY_WEBHOOK_SECRET", "whsec_test")

import pytest  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402

from app.db import get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.seed import seed  # noqa: E402


@pytest.fixture
async def db():
    database = get_db()
    for name in await database.list_collection_names():
        await database[name].delete_many({})
    await seed(database)
    yield database


@pytest.fixture
async def client(db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
