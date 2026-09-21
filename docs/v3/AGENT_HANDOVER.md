# Vittavaan v3 — Agent Handover

> **Last updated:** 21 Sep 2026
> **Current phase:** S1 Repository Foundation implementation
> **Application code status:** Foundation implemented; wealth-management features have not started
> **Canonical documentation:** `docs/v3/`
> **Baseline approval:** Owner approved `DEC3-001`–`DEC3-007` on 20 Sep 2026; S1 foundation is authorized.
> **S1 setup approval:** Owner approved the recommended branch, GitHub CI/registry, platform, package-manager, Valkey candidate, storage compatible with the S3 API and review defaults on 20 Sep 2026.

## Mission

Implement Vittavaan from the approved, professional OOSE/OOP-oriented v3 specification while keeping the documentation, decisions, implementation evidence and next actions synchronized. Preserve traceability across product intent, actors, use cases, requirements, analysis, system/object design, delivery, testing and operations. All documentation diagrams use Mermaid.

## New agent: start here

This file is the canonical continuation guide. A replacement coding agent should not restart discovery or infer the next task from chat history. Use this sequence:

1. Read this file completely.
2. Read `README.md`, `05_Delivery/03_Sprint_and_Milestone_Plan.md`, `05_Delivery/04_S1_Repository_Foundation_Backlog.md` and `05_Delivery/05_Implementation_and_Verification_Log.md`.
3. Run `git status --short`. The working tree contains intentional, uncommitted owner/agent work; do not discard, reset, overwrite or broadly reformat it.
4. Run `make check`, followed by `make integration`, before changing the foundation. Both are expected to pass at this checkpoint.
5. Resume at **Exact next implementation sequence** below. Do not start S2 or wealth features until the S1 completion gate is met and the owner approves moving forward.
6. After every meaningful slice, update the implementation log, progress tracker and this handover with the date, actual evidence, known limitations and exact next action.

### Known-good local commands

| Purpose | Command | Expected result at handover |
|---|---|---|
| Prepare local-only secrets | `./scripts/bootstrap-local.sh` | Files created/refreshed under ignored `runtime/secrets/` |
| Fast quality checks | `make check` | 20 backend tests, 80% line coverage, web lint/type/test pass |
| Full container/integration check | `make integration` | Stack healthy and 6 integration tests pass |
| Forced worker recovery drill | `make recovery-drill` | Active synthetic task is re-delivered and completes after worker replacement |
| Start the local application | `make up` | Web/API/worker/PostgreSQL/Valkey healthy after bootstrap/migration |
| Stop containers, retain data | `make down` | Containers/networks removed; images and named data volume retained |
| Validate Compose model | `docker compose -f compose.yaml -f compose.local.yaml config --quiet` | No output and exit status 0 |
| Check patch formatting | `git diff --check` | No output and exit status 0 |

Do not place credentials in documentation, Git, command output copied into logs or frontend configuration. Do not run a destructive database reset merely to obtain a clean test; the integration suite is designed to be repeatable.

## Why v3 exists

The v2 documents contain substantial useful work but were based on an older 19-screen wireframe set and incorrectly planned a Supabase authentication subsystem. The current source has 25 wireframe HTML files, richer household/verification/marketplace/estate behavior, and a working sibling repository at `../auth-core`.

v1 and v2 must remain untouched as historical references. Do not move, delete or “clean up” the user’s current wireframe changes.

## Confirmed owner decisions

