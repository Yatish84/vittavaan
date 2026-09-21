"""Fail when fake secret canaries appear in generated public artifacts."""

import os
from pathlib import Path

canaries = [
    os.getenv("VITTAVAAN_CANARY_DATABASE_SECRET", "VITTAVAAN_DB_CANARY_NOT_FOR_USE"),
    os.getenv("VITTAVAAN_CANARY_REDIS_SECRET", "VITTAVAAN_REDIS_CANARY_NOT_FOR_USE"),
]
targets = [Path("apps/web/dist"), Path("packages/contracts/openapi.json")]
violations: list[str] = []

for target in targets:
    paths = sorted(target.rglob("*")) if target.is_dir() else [target]
    for path in paths:
        if not path.is_file():
            continue
        content = path.read_bytes()
        for canary in canaries:
            if canary.encode() in content:
                violations.append(f"{path}: contains a secret canary")

if violations:
    raise SystemExit("Public artifact secret scan failed:\n" + "\n".join(violations))

print("Public artifacts contain no configured secret canaries.")
