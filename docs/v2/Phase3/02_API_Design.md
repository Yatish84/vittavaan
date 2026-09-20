# Phase 3 — System Design: API Design

> **OOSE Phase:** System Design
> **Purpose:** Defines the complete REST API contract between backend and clients. This is the single source of truth for frontend developers and future mobile developers. All endpoints are implemented by the FastAPI backend and auto-documented via OpenAPI.
> **Status:** Draft

---

## 1. API Conventions

### Base URL
```
Local:    http://localhost:8000/api/v1
Staging:  https://api-staging.vittavaan.in/api/v1
Prod:     https://api.vittavaan.in/api/v1
```

### Versioning
All endpoints are prefixed `/api/v1/`. When breaking changes are introduced, `/api/v2/` is added without removing v1. Mobile clients are notified to upgrade before v1 is sunset.

### Authentication
Every protected endpoint requires a `Bearer` JWT in the `Authorization` header:
```
Authorization: Bearer <supabase_jwt>
```
Unauthenticated requests return `401 Unauthorized`.

### Request / Response Format
- All request bodies and responses: `Content-Type: application/json`
- All timestamps: ISO 8601, UTC (`2026-09-19T10:00:00Z`)
- All monetary amounts: integers in paise (`minor_units` suffix)
- All percentages: floats, e.g., `50.0` = 50%
- All UUIDs: lowercase hyphenated string (`"550e8400-e29b-41d4-a716-446655440000"`)

### Indian Locale in API
- The API returns raw integers for monetary values (no formatting)
- The **client** formats using the Indian number system (₹ lakh/crore)
- A shared `packages/types/formatters.ts` utility handles this

### Pagination (List Endpoints)
Cursor-based pagination is used for all list endpoints:
```json
{
  "items": [...],
  "pagination": {
    "next_cursor": "base64encodedcursor",
    "prev_cursor": null,
    "total_count": 47,
    "has_more": true
  }
}
```
Request parameters: `?cursor=<token>&limit=50` (default limit: 50, max: 200)

### Provenance Metadata
All calculated metric responses include:
```json
{
  "data": { ... },
  "provenance": {
    "as_of": "2026-09-19T10:00:00Z",
    "calculation_version": "v1.3",
    "is_partial": false,
    "performance_basis": "ESTIMATED"
  }
}
```

### Standard Error Response
```json
{
  "error": {
    "code": "ALLOCATION_EXCEEDS_100",
    "message": "Allocation would exceed 100% for this asset. Remaining: 25.0%",
    "field": "percentage_share",
    "details": { "remaining_pct": 25.0 }
  }
}
```

---

## 2. HTTP Status Codes Used

| Code | When Used |
|---|---|
| `200 OK` | Successful GET, PATCH, or action |
| `201 Created` | Successful POST creating a new resource |
| `204 No Content` | Successful DELETE |
| `400 Bad Request` | Request is structurally malformed |
| `401 Unauthorized` | Missing or invalid JWT |
| `403 Forbidden` | Valid JWT but insufficient permissions (RBAC/ABAC) |
| `404 Not Found` | Resource does not exist (or caller cannot see it) |
| `409 Conflict` | Duplicate resource (e.g., duplicate connection request) |
| `422 Unprocessable Entity` | Request is valid JSON but fails business rules |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Unexpected server error (always logged, never exposes stack trace) |
| `503 Service Unavailable` | Dependency unavailable (auth, storage) |

---

## 3. Endpoint Reference

### 3.1 Auth & Session

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/session` | Public | Create session from JWT |
| `DELETE` | `/auth/session` | Required | Logout (terminate current session) |
| `DELETE` | `/auth/sessions` | Required | Logout everywhere (all sessions) |
| `GET` | `/auth/sessions` | Required | List active sessions |

**POST /auth/session**
```
Request:  { "jwt_token": "eyJ..." }
Response: {
  "user_id": "uuid",
  "session_id": "uuid",
  "active_role": "INVESTOR",
  "is_new_user": true
}
```

---

### 3.2 Users

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/users/me` | Required | Get current user profile |
| `PATCH` | `/users/me` | Required | Update user name, DOB |
| `PATCH` | `/users/me/role-context` | Required | Switch active role (INVESTOR/ADVISOR) |
| `GET` | `/users/search` | Required | Search platform users |
| `POST` | `/users/me/export` | Required | Request data export |
| `DELETE` | `/users/me` | Required | Initiate account closure |

