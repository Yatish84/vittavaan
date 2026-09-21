"""Dispatch and observe the synthetic worker interruption probe."""

import argparse
import json
from datetime import UTC, datetime

from celery import Celery  # type: ignore[import-untyped]
from vittavaan.config import get_settings


def client() -> Celery:
    settings = get_settings()
    return Celery("recovery-probe", broker=settings.REDIS_URL, backend=settings.REDIS_URL)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("dispatch", "started", "wait"))
    parser.add_argument("task_id")
    parser.add_argument("--duration", type=int, default=30)
    args = parser.parse_args()
    celery_client = client()

    if args.action == "dispatch":
        headers = {
            "vittavaan_correlation_id": args.task_id,
            "vittavaan_causation_id": args.task_id,
            "vittavaan_enqueued_at": datetime.now(UTC).isoformat(),
        }
        celery_client.send_task(
            "foundation.recovery_probe.v1",
            args=[args.task_id, args.duration],
            task_id=args.task_id,
            headers=headers,
        )
        print(json.dumps({"task_id": args.task_id, "status": "dispatched"}))
        return 0

    result = celery_client.AsyncResult(args.task_id)
    if args.action == "started":
        print(json.dumps({"task_id": args.task_id, "status": result.status}))
        return 0 if result.status == "STARTED" else 1

    value = result.get(timeout=90)
    expected = {"status": "recovered", "correlation_id": args.task_id}
    if value != expected:
        raise RuntimeError("Recovery probe returned an unexpected synthetic result")
    print(json.dumps({"task_id": args.task_id, "status": "recovered"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
