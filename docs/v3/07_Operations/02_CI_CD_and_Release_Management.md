# CI/CD and Release Management

## Pipeline

1. Validate docs/trace IDs, formatting, generated-contract drift and migrations.
2. Lint/type/test/security scan backend/frontend/IaC.
3. Build immutable signed `linux/arm64` and `linux/amd64` images, record digests, and publish SBOM/provenance.
4. Deploy the exact ARM64 image digests to OCI staging through the staging Compose overlay; run migrations with expand/migrate rules.
5. Run smoke, contract, integration, E2E/accessibility and scheduled load/security suites.
6. Require protected production approval.
7. Deploy progressively, validate technical/business signals and retain rapid application rollback.
8. Contract schema only after all compatible versions and data migration evidence permit it.

## Branch/environment policy

PRs create ephemeral validation where cost-effective. Merges to the integration branch deploy staging automatically after gates. Production uses tagged immutable releases and GitHub protected environments/manual approval. Direct production changes are prohibited except documented emergency workflow.

## OCI staging deployment sequence

1. A merge to the integration branch completes all tests and publishes multi-architecture images to the approved registry.
2. The deployment job authenticates using a short-lived deployment identity, transfers only versioned Compose/configuration files, and selects images by digest.
3. The host validates free disk/memory, backup freshness, required secrets and auth-core reachability.
4. A pre-deployment encrypted database backup is copied off-host.
5. The release's one-shot migration container applies forward-compatible migrations under an advisory lock.
6. `docker compose` reconciles services, waits for declared health checks, and exposes traffic only after API/web readiness.
7. Smoke tests cover auth-core redirect/callback, authorized API access, database/Redis/object health and a synthetic portfolio read/write path.
8. Failure restores the prior application image digests. Database recovery follows forward repair unless the documented migration recovery procedure explicitly permits restore.

Building source or using mutable `latest` tags on the VM is prohibited. The same release manifest records source commit, image digests, migration head, Compose/config versions and smoke evidence. A manual runbook remains available when hosted deployment connectivity is unavailable.

## Database release policy

- Expand: additive nullable/default-safe structures/indexes built safely.
- Migrate: resumable observable backfill with throttling/checkpoints.
- Switch: application reads/writes compatible paths under controlled flag.
- Contract: remove old structures only after evidence and recovery window.

Failed migrations halt deployment. Destructive rollback is not assumed; prefer application rollback plus forward database repair.

## Feature release

Deployment and capability activation are separate. Feature flags default safe/off, are environment-scoped, audited and require approval records for gated modules. Kill switches are tested and do not depend on a broken deployment path.

## Release evidence

Artifact digests, source commit, migration versions, test reports, vulnerability disposition, approvals, flags, deployment times, smoke/SLO results and rollback decision are retained per policy.
