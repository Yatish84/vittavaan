# End-to-End Traceability Matrix

## Beta capability traceability

| Capability | Wireframe/tab | Requirement/use case | Domain/control | API/data/event | Test evidence | Sprint |
|---|---|---|---|---|---|---|
| Auth/bootstrap | All / First run | FR3-IAM; UC3-IAM-001 | Principal, Bootstrap/Authz | `/bootstrap`; principals; auth contract | token/revocation/denial | S2 |
| Household/person | Household | FR3-HH; UC3-HH-001 | HouseholdControl | household/person routes/tables; membership event | role/minor/duplicate/authz | S3 |
| Access grant | Consents/Settings/Household | FR3-HH; UC3-GRANT-001 | AccessGrantControl | grant routes/table/event | expiry/revoke/totals-only/IDOR | S3 |
| Manual holding | Assets/Holding/First run | FR3-HOLD; UC3-HOLD-001 | HoldingControl/Catalogue | holding/ownership/valuation routes/tables/events | subtype/allocation/concurrency | S4 |
| CSV import | Account setup/Connections | FR3-IMPORT; UC3-IMPORT-001 | Import/Reconciliation | import routes/staging/events | malformed/replay/partial/formula | S5 |
| Valuation | Holding/Net worth | FR3-HOLD; UC3-VAL-001 | ValuationControl/Policy | valuation append/correct; event | stale/conflict/supersession | S6 |
| Transaction/cash flow | Cash flow/Holding | FR3-LEDGER; UC3-LEDGER-001 | LedgerControl | transaction append/correct; event | transfer/correction/append-only | S6 |
| Liabilities | Liabilities/Holding | FR3-LEDGER | LiabilityControl | liability/schedule/security | EMI/direct-contingent/collateral | S6 |
| Documents | Data room/Holding | FR3-DOC; UC3-DOC-001 | DocumentControl | document routes/tables/scan events | malware/outage/URL/revocation | S7 |
| Wealth dashboard | Net worth + embedded tabs | FR3-WEALTH; UC3-WEALTH-001 | WealthEngine/Projection | wealth routes/projections/events | reconciliation/stale/negative/partial | S8 |
| Analysis/attribution | Analysis/Attribution | FR3-AN; UC3-AN-001 | PerformanceEngine | analysis routes/projections | golden XIRR/TWRR/attribution | S9 |
| Goals/scenarios | Planning | FR3-PLAN; UC3-PLAN-001 | Goal/PlanningEngine | goal/scenario routes/tables | liquidity/assumption/version | S10 |
| Preferences | Settings | FR3-SET | SettingsControl | preference routes/table | display/accessibility/version | S10 |
| Export/closure | Settings | FR3-SET; UC3-SET-001 | PrivacyWorkflow | privacy routes/jobs/cases | retry/auth-core/retention/shared facts | S11 |

## Global quality traceability

| Quality family | Design home | Evidence home |
|---|---|---|
| Performance/scale | Architecture, projections, indexes, bounded API | Load/SLO dashboards and capacity report |
| Reliability/recovery | Outbox/jobs, backups, release/runbooks | Chaos/dependency and restore/replay drills |
| Security/privacy | Auth integration, threat model, grants, retention | Security/IDOR/penetration/privacy tests |
| Financial correctness | Calculation contracts/domain algorithms | Golden/property/reconciliation tests |
| Accessibility/UX | Wireframe states/frontend standards | Automated/manual WCAG and E2E |
| Maintainability/operations | Project standards, CI/CD, observability | CI reports, artifact/SBOM and release evidence |

## Deferred capability traceability

Deferred wireframes map to `FR3-GATE-*`, their `GATE-LEGAL-*` approval, feature-gate records and future independent milestones. They have architecture seams but no authorization to implement/enable production behavior until their detailed requirements/use cases are approved.

