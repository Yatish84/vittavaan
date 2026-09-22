# Implementation and Verification Log

## Purpose

This is the detailed, dated audit trail of implementation work. It complements:

- `03_Sprint_and_Milestone_Plan.md`, which explains the complete S0–S12 roadmap;
- `04_S1_Repository_Foundation_Backlog.md`, which defines S1 tasks and acceptance criteria;
- `../00_Governance/03_Progress_Tracker.md`, which summarizes current status; and
- `../AGENT_HANDOVER.md`, which tells the next agent where to resume.

Never record credentials, tokens, personal data or local secret values here. A command is evidence only when its result was actually checked.

## Status vocabulary

| Status | Plain-English meaning |
|---|---|
| Planned | Agreed work that has not started. |
| In progress | Some work or checks are complete, but the acceptance criteria are not all met. |
| Blocked | Work cannot safely continue without a recorded decision or external dependency. |
| Complete | Every stated acceptance criterion has evidence and no required work remains. |

## Execution record

### 20 Sep 2026 — S1 foundation slice 1

**Status:** Verified; S1 remains in progress.

**Implemented**

- Pinned Python 3.12.13, Node 24 and pnpm 12.5.1; committed Python and JavaScript lockfiles.
- Created the layered backend skeleton, FastAPI shell, React shell and Celery worker shell.
- Added typed configuration and local `_FILE` secret handling.
- Added PostgreSQL 17.11 and Valkey 8.1 to the private Compose data network.
- Added API/web/worker images, local and staging Compose overlays and local bootstrap commands.
- Added Alembic baseline revision `20260920_0001` without business tables.
- Added liveness/readiness endpoints, correlation IDs and structured logging foundation.
- Added GitHub backend, frontend and Compose-contract quality jobs.

**Verified**

| Check | Result |
|---|---|
| Python lint (`uv run ruff check .`) | Passed |
| Python strict typing (`uv run mypy`) | Passed |
| Python unit tests | 3 passed at the slice checkpoint |
| Web lint and strict typing | Passed |
| Web unit test | 1 passed |
| Web production build | Passed |
| Compose configuration validation | Passed |
| Container build on local ARM64 machine | Passed |
| Local services | Web, API, worker, PostgreSQL and Valkey all healthy |
| API health endpoints | Liveness and readiness both returned success |
| Web production image | Served successfully on local port 5173 |
| Clean migration | Baseline revision applied to PostgreSQL |
| Migration result | Database reported exactly `20260920_0001` |
| Whitespace/error check (`git diff --check`) | Passed |

**Important limits**

- No portfolio, household, asset, liability, financial calculation or authentication feature was implemented.
- Docker containers were removed after verification to release memory; images and the named database volume were retained.
- CI has been defined but a real GitHub Actions run is not yet evidence until changes are pushed.
- AMD64, security-scan, object-storage and OCI checks remain outstanding.

### 20 Sep 2026 — S1 quality slice 2

**Status:** Verified; S1 remains in progress.

**Implemented**

- Added executable dependency rules for domain, application, infrastructure and boundary layers.
- Added a controlled planted-violation test proving the architecture guard detects an invalid import.
- Added safe RFC 9457-style responses for missing routes and request-validation failures.
- Added deterministic OpenAPI generation and committed-contract drift checking.

**Verification evidence**

The exact results belong below after the complete local quality command passes.

| Check | Result |
|---|---|
| Architecture direction and planted violation | Passed |
| Safe missing-route response | Passed |
| Deterministic OpenAPI contract | Passed; SHA-256 `e886326e138aa987a3c39a0889c07cb289a3f042418ccafb0d1a87759adbfa61` |
| Full local quality command | Passed: 7 Python tests and 1 web test, with lint and strict typing successful |

### 20 Sep 2026 — S1 database and service reliability slice 3

**Status:** Verified; S1 remains in progress.

**Implemented**

- Added a one-shot migration container that must finish successfully before the API and worker start.
- Strengthened readiness so it requires both a reachable PostgreSQL database and migration head `20260920_0001`.
- Separated fast checks from real-service integration checks with an explicit pytest marker.
- Added a non-root Docker test runner attached to the private application/data networks; PostgreSQL and Valkey remain unavailable as public host ports.
- Added real PostgreSQL, Valkey and Celery worker checks using synthetic isolated identifiers.
- Added `make integration` as the reproducible service-test command.

