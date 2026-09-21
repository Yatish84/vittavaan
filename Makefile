.PHONY: setup bootstrap lint typecheck test integration recovery-drill secret-scan check openapi migrate migrate-compose up down status logs

setup:
	uv sync --python 3.12.13
	pnpm install

bootstrap:
	./scripts/bootstrap-local.sh

lint:
	uv run ruff check .
	pnpm lint

typecheck:
	uv run mypy
	pnpm typecheck

test:
	PYTHONPATH=backend uv run pytest -m "not integration"
	pnpm test

integration: up
	docker compose -f compose.yaml -f compose.local.yaml --profile test run --build --rm integration-test

recovery-drill: up
	./scripts/verify-worker-redelivery.sh

secret-scan:
	VITTAVAAN_CANARY_DATABASE_SECRET=VITTAVAAN_DB_CANARY_NOT_FOR_USE \
	VITTAVAAN_CANARY_REDIS_SECRET=VITTAVAAN_REDIS_CANARY_NOT_FOR_USE \
	DATABASE_URL=VITTAVAAN_DB_CANARY_NOT_FOR_USE \
	REDIS_URL=VITTAVAAN_REDIS_CANARY_NOT_FOR_USE pnpm build
	VITTAVAAN_CANARY_DATABASE_SECRET=VITTAVAAN_DB_CANARY_NOT_FOR_USE \
	VITTAVAAN_CANARY_REDIS_SECRET=VITTAVAAN_REDIS_CANARY_NOT_FOR_USE \
	uv run python scripts/check-secret-canaries.py

check: lint typecheck test

openapi:
	PYTHONPATH=backend uv run python scripts/export-openapi.py

migrate:
	PYTHONPATH=backend uv run alembic upgrade head

migrate-compose:
	docker compose -f compose.yaml -f compose.local.yaml exec -T api .venv/bin/alembic upgrade head

up: bootstrap
	docker compose -f compose.yaml -f compose.local.yaml up --build --wait

down:
	docker compose -f compose.yaml -f compose.local.yaml down

status:
	docker compose -f compose.yaml -f compose.local.yaml ps

logs:
	docker compose -f compose.yaml -f compose.local.yaml logs --tail=200
