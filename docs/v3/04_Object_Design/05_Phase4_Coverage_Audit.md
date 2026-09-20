# Phase 4 Coverage Audit

| Phase 3 decision | Object-design realization | Status |
|---|---|---|
| Integer money/fixed decimals | `Money`, `MinorUnits`, `Percentage`, no float rule | Covered |
| Shared holdings | Holding aggregate and effective ownership algorithm | Covered |
| Append-only facts | Valuation/transaction repository append and correction contracts | Covered |
| Auth/application authorization separation | IdentityVerifier port plus AuthorityContext/AccessGrantControl | Covered |
| Fact/projection separation | Pure engines, ProjectionRepository/checkpoints, CQRS-lite | Covered |
| Import isolation | ImportControl and staged/reconciliation algorithms | Covered |
| Document quarantine | DocumentControl, ObjectStore, Scanner ports | Covered |
| Idempotency/concurrency | Command keys, expected versions, UoW/outbox | Covered |
| Calculation provenance | Generic CalculationResult/Provenance/failure contract | Covered |
| FX/history | Append-only rate selection and versioned conversion contract | Covered |
| Performance/planning | Exact high-level formulas and named failure states | Covered; golden vectors needed in testing phase |

## Remaining detail assigned to delivery/testing

- Concrete Pydantic/TypeScript schemas generated from OpenAPI.
- Full subtype-specific form/schema field dictionary.
- Golden numerical test vectors and tolerances.
- Benchmark/look-through algorithms after licensed sources are chosen.
- Exact calculator inventory beyond invest/prepay and goal funding.
- Professional-reviewed legal calculation contracts remain gated.

Phase 4 is complete at draft level and is sufficient to prepare implementation structure, code standards and test specifications without writing application code.