**Verified**

| Check | Result |
|---|---|
| Automatic migration before API/worker | Passed |
| First migration repeat-run | Passed |
| Second migration repeat-run | Passed; no duplicate changes or error |
| Expected migration head | Exactly `20260920_0001` |
| Deliberately incorrect migration head | Readiness check rejected it |
| PostgreSQL real connection/query | Passed |
| Valkey ping/set/get/delete with isolated key | Passed; key removed |
| Duplicate synthetic Celery delivery | Both deliveries returned the same deterministic result; no durable business record exists |
| Database container restart | Synthetic probe survived restart and was then removed |
| PostgreSQL unavailable | API readiness returned HTTP 503 with safe `not_ready` body |
| PostgreSQL recovery | API readiness returned HTTP 200 again |
| Integration suite | 3 passed in Linux ARM64 Docker |
| Fast foundation suite | 7 passed, 3 integration checks deliberately excluded |
| Web suite | 1 passed |
| Python/web lint and strict types | Passed |
| Diff formatting check | Passed |

**Issues found and resolved during verification**

1. Docker Desktop did not make private-network database/cache ports usable by the host test runner. The safer resolution was to keep those ports private and run tests in a dedicated Docker service on the internal network.
2. The first container test execution passed all three tests but could not write its optional coverage/cache files as the non-root user. Integration coverage duplication and pytest caching were disabled for that runner; normal local tests continue to collect coverage.

**Important limits**

- The integration database is the local synthetic development database, not a staging or production database.
- Migration advisory locking and separate migration/application database roles still require implementation evidence.
- Broker-loss shutdown/retry behavior needs a separate controlled test.

### 20 Sep 2026 — S1 monitoring and secret-protection slice 4

**Status:** Verified; S1 remains in progress.

**Implemented**

- Added structured JSON request-completion logs with UTC timestamp, service, environment, release, method, route template, status, duration, correlation and causation IDs.
- Added recursive key-based redaction before structured events reach the JSON renderer.
- Added process-local OpenTelemetry spans using a no-network in-memory exporter for the foundation environment.
- Added Prometheus-format HTTP request, duration-bucket and in-flight metrics.
- Restricted metric labels to method, route template, status class and fixed duration buckets; user/resource/correlation IDs are prohibited as metric labels.
- Added a hidden `/metrics` endpoint that is not part of the public OpenAPI contract.
- Added generated-artifact scanning with fake database and Valkey secret canaries.
- Added monitoring/redaction tests and locked OpenTelemetry SDK dependencies.

**Verified**

| Check | Result |
|---|---|
| Structured container logs | Valid JSON events with UTC timestamps and approved technical fields |
| Caller correlation ID | Exact valid UUID returned and logged |
| Caller causation ID | Exact valid UUID returned and logged |
| OpenTelemetry request span | Created with safe method, route template and status attributes |
| Metrics endpoint | Served bounded request totals, latency buckets and in-flight gauge |
| Metrics cardinality | No user, resource, financial, correlation or causation labels |
| Public OpenAPI contract | `/metrics` excluded; deterministic contract test still passed |
| Recursive redaction canary | Passed for top-level, nested and list-contained sensitive keys |
| Settings/health/OpenAPI canary | Fake database/cache credential absent |
| Web production build canary | Fake database/cache credential absent |
| Runtime log canary scan | No configured fake secret found |
| Fast backend suite | 10 passed; 3 real-service tests deliberately excluded |
| Overall backend line coverage | 81%, above the documented 80% overall threshold |
| Web suite, lint and strict types | Passed |

**Issue found and resolved during verification**

The first redaction test proved that nested sensitive fields were protected but a top-level `password` field was not. The processor was corrected to apply the same sensitive-key rule at every level, and the complete suite then passed.

**Important limits**

- The in-memory trace exporter proves instrumentation without transmitting data. An approved staging collector/export destination remains future work.
- Queue depth/age, database-pool saturation and worker runtime metrics require the remaining S1 instrumentation work.
- Operational dashboard and alert routing are not activated in this local slice.