1. Preserve v1/v2 and create a canonical `docs/v3`.
2. Plan the full vision in phases.
3. First beta: wealth foundation only.
4. Initial ingestion: manual entry plus controlled imports; live financial connectors later.
5. Main app and auth-core remain separately deployable.
6. Auth-core owns all authentication and session behavior.
7. Initial ownership model is people, not HUF/trust/company entities.
8. Joint asset: one holding plus multiple person ownership allocations totalling 100%.
9. Design envelope: 100,000 registered users and 10,000 concurrent sessions.
10. Every asset/liability in the operator PDF is recordable.
11. Priority-1 assets receive rich models; long-tail types use extensible subtype attributes initially.
12. The PDF is a coverage catalogue, not a list of products Vittavaan sells or intermediates.
13. Counsel/vendor-dependent capabilities are feature-gated and disabled by default.
14. All diagrams must be Mermaid.
15. Initial shared staging targets an OCI Ampere A1 Always Free-eligible VM, sized to the lower documented 2 OCPU/12 GB allowance unless the tenancy console confirms more; it is not accepted as HA or final performance evidence.
16. The owner approved the v3 baseline, foundation-only S1 scope, technology stack, separate auth-core boundary, OCI staging direction, AWS Mumbai production direction and protected delivery workflow on 20 Sep 2026.
17. S1 defaults are `main`/`develop`, GitHub Actions/GHCR, macOS ARM64 plus Linux AMD64 CI/WSL2, `uv`, `pnpm`/Corepack, Valkey candidate, local object storage using the S3 API and protected checks; compatibility/licence checks still precede final Valkey/object-store locks.

## Sources reviewed

- All Markdown documentation under `docs/v1/` and `docs/v2/` was inventoried; v2 handover and relevant requirements/design sections were read closely.
- All 25 current files in `docs/v2/Wireframe/` were inventoried and their visible structure/headings extracted.
- The full text of `User Story.dc.html`, `User Flow.dc.html` and `Schema.dc.html` was reviewed for invariants, states and open decisions.
- Both pages of `docs/v2/Wireframe/uploads/Wealth Monitoring - Asset Classes - Operator.pdf` were extracted and visually inspected.
- `../auth-core/AGENTS.md`, README, client reuse strategy, session/token foundation, security architecture and OpenAPI/JWKS boundaries were inspected.

## Work completed in v3

