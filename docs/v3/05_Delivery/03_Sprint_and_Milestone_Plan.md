# Sprint and Milestone Plan

## Cadence

Two-week iterations are assumed for planning; scope is accepted by outcome rather than date. Each milestone is independently deployable to staging and closes only with traceability and evidence.

| Sprint | Outcome | Primary trace families |
|---|---|---|
| S0 Documentation approval — COMPLETE 20 Sep 2026 | Reconciled v3 baseline, open decisions/gates owned | All |
| S1 Repository foundation — IN PROGRESS | Monorepo, local stack, CI, configuration, health and telemetry; detailed in [S1 Repository Foundation Backlog](./04_S1_Repository_Foundation_Backlog.md) and recorded in the [Implementation and Verification Log](./05_Implementation_and_Verification_Log.md) | NFR3-MAINT/OPS/SEC |
| S2 Auth/bootstrap | Auth-core handoff/verifier, local principal, first-run and denial behavior | UC3-IAM-001, FR3-IAM |
| S3 Household/access | People, households, memberships, grants, scope selector and ownership authority | UC3-HH-001, UC3-GRANT-001, FR3-HH |
| S4 Holding catalogue | Universal holding, allocations, priority-1 subtype forms and manual entry | UC3-HOLD-001, FR3-HOLD |
| S5 Imports | CSV upload, staging, mapping, duplicate detection, reconciliation and commit | UC3-IMPORT-001, FR3-IMPORT |
| S6 Valuation/ledger/liability | Append/correct valuation/transactions, income streams, liabilities and schedules | UC3-VAL/LEDGER, FR3-LEDGER |
| S7 Data room | Upload, quarantine/scan, links, versions, signed access and audit | UC3-DOC-001, FR3-DOC |
| S8 Wealth read models | Projection pipeline, Net worth and every Assets/Liabilities embedded tab/state | UC3-WEALTH-001, FR3-WEALTH |
| S9 Analysis | XIRR/TWRR, attribution, basis, drawdown and permitted benchmark adapter | UC3-AN-001, FR3-AN |
| S10 Planning/settings | Goals, liquidity, scenarios, preferences, notifications and auth-core security links | UC3-PLAN-001, FR3-PLAN/SET |
| S11 Privacy/reliability | Export/closure orchestration, retention controls, restore/replay and failure UX | UC3-SET-001, NFR3-PRIV/REL |
| S12 Beta hardening | E2E/accessibility/security/load/recovery, runbooks and production readiness | All beta traces |

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