### 20 Sep 2026 — S1 worker recovery and migration safety slice 5

**Status:** Verified; S1 remains in progress.

**Implemented**

- Added a PostgreSQL advisory lock around Alembic execution so concurrent deployment attempts serialize migrations.
- Changed the integration proof from sequential to concurrent migration attempts.
- Added bounded Celery connection retries, socket timeouts, task time limits, late acknowledgement, worker-loss rejection and one-at-a-time prefetch behavior.
- Added safe worker start/completion timing logs without task arguments or result payloads.
- Added explicit worker correlation/causation headers and context clearing between tasks.
- Added Valkey to API readiness, alongside PostgreSQL and migration-head validation.
- Added bounded PostgreSQL/Valkey readiness gauges and rejection of unapproved dependency labels.
- Added isolated cache readiness unit tests and worker reliability/configuration tests.

**Verified**

| Check | Result |
|---|---|
| Two simultaneous Alembic upgrade processes | Both passed under the advisory lock |
| Worker settings | Retry maximum 12, bounded sockets, soft/hard time limits and safe acknowledgement settings verified |
| Deliberate Valkey outage | Worker logged connection refusal and visible retry attempt |
| Worker recovery | Worker reconnected automatically after Valkey restart |
| Post-recovery task | Synthetic worker task passed |
| Duplicate delivery after changes | Both deterministic deliveries passed |
| Cross-task trace isolation | Start/completion logs carried the current task's matching IDs; preceding context was cleared |
| API during Valkey outage | HTTP 503 with safe `not_ready` body |
| Valkey outage metric | `vittavaan_dependency_ready{dependency="valkey"} 0` |
| Valkey recovery | API returned HTTP 200; PostgreSQL and Valkey gauges both returned 1 |
| Fast backend suite | 15 passed; 3 integration tests deliberately excluded |
| Real-service integration suite | 3 passed in Linux ARM64 Docker |
| Overall backend coverage | 84% |
| Web suite, lint, strict types and diff check | Passed |

**Issue found and resolved during verification**

The first outage-recovery log review showed that Celery's task-start signal ran before the task body bound its correlation ID, allowing a preceding context to appear. Worker signals now clear context first and read validated UUIDs from namespaced message headers. Rebuilt-container logs prove matching current-task IDs at start and completion.

**Important limits**

- The outage exercise covered an idle worker and post-recovery tasks. An interrupted long-running task/re-delivery drill remains future reliability evidence.
- Queue depth/oldest-age monitoring still requires a collector or broker inspection component.

### 21 Sep 2026 — S1 database privilege separation slice 6

**Status:** Verified; S1 remains in progress.

**Implemented**

- Added an idempotent database bootstrap that creates separate `vittavaan_migrator` and `vittavaan_app` accounts without administrator privileges.
- Restricted database-structure changes to the migration account. The normal API and worker account receives only the permissions required to read and change application data.
- Split local secret files and connection URLs so Alembic uses the migration account while the API, worker and integration probes use the normal application account.
- Added direct integration evidence proving the normal application account cannot create a table while the migration account can.

**Verified**

| Check | Result |
|---|---|
| Application and migration accounts | Neither is superuser and neither can create databases or other roles |
| Application account table creation | Correctly rejected by PostgreSQL |
| Migration account table creation/removal | Passed |
| Alembic version-table owner | `vittavaan_migrator` |
| API readiness after role split | Healthy |
| Fast quality suite | 15 backend tests passed with 84% coverage; web checks passed |
| Real-service integration suite | 4 passed in Linux ARM64 Docker |

**Plain-English security benefit**

If the everyday application connection were compromised, it could not redesign or delete the database structure. Structural changes require the separate migration credential used only during controlled deployments.

### 21 Sep 2026 — S1 security and container portability slice 7

**Status:** Partially verified; the local security evidence is complete, while the native GitHub AMD64 run remains pending.

**Implemented**