| File | Content |
|---|---|
| `README.md` | Canonical index, purpose, document architecture, invariant rules and traceability chain. |
| `00_Governance/01_Documentation_Governance.md` | Source precedence, ADR summary, document states and review gates. |
| `00_Governance/02_Wireframe_Coverage_Matrix.md` | All 25 files categorized; first-beta tabs and deferred gates mapped. |
| `00_Governance/03_Progress_Tracker.md` | Current workstream status and dependencies. |
| `01_Requirements/01_Product_Scope_and_Release_Boundaries.md` | Beta scope, exclusions, actors, verification capability model, scale envelope and gate contract. |
| `01_Requirements/02_Actors_and_System_Boundary.md` | Human/system actors, authority distinctions, trust boundaries and beta actor-use-case matrix. |
| `01_Requirements/03_Functional_Requirements.md` | Stable FR3 requirement families for beta and gated future capabilities. |
| `01_Requirements/04_Non_Functional_Requirements.md` | Measurable SLOs and non-functional requirements for scale, correctness, security, privacy, accessibility and operations. |
| `01_Requirements/05_Use_Cases.md` | Fifteen Cockburn-style beta use cases with alternate/error flows and wireframe/requirement links. |
| `01_Requirements/06_Legal_and_Approval_Register.md` | Disabled-by-default legal/vendor approval gates and evidence template. |
| `02_Analysis/01_Asset_and_Liability_Coverage.md` | Universal holding contract, complete catalogue treatment, rich P1 models, long-tail types and all liability classes. |
| `02_Analysis/02_Domain_Glossary.md` | Canonical domain terminology and explicitly rejected ambiguous terms. |
| `02_Analysis/03_ECB_Object_Model.md` | Entity–Boundary–Control modules, aggregate roots, controls, boundaries and dependency rules. |
| `02_Analysis/04_Sequence_and_State_Diagrams.md` | Mermaid sequences for core workflows and lifecycle state machines. |
| `02_Analysis/05_Requirements_to_Domain_Coverage.md` | Requirement-family/surface coverage and analysis gaps carried to design. |
| `02_Analysis/06_Asset_and_Liability_Field_Dictionary.md` | Universal fields, reusable profile schemas, complete operator-catalogue seed mapping, liability subtype contracts and conditional validation rules. |
| `03_System_Design/01_Auth_Core_Integration.md` | Authentication boundary, sequence, claim validation, authorization order, failure and lifecycle behavior. |
| `03_System_Design/02_Architecture_Overview.md` | Modular-monolith topology, modules, fact/projection paths, environments, scaling and failure boundaries. |
| `03_System_Design/03_Database_Design.md` | Implementation-level PostgreSQL design for 50 tables: purpose, every planned column, PK/FK/UQ/CHK role, type, nullability/default, direct-relationship Mermaid per table, indexes, integrity, migrations and retention. |
| `03_System_Design/04_API_Design.md` | OpenAPI conventions, error model, endpoint inventory, projection envelope, idempotency and compatibility. |
| `03_System_Design/05_Events_Jobs_and_Projections.md` | Outbox/event guarantees, job catalogue, retries, read projections and cache policy. |
| `03_System_Design/06_Imports_and_Reconciliation.md` | Staging, matching, commit semantics, error classes and connector adapter boundary. |
| `03_System_Design/07_Data_Room_Architecture.md` | Document/object model, quarantine/scan, authorization, lifecycle and retention. |
| `03_System_Design/08_Security_and_Threat_Model.md` | Protected assets, major threats/controls, authorization flow and verification requirements. |
| `03_System_Design/09_Observability_and_Operations_Design.md` | Telemetry signals, SLO/error-budget monitoring, runbooks and release operations. |
| `03_System_Design/10_Phase3_Coverage_Audit.md` | Cross-artifact reconciliation and decisions carried into object design. |
| `03_System_Design/11_Catalogue_Seeds_Validation_and_Indexes.md` | Deterministic seed/version contract, validation layers, JSONB promotion rules, constraints, indexes, API and test evidence. |
| `04_Object_Design/01_Shared_Types_and_Interfaces.md` | Typed value/provenance contracts and control, engine, repository and adapter protocols. |
| `04_Object_Design/02_Calculation_Contracts.md` | Financial formulas, rounding/reconciliation, preconditions and named failure vocabulary. |
| `04_Object_Design/03_Domain_Algorithms.md` | Effective ownership, valuation selection, corrections, projections, imports, verification and permissions. |
| `04_Object_Design/04_Design_Patterns_and_Object_Decisions.md` | Selected patterns, aggregate boundaries, dependency direction and rejected shortcuts. |
| `04_Object_Design/05_Phase4_Coverage_Audit.md` | Phase 3-to-object-design reconciliation and remaining delivery/test work. |
| `05_Delivery/01_Implementation_Roadmap.md` | Documentation sequence, implementation milestones and quality gates. |
| `05_Delivery/02_Project_Structure_and_Standards.md` | Planned monorepo, dependency rules and backend/frontend/API/migration/review standards. |
| `05_Delivery/03_Sprint_and_Milestone_Plan.md` | S0–S12 staged outcomes, readiness/done definitions and release gates. |
| `05_Delivery/04_S1_Repository_Foundation_Backlog.md` | Twelve foundation work packages with dependencies, tasks, acceptance criteria, evidence, execution slices, toolchain lock policy and kickoff decisions. |
| `05_Delivery/05_Implementation_and_Verification_Log.md` | Dated, detailed record of implementation changes, commands/checks, results, limitations and next work. |
| `05_Delivery/06_Developer_Onboarding_and_Troubleshooting.md` | Plain-English setup, routine commands, safe recovery, platform differences, common failures and S1 work-package evidence checklist. |
| `06_Testing/*` | Test pyramid, synthetic personas, golden scenarios and security/performance/recovery plans. |
| `07_Operations/*` | OCI Always Free staging with local Compose portability and immutable ARM64 deployment; AWS India production infrastructure, CI/CD/release management and incident runbooks. |
| `07_Operations/04_Local_to_OCI_Deployment_Specification.md` | Planned Compose overlays/services, multi-architecture image contract, 2-OCPU/12-GB resource budget, storage, OCI Terraform inventory, networking, secrets, auth-core, release manifest, rollback/recovery and free-tier controls. |
| `07_Operations/05_OCI_Staging_Deployment_Runbook.md` | Operator-ready lifecycle for OCI provision/bootstrap/deploy/smoke/rollback/backup/restore/rebuild/exit/retirement, with evidence requirements. |
| `00_Governance/04_Traceability_Matrix.md` | Beta capability and global quality traceability through sprint/test evidence. |
| `00_Governance/05_End_to_End_Consistency_Audit.md` | Resolved contradictions and remaining approvals. |
| `00_Governance/06_Owner_Review_and_Decision_Checklist.md` | Prioritized owner decisions: baseline/S1 blockers, sprint gates, release approvals and recommended positions. |

