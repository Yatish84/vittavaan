# Sprint and Milestone Plan

## Cadence

Two-week iterations are assumed for planning; scope is accepted by outcome rather than date. Each milestone is independently deployable to staging and closes only with traceability and evidence.

## Sprint overview

| Sprint | Plain-English outcome | Primary trace families |
|---|---|---|
| S0 — Documentation approval | Agree what will be built, what will not be built yet and which decisions need specialist approval. | All |
| S1 — Repository foundation | Establish the secure, repeatable technical base on which the application will be built. | NFR3-MAINT/OPS/SEC |
| S2 — Auth/bootstrap | Allow Vittavaan to recognize a user authenticated by auth-core and handle first entry safely. | UC3-IAM-001, FR3-IAM |
| S3 — Household/access | Allow users to create and manage households, people, membership and access permissions. | UC3-HH-001, UC3-GRANT-001, FR3-HH |
| S4 — Holding catalogue | Allow users to record assets and ownership details manually. | UC3-HOLD-001, FR3-HOLD |
| S5 — Imports | Allow supported financial data to be uploaded, checked and committed safely. | UC3-IMPORT-001, FR3-IMPORT |
| S6 — Valuation/ledger/liability | Record changing values, transactions, income and debts accurately over time. | UC3-VAL/LEDGER, FR3-LEDGER |
| S7 — Data Room | Store and retrieve supporting documents securely. | UC3-DOC-001, FR3-DOC |
| S8 — Wealth views | Assemble the underlying data into the complete Net Worth, Assets and Liabilities experience. | UC3-WEALTH-001, FR3-WEALTH |
| S9 — Analysis | Explain performance, gains, losses, risk and contributing factors. | UC3-AN-001, FR3-AN |
| S10 — Planning/settings | Add goals, scenarios, preferences and notification controls. | UC3-PLAN-001, FR3-PLAN/SET |
| S11 — Privacy/reliability | Add data export/closure, retention and operational recovery behavior. | UC3-SET-001, NFR3-PRIV/REL |
| S12 — Beta hardening | Verify that the complete beta is secure, accessible, resilient and ready for controlled users. | All beta traces |

## Detailed sprint plan

### S0 — Documentation approval — COMPLETE 20 Sep 2026

**Description:** Establish a single agreed specification before implementation begins.

**What will be implemented:** No application feature code. The work reconciles the current wireframes, asset catalogue, requirements, use cases, architecture, database design, delivery plan, legal gates and auth-core boundary.

**Desired outputs**

- **Back-end:** Approved domain, database, API, event, security, scale and operational designs for future implementation.
- **Front-end:** Approved wireframe coverage and screen/state mapping; no working product interface yet.

### S1 — Repository foundation — REVIEW READY 21 Sep 2026

**Description:** Build and verify the shared technical foundation required by every later feature.

**What will be implemented:** Monorepo structure, React shell, FastAPI shell, background worker, PostgreSQL, Valkey, private object storage, migrations, configuration, secret handling, health checks, telemetry, automated tests, security scanning and native ARM64/AMD64 container builds. Detailed scope is in the [S1 Repository Foundation Backlog](./04_S1_Repository_Foundation_Backlog.md), with evidence in the [Implementation and Verification Log](./05_Implementation_and_Verification_Log.md).

**Desired outputs**

- **Back-end:** Healthy API/worker/data-service foundation; safe migration and least-privilege accounts; repeatable local, clean-environment and hosted-CI verification.
- **Front-end:** A minimal React application shell proving that the web application builds and is served; no usable wealth-management workflow yet.

### S2 — Authentication and application bootstrap

**Description:** Safely transfer an authenticated identity from the separate auth-core service into Vittavaan and establish the user's initial application state.

**What will be implemented:** Auth-core redirect/return contract, signed-token verification, issuer/audience/JWKS configuration, local principal mapping, revocation/expiry handling, logout/security links, first-run bootstrap and safe unauthenticated/unauthorized behavior. Vittavaan will not implement passwords, OTP, MFA, account recovery or its own login system.

**Desired outputs**

- **Back-end:** Verified auth-core identity becomes a safe internal user principal; invalid, expired or revoked identities are rejected; identity events are logged without exposing tokens.
- **Front-end:** Authentication handoff, return/loading state, first-run screen, session-expired state, access-denied screen and links back to auth-core security/account functions.

### S3 — Household and access management

**Description:** Give an authenticated user a household context and control who may see or change household information.

**What will be implemented:** People, households, memberships, invitations where approved, household roles, resource grants, household switching, effective access checks and ownership-authority foundations. Negative authorization tests will prove that unrelated users cannot access each other's information.

**Desired outputs**

- **Back-end:** Household/person/member/grant records, authorization services and auditable membership lifecycle APIs.
- **Front-end:** Household creation, add/manage household member, invitation/acceptance where enabled, role/access management, household selector and clear permission-denied states.

### S4 — Holding catalogue and manual asset entry

**Description:** Allow households to record what they own, who owns it and the information needed for each supported asset type.

**What will be implemented:** Universal holding records, effective-dated ownership allocations, catalogue seeds, priority-1 subtype schemas/forms, common validation, provenance and manual create/read/update/correction workflows. Every catalogue asset remains recordable; richer subtype behavior follows the approved priority order.

**Desired outputs**

- **Back-end:** Holding, subtype-detail, ownership-allocation and source/provenance persistence with validated APIs and migrations.
- **Front-end:** Assets list, add-asset chooser, priority-asset forms, holding detail/edit flows, joint-ownership controls, validation and empty/loading/error states.

### S5 — Imports and reconciliation

**Description:** Let users bring supported data into Vittavaan without silently creating duplicates or corrupting existing records.