- Added a GitHub security workflow for leaked-secret detection, Python and JavaScript dependency audits, repository/container vulnerability scanning and native ARM64/AMD64 image builds.
- Configured image builds to create software-bill-of-materials and provenance attestations without publishing images during this verification stage.
- Changed the web container to run as the restricted `nginx` user on port 8080 with writable temporary files kept under `/tmp`.
- Updated operating-system packages during API and web image construction to include available security fixes.
- Pinned the container installation of `uv` to the repository-approved version.

**Verified locally**

| Check | Result |
|---|---|
| Python locked dependency audit | No known vulnerabilities found |
| JavaScript locked dependency audit | No known vulnerabilities found |
| Repository/container-definition scan | 0 HIGH/CRITICAL vulnerabilities, secrets or misconfigurations after remediation |
| API image scan | 0 fixed HIGH/CRITICAL findings |
| Web image scan | 0 fixed HIGH/CRITICAL findings |
| Web runtime identity | Restricted `nginx` account, UID/GID 101 |
| Web runtime response | Served successfully on local port 5173 through container port 8080 |
| Native local ARM64 image builds | API and web passed |

**Issue found and resolved during verification**

The first scans found that the web server ran as root and both final images contained operating-system packages with available security fixes. The web server was moved to a restricted account and current package fixes were applied during image construction. Repeat scans then returned zero HIGH/CRITICAL findings covered by the configured policy.

**Important limits**

- A locally emulated AMD64 API build stopped when the `uv` executable encountered a QEMU segmentation fault. This is an emulation-tool limitation, not a demonstrated application defect. The workflow therefore uses GitHub's native Intel and ARM runners instead of emulating one processor on the other.
- The GitHub workflow is defined but has not yet run on GitHub. AMD64 success, leaked-secret scanning, image attestations and hosted-CI status must not be claimed as verified until that run passes.
- Scans report vulnerabilities known to the selected scanners and databases at the time of execution; they reduce risk but cannot prove an image has no security flaw.

### 21 Sep 2026 — S1 capacity monitoring and worker re-delivery slice 8

**Status:** Verified; S1 remains in progress.

**Implemented**

- Added bounded database-pool size, checked-out and overflow gauges to the existing internal Prometheus endpoint.
- Added worker-queue depth and oldest-message-age gauges. Queue inspection reads only the approved technical enqueue timestamp; task arguments and message bodies are never emitted.
- Added approved-name worker completion counters and runtime histograms. Workers atomically store only bounded aggregate fields in Valkey, and the API metrics endpoint loads them for cross-process scraping.
- Added a bounded synthetic long-running recovery task and a repeatable `make recovery-drill` command.
- Added a separate recovery-only Compose overlay with a five-second visibility timeout. Normal runtime retains the safer one-hour value; the short setting cannot accidentally apply unless the drill overlay is explicitly selected.
- Applied the Redis visibility timeout consistently to Celery's broker, result backend and application setting after the first drill exposed incomplete configuration.

**Verified**

| Check | Result |
|---|---|
| Database-pool metrics | Exported aggregate size/checked-out/overflow values |
| Queue pressure metrics | Exported aggregate depth/oldest age without task payloads |
| Cross-process worker metrics | Completion totals and duration buckets visible from the API metrics endpoint after worker execution/restart |
| High-cardinality protections | Unknown task names, dependency names and invalid values rejected in tests |
| Interrupted synthetic task | Worker force-killed while the task was active |
| Unfinished-work handling | Task was not silently acknowledged; it became visible again |
| Worker restart and re-delivery | Same task ID was delivered again and returned the expected synthetic result |
| Fast suite | 19 backend tests passed with 82% overall coverage; web checks passed |
| Real-service integration suite | 5 passed in Linux ARM64 Docker |

**Issue found and resolved during verification**

The first automated drill showed that setting only Celery's broker visibility timeout did not make interrupted Redis-backed work visible on the intended schedule. The same validated timeout is now supplied to the broker transport, result-backend transport and Celery application setting. The repeated force-kill drill then passed.

**Metric privacy boundary**

The shared worker metric store accepts only predefined task aliases, predefined outcome values and predefined duration buckets. It has a 24-hour expiry and contains no task IDs, correlation IDs, arguments, users, resources or financial values. Failure to write metrics is logged safely and does not change the business outcome of a task.