Foundation code now exists. It deliberately contains no portfolio, household, holding, liability, financial-calculation or Vittavaan authentication workflow.

## Critical product interpretation

### Assets and liabilities page

All embedded tabs/states are in beta scope: Net worth, Assets, Liabilities, Cash flow, Data room, Consents, Holding, First run and Account setup. Consents/account setup are designed now, but real financial connectors remain gated.

### Asset catalogue

Every asset in the PDF must be addable and visible in portfolio/net-worth/liquidity/provenance views. “Priority to build” controls rich modelling order only. Do not accidentally omit exotic assets or treat the regulator/licence/cost columns as confirmed obligations.

### Ownership

Although `Schema.dc.html` proposes a generic legal `Entity`, the owner selected a person-only initial model. Preserve a migration seam for legal entities, but do not reintroduce HUF/trust/company ownership into beta. Store a jointly owned holding once and attribute through effective-dated ownership allocations.

### Authentication

Do not create login, signup, password, OTP, MFA, recovery, refresh, session-management or Supabase-auth features in Vittavaan. Consume auth-core RS256/JWKS and revocation-aware identity context. Auth-core workspace roles do not automatically authorize household financial access.

## Current implementation checkpoint

S1 Repository Foundation began on 20 Sep 2026. The repository root now contains pinned Python and Node toolchains, lockfiles, a minimal React web shell, a layered FastAPI package, Celery worker foundation, PostgreSQL and Valkey services, Compose local/staging overlays, an Alembic baseline, local-only secret bootstrap and GitHub quality checks.

Verified evidence from the first slice:

- backend lint, strict typing and three unit tests pass;
- frontend lint, typing, unit test and production build pass;
- all five local services (`web`, `api`, `worker`, `postgres`, `valkey`) build and become healthy;
- `/health/live` and `/health/ready` respond successfully;
- the web shell is served on port 5173;
- baseline migration `20260920_0001` applies successfully to PostgreSQL.
- backend architecture direction, safe problem responses and deterministic OpenAPI drift checks pass; the foundation suite now has seven Python tests plus one web test.
- automatic migration ordering and real-service integration checks pass: three Docker tests cover PostgreSQL/head/repeat migrations, isolated Valkey operations and duplicate synthetic Celery delivery; persistence and API 503/recovery behavior were also manually verified.
- JSON request logs, caller correlation/causation propagation, bounded Prometheus metrics, local in-memory OpenTelemetry spans and recursive secret redaction pass. Fake-secret scans cover public build artifacts and runtime surfaces; overall backend coverage is 81%.
- concurrent migrations serialize through a PostgreSQL advisory lock; bounded Celery failure/retry settings, worker timing logs and PostgreSQL/Valkey readiness gauges pass. A deliberate Valkey outage/recovery and post-recovery task passed, and a discovered cross-task tracing carryover defect was fixed. Backend coverage is 84%.
- separate non-administrative migration and application database accounts are active. The application account is denied table creation, the migration account owns Alembic state, and four real-service integration tests pass.
- the local Python/JavaScript dependency audits, repository scan, API image scan and web image scan have no findings at the enforced HIGH/CRITICAL threshold after remediation. The web image runs as UID/GID 101, and native ARM64 API/web builds pass.
- `.github/workflows/security-and-images.yml` defines leaked-secret scanning, dependency scans, native GitHub ARM64/AMD64 image builds, image scanning, SBOM and provenance. It has not run on GitHub yet, so native AMD64 and hosted-CI evidence remain pending. Local QEMU AMD64 emulation is unsuitable because `uv` segfaulted under emulation.
- database-pool, worker-queue depth/oldest-age and cross-process worker completion/runtime metrics are exported with bounded labels. Workers share only predefined aggregate counters through an expiring Valkey hash; no task IDs, arguments or business values are stored. `make recovery-drill` force-kills the worker during a synthetic task and proves the same task is re-delivered and completed after restart. Fast checks cover 20 backend tests at 80% coverage, and 6 real-service integration tests pass.
- digest-pinned RustFS 1.0.0 provides the private local S3-compatible service. It is Apache-2.0, non-root UID/GID 10001, ARM64/AMD64 and passed the HIGH/CRITICAL image scan. The sixth integration test proves authenticated create/upload/download/delete cleanup. SeaweedFS 4.47 was rejected after a functional pass because Trivy found fixable HIGH `CVE-2026-84445`; do not reintroduce it without a patched, rescanned release.
- the onboarding path was repeated in an isolated repository copy without `.git`, existing language dependencies, runtime secrets, caches, containers or data volumes. It exposed and fixed an Alembic/advisory-lock transaction bug that rolled back the version marker only on a truly new database. A second from-zero run passed `make setup`, `make check` and all six integration tests.

