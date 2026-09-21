# Vittavaan

Vittavaan is an enterprise-grade wealth-management application. The repository
currently contains the approved v3 design documentation and the first S1
repository-foundation slice. Product features have not been implemented yet.

Authentication remains a separate responsibility of `auth-core`. Vittavaan
will trust the identity supplied by that service; this repository must not grow
its own login, password, OTP, MFA or account-recovery implementation.

## What is here now

- `docs/v3/` — the current product, architecture, database, delivery and
  operations specification.
- `apps/web/` — a minimal React shell used to prove the web build and container.
- `backend/vittavaan/` — the FastAPI, configuration, database and worker
  foundation, split into domain, application, infrastructure and boundary
  layers.
- `database/migrations/` — Alembic database migrations. The first migration is
  deliberately an empty baseline; product tables come in their owning sprints.
- `compose*.yaml` — the shared, local and OCI-staging container definitions.
- `.github/workflows/` — automatic quality, leaked-secret, dependency,
  container-security and native ARM64/AMD64 image checks.

## Start the local foundation

You need Docker Desktop. The `make up` command creates local-only development
credentials, builds the images and waits for every service to become healthy.

```sh
make up
```

Database migrations run automatically before the API and worker start. The
`make migrate-compose` command is still available as a safe manual repeat-run.

Then open:

- Web shell: <http://localhost:5173>
- API liveness: <http://localhost:8000/health/live>
- API readiness: <http://localhost:8000/health/ready>
- Local technical metrics: <http://localhost:8000/metrics>

Useful commands:

```sh
make status       # show which services are healthy
make logs         # show recent service logs
make check        # run backend and frontend quality checks
make integration  # test PostgreSQL, Valkey, worker and S3-compatible storage
make recovery-drill # prove an interrupted worker task is safely re-delivered
make down         # stop services; database and object data are retained
```

The files created under `runtime/secrets/` are local-only and ignored by Git.
They are never staging or production credentials.

## Current delivery status

S0 documentation is complete and approved. S1 Repository Foundation is in
progress. The current foundation proves that the web application, API,
background worker, PostgreSQL, Valkey and private S3-compatible object store
can build and run together. It does not yet
implement portfolio, asset, liability, household or authentication features.

Start with [the v3 documentation index](docs/v3/README.md) and
[the agent handover](docs/v3/AGENT_HANDOVER.md) for the detailed plan and the
next work packages.
