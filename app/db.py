"""MongoDB access.

The client is created lazily on first use so that tests can set the
environment before anything connects. Collections are reached through
``get_db()``; repositories own the queries.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

ORDERS = "orders"

_client = None


def get_client():
    global _client
    if _client is None:
        if settings.mongo_url.startswith("mongomock://"):
            from mongomock_motor import AsyncMongoMockClient

            _client = AsyncMongoMockClient()
        else:
            _client = AsyncIOMotorClient(settings.mongo_url, tz_aware=True)
    return _client


def get_db() -> AsyncIOMotorDatabase:
    return get_client()[settings.mongo_db]