This is foundation only. Do not describe it as working wealth-management functionality and do not add authentication features owned by auth-core.

## Next work, in order

1. Continue the twelve-package S1 backlog from the verified foundation slice; do not implement product features early.
2. Push/trigger the GitHub workflows and retain the first native AMD64/ARM64 build and hosted security-scan evidence; do not mark it verified merely because the workflow file exists.
3. Preserve the completed clean-copy onboarding rehearsal and final evidence mapping, then record the baseline commit/tag when approved changes are committed.
4. Add element-level wireframe trace IDs during each owning sprint; do not delay S1 for purely presentational trace granularity.
5. Resolve Sections B-E by their stated sprint/release gates, especially auth-core values, catalogue approval, retention, OCI limits and RPO/RTO.

## Exact next implementation sequence

This is the executable queue for the next coding agent. Work from the top and stop at any owner decision or external-access boundary instead of silently bypassing it.

### Next 1 — Obtain hosted GitHub evidence

**Goal:** prove the already-defined workflows on real GitHub Intel and ARM machines.

1. Inspect `.github/workflows/quality.yml` and `.github/workflows/security-and-images.yml`; do not redesign them without a demonstrated failure.
2. If the owner has authorized committing and pushing, create a narrowly scoped commit that preserves all intentional work, push it to the agreed branch and observe both workflows. If push/commit authorization is absent, report that this external step is awaiting owner approval and continue only with independent local tasks.
3. Capture the workflow URL, commit SHA, job conclusions and image-build platforms in `05_Delivery/05_Implementation_and_Verification_Log.md`.
4. Fix reproducible application/workflow failures and rerun. Do not hide or waive a failed security finding. Document infrastructure/transient failures separately.

**Done when:** quality and security workflows pass on GitHub; API and web build natively for Linux AMD64 and ARM64; dependency, secret, filesystem and built-image scans pass; SBOM/provenance generation is evidenced. A workflow file existing locally is not completion evidence.

### Next 2 — Complete remaining reliability/capacity evidence

**Goal:** close the worker and runtime-observability gaps already identified in S1.

1. Preserve the completed database-pool, queue depth/oldest-age and cross-process worker completion/runtime metrics and their label-rejection tests.
2. Preserve the worker aggregate boundary: predefined task aliases/outcomes/buckets only, a 24-hour expiry, and no task IDs, correlation IDs, arguments, users, resources or financial values.
3. Preserve `make recovery-drill`: it uses a recovery-only five-second visibility timeout, force-kills an active worker, and has passed re-delivery of the same task ID. Normal runtime must retain its one-hour timeout.
4. This reliability/capacity item is complete. Continue with **Next 3 — Complete S3-compatible local object storage**.

**Done when:** metrics and tests pass, deliberate interruption/re-delivery is demonstrated, `make check` and `make integration` remain green, and evidence is recorded.