**PATCH /users/me/role-context**
```
Request:  { "active_role": "ADVISOR" }
Response: { "user_id": "uuid", "active_role": "ADVISOR" }
```

---

### 3.3 Investor Profile

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/profile/investor` | Required | Get investor profile |
| `PUT` | `/profile/investor` | Required | Create or replace investor profile |
| `GET` | `/profile/investor/resume` | Required | Get Financial Resume data |
| `POST` | `/profile/investor/resume/share` | Required | Generate shareable resume (with field selection) |

---

### 3.4 Advisor Profile

| Method | Path | Auth (Advisor) | Description |
|---|---|---|---|
| `GET` | `/profile/advisor` | Required | Get own advisor profile |
| `PUT` | `/profile/advisor` | Required | Create or replace advisor profile |
| `GET` | `/advisors` | Required | List/search advisor marketplace |
| `GET` | `/advisors/{advisor_id}` | Required | Get public advisor profile |

**GET /advisors (query params)**
```
?specialties=ESTATE,TAX&certification=CA&city_tier=TIER_1&limit=20
Response: {
  "items": [
    {
      "advisor_id": "uuid",
      "display_name": "...",
      "firm_name": "...",
      "certifications": ["CA", "SEBI_RIA"],
      "credential_verification_status": "VERIFIED",
      "specialty_areas": ["estate", "taxation"],
      "match_reason": "Specialises in estate planning — matches your Will status"
    }
  ],
  "pagination": { ... }
}
```

---

### 3.5 Portfolio — Dashboard

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/dashboard` | Required | Full dashboard metrics (DashboardFacade) |
| `GET` | `/dashboard/net-worth-trend` | Required | Net worth history (FinancialSnapshots) |
| `GET` | `/dashboard/alerts` | Required | Worth-a-Look alerts |

**GET /dashboard**
```json
{
  "data": {
    "net_worth_minor_units": 147325000,
    "total_assets_minor_units": 198500000,
    "total_liabilities_minor_units": 51175000,
    "mom_change_minor_units": 1250000,
    "mom_change_pct": 0.86,
    "ytd_change_pct": 8.4,
    "verified_wealth_pct": 72.4,
    "income_this_month_minor_units": 850000,
    "expenses_this_month_minor_units": 620000,
    "surplus_this_month_minor_units": 230000,
    "asset_allocation": {
      "liquid_pct": 45.2,
      "real_estate_pct": 41.8,
      "alternative_pct": 13.0
    },
    "waterfall": [
      { "label": "Equity Gain", "value_minor_units": 450000 },
      { "label": "RE Revaluation", "value_minor_units": 800000 }
    ],
    "alerts": [
      { "type": "STALE_VALUATION", "asset_name": "Karjat Plot", "days_stale": 312 }
    ]
  },
  "provenance": {
    "as_of": "2026-09-19T10:00:00Z",
    "calculation_version": "v1.3",
    "is_partial": false
  }
}
```

---

### 3.6 Portfolio — Assets

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/portfolio/assets` | Required | List all assets (paginated) |
| `POST` | `/portfolio/assets` | Required | Create asset (type determined by body) |
| `GET` | `/portfolio/assets/{asset_id}` | Required | Get asset detail |
| `PATCH` | `/portfolio/assets/{asset_id}` | Required | Update asset details / valuation |
| `DELETE` | `/portfolio/assets/{asset_id}` | Required | Soft-delete asset (mark inactive) |
| `GET` | `/portfolio/assets/{asset_id}/documents` | Required | List linked documents |
| `POST` | `/portfolio/assets/{asset_id}/documents` | Required | Upload document for asset |

**POST /portfolio/assets (Liquid Asset example)**
```json
Request:
{
  "asset_type": "LIQUID",
  "name": "HDFC Bank Savings Account",
  "liquid_sub_type": "BANK_SAVINGS",
  "institution_name": "HDFC Bank",
  "ownership_split_pct": 100.0,
  "purchase_price_minor_units": 0,
  "current_value_minor_units": 2500000,
  "purchase_date": "2020-01-15",
  "currency": "INR",
  "verification_level": "SELF_DECLARED"
}

