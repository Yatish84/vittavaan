# API Design

## Contract conventions

- Base path `/api/v1`; OpenAPI is the contract source.
- JSON uses `snake_case`; timestamps RFC 3339 UTC; dates ISO `YYYY-MM-DD`.
- Money is `{amount_minor_units, currency}`; decimals are JSON strings to preserve precision.
- IDs are UUIDs and are opaque to clients.
- Collections use opaque cursor pagination and bounded page size.
- Mutating retries require `Idempotency-Key`; editable aggregates require `If-Match` version.
- Every response includes or propagates `X-Correlation-ID`.

## Error contract

```json
{
  "type": "https://api.vittavaan.example/problems/ownership-allocation-invalid",
  "title": "Ownership allocation is incomplete",
  "status": 422,
  "code": "OWNERSHIP_ALLOCATION_TOTAL_INVALID",
  "detail": "Active ownership allocations must total 100%.",
  "correlation_id": "uuid",
  "field_errors": [{"field": "allocations", "code": "TOTAL_NOT_100"}]
}
```

Use RFC 9457-style problem details. `401` means authentication is absent/invalid; `403` is used only when safe; out-of-scope resource access normally returns non-enumerating `404`. `409` represents version/idempotency/state conflict; `422` represents valid syntax violating domain rules; `429` includes retry metadata; `503` describes temporary dependency failure.

## Bootstrap and catalogue

| Method/path | Purpose |
|---|---|
| `GET /bootstrap` | Principal, permitted scopes, preferences, feature gates and first-run route. |
| `GET /catalogue/asset-classes` | Active class/subtype schemas, units and allowed valuation methods. |
| `GET /catalogue/liability-types` | Active liability schemas. |
| `GET /catalogue/policies` | Safe presentation of staleness/verification policy metadata. |

## Households, people and grants

| Method/path | Purpose |
|---|---|
| `GET/POST /households` | List permitted/create household. |
| `GET/PATCH /households/{id}` | Read/update versioned household. |
| `GET/POST /households/{id}/people` | List permitted/add person/member. |
| `GET/PATCH /people/{id}` | Scoped person detail/update. |
| `GET/POST /access-grants` | List permitted/create scoped grant. |
| `GET /access-grants/{id}` | Grant details/effective state. |
| `POST /access-grants/{id}/revoke` | Append revocation. |

## Holdings and valuations

| Method/path | Purpose |
|---|---|
| `GET/POST /holdings` | Cursor list/create canonical holding with ownership and optional initial valuation. |
| `GET/PATCH /holdings/{id}` | Detail/update mutable metadata with version check. |
| `POST /holdings/{id}/archive` | Authorized lifecycle transition; no destructive delete. |
| `GET/POST /holdings/{id}/ownership-schedules` | Read/replace future/current effective allocation schedule atomically. |
| `GET/POST /holdings/{id}/valuations` | Valuation history/append assertion. |
| `POST /holdings/{id}/valuations/{valuation_id}/correct` | Append superseding correction. |
| `GET/POST /holdings/{id}/restrictions` | Read/record pledge/lien/hold state. |
| `GET/POST /holdings/{id}/cost-basis-lots` | Read/append lots/corrections. |
| `GET/POST /holdings/{id}/commitments` | Read/create/update versioned commitments. |

## Ledger, income and liabilities

| Method/path | Purpose |
|---|---|
| `GET/POST /transactions` | Filtered cursor ledger/append event. |
| `GET /transactions/{id}` | Authorized transaction detail. |
| `POST /transactions/{id}/correct` | Append reversing/correcting event. |
| `GET/POST /income-streams` | Scoped streams/observed receipt definitions. |
| `GET/POST /liabilities` | List/create direct or contingent obligation. |
| `GET/PATCH /liabilities/{id}` | Detail/update terms with version. |
| `POST /liabilities/{id}/archive` | Close/archive obligation. |
| `GET/POST /liabilities/{id}/schedules` | Versioned expected schedule. |
| `GET/POST /liabilities/{id}/security-links` | Linked collateral/pledge details. |

## Imports and reconciliation

