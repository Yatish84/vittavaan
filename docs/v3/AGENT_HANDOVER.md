# Vittavaan v3 — Agent Handover

> **Last updated:** 20 Sep 2026  
> **Current phase:** v3 documentation rebuild  
> **Application code status:** Not started by v3 work  
> **Canonical documentation:** `docs/v3/`

## Mission

Produce a decision-complete, professional OOSE/OOP-oriented specification for Vittavaan before application implementation. Documentation must cover product intent, actors, use cases, requirements, analysis, system/object design, delivery, testing and operations. All diagrams use Mermaid.

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
| `01_Requirements/05_Use_Cases.md` | Eleven Cockburn-style beta use cases with alternate/error flows and wireframe/requirement links. |
| `01_Requirements/06_Legal_and_Approval_Register.md` | Disabled-by-default legal/vendor approval gates and evidence template. |
| `02_Analysis/01_Asset_and_Liability_Coverage.md` | Universal holding contract, complete catalogue treatment, rich P1 models, long-tail types and all liability classes. |
| `02_Analysis/02_Domain_Glossary.md` | Canonical domain terminology and explicitly rejected ambiguous terms. |
| `02_Analysis/03_ECB_Object_Model.md` | Entity–Boundary–Control modules, aggregate roots, controls, boundaries and dependency rules. |
| `02_Analysis/04_Sequence_and_State_Diagrams.md` | Mermaid sequences for core workflows and lifecycle state machines. |
| `02_Analysis/05_Requirements_to_Domain_Coverage.md` | Requirement-family/surface coverage and analysis gaps carried to design. |
| `03_System_Design/01_Auth_Core_Integration.md` | Authentication boundary, sequence, claim validation, authorization order, failure and lifecycle behavior. |
| `03_System_Design/02_Architecture_Overview.md` | Modular-monolith topology, modules, fact/projection paths, environments, scaling and failure boundaries. |
| `03_System_Design/03_Database_Design.md` | Implementation-level PostgreSQL design for 48 tables: purpose, every planned column, PK/FK/UQ/CHK role, type, nullability/default, direct-relationship Mermaid per table, indexes, integrity, migrations and retention. |
| `03_System_Design/04_API_Design.md` | OpenAPI conventions, error model, endpoint inventory, projection envelope, idempotency and compatibility. |
| `03_System_Design/05_Events_Jobs_and_Projections.md` | Outbox/event guarantees, job catalogue, retries, read projections and cache policy. |
| `03_System_Design/06_Imports_and_Reconciliation.md` | Staging, matching, commit semantics, error classes and connector adapter boundary. |
| `03_System_Design/07_Data_Room_Architecture.md` | Document/object model, quarantine/scan, authorization, lifecycle and retention. |
| `03_System_Design/08_Security_and_Threat_Model.md` | Protected assets, major threats/controls, authorization flow and verification requirements. |
| `03_System_Design/09_Observability_and_Operations_Design.md` | Telemetry signals, SLO/error-budget monitoring, runbooks and release operations. |
| `03_System_Design/10_Phase3_Coverage_Audit.md` | Cross-artifact reconciliation and decisions carried into object design. |
| `04_Object_Design/01_Shared_Types_and_Interfaces.md` | Typed value/provenance contracts and control, engine, repository and adapter protocols. |
| `04_Object_Design/02_Calculation_Contracts.md` | Financial formulas, rounding/reconciliation, preconditions and named failure vocabulary. |
| `04_Object_Design/03_Domain_Algorithms.md` | Effective ownership, valuation selection, corrections, projections, imports, verification and permissions. |
| `04_Object_Design/04_Design_Patterns_and_Object_Decisions.md` | Selected patterns, aggregate boundaries, dependency direction and rejected shortcuts. |
| `04_Object_Design/05_Phase4_Coverage_Audit.md` | Phase 3-to-object-design reconciliation and remaining delivery/test work. |
| `05_Delivery/01_Implementation_Roadmap.md` | Documentation sequence, implementation milestones and quality gates. |
| `05_Delivery/02_Project_Structure_and_Standards.md` | Planned monorepo, dependency rules and backend/frontend/API/migration/review standards. |
| `05_Delivery/03_Sprint_and_Milestone_Plan.md` | S0–S12 staged outcomes, readiness/done definitions and release gates. |
| `06_Testing/*` | Test pyramid, synthetic personas, golden scenarios and security/performance/recovery plans. |
| `07_Operations/*` | OCI Always Free staging with local Compose portability and immutable ARM64 deployment; AWS India production infrastructure, CI/CD/release management and incident runbooks. |
| `00_Governance/04_Traceability_Matrix.md` | Beta capability and global quality traceability through sprint/test evidence. |
| `00_Governance/05_End_to_End_Consistency_Audit.md` | Resolved contradictions and remaining approvals. |

No application code was created or modified.

## Critical product interpretation

### Assets and liabilities page

All embedded tabs/states are in beta scope: Net worth, Assets, Liabilities, Cash flow, Data room, Consents, Holding, First run and Account setup. Consents/account setup are designed now, but real financial connectors remain gated.

### Asset catalogue

Every asset in the PDF must be addable and visible in portfolio/net-worth/liquidity/provenance views. “Priority to build” controls rich modelling order only. Do not accidentally omit exotic assets or treat the regulator/licence/cost columns as confirmed obligations.

### Ownership

Although `Schema.dc.html` proposes a generic legal `Entity`, the owner selected a person-only initial model. Preserve a migration seam for legal entities, but do not reintroduce HUF/trust/company ownership into beta. Store a jointly owned holding once and attribute through effective-dated ownership allocations.

### Authentication

Do not create login, signup, password, OTP, MFA, recovery, refresh, session-management or Supabase-auth features in Vittavaan. Consume auth-core RS256/JWKS and revocation-aware identity context. Auth-core workspace roles do not automatically authorize household financial access.

## Next documentation work, in order

1. Expand the use-case set where later design identifies uncovered beta interactions; add element-level wireframe trace IDs.
2. Obtain owner review of the full v3 baseline and record requested corrections/approvals.
3. Refine element-level wireframe trace IDs, subtype field dictionary and exact golden fixture values during sprint planning.
4. Confirm auth-core environment contract, benchmark choice, retention schedule, gate owners and RPO/RTO approvals.
5. Only after documentation approval, begin S1 repository foundation; do not implement product features early.

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
- Update the progress tracker, README and this handover with every completed document group.
- Do not begin application code until the owner approves the documentation baseline.

## Repository state warning

At v3 start, Git showed deletions under the historical `docs/Wireframe/` location and untracked `docs/v1/Wireframe/` and `docs/v2/Wireframe/`. These are pre-existing user changes associated with reorganizing/replacing wireframes. Do not revert, stage or modify them without explicit instruction.
