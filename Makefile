.PHONY: install test test-mongo run seed

install:
	pip install -r requirements.txt

# In-memory Mongo; no Docker needed.
test:
	MONGO_URL=mongomock://localhost python -m pytest

# Against the replica set started by docker compose (supports transactions).
test-mongo:
	docker compose up -d mongo
	docker compose run --rm api python -m pytest

run:
	uvicorn app.main:app --reload

seed:
	python -m app.seed