**What will be implemented:** CSV upload, secure parsing, staging, field mapping, validation, duplicate/match suggestions, reconciliation decisions, chunked commit, idempotency and import audit history. Live bank/broker connectors remain gated.

**Desired outputs**

- **Back-end:** Import batches, staged rows, normalized proposals, matching/reconciliation engine and controlled commit/rollback behavior.
- **Front-end:** File upload, column mapping, validation results, duplicate review, reconciliation choices, progress, completion summary and recoverable failure screens.

### S6 — Valuation, ledger and liabilities

**Description:** Track how assets and debts change over time and preserve a trustworthy financial history.

**What will be implemented:** Append/correct valuations, transactions, income streams, liabilities, balance history, repayment schedules, provenance, money/FX handling and calculation rules. Corrections preserve history instead of silently overwriting financial facts.

**Desired outputs**

- **Back-end:** Valuation, transaction, income, liability and schedule records; calculation services; correction/audit behavior and related APIs.
- **Front-end:** Valuation and transaction entry/history, income records, liabilities list/detail, add/edit liability forms, repayment information and correction explanations.

### S7 — Data Room

**Description:** Store documents that support portfolio records while controlling scanning, access, versioning and retention.

**What will be implemented:** Upload initiation, quarantine, malware-scan workflow, secure object storage, document metadata, links to financial records, versions/supersession, signed retrieval, audit events and lifecycle/retention controls.

**Desired outputs**

- **Back-end:** Secure document pipeline and metadata APIs with authorization, scanning states, version history and expiring access links.
- **Front-end:** Data Room list/search, upload progress, scan/pending/error states, document detail, linked-record display, version history and secure download actions.

### S8 — Wealth read models and complete portfolio views

**Description:** Combine household, holding, valuation, ledger and liability information into the principal wealth-management experience shown in the wireframes.

**What will be implemented:** Projection/read-model pipeline, net-worth calculations, historical series, movement explanations, asset/liability groupings, cash-flow summaries and every approved embedded Assets and Liabilities tab/state.

**Desired outputs**

- **Back-end:** Fast, rebuildable wealth projections and APIs for net worth, assets, liabilities, cash flow, movements and holding summaries.
- **Front-end:** Complete Net Worth, Assets, Liabilities, Cash Flow, Holding, First Run, Account Setup, Consents and relevant Data Room embedded states from the current wireframes.

### S9 — Portfolio analysis

**Description:** Help users understand performance and the reasons their wealth changed, with transparent calculation bases.

**What will be implemented:** XIRR/TWRR, contribution and attribution logic, gain/loss basis, drawdown, allocation/concentration views and permitted benchmark integration. Calculation limitations and data quality are shown rather than hidden.

**Desired outputs**

- **Back-end:** Reproducible analysis calculations, benchmark adapter boundary, cached analysis projections and explanation metadata.
- **Front-end:** Performance, attribution, allocation, concentration, drawdown and benchmark views with periods, basis disclosures and insufficient-data states.

### S10 — Planning and settings

**Description:** Add forward-looking goals and scenarios plus the controls users need to personalize the application.

**What will be implemented:** Goals, liquidity needs, commitments, scenarios, projections, preferences, notification rules and links to auth-core-owned security settings. Regulated advice or legally gated behavior remains disabled until approved.

**Desired outputs**

- **Back-end:** Goal/scenario/projection services, preference and notification configuration APIs, assumptions/versioning and gated-capability enforcement.
- **Front-end:** Goals, liquidity, scenario comparison, planning results, profile/preferences, notification settings and auth-core security links.

### S11 — Privacy and reliability

**Description:** Give users and operators controlled ways to export or close data and prove that the system can recover from failures.

**What will be implemented:** Export orchestration, account/household closure, retention, anonymization, legal holds, projection replay, backup/restore validation, failure handling and operational recovery workflows.

**Desired outputs**

- **Back-end:** Audited export/closure jobs, retention enforcement, legal-hold safeguards, restore/replay evidence and reliability controls.
- **Front-end:** Export request/status/download, closure confirmation/status, retention explanations and clear retry/recovery experiences for failed operations.

### S12 — Beta hardening

**Description:** Test and refine the complete product so it is suitable for a controlled beta rather than only developer demonstrations.

**What will be implemented:** End-to-end regression, authorization/security testing, accessibility review, performance/load testing, recovery drills, observability dashboards, runbooks, release checks and production-readiness evidence. Defects found are fixed and retested.

**Desired outputs**

- **Back-end:** Security, load, recovery and data-correctness gates pass; operational monitoring/runbooks and release evidence are complete.
- **Front-end:** Critical journeys pass browser and accessibility tests across supported screen sizes; loading, empty, error and recovery states are consistent and beta-ready.

## Per-sprint Definition of Ready

- Requirements/use cases and wireframe states identified.
- API/schema/event/interfaces approved and gates resolved or disabled.
- Acceptance, negative authorization, accessibility and observability scenarios defined.
- Migration/data impact and rollback/forward recovery understood.
- Dependencies/test data/environment available.

## Per-sprint Definition of Done

- Code, migrations, generated contract/client and documentation agree.
- Unit/property/contract/integration/E2E checks proportional to risk pass.
- Security/privacy/accessibility requirements pass.
- Telemetry/dashboard/alerts and relevant runbook exist.
- Staging acceptance evidence and traceability links recorded.
- No gated capability becomes enabled implicitly.

## Release gates

Alpha uses synthetic data; controlled beta requires threat-model review, restore drill, auth-core contract testing, independent security review scheduling and approved privacy/legal baseline. Production requires all SLO instrumentation, operational ownership, penetration-test disposition and manual approval.