### 21 Sep 2026 — S1 S3-compatible object-storage slice 9

**Status:** Verified; S1 remains in progress.

**Decision**

RustFS 1.0.0 was selected for local S3-compatible development and foundation tests. It is Apache-2.0 licensed, provides official ARM64 and AMD64 images, runs as non-root UID/GID 10001, and passed the configured HIGH/CRITICAL image scan. The multi-architecture image index is pinned by digest.

This is an adapter-level development choice, not a commitment to operate RustFS as production storage. OCI staging can use OCI Object Storage through its path-style S3 compatibility API, subject to its documented API differences; AWS production remains native S3 by the same application port.

**Implemented**

- Added a private-network object-store service with a persistent named volume, secret-file credential bootstrap and authenticated S3 endpoint.
- Added Boto3 to the deterministic Python lock and a synthetic S3 integration probe.
- Made API and worker startup wait for object-store health without exposing its S3 or administration ports to the host.
- Added the pinned third-party image to the GitHub security workflow.

**Verified**

| Check | Result |
|---|---|
| Licence | Apache License 2.0 |
| Image architectures | Linux AMD64 and ARM64 manifests present |
| Runtime identity | Non-root `rustfs`, UID/GID 10001 |
| Host exposure | No object-store port published |
| Health/start ordering | Service healthy before API/worker start |
| Signed S3 workflow | Isolated bucket create, object upload, download/content comparison, object delete and bucket delete passed |
| Cleanup | Synthetic bucket/object removed in `finally` cleanup |
| Image security scan | 0 HIGH/CRITICAL known fixed findings under Trivy 0.74.0 |
| Real-service integration suite | 6 passed in Linux ARM64 Docker |

**Candidates rejected or deferred**

- MinIO was not selected because its current community maintenance/distribution position no longer matches the low-friction maintained-image requirement.
- SeaweedFS 4.47 was functionally proven with the same six integration tests and is Apache-2.0/multi-architecture, but its compiled gRPC dependency produced one fixable HIGH finding (`CVE-2026-84445`). It was removed from the active Compose definition rather than adding a security exception.
- RustFS 1.0.0 is newly generally available. Keep the S3 adapter portable, pin/scan upgrades and do not depend on its administration API or implementation-specific extensions.

### 21 Sep 2026 — S1 onboarding and evidence slice 10

**Status:** Verified locally in an isolated clean copy; hosted-CI evidence and owner baseline approval remain.

**Implemented**

- Added a plain-English developer guide covering prerequisites, first setup, service topology, routine commands, data/secret handling and safe stopping.
- Added targeted troubleshooting for Docker availability/resources, occupied ports, unhealthy dependencies, stale secrets, migrations, readiness, worker queues, RustFS and ARM64/AMD64 differences.
- Added a twelve-work-package S1 evidence checklist that distinguishes locally verified work from incomplete hosted/independent evidence.
- Updated the root README, v3 index and agent handover to route future developers and coding agents to the guide.

**Verified**

| Check | Result |
|---|---|
| Documented fast command | `make check` passed: 20 backend tests at 80% coverage plus web checks |
| Documented integration command | `make integration` passed: 6 real-service tests |
| Documented worker drill | Passed after forced active-worker replacement and same-task re-delivery |
| Python dependency audit after Boto3 | No known vulnerabilities found |
| Repository dependency/secret/configuration scan | 0 enforced HIGH/CRITICAL findings |
| RustFS image scan | 0 enforced HIGH/CRITICAL findings |
| Documentation formatting check | `git diff --check` passed at the slice checkpoint |
| Isolated clean-copy setup | `make setup` succeeded without reusing the repository virtual environment or JavaScript dependencies |
| Isolated clean-copy fast suite | `make check` passed: 20 backend tests at 80% coverage plus web checks |
| Isolated clean-copy Docker integration | Fresh named volumes and containers became healthy; all 6 real-service tests passed |

**Issue found and resolved during the clean-copy rehearsal**