Response (201):
{
  "asset_id": "uuid",
  "name": "HDFC Bank Savings Account",
  "asset_type": "LIQUID",
  "attributed_value_minor_units": 2500000,
  "verification_level": "SELF_DECLARED",
  "staleness_status": "CURRENT",
  "unrealised_gain_minor_units": 0
}
```

**POST /portfolio/assets (Real Estate example)**
```json
Request:
{
  "asset_type": "REAL_ESTATE",
  "name": "Karjat Plot",
  "property_type": "LAND",
  "location_address": "Survey No. 123, Karjat, Maharashtra 410201",
  "area_sqft": 5000.0,
  "price_per_sqft_minor_units": 150000,
  "ownership_split_pct": 100.0,
  "purchase_price_minor_units": 60000000,
  "purchase_date": "2022-03-10",
  "currency": "INR",
  "valuation_method": "USER_ESTIMATE",
  "valuation_as_of": "2026-06-01T00:00:00Z",
  "title_verification_status": "VERIFIED",
  "encumbrance_status": "CLEAR",
  "mutation_status": "COMPLETED"
}
```

---

### 3.7 Portfolio — Liabilities

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/portfolio/liabilities` | Required | List all liabilities |
| `POST` | `/portfolio/liabilities` | Required | Add liability |
| `GET` | `/portfolio/liabilities/{id}` | Required | Get liability detail |
| `PATCH` | `/portfolio/liabilities/{id}` | Required | Update liability |
| `DELETE` | `/portfolio/liabilities/{id}` | Required | Remove liability |
| `GET` | `/portfolio/liabilities/{id}/schedule` | Required | Amortization schedule |

---

### 3.8 Portfolio — Transactions

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/portfolio/transactions` | Required | List transactions (paginated, filterable) |
| `POST` | `/portfolio/transactions` | Required | Log new transaction (append-only) |
| `GET` | `/portfolio/transactions/{id}` | Required | Get transaction detail |
| `POST` | `/portfolio/transactions/{id}/correct` | Required | Log correcting entry for this transaction |

**Note:** No `PUT`, `PATCH`, or `DELETE` on transactions — append-only ledger.

**GET /portfolio/transactions (query params)**
```
?start_date=2026-04-01&end_date=2026-09-19&type=INFLOW&category=SALARY&asset_id=uuid&limit=50
```

---

### 3.9 Analysis & Performance

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/portfolio/performance` | Required | XIRR, TWRR, drawdown |
| `GET` | `/portfolio/attribution` | Required | Return attribution by asset class |
| `GET` | `/portfolio/allocation` | Required | Current asset allocation breakdown |
| `GET` | `/portfolio/cashflow` | Required | Monthly cashflow summary |

**GET /portfolio/performance (query params)**
```
?window=3Y   (options: 1Y, 3Y, 5Y, inception)
```

```json
Response:
{
  "data": {
    "xirr_pct": 14.2,
    "twrr_pct": 12.8,
    "benchmark_return_pct": 11.4,
    "excess_return_pct": 1.4,
    "max_drawdown_pct": -18.3,
    "drawdown_start_date": "2023-01-15",
    "drawdown_trough_date": "2023-06-30",
    "recovery_months": 7
  },
  "provenance": {
    "as_of": "2026-09-19T10:00:00Z",
    "is_partial": false,
    "performance_basis": "ESTIMATED"
  }
}
```

---

### 3.10 Financial Goals

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/goals` | Required | List all financial goals |
| `POST` | `/goals` | Required | Create goal |
| `GET` | `/goals/{id}` | Required | Get goal with funding calculation |
| `PATCH` | `/goals/{id}` | Required | Update goal |
| `DELETE` | `/goals/{id}` | Required | Delete goal |
| `POST` | `/goals/{id}/assets` | Required | Link asset to goal |
| `DELETE` | `/goals/{id}/assets/{asset_id}` | Required | Unlink asset from goal |
| `GET` | `/goals/{id}/scenario` | Required | Invest vs. prepay or assumption scenarios |

---

### 3.11 Estate Planning — Household

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/household` | Required | Get household summary + member list |
| `POST` | `/household/members` | Required | Add household member |
| `GET` | `/household/members/{id}` | Required | Get member detail |
| `PATCH` | `/household/members/{id}` | Required | Update member |
| `DELETE` | `/household/members/{id}` | Required | Remove member |

---

### 3.12 Estate Planning — Estate Plan & Will

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/estate` | Required | Get estate plan + coverage analysis |
| `PATCH` | `/estate/executors` | Required | Update executor details |
| `POST` | `/estate/will` | Required | Create will record + upload document |
| `PATCH` | `/estate/will/{id}` | Required | Update will status |
| `GET` | `/estate/succession-defaults` | Required | Get default intestacy shares |

---

### 3.13 Estate Planning — Inheritance

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/estate/allocations` | Required | Get all inheritance allocations |
| `POST` | `/estate/allocations` | Required | Create allocation |
| `PATCH` | `/estate/allocations/{id}` | Required | Update allocation percentage |
| `DELETE` | `/estate/allocations/{id}` | Required | Remove allocation |

