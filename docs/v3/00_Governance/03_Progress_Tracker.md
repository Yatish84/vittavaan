# v3 Progress Tracker

> Updated: 20 Sep 2026

## Documentation rebuild

| Workstream | Status | Evidence / next action |
|---|---|---|
| Source inventory | Complete | 25 current wireframes, v1/v2 docs, operator PDF and sibling auth-core inspected. |
| Governance and source precedence | Draft | Reconcile after the first complete cross-document pass. |
| Wireframe coverage matrix | Draft | Add element-level IDs and route/state acceptance mapping. |
| Product scope/release boundaries | Draft | Convert to stable requirement IDs. |
| Asset/liability catalogue | Draft | Expand rich schemas and validation per priority-1 subtype. |
| Auth-core integration | Draft | Confirm audience, redirect and deployment-specific values during implementation planning. |
| Actors and system boundary | Draft | Formal actor distinctions, authority matrix and trust boundaries added. |
| Functional requirements | Draft | Stable FR3 families added; next map them to detailed use cases and API/schema contracts. |
| Non-functional requirements/SLOs | Draft | Measurable performance, scale, reliability, security, privacy, finance, UX and operations requirements added. |
| Detailed use cases | Draft | Eleven beta use cases added with main flows, extensions and postconditions. |
| Legal and approval register | Draft | Twelve product gates and cross-cutting review topics recorded; all gated features default disabled. |
| Domain glossary | Draft | Canonical identity, ownership, valuation, ledger, planning and operational terms added. |
| ECB/domain analysis | Draft | Entities, aggregate roots, controls, boundaries and prohibited dependencies documented. |
| Sequence/state analysis | Draft | Core beta sequences and six lifecycle state machines added in Mermaid. |
| Requirements/domain coverage | Draft | All beta requirement families have entity/control/boundary homes; ten system-design gaps carried forward. |
| Architecture overview | Draft | Modular-monolith boundaries, deployment topology, write/read paths, scaling and degradation behavior added. |
| API contracts | Draft | v1 conventions, errors, endpoint surface, projection envelopes, idempotency and evolution added. |
| Database design | Draft | Expanded to a 48-table implementation dictionary with every planned column, key/constraint role, PostgreSQL type, nullability/default, meaning, and one direct-relationship Mermaid per table; physical DDL awaits the listed implementation decisions. |
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
| Testing and traceability | Draft | Test pyramid, personas, golden scenarios, security/load/recovery and end-to-end matrix added. |
| Operations/deployment | Draft | OCI Always Free single-VM staging, local/CI Compose parity, multi-architecture immutable deployment, safeguards and exit path added; AWS India remains the production and production-shaped performance target. |
| End-to-end consistency | Draft | Major v2 conflicts reconciled; approval items recorded. |

## Implementation status

Application implementation has **not started**. No application source code, migrations, infrastructure or CI configuration has been created in this repository as part of v3.

## Known review dependencies

| Dependency | Effect |
|---|---|
| Legal view on advisor marketplace, credit auction and escrow | Production gates remain disabled. |
| CA/advocate review of tax, gift and succession rules | Calculations cannot be represented as legally approved. |
| Connector/vendor contracts | Live import sources cannot be promised or activated. |
| Benchmark/news licensing | Licensed data cannot appear in production analysis. |
| Auth-core integration values | Issuer, audience, redirect origins and verifier topology require environment configuration. |
