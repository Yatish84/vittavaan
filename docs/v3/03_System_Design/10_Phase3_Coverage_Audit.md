# Phase 3 Coverage Audit

## Cross-artifact coverage

| Concern | Architecture | Database | API | Events/jobs | Specialized design |
|---|---|---|---|---|---|
| Auth-core bridge | verifier boundary | local principal only | bootstrap | cache invalidation | Auth-core integration, threat model |
| Household/access | module/policy | people/membership/grants | household/grant routes | grant expiry/events | Threat model |
| Shared holdings | holding module | holding/allocations | holding/ownership routes | projection invalidation | Import design |
| Append-only ledger/valuation | fact path | events/lots/transactions | append/correct routes | projection events | Projection design |
| Imports | worker path | jobs/staged rows/decisions | workflow routes | parse/commit jobs | Import architecture |
| Documents | storage boundary | metadata/version/access | document routes | scan/OCR jobs | Data room |
| Wealth/analysis/planning | projection path | projection/checkpoint | query routes | rebuild/reconcile | Projection strategy |
| Privacy/closure | module boundary | jobs/cases/audit | privacy routes | export/retention jobs | Threat/operations |
| Scale/SLO | topology | indexes/partition seams | bounded contracts | queues/backpressure | Observability |

## Carried decisions for object design

1. Exact calculation formulas, rounding and failure codes.
2. Protocol interfaces for aggregates, repositories, engines, adapters and authorization.
3. Movement reconciliation taxonomy and residual handling.
4. Effective-dated ownership algorithm and historical attribution.
5. FX selection and multi-currency calculation contracts.
6. Transaction transfer pairing and correction contracts.
7. Subtype schema registry and validation interface.
8. Provenance response types shared by all engines.

## Phase result

Phase 3 is complete at draft level: every beta module has a runtime boundary, persistence home, API surface, event/job behavior and security/operations treatment. These documents require reconciliation during object design and test-plan creation before approval for implementation.