The clean PostgreSQL volume exposed a migration transaction defect that an already-initialized development volume had hidden. The advisory-lock query caused SQLAlchemy to open a transaction before Alembic opened its own migration transaction, so the new `alembic_version` table was rolled back when the connection closed even though Alembic reported success. Migration execution now commits the lock-acquisition transaction before Alembic begins, retains the PostgreSQL session-level lock across that commit, and commits the unlock query afterward. The stack was then destroyed with its synthetic rehearsal volumes and recreated from zero; readiness and all six integration tests passed.

**Remaining evidence**

- The GitHub workflows must pass on hosted native AMD64/ARM64 runners and produce the recorded SBOM/provenance evidence.
- The owner must authorize and record the intended baseline commit/tag before S1 can close.

## Next planned work

1. Present the completed S1 evidence to the owner and obtain approval before beginning S2.
2. After approval, begin S2 with the external auth-core contract verification defined in the sprint plan; do not implement authentication inside Vittavaan.

### 21 Sep 2026 — S1 hosted CI and baseline slice 11

**Status:** Verified; S1 is ready for owner completion review.

**Baseline**

- Branch: `develop`
- Foundation commit: `8fba18be1787c4e7cf8183d40651f58cfa2327c4`
- Passing hosted-evidence commit: `e8376e9a98c92ded2d4ac3b6c6439c50fbb9ae26`
- Quality workflow: <https://github.com/Yatish84/vittavaan/actions/runs/35620607835>
- Security and images workflow: <https://github.com/Yatish84/vittavaan/actions/runs/35620607828>

**Hosted evidence**

| Check | Result |
|---|---|
| Backend lint, strict types and tests | Passed on GitHub Ubuntu |
| Web lint, types, test, build and secret canary | Passed on GitHub Ubuntu |
| Compose contract | Passed after local-only secret bootstrap |
| Git history leaked-secret scan | Passed |
| Python and JavaScript dependency audits | Passed |
| Repository vulnerability/secret/configuration scan | Passed at the enforced HIGH/CRITICAL threshold |
| RustFS pinned-image scan | Passed at the enforced HIGH/CRITICAL threshold |
| API native AMD64 build and image scan | Passed |
| API native ARM64 build and image scan | Passed |
| Web native AMD64 build and image scan | Passed |
| Web native ARM64 build and image scan | Passed |
| SBOM and provenance generation | Passed for all four native image builds; build records retained as workflow artifacts |

**Issues found and resolved during the hosted run**

1. The web job called `uv` without installing it. The dependency-free canary script now uses the runner's `python3` directly.
2. Gitleaks correctly stopped the workflow, but the findings were two false positives for the literal phrase “S3-compatible”; wording was clarified without adding a scanner exception. A local repeat and the hosted Git-history scan then passed.
3. Trivy could not directly scan the attested OCI archive format. The workflow now retains the native attested OCI build and uses the same native build cache to load an equivalent image into the runner for vulnerability scanning. This keeps both provenance/SBOM evidence and image vulnerability enforcement.

The remaining gate is the owner's explicit acceptance of the S1 completion report and authorization to begin S2.

### 21 Sep 2026 — S2 contract and auth-core verifier slices 1–2

**Status:** Verified locally; S2 remains in progress.

**Owner direction**

The owner retained the original sprint plan and authorized S2. The separate demo-first proposal is not implementation authority.

**Implemented**

- Confirmed the existing auth-core Go `GET /verify` service as the revocation-aware identity boundary. Vittavaan does not implement passwords, OTPs, MFA, recovery, refresh tokens or token decoding.
- Added validated settings for the auth-core web/verifier locations, same-origin return URL, bounded verifier timeout and approved client types.
- Added an immutable domain identity that carries authentication facts but grants no household or wealth permissions.
- Added a strict, fail-closed HTTP adapter. It forwards a bearer token only to auth-core, disables redirects, accepts only the expected response structure and never stores or logs the token.
- Added a reusable protected-route dependency with safe, distinct HTTP 401 and 503 problem responses.
- Added local/Compose configuration seams. Deployment-specific URLs, issuer, audience and browser handoff remain staging decisions.

**Verified**

