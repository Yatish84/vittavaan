# v3 Progress Tracker

> Updated: 22 Sep 2026

> Baseline: Owner approved `DEC3-001` through `DEC3-007` on 20 Sep 2026. S0 and S1 are complete. On 21 Sep 2026 the owner retained the original sprint plan and authorized S2 Authentication and Application Bootstrap. Wealth-feature implementation has not started.

## Documentation rebuild

| Workstream | Status | Evidence / next action |
|---|---|---|
| Source inventory | Complete | 25 current wireframes, v1/v2 docs, operator PDF and sibling auth-core inspected. |
| Governance and source precedence | Draft | Reconcile after the first complete cross-document pass. |
| Wireframe coverage matrix | Draft | Add element-level IDs and route/state acceptance mapping. |
| Product scope/release boundaries | Draft | Convert to stable requirement IDs. |
| Asset/liability catalogue | Draft | Complete PDF subtype contracts and seed mapping added. The colleague JSON was reviewed as a field-template reference without narrowing the larger catalogue; finalize the documented owner/legal/valuation-policy decisions. |
| Subtype field dictionary | Draft | Universal fields, reusable profiles, complete asset seeds, all 13 PDF liability contracts, conditional rules and a field-capture/form-family crosswalk for the colleague JSON are documented. |
| India subtype schemas | Draft | Exact permitted attribute composition is documented for all 93 asset and 13 liability subtypes, including data types, required/conditional/optional markers, sensitivity, normalized destinations, India-specific identifiers and official-source baseline. Next: owner/domain review, machine-readable JSON Schema and UI-hint generation. |
| Catalogue seeds/constraints | Draft | Deterministic seed package, schema versioning, persistence rules, database constraints, index matrix, API behavior and verification evidence specified. |
| Auth-core integration | Draft | Confirm audience, redirect and deployment-specific values during implementation planning. |
| Actors and system boundary | Draft | Formal actor distinctions, authority matrix and trust boundaries added. |
| Functional requirements | Draft | Stable FR3 families added; next map them to detailed use cases and API/schema contracts. |
| Non-functional requirements/SLOs | Draft | Measurable performance, scale, reliability, security, privacy, finance, UX and operations requirements added. |
| Detailed use cases | Draft | Fifteen beta use cases now cover auth, household, holdings, imports, valuations, ledger, documents, wealth, analysis, planning, export/closure, grants, source consent, liabilities and preferences. |
| Legal and approval register | Draft | Twelve product gates and cross-cutting review topics recorded; all gated features default disabled. |
| Domain glossary | Draft | Canonical identity, ownership, valuation, ledger, planning and operational terms added. |
| ECB/domain analysis | Draft | Entities, aggregate roots, controls, boundaries and prohibited dependencies documented. |
| Sequence/state analysis | Draft | Core beta sequences and six lifecycle state machines added in Mermaid. |
| Requirements/domain coverage | Draft | All beta requirement families have entity/control/boundary homes; ten system-design gaps carried forward. |
| Architecture overview | Draft | Modular-monolith boundaries, deployment topology, write/read paths, scaling and degradation behavior added. |
| API contracts | Draft | v1 conventions, errors, endpoint surface, projection envelopes, idempotency and evolution added. |
| Database design | Draft | Expanded to a 50-table implementation dictionary; subtype schema versions, append-only balances, source consent and the asset/liability field-template storage mapping cover the detailed field contracts. Physical DDL awaits the listed implementation decisions. |
| Events/jobs/projections | Draft | Outbox guarantees, events, jobs, retries, projection invalidation and cache rules added. |
| Imports/reconciliation | Draft | Staging, normalized proposals, matching, chunk commit and future adapter behavior added. |
| Data room | Draft | Quarantine, scanning, object security, links, lifecycle and retention added. |
| Security/threat model | Draft | Assets, threats, controls, authorization decision and verification programme added. |
| Observability/operations | Draft | Telemetry, SLO signals, runbooks and release workflow added. |
| Phase 3 coverage audit | Draft | Runtime, persistence, API, events and specialized-design coverage reconciled. |
| Shared object interfaces | Draft | Domain types, control/engine/repository/adapter protocols and exception mapping added. |
| Calculation contracts | Draft | Wealth, movement, cash flow, debt, performance, planning and FX contracts added. |
| Domain algorithms | Draft | Ownership, valuation, corrections, projections, imports, verification and filtering algorithms added. |
| Design patterns | Draft | Ports/adapters, UoW, policies, outbox, CQRS-lite and aggregate decisions added. |
| Phase 4 coverage audit | Draft | Phase 3 decisions reconciled to object contracts; remaining test/delivery detail recorded. |
| Delivery structure/standards | Draft | Monorepo, dependency, language, API, migration and review standards added. |
| Sprint roadmap | Draft | S0–S12 outcomes mapped to trace families and release gates. |
| S1 implementation backlog | Complete | Eleven foundation slices are recorded. Local, clean-copy and hosted GitHub evidence pass, including native AMD64/ARM64 builds, scans, SBOM and provenance. Owner accepted the original plan and authorized progression to S2 on 21 Sep 2026. |
| S2 authentication/bootstrap | Review ready | S2-01 through S2-06 pass locally and Vittavaan hosted quality/security checks pass at commit `6f188b5`. A real two-stack test completed login, one-time handoff and first-run bootstrap; replay was denied. The verifier rejects malformed, expired, wrong-issuer, wrong-audience, unknown-key, wrong-signature and revoked tokens. A real outage returned a safe 503 and recovered to normal 401 behavior. Shared-staging values remain deployment inputs; owner completion review is next. |
| Testing and traceability | Draft | Test pyramid, personas, golden scenarios, security/load/recovery and end-to-end matrix added. |
| Operations/deployment | Draft | OCI Always Free single-VM staging, local/CI Compose parity, multi-architecture immutable deployment, safeguards and exit path added; AWS India remains the production and production-shaped performance target. |
| Local-to-OCI deployment specification | Draft | Compose topology/overlays, ARM64/AMD64 images, conservative resource/storage budgets, Terraform resources, network/TLS, configuration/secrets, auth-core, manifest, rollback, recovery and cost guardrails specified. |
| OCI staging runbook | Draft | Provision, bootstrap, DNS/TLS, secret install, deploy, preflight, smoke, rollback, failed migration, backup, isolated restore, VM loss, capacity, exit and retirement procedures specified. |
| End-to-end consistency | Review ready | Final trace audit completed; source consent gap closed, stale phase wording corrected and implementation/release dispositions recorded. |
| Owner decision checklist | Review required | S1 blockers and sprint/release decisions are prioritized with recommendations, due gates and required approval record. |