**POST /estate/allocations**
```json
Request:
{
  "asset_id": "uuid",
  "beneficiary_id": "household_member_uuid",
  "percentage_share": 40.0,
  "distribution_conditions": "To be used for education expenses only"
}

Response (201):
{
  "allocation_id": "uuid",
  "asset_id": "uuid",
  "beneficiary_name": "Arjun Karkera",
  "percentage_share": 40.0,
  "remaining_unallocated_pct": 60.0,
  "updated_estate_coverage_pct": 68.4
}
```

---

### 3.14 Estate Planning — Gift Rules & Transfers

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/gifts/rules` | Required | Get applicable gift rules (jurisdiction) |
| `POST` | `/gifts/evaluate` | Required | Evaluate gift eligibility + tax status |
| `GET` | `/gifts/transfers` | Required | List all gift transfers |
| `POST` | `/gifts/transfers` | Required | Initiate gift transfer |
| `PATCH` | `/gifts/transfers/{id}` | Required | Update transfer checklist status |
| `GET` | `/gifts/transfers/{id}` | Required | Get transfer detail + checklist |

**POST /gifts/evaluate**
```json
Request:
{
  "asset_id": "uuid",
  "recipient_member_id": "uuid",
  "gift_occasion": "GENERAL"
}

Response:
{
  "eligibility": "ELIGIBLE",
  "tax_status": "EXEMPT_RELATIVE",
  "applicable_rule": "Income Tax Act 1961, Section 56(2)(x)",
  "rule_version": "FA2024",
  "stamp_duty_minor_units": 150000,
  "registration_fee_minor_units": 30000,
  "total_transfer_cost_minor_units": 180000,
  "warnings": [],
  "recipient_cost_basis_minor_units": 60000000,
  "recipient_holding_period_start": "2022-03-10"
}
```

---

### 3.15 Connections & Consent

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/connections` | Required | List all connections (filterable by status) |
| `POST` | `/connections` | Required | Send connection request |
| `PATCH` | `/connections/{id}` | Required | Accept or reject connection |
| `DELETE` | `/connections/{id}` | Required | Revoke connection |
| `GET` | `/connections/{id}/consent` | Required | Get current consent configuration |
| `PATCH` | `/connections/{id}/consent` | Required | Update consent (fields + expiry) |
| `DELETE` | `/connections/{id}/consent` | Required | Revoke all consent (keep connection) |
| `GET` | `/connections/{id}/consent/audit` | Required | Get consent audit log |

**PATCH /connections/{id}/consent**
```json
Request:
{
  "permitted_fields": ["total_net_worth", "real_estate_assets", "financial_goals"],
  "consent_purpose": "Annual tax filing review",
  "consent_expires_at": "2027-01-01T00:00:00Z"
}

Response:
{
  "connection_id": "uuid",
  "grantee_name": "Vikram Sharma (CA)",
  "permitted_fields": ["total_net_worth", "real_estate_assets", "financial_goals"],
  "consent_purpose": "Annual tax filing review",
  "consent_granted_at": "2026-09-19T11:00:00Z",
  "consent_expires_at": "2027-01-01T00:00:00Z",
  "days_until_expiry": 104
}
```

---

### 3.16 Peers

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/peers` | Required | Get peer connections list |
| `GET` | `/peers/{user_id}/portfolio` | Required | Get peer's permitted portfolio data |
| `GET` | `/peers/benchmarks` | Required | Get peer benchmark comparisons |

**GET /peers/{user_id}/portfolio** — returns only the fields the peer has consented to share. All other fields are absent from the response (not null, not redacted — simply absent).

---

### 3.17 Advisory — Queries

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/queries` | Required | List queries (as asker or answerer) |
| `POST` | `/queries` | Required | Submit advisory query |
| `GET` | `/queries/{id}` | Required | Get query + thread |
| `POST` | `/queries/{id}/respond` | Advisor | Add response to thread |
| `PATCH` | `/queries/{id}/status` | Required | Transition query status |
| `GET` | `/queries/{id}/context` | Advisor | Get portfolio context for this query |

---