### Next 3 — Complete S3-compatible local object storage (complete)

**Goal:** satisfy `S1-FND-007` without implementing the future Data Room feature.

Completed with RustFS 1.0.0. Preserve the digest pin, non-root execution, private network, secret files and isolated cleanup test. Keep real document upload, metadata tables, malware processing and business authorization out of S1. OCI/AWS use the portable S3 boundary; do not assume every vendor-specific S3 extension is supported.

**Done when:** clean local startup is healthy on ARM64, the isolated S3-compatible probe passes and cleans up after itself, no object-store secret is exposed, and the Compose contract remains suitable for OCI staging.

### Next 4 — Finish developer onboarding and S1 evidence

**Goal:** allow a new developer—not only the authoring agent—to reproduce the foundation.

1. Preserve the twelve-package status/evidence checklist in `05_Delivery/06_Developer_Onboarding_and_Troubleshooting.md`; only toolchain/hosted CI remains explicitly in progress.
2. The root README and detailed onboarding guide now cover prerequisites, first setup, start/stop, tests, logs, safe recovery, external auth and common Docker/database/Valkey/worker/object-store/platform failures.
3. The equivalent clean-environment rehearsal is complete: a repository copy excluding `.git`, `.venv`, `node_modules`, runtime secrets and caches passed `make setup`, `make check` and a fresh-volume `make integration`. Preserve this evidence.
4. Obtain the hosted GitHub CI evidence described in Next 1.
5. Reconcile the final trace/evidence index, progress tracker, implementation log and this handover; then present the S1 completion report to the owner.

**Done when:** every S1 acceptance criterion is either evidenced or explicitly open, all required checks pass, and the owner can review a concise S1 completion report. The clean-environment criterion is satisfied; do not declare S1 complete while hosted CI or another mandatory criterion is pending.

### After S1 owner approval

Begin S2 exactly as defined in `05_Delivery/03_Sprint_and_Milestone_Plan.md`. S2 integrates the existing external auth-core contract; it does not create Vittavaan login, password, OTP, MFA, token-refresh or recovery features. Reconfirm auth-core issuer, audience, JWKS/revocation topology and redirect origins before implementation.

## Resolved v2 contradictions to preserve during implementation

- Shared holdings and effective-dated person ownership allocations replace user-owned portfolio rows.
- Append-only valuation facts with provenance replace a mutable current-value field.
- Four evidence/capability levels replace ambiguous verification badges.
- Beta presents manual/import sources honestly and gates unavailable live connectors.
- auth-core replaces Supabase Auth and local authentication/session tables.
- v3 adds imports, reconciliation, income, commitments, grants, document supersession, projections and audit boundaries missing from v2.
- Retention, anonymization and legal holds reconcile durable records with privacy erasure.
- Counsel/vendor-dependent wireframes remain disabled behind recorded gates.
- The 100,000-user/10,000-concurrent-session envelope supersedes v2’s smaller target.

## Working rules for the next agent

- Read this file and `docs/v3/README.md` first.
- Inspect the exact wireframe before specifying a screen; do not rely only on filenames.
- Preserve user changes outside `docs/v3`; the worktree was already dirty when v3 began.
- Use integer minor units plus currency for money and fixed-precision decimals for rates/percentages.
- Never allow a generic attribute bag to bypass ownership, provenance, access or audit invariants.
- Treat legal statements as requiring jurisdiction/effective-date/source/review metadata.
- Add Mermaid diagrams where relationships or state transitions materially improve clarity.
- Update the implementation log, progress tracker and this handover after every completed implementation slice; update the README whenever operator/developer instructions change.
- Implement only the currently approved sprint. Do not begin S2 or wealth-management features until the S1 completion gate and owner approval are recorded.

## Repository state warning

The repository currently contains extensive intentional, uncommitted documentation and S1 foundation work. Historical wireframe moves/replacements and any unrelated owner changes must be treated as owner-owned. Inspect paths before staging; do not revert, discard, reset or broadly rewrite existing work. Record an exact baseline commit only after the owner authorizes committing the intended scope.