## Implementation status

S1 foundation is complete and S2 authentication/application bootstrap is **ready for owner completion review**. S2-01 through S2-06 pass, including the complete negative-token matrix, a real verifier outage/recovery drill and hosted quality/security checks. Deployment-specific shared-staging configuration remains an environment input and does not block reviewing the implemented sprint. On 20 Sep 2026 the first local foundation slice was built and verified: the web shell, API, worker, PostgreSQL and Valkey all became healthy through Docker Compose; both API health endpoints responded; the web page was served; and Alembic applied baseline revision `20260920_0001` to PostgreSQL. Backend and frontend lint, type, unit-test and build checks also pass locally.

The second verified slice added automatic backend layer-direction checks, a planted invalid-import proof, safe RFC 9457-style error responses, and deterministic OpenAPI generation/drift detection. The detailed commands, results and limitations are recorded in `05_Delivery/05_Implementation_and_Verification_Log.md`.

The third verified slice added automatic pre-start migrations, migration-head-aware readiness and real Docker integration tests for PostgreSQL, Valkey and duplicate synthetic worker tasks. Migration repeatability, named-volume persistence, safe HTTP 503 degradation and recovery to HTTP 200 were demonstrated. Data services remain on a private network.

The fourth verified slice added JSON request logs, correlation/causation propagation, bounded Prometheus metrics, local OpenTelemetry spans and recursive secret redaction. Fake-secret scans passed across settings, health, OpenAPI, traces, runtime logs and the built web output. Overall backend coverage reached 81%.

The fifth verified slice added concurrent-migration advisory locking, bounded worker failure settings, safe worker timing logs and PostgreSQL/Valkey readiness gauges. A deliberate Valkey outage produced HTTP 503 and a zero readiness gauge; the worker reconnected and completed a post-recovery task. Cross-task trace-context carryover found during the drill was corrected. Backend coverage is now 84%.

The sixth verified slice separated the database-structure migration account from the everyday application account. Both accounts are non-administrative; integration evidence proves the application account cannot create tables while the migration account can. The real-service suite now has four passing checks.

The seventh slice added dependency, leaked-secret, repository and container-image security checks plus native ARM64/AMD64 GitHub build jobs. Local dependency and image scans are clean at the enforced HIGH/CRITICAL threshold, the web image now runs as a restricted user, and native ARM64 builds pass. The hosted GitHub run is still required before native AMD64 and hosted security evidence can be marked verified.

The eighth slice added bounded database-pool, worker-queue and cross-process worker completion/runtime measurements plus a repeatable worker interruption drill. A synthetic active task survived a force-killed worker through broker re-delivery and completed after restart. Its aggregate success/runtime metrics remained visible through the API endpoint. Five real-service integration tests and 20 fast backend tests pass.

The ninth slice selected digest-pinned RustFS 1.0.0 for local S3-compatible testing after rejecting a functionally successful SeaweedFS candidate that failed the HIGH vulnerability gate. RustFS is Apache-2.0, non-root, ARM64/AMD64 and scan-clean at the enforced threshold. A signed create/upload/download/delete integration probe passes; the real-service suite now has six tests.

The tenth slice added the plain-English onboarding/troubleshooting guide and rehearsed it in an isolated repository copy with fresh language dependencies, containers and data volumes. That rehearsal found that the advisory-lock transaction could roll back Alembic's version marker on a truly empty database; the migration transaction boundary was corrected and a second from-zero run passed all setup, fast and six real-service integration checks.

The eleventh slice created and pushed the owner-authorized `develop` baseline. After correcting three workflow integration defects without weakening a gate, the hosted quality and security workflows passed. API and web images built and scanned natively on Linux AMD64 and ARM64, with SBOM/provenance build records retained. S1 is ready for owner completion review; S2 has not started.

No wealth-management feature has been implemented. There are no portfolio, asset, liability, household or local-authentication workflows yet. Those remain assigned to later sprints under the approved scope and auth-core boundary.

## Known review dependencies

| Dependency | Effect |
|---|---|
| Legal view on advisor marketplace, credit auction and escrow | Production gates remain disabled. |
| CA/advocate review of tax, gift and succession rules | Calculations cannot be represented as legally approved. |
| Connector/vendor contracts | Live import sources cannot be promised or activated. |
| Benchmark/news licensing | Licensed data cannot appear in production analysis. |
| Auth-core integration values | Issuer, audience, redirect origins and verifier topology require environment configuration. |