### 3.18 Advisory — Market Insights

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/insights` | Required | Get personalised insights feed |
| `POST` | `/insights` | Advisor | Publish new market insight |
| `PATCH` | `/insights/{id}` | Advisor | Edit own insight |
| `DELETE` | `/insights/{id}` | Advisor | Remove own insight |

---

### 3.19 Marketplace

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/marketplace` | Required | Browse all active listings |
| `POST` | `/marketplace` | Required | Create listing |
| `GET` | `/marketplace/{id}` | Required | Get listing detail |
| `PATCH` | `/marketplace/{id}` | Required | Update listing |
| `DELETE` | `/marketplace/{id}` | Required | Remove listing |
| `POST` | `/marketplace/{id}/interest` | Required | Express interest in a listing |

---

### 3.20 Credit

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/credit/evaluate` | Required | Build and evaluate anonymous borrower profile |
| `POST` | `/credit/submit` | Required | Submit to empanelled lenders |
| `GET` | `/credit/requests` | Required | List credit requests |
| `GET` | `/credit/requests/{id}/bids` | Required | Get lender bids for a request |
| `POST` | `/credit/requests/{id}/select-bid` | Required | Select bid + consent to identity disclosure |

---

### 3.21 Documents (Data Room)

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/documents` | Required | List all documents |
| `POST` | `/documents` | Required | Upload document (multipart/form-data) |
| `GET` | `/documents/{id}` | Required | Get document metadata |
| `GET` | `/documents/{id}/download` | Required | Get time-limited signed URL |
| `DELETE` | `/documents/{id}` | Required | Soft-delete document |

**POST /documents (multipart form)**
```
Fields:
  file: (binary)
  document_type: "TITLE_DEED"
  linked_asset_id: "uuid" (optional)
  document_date: "2022-03-10" (optional)
  document_expiry: null (optional)

Response (201):
{
  "document_id": "uuid",
  "document_type": "TITLE_DEED",
  "storage_key": "users/uuid/documents/uuid.pdf",
  "file_size_bytes": 1245302,
  "mime_type": "application/pdf",
  "scan_status": "PENDING"
}
```

---

### 3.22 Settings

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/settings` | Required | Get user settings |
| `PATCH` | `/settings` | Required | Update settings |
| `PATCH` | `/settings/2fa` | Required | Enable/disable 2FA |
| `GET` | `/settings/audit-log` | Required | Get settings change audit log |

---

## 4. Rate Limits

| Endpoint Group | Limit |
|---|---|
| Auth endpoints | 10 requests / minute / IP |
| Read endpoints (GET) | 120 requests / minute / user |
| Write endpoints (POST, PATCH, DELETE) | 60 requests / minute / user |
| File upload (`POST /documents`) | 10 uploads / minute / user |
| Export (`POST /users/me/export`) | 1 request / 24 hours / user |
| Credit submission | 5 submissions / day / user |

Rate limit exceeded: `429 Too Many Requests` with header `Retry-After: <seconds>`

---

## 5. Field Naming Conventions

| Rule | Example |
|---|---|
| All JSON fields: `snake_case` | `attributed_value_minor_units` |
| All monetary fields end in `_minor_units` | `net_worth_minor_units` |
| All percentage fields end in `_pct` | `ownership_split_pct` |
| All datetime fields end in `_at` | `created_at`, `consent_expires_at` |
| All date-only fields end in `_date` | `purchase_date`, `signature_date` |
| Boolean fields: plain adjective | `is_partial`, `is_active`, `has_more` |
| UUID foreign keys: `{entity}_id` | `portfolio_id`, `asset_id`, `user_id` |

---

## 6. Shared Response Types

### UserSummary
```json
{
  "user_id": "uuid",
  "display_name": "Yatish Karkera",
  "is_investor": true,
  "is_advisor": false,
  "active_role": "INVESTOR"
}
```

### AssetSummary
```json
{
  "asset_id": "uuid",
  "name": "Karjat Plot",
  "asset_type": "REAL_ESTATE",
  "asset_category": "REAL_ESTATE",
  "gross_value_minor_units": 75000000,
  "ownership_split_pct": 100.0,
  "attributed_value_minor_units": 75000000,
  "unrealised_gain_minor_units": 15000000,
  "verification_level": "VERIFIED",
  "staleness_status": "CURRENT",
  "valuation_as_of": "2026-06-01T00:00:00Z"
}
```

### Provenance
```json
{
  "as_of": "2026-09-19T10:00:00Z",
  "calculation_version": "v1.3",
  "source_ids": ["uuid1", "uuid2"],
  "is_partial": false,
  "performance_basis": "ESTIMATED"
}
```

---

*Next document: [03_Database_Schema.md](./03_Database_Schema.md)*