| Check | Result |
|---|---|
| Python lint | Passed |
| Python strict typing | Passed |
| Backend unit, architecture and OpenAPI contract tests | 32 passed; 82% aggregate coverage |
| Valid auth-core response mapping | Passed |
| Rejected token and unapproved client type | Safely returned unauthenticated behavior |
| Malformed verifier response and verifier outage | Failed closed; no protected access |
| Missing/wrong browser authorization scheme | Safe HTTP 401 with bearer challenge |
| Existing public OpenAPI contract | Unchanged and passed |

**Next**

Implement S2-03: the minimal local principal database record and idempotent persistence. This record links an auth-core subject to Vittavaan but does not duplicate credentials or grant household access.

### 22 Sep 2026 — S2 local principal and bootstrap API slices 3–4

**Status:** S2-03 complete locally; S2-04 back-end complete locally; S2 remains in progress.

**Implemented**

- Added migration `20260921_0002` for the minimal `app_principals` table exactly as specified in the database design: local UUID, unique auth subject, constrained principal type/status, first/last-seen and audit timestamps, and optimistic version.
- Added no email, phone, password, factor, token, session or household-permission columns.
- Added a PostgreSQL repository that creates at most one row per auth subject and safely updates `last_seen_at` on repeat entry.
- Added application rules that reject locally `SUSPENDED` or `CLOSED` principals even when auth-core verifies the caller.
- Added authenticated `GET /api/v1/bootstrap`. Until S3 creates person/household links, it returns empty permitted scopes and routes the user to `/account-setup`.
- Updated the deterministic OpenAPI contract with the protected bootstrap endpoint and bearer security scheme.

**Verified**

| Check | Result |
|---|---|
| Fast backend suite after API contract update | 37 passed; 83% aggregate coverage |
| Real PostgreSQL integration suite | 7 passed in Linux ARM64 Docker |
| Concurrent first entry for one synthetic auth subject | Exactly one row and one stable principal ID |
| Restricted application database account | Insert, update, select and cleanup passed without schema privileges |
| Suspended local principal with valid identity | HTTP 403 safe denial |
| First-run bootstrap response | Stable principal summary, empty scopes and `/account-setup` route |
| Migration/readiness head | `20260921_0002` |

**Important limit**

The browser handoff is not yet implemented. The S2-04 frontend client/states and all S2-05/S2-06 cross-service work remain open. No token transport workaround was introduced.

### 22 Sep 2026 — S2 frontend bootstrap states

**Status:** S2-04 complete locally; S2-05 requires a coordinated auth-core decision/change.

**Implemented**

- Added a typed frontend bootstrap client that accepts a token only as an in-memory argument, makes a no-cache same-origin request and rejects redirects.
- Added runtime response-shape validation so an unexpected or incomplete success response fails closed.
- Added accessible loading, first-run, ready, signed-out, denied and temporary-unavailable states, including a retry action only for temporary failures.
- Added a same-origin `/api` reverse proxy in the production web server and matching local Vite development proxy.
- Left the production shell safely signed out. It does not inspect URLs, `localStorage` or `sessionStorage` for an access token.

**Verified**

| Check | Result |
|---|---|
| Frontend lint and strict types | Passed |
| Frontend tests | 7 passed across 3 files |
| Production frontend build | Passed |
| First-run, 401, 403 and retry states | Passed |
| Request security options and response validation | Passed |

**Finding before S2-05**

The current auth-core web implementation writes `vittavaan.accessToken` to browser `sessionStorage` after login. That is an auth-core implementation fact, not an instruction to Vittavaan. It conflicts with the approved Vittavaan rule that access tokens must not be placed in persistent browser storage. S2-05 therefore needs an explicitly reviewed, coordinated handoff—recommended as a short-lived, single-use, state-bound exchange—before either repository is changed further.

### 22 Sep 2026 — Secure auth-core browser handoff

**Status:** S2-05 complete locally; S2-06 cross-service negative and outage cases remain.

**Implemented**

