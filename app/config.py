"""Runtime configuration, read from the environment.

MONGO_URL
    ``mongomock://`` (the default) uses an in-memory Mongo, which is what
    ``make test`` does. Anything else is passed to Motor as a real connection
    string, e.g. ``mongodb://localhost:27017/?directConnection=true`` for the
    ``docker compose`` replica set from your machine (inside compose the api
    service uses ``mongodb://mongo:27017/?replicaSet=rs0``).
MONGO_DB
    Database name. Defaults to ``rayy_exercise``.
GATEWAY_WEBHOOK_SECRET
    Shared secret the payment gateway signs webhook bodies with.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    mongo_url: str
    mongo_db: str
    gateway_webhook_secret: str


def load_settings() -> Settings:
    return Settings(
        mongo_url=os.environ.get("MONGO_URL", "mongomock://localhost"),
        mongo_db=os.environ.get("MONGO_DB", "rayy_exercise"),
        gateway_webhook_secret=os.environ.get("GATEWAY_WEBHOOK_SECRET", "whsec_local_dev_only"),
    )


settings = load_settings()
