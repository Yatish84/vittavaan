#!/bin/sh
set -eu

base_compose_files="-f compose.yaml -f compose.local.yaml"
drill_compose_files="$base_compose_files -f compose.recovery.yaml"
probe_id="$(python3 -c 'import uuid; print(uuid.uuid4())')"

restore_worker() {
  docker compose $base_compose_files up --detach --force-recreate --wait worker >/dev/null
}
trap restore_worker EXIT INT TERM

docker compose $drill_compose_files up --detach --force-recreate --wait worker
docker compose $base_compose_files exec -T api \
  .venv/bin/python scripts/worker-recovery-probe.py dispatch "$probe_id" --duration 15

attempt=0
until docker compose $base_compose_files exec -T api \
  .venv/bin/python scripts/worker-recovery-probe.py started "$probe_id" >/dev/null 2>&1; do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 20 ]; then
    echo "Recovery probe did not start within 20 seconds" >&2
    exit 1
  fi
  sleep 1
done

docker compose $drill_compose_files kill --signal SIGKILL worker
docker compose $drill_compose_files rm --force worker
docker compose $drill_compose_files up --detach --wait worker
docker compose $base_compose_files exec -T api \
  .venv/bin/python scripts/worker-recovery-probe.py wait "$probe_id"

trap - EXIT INT TERM
echo "Worker interruption and re-delivery probe passed."
