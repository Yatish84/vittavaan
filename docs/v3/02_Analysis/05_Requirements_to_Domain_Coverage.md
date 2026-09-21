# Requirements-to-Domain Coverage Audit

## Purpose

This audit verifies that every current requirement family has a domain home before database/API design. Detailed endpoint/table/test traceability will extend this matrix in later phases.

| Requirement family | Primary entities/value objects | Primary controls/policies | Boundary/surface | Status |
|---|---|---|---|---|
| FR3-IAM | AuthenticatedPrincipal, PrincipalPersonLink | ApplicationBootstrapControl, AuthorizationControl | Auth boundary, all protected routes | Covered |
| FR3-HH | Person, Household, Membership, AccessGrant, OwnershipAllocation | HouseholdControl, AccessGrantControl, AuthorityPolicy | Household, scope selector, Consents | Covered |
| FR3-HOLD | Holding, OwnershipAllocation, ValuationEvent, CostBasisLot, Commitment | HoldingCommandControl, ValuationControl, CataloguePolicy | Assets, Holding, Account setup | Covered |
| FR3-LEDGER | Transaction, IncomeStream, Liability, ScheduleVersion | LedgerControl, LiabilityControl | Cash flow, Liabilities, Holding | Covered |
| FR3-IMPORT | ImportJob, ImportFile, StagedRow, ReconciliationDecision | ImportControl, ReconciliationControl | First run, Account setup, Connections | Covered |
| FR3-CONSENT | SourceConsent, Source | ConsentControl, ProcessingBasisPolicy | Consents, Connections, Account setup | Covered |
| FR3-DOC | Document, DocumentVersion, ScanResult | DocumentControl, MalwareScanControl | Data room, Holding | Covered |
| FR3-WEALTH | FinancialSnapshot, WealthProjection, Provenance | ProjectionControl, WealthEngine, ValuationPolicy | Net worth, Assets/Liabilities tabs | Covered |
| FR3-AN | PerformanceProjection, Provenance, benchmark facts | PerformanceEngine, ProjectionControl | Analysis, Attribution | Covered; benchmark licence remains gated |
| FR3-PLAN | Goal, FundingLink, Scenario | GoalControl, PlanningEngine | Planning | Covered |
| FR3-SET | Preference, ExportJob, ClosureCase, AuditEvidence | SettingsControl, PrivacyWorkflowControl, AuditEvidenceControl | Settings | Covered |
| FR3-GATE | ApprovalRecord, FeatureGate | FeatureGateControl plus future module controls | Deferred surfaces | Boundary covered; detailed future models deferred |
| NFR3-PERF/SCALE | Projection/read model, queue/outbox metadata | ProjectionControl, OutboxControl, capacity policies | API/workers/observability | Covered in architecture, persistence, SLO and performance-test plan |
| NFR3-REL | OutboxEvent, idempotency record, recovery evidence | OutboxControl, retry/circuit policies | Infrastructure boundaries | Covered in jobs, deployment, backup/restore and runbooks |
| NFR3-SEC/PRIV | AuthorityContext, AccessGrant, Consent, AuditEvidence | Authorization, feature gate, privacy workflow | All boundaries | Covered |
| NFR3-FIN | Money, Percentage, FXRate, Provenance, CalculationVersion | MoneyPolicy, calculation engines | All financial outputs | Covered |
| NFR3-UX | Accessible state/result view models | Boundary presentation policies | All beta wireframes | Covered at requirements/test-strategy level; element trace IDs remain sprint refinement |
| NFR3-MAINT/OPS | Contract/event/version metadata | Cross-cutting delivery controls | CI/CD and operations | Covered in delivery standards, deployment specification and runbooks |

## Wireframe surface coverage

| Surface | Domain coverage | Remaining analysis concern |
|---|---|---|
| Net worth | WealthProjection, valuation/ledger facts, provenance | Formal movement reconciliation and snapshot policy contract. |
| Assets/Liabilities tabs | Holding, Liability, Transaction, Document, Import, Consent/Grant | Element-level field catalogue and route-state mapping. |
| Household | Person, Membership, OwnershipAllocation, AccessGrant | Departure/death are later gated workflows; beta archive behavior needs API design. |
| Analysis/Attribution | PerformanceProjection and engine | Benchmark/look-through source contracts. |
| Planning | Goal, FundingLink, Scenario | Calculator inventory and exact contracts. |
| Settings | Preferences, grants, export/closure | Revenue transparency data exists only when commercial modules activate. |
| Investor profile | Person facts/preferences | Suitability/recommendation profile stays outside beta. |
| Connections | Import source and connector consent metadata | Avoid portraying manual/import source as a live connection. |

## Former analysis gaps and resolution homes

1. Aggregate concurrency: database optimistic versions, API `If-Match`, idempotency records and unit-of-work contracts.
2. Effective ownership: append/effective-date algorithm and projection invalidation rules.
3. FX: immutable FX events and versioned selection/calculation contracts.
4. Event taxonomy: event/job/projection catalogue and outbox guarantees.
5. Movement reconciliation: calculation contracts and residual failure behavior.
6. Transfer/corrections: append-only ledger algorithms and correction links.
7. Import atomicity: staged workflow, frozen job versions and resumable chunk contract.
8. Documents: retention classes, quarantine, supersession and legal-hold design.
9. Permissions: authority context, scoped query objects and totals-only grant behavior.
10. Planning: goal/scenario contracts; additional regulated/legal calculators remain gated.

## Coverage conclusion

All beta functional requirement families have an identified entity/control/boundary home. No database or API design should introduce a new business entity or rule without updating this analysis and traceability chain.