| Method/path | Purpose |
|---|---|
| `POST /imports` | Initialize idempotent upload/import job. |
| `GET /imports/{id}` | Job state, progress, counts and safe errors. |
| `POST /imports/{id}/mapping` | Submit versioned column/semantic mapping. |
| `GET /imports/{id}/rows` | Cursor staged validation/reconciliation view. |
| `POST /imports/{id}/decisions` | Batch explicit duplicate/match/skip decisions. |
| `POST /imports/{id}/commit` | Confirm exact job version/selected rows. |
| `POST /imports/{id}/cancel` | Cancel pre-commit remaining work. |
| `GET /imports/{id}/error-report` | Authorized expiring report artifact. |

## Documents

| Method/path | Purpose |
|---|---|
| `GET/POST /documents` | List metadata/initialize document and bounded upload. |
| `GET /documents/{id}` | Authorized metadata/version/link state. |
| `POST /documents/{id}/versions` | Add replacement version. |
| `POST /documents/{id}/links` | Add authorized domain link. |
| `POST /documents/{id}/access-url` | Issue short-lived URL after current authorization/scan check. |
| `POST /documents/{id}/deactivate` | Lifecycle transition under retention policy. |
| `GET /documents/{id}/access-history` | Owner/authorized audit view. |

## Wealth, analysis and planning queries

| Method/path | Purpose |
|---|---|
| `GET /wealth/overview` | Net worth/assets/liabilities/verified share for scope/as-of. |
| `GET /wealth/trend` | Versioned non-interpolated series and gaps. |
| `GET /wealth/movements` | Reconciled period movement components/residual. |
| `GET /wealth/allocation` | Class/subtype/owner/liquidity breakdown. |
| `GET /cash-flow/summary` | In/out/surplus/savings/debt-service by period. |
| `GET /analysis/performance` | XIRR, TWRR, benchmark, basis and named failures. |
| `GET /analysis/attribution` | Reconciled contribution and drill-down. |
| `GET /analysis/exposure` | Direct/look-through exposure where approved data exists. |
| `GET/POST /goals` | List/create goal. |
| `GET/PATCH /goals/{id}` | Goal/funding/liquidity detail/update. |
| `POST /goals/{id}/funding-links` | Link permitted holding. |
| `POST /goals/{id}/scenarios` | Calculate and optionally persist immutable scenario. |

Query parameters use a typed `scope_type`, `scope_id`, `as_of`/period and `basis`. The server derives authorization and does not trust a scope merely because its ID was supplied.

## Settings, privacy and operations

| Method/path | Purpose |
|---|---|
| `GET/PATCH /preferences` | Display/accessibility settings with version. |
| `GET/PATCH /notification-preferences` | Event/channel choices. |
| `POST/GET /privacy/exports` | Request/list export jobs. |
| `POST /privacy/closure-cases` | Initiate governed application closure. |
| `GET /privacy/closure-cases/{id}` | Authorized status. |
| `GET /audit-evidence` | Owner-authorized bounded audit view; never raw unrestricted logs. |
| `GET /health/live` | Process liveness, no dependency details. |
| `GET /health/ready` | Load-balancer readiness with safe dependency status. |

## Projection response envelope

```json
{
  "data": {},
  "scope": {"type": "household", "id": "uuid"},
  "as_of": "2026-09-20T12:00:00Z",
  "projection": {
    "state": "current",
    "calculated_at": "2026-09-20T12:00:05Z",
    "source_checkpoint": "opaque",
    "calculation_version": "wealth-1.0.0",
    "policy_version": "valuation-selection-1.0.0",
    "completeness": "partial",
    "omissions": ["holding:uuid:stale"]
  }
}
```

## Idempotency and concurrency

- Same key and identical request returns the original outcome.
- Same key with different request hash returns `409 IDEMPOTENCY_KEY_REUSED`.
- `If-Match` mismatch returns `409 VERSION_CONFLICT` with safe current version metadata.
- Append-only commands deduplicate by principal, operation and idempotency key/source external ID.
- Batch endpoints return per-item status only where partial commit semantics are explicitly documented.

## Contract evolution

- Additive optional response fields are allowed in v1.
- Enum additions require tolerant generated clients or an API version/review.
- Breaking field/semantic changes require a new version or negotiated deprecation window.
- Every endpoint maps to requirements/use cases and has positive/negative authorization contract tests.