- Added a coordinated auth-core contract that converts a valid web session into a random 60-second, single-use code bound to an exact allow-listed return URL.
- Added a private server-to-server exchange protected by a separate client secret. Only the one-time code and browser state travel through the URL; the access token does not.
- Removed auth-core's access-token `sessionStorage` writes from direct and Google login completion.
- Added Vittavaan start and exchange endpoints, an `HttpOnly` state cookie, immediate URL cleanup and in-memory-only access-token handling.
- Added production safeguards that reject the documented local handoff secret and require HTTPS for public auth/return URLs.

**Verified**

| Check | Result |
|---|---|
| Auth-core focused backend checks | 11 handoff/API tests passed, including real Redis TTL and consume-once behavior |
| Auth-core focused frontend checks | 11 tests plus lint and strict types passed |
| Vittavaan focused backend checks | 18 tests passed after OpenAPI regeneration |
| Vittavaan frontend checks | 10 tests across 4 files plus lint, strict types and production build passed |
| Real two-stack login-to-bootstrap flow | `session_ready`, bootstrap HTTP 200, `first_run=true` |
| Reuse of consumed handoff code | Rejected with HTTP 400 |

**Integration finding and correction**

The first real cross-service run exposed a case-sensitive contract mismatch: auth-core correctly emits client type `WEB`, while Vittavaan had initially allowed lowercase `web`. Vittavaan failed closed with HTTP 401. Its default and deployment configuration were corrected to `WEB`, after which the complete flow passed. This is retained as regression coverage and operational evidence.

### 22 Sep 2026 — India-first subtype attribute schema baseline

**Status:** Logical field composition complete; owner/domain/legal review and machine-readable schema generation remain.

**Documented**

- Defined the exact permitted `subtype_attributes` composition for all 93 planned asset class/subtype pairs and all 13 liability subtypes.
- Classified fields as required, conditional, optional, derived and/or sensitive, with precise logical types and cross-field rules.
- Kept ownership, valuations, cost basis, transactions, income, documents, restrictions, liability balances, schedules, collateral and calculations in their normalized tables rather than duplicating them in subtype JSON.
- Added India-specific identifiers and product details for demat/ISIN securities, Indian bank/deposit products, mutual funds/PMS/AIF, EPF/PPF/NPS/SSY/SCSS/APY/gratuity/annuities, RERA property, VDA/crypto, GST input credit and Indian loan/dues categories.
- Recorded current official-source families from SEBI, RBI, NSDL, India Post, PFRDA, EPFO, Ministry of Labour, MoHUA/RERA, IRDAI, FIU-IND, Income Tax and GST. These remain time-sensitive and require revalidation at implementation and legal-release gates.

**Verified**

| Check | Result |
|---|---|
| Asset catalogue coverage | 93 of 93 subtype pairs have a matching schema entry |
| Liability catalogue coverage | 13 of 13 liability subtypes have a matching schema entry |
| Markdown integrity | Code fences balanced and `git diff --check` clean |
| Schema boundary | Current value, balance, ownership and derived metrics remain outside unrestricted subtype JSON |

### 22 Sep 2026 — S2 cross-service failure and recovery verification

**Status:** S2-06 complete locally; hosted checks and shared-staging configuration remain.

**Implemented**

- Expanded auth-core's real Go verifier tests to prove rejection of malformed, expired, wrong-issuer, wrong-audience, unknown-key and wrong-signature tokens in addition to its existing revocation coverage.
- Expanded Vittavaan adapter tests to prove that connection errors, timeouts and upstream server errors fail closed, and that a later request succeeds after a temporary outage.
- Added explicit handoff-exchange outage coverage so an unavailable auth API cannot yield an application session.

**Verified**

| Check | Result |
|---|---|
| Auth-core Go verifier suite | Passed with valid, malformed, expired, wrong issuer/audience/key/signature and revoked cases |
| Vittavaan focused authentication/bootstrap suite | 19 passed |
| Real verifier outage | Protected bootstrap returned safe HTTP 503 with no access |
| Real verifier recovery | Verifier became healthy and the same invalid credential returned normal HTTP 401 |
| Data impact | No database or user data was stopped, deleted or changed by the drill |

**Remaining release evidence**

- Run the S2 commits through hosted quality and security workflows.
- Provision and record the shared-staging HTTPS URLs, return origin, verifier placement, issuer, audience and independently managed handoff secret before claiming staging readiness.
