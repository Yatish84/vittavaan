# Vittavaan — Agent Knowledge Transfer Document

> **Purpose:** Complete handover document for any AI agent continuing this project. Read this document in full before taking any action. It contains everything you need to understand the project, the work already done, the conventions you MUST follow, and exactly what to do next.
> **Last Updated:** 2026-09-19
> **Phases Complete:** Phase 1, Phase 2, Phase 3, Phase 4
> **Phase In Progress:** None (clean handover point)
> **Phase Next:** Phase 5 — Implementation

---

## 1. Project Identity

**Name:** Vittavaan (ਵਿੱਤਵਾਨ — "one who is wealthy" in Punjabi)

**What it is:** A desktop-first personal wealth management and estate planning web application for Indian investors. It is NOT a trading platform, robo-advisor, or brokerage. It is a private portfolio ledger + estate intelligence tool.

**Who it is for:**
- **Primary:** High-net-worth Indian investors managing a complex, multi-asset portfolio (equity, real estate, alternatives, liabilities)
- **Secondary:** SEBI-registered investment advisors who serve those investors

**The core problem it solves:** Most Indian HNI investors own a mix of liquid assets, multiple properties, collections, and loans — but have no single tool that shows them their true net worth (ownership-attributed, not gross), tracks gift transfers under Indian law, manages the estate plan, and securely shares data with advisors — all in one place.

**V1 Scope (non-negotiable):**
1. Net Worth Dashboard
2. Portfolio Ledger (assets, liabilities, transactions)
3. Estate Planning (household, inheritance allocation, will, gift transfers)
4. Connections & Consent (advisor data sharing with ABAC gate)

**V1 Exclusions:** No trading/order execution. No live market data feeds (manual entry only). No bank account linking (Account Aggregator API is V2). No mobile app (React Native is V2). No robo-advisory.

---

## 2. Developer Context

- **Solo developer + AI agents** — Yatish Karkera is the sole developer. Documentation must be detailed enough to serve as team-level specs.
- **Build workflow:** Local (Docker) → test locally → push to staging (Railway) → repeat per feature chunk
- **Do NOT wait** until the whole app is done before staging deployment
- **India locale everywhere** — all monetary values use Indian numbering (lakh/crore), ₹ symbol, financial year Apr–Mar
- **Data residency:** India (AWS `ap-south-1` Mumbai for production)

---

## 3. OOSE Methodology Being Followed

This project uses **Object-Oriented Software Engineering (OOSE / Jacobson)** structured phases:

```
Phase 1 — Requirements     ✅ COMPLETE (5 documents)
Phase 2 — Analysis         ✅ COMPLETE (3 documents)
Phase 3 — System Design    ✅ COMPLETE (6 documents)
Phase 4 — Object Design    ✅ COMPLETE (4 documents)
Phase 5 — Implementation   🔲 NOT STARTED — THIS IS WHAT YOU DO NEXT
Phase 6 — Testing          🔲 NOT STARTED
Phase 7 — Deployment       🔲 NOT STARTED
```

**All documents go in `/Users/yatishkarkera/Documents/Projects/vittavaan/docs/v2/`**
**NEVER modify** the old `docs/` folder (non-v2). It is read-only reference.

---

## 4. Repository Structure

```
/Users/yatishkarkera/Documents/Projects/vittavaan/
├── docs/                          ← READ-ONLY reference (old agent's work)
│   ├── class-architecture.md      ← Original class design (useful reference)
│   ├── metric_dictionary_by_page.md  ← 1085-line metric reference (critical)
│   ├── Analysis.md, System_Design.md, Object_Design.md  ← reference only
│   └── Wireframe/                 ← 19 HTML wireframe files (V1 screens)
└── docs/v2/                       ← ALL NEW WORK GOES HERE
    ├── README.md                  ← Master document index (keep updated)
    ├── Tech_Stack.md              ← Confirmed tech stack
    ├── Phase1/
    │   ├── 01_Actors_and_System_Boundary.md
    │   ├── 02_Functional_Requirements.md
    │   ├── 03_Non_Functional_Requirements.md
    │   ├── 04_India_Legal_Rules_Catalogue.md
    │   └── 05_Use_Cases.md
    ├── Phase2/
    │   ├── 01_ECB_Object_Model.md
    │   ├── 02_Sequence_Diagrams.md
    │   └── 03_Domain_Glossary.md
    └── Phase3/
        ├── 01_Architecture_Overview.md
        ├── 02_API_Design.md
        ├── 03_Database_Schema.md
        ├── 04_Auth_and_Authorization.md
        ├── 05_Event_and_Background_Jobs.md
        └── 06_Data_Room_Architecture.md
```

---

## 5. Tech Stack (Confirmed — Do Not Deviate)

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12 + FastAPI + Pydantic v2 + SQLAlchemy 2.0 (async) + Alembic + asyncpg |
| **Background jobs** | Celery 5.x + Redis (broker + result backend) |
| **Financial math** | `numpy-financial` (XIRR, NPV), `scipy` (TWRR numerical methods) |
| **Auth** | Supabase Auth (JWT issuance, OTP) — FastAPI verifies the JWT |
| **Frontend** | React 19 + TypeScript + Vite (NOT Next.js) |
| **State** | TanStack Query (React Query) |
| **Routing** | React Router v6 |
| **UI** | Tailwind CSS + shadcn/ui (Radix UI) |
| **Charts** | Recharts |
| **Forms** | React Hook Form + Zod |
| **Database** | PostgreSQL 16 (Docker local, RDS prod) |
| **Object Storage** | Supabase Storage (local/staging), AWS S3 `ap-south-1` (prod) |
| **Testing (backend)** | pytest-asyncio + httpx |
| **Testing (frontend)** | Vitest + Testing Library |
| **Linting** | ruff + mypy (backend), ESLint + TypeScript strict (frontend) |
| **Local infra** | Docker Compose (`make dev`) |
| **Staging** | Railway (auto-deploy from `develop` branch) |
| **Production** | AWS ECS Fargate + RDS + ElastiCache + S3 + CloudFront + Route 53 |
| **IaC** | Terraform in `infrastructure/terraform/` |
| **Mobile (V2 only)** | React Native + Expo |

**Monorepo structure:**
```
vittavaan/
├── backend/app/{api,services,models,schemas,db,core}/
├── frontend/src/{pages,components,hooks,lib}/
├── packages/types/       ← shared TypeScript types
├── infrastructure/terraform/
├── docs/v2/
├── docker-compose.yml
└── Makefile
```

---

## 6. Critical Non-Negotiable Conventions

These are fundamental rules that MUST be followed in all documentation, schemas, API design, and code. Violating any of these is a serious error.

### 6.1 Integer Money (Paise)
- **ALL monetary values are stored and calculated as integers in paise (minor units)**
- `1 INR = 100 paise`
- All DB columns storing money: `BIGINT`, never `FLOAT` or `NUMERIC`
- All Pydantic schemas: `MinorUnits = Annotated[int, Field(ge=0)]`
- All API JSON fields end in `_minor_units`
- The frontend converts paise → ₹ for display using `formatINR()` utility
- No floating-point arithmetic ever used for money

### 6.2 Ownership Before Aggregation
- `AttributedValue = GrossValue × (ownership_split_pct / 100)`
- Never add gross values directly to net worth
- A property worth ₹1 Cr owned 60% → contributes ₹60L to net worth, not ₹1 Cr
- `ownership_split_pct` is a float 0–100 with a DB CHECK constraint

### 6.3 XIRR ≠ TWRR (Never Interchangeable)
- **XIRR** = Money-weighted return. Answers: "how much did MY money grow?" (accounts for when I deployed capital)
- **TWRR** = Time-weighted return. Answers: "how well did the assets perform independently of my timing?"
- These must always be labelled separately in UI and API. Never use one label for the other.

### 6.4 Provenance on Every Metric
Every API response for a calculated metric MUST include:
```json
"provenance": {
  "as_of": "2026-09-19T10:00:00Z",
  "calculation_version": "v1.3",
  "source_ids": ["uuid1", "uuid2"],
  "is_partial": false,
  "performance_basis": "ESTIMATED"
}
```
`is_partial = true` must be disclosed to the user whenever data is incomplete. Never silently present partial data as complete.

### 6.5 Append-Only Tables
`transactions` and `financial_snapshots` are NEVER updated or deleted. Database rules enforce this:
```sql
CREATE RULE no_update_transactions AS ON UPDATE TO transactions DO INSTEAD NOTHING;
CREATE RULE no_delete_transactions AS ON DELETE TO transactions DO INSTEAD NOTHING;
```
Corrections are done by logging a new entry with `is_correction_for = original_transaction_id`.

### 6.6 Legal Rules in DB, Not Code
All gift tax rules, stamp duty rates, succession defaults are stored in the `gift_rules` DB table with `rule_effective_date` and `rule_version`. A Finance Act change = a new DB record, NOT a code change.

### 6.7 Indian Numbering System
Display: `₹1,47,32,500` (not `₹14,732,500`)
- 3 digits rightmost group, then 2-digit groups
- Use `Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' })` in TypeScript

### 6.8 Indian Financial Year
FY runs **April 1 → March 31**. All tax-related aggregations (gift limits, LTCG windows) use Indian FY, not calendar year.

### 6.9 ABAC Consent Gate (Protection Proxy)
ALL access to one user's data by another user goes through `ConsentAndMarketplaceEngine`. The consent gate:
1. Checks: accepted connection exists
2. Checks: `consent_expires_at > now()`
3. Checks: requested field is in `connection.permissions` JSONB array
4. Strips any field not in the permissions list from the response
Never bypass this gate. Never make access decisions on the client side.

### 6.10 Mermaid Diagrams
The user explicitly requested Mermaid syntax for all diagrams. Use:
- `classDiagram` for class/entity diagrams
- `sequenceDiagram` for object interactions
- `flowchart TD` / `flowchart LR` for flow diagrams
- `erDiagram` for ER diagrams
- `stateDiagram-v2` for state machines
Do NOT use PlantUML, Lucidchart, or ASCII art.

---

## 7. Key Domain Knowledge

### Asset Model
Three concrete asset types sharing a base:
- **LiquidAsset** — bank accounts, FDs, equity, mutual funds, ETFs, PPF, EPF, NPS, crypto, bonds
- **RealEstateAsset** — land, residential, commercial properties; has title/encumbrance/mutation status
- **AlternativeAsset** — philately, fine art, numismatics, physical gold, vintage items; requires appraisal

Database: **Joined Table Inheritance** — `assets` base table + `liquid_assets`, `real_estate_assets`, `alternative_assets` extension tables (joined on `asset_id`).

### Estate Planning Domain
- **EstatePlan** → has one optional **Will** → has many **InheritanceAllocation** records
- **HouseholdMember** = registered family member who can be a beneficiary
- **GiftTransfer** = tracked gift of an asset with Indian law compliance checking
- **GiftRule** = versioned DB record of Indian law (Section 56(2)(x), stamp duty rates etc.)
- Key alert: `NomineeMismatch` — a nominee ≠ legal heir in Indian law; the system flags this
- `EstateCoveragePct` = % of net worth that has been allocated to beneficiaries

### Calculation Engines (8 total)
| Engine | What it computes |
|---|---|
| `WealthAndOwnershipEngine` | Net worth, attributed values, asset class breakdown, waterfall |
| `ValuationAndVerificationEngine` | Staleness, verified wealth %, verification level |
| `CashFlowAndDebtEngine` | Monthly surplus, DSR, amortization, income/expense groups, savings rate |
| `PerformanceAndAttributionEngine` | XIRR, TWRR, max drawdown, attribution by class, benchmark comparison |
| `PlanningAndScenarioEngine` | Goal funding gap, invest-vs-prepay scenarios, upcoming financial events |
| `ConsentAndMarketplaceEngine` | ABAC gate, advisor matching, re-identification risk, credit profile |
| `EstatePlanningControl` + `GiftRuleEngine` | Inheritance allocation, estate coverage, will coverage, gift eligibility, stamp duty |
| `PeerBenchmarkingControl` | Cohort comparison (min 10 members for anonymity) |

### Connection & Consent Model
- A `Connection` is a mutual social link (like a LinkedIn connection)
- Data access is separate: `connection.permissions` JSONB array lists permitted field identifiers
- `connection.consent_expires_at` — all consents have a mandatory expiry
- Consent audit logs are immutable (S3 Object Lock in production)
- Celery Beat runs `expire_stale_consents` every 15 minutes

### Credit Module
- Investor's portfolio data → anonymised `BorrowerProfile` → submitted to lenders
- Anonymised attributes: age band (not exact), city tier (not city), income type (not amount), net worth band, security coverage, DSR
- `check_reidentification_risk()` runs before submission; HIGH risk gets a user warning
- Identity only disclosed to a specific lender after investor explicitly consents to that lender's bid

---

## 8. Phase 1 Summary (What Was Created)

| Document | Key Content |
|---|---|
| `01_Actors_and_System_Boundary.md` | 6 actors (Investor, Advisor, Household Member, Admin, Auth Provider, External API), Actor-Use Case matrix, in/out of scope boundary |
| `02_Functional_Requirements.md` | ~130 requirements in `FR-[DOMAIN]-[NNN]` format across 13 domains (AUTH, PROF, ASSET, LIAB, TXN, DASH, PLAN, ESTATE, NET, MKT, CREDIT, DOCS, SETT) |
| `03_Non_Functional_Requirements.md` | ~60 NFRs across 9 categories (PERF, SCALE, REL, SEC, PRIV, REG, UX, MAINT, OPS) |
| `04_India_Legal_Rules_Catalogue.md` | 7 rule sets: gift tax (S.56(2)(x)), HSA succession, stamp duty, capital gains carry-over, credit regulations, SEBI RIA rules, data retention; each with DB encoding instructions |
| `05_Use_Cases.md` | 17 use cases in Cockburn format across 8 domains (AUTH, PORT, DASH, ESTATE, NET, MKT, CREDIT, SETT) |

## 9. Phase 2 Summary (What Was Created)

| Document | Key Content |
|---|---|
| `01_ECB_Object_Model.md` | Full ECB decomposition: 5 Mermaid `classDiagram` blocks across 4 modules, 12 Control objects with full method signatures, 25 Boundary objects mapped to wireframes, complete Mermaid ER diagram, design decisions (JTI, JSONB, append-only, correcting-entry pattern) |
| `02_Sequence_Diagrams.md` | 11 Mermaid `sequenceDiagram` blocks (UC-AUTH-001, UC-PORT-001, UC-PORT-004, UC-DASH-001, UC-DASH-002, UC-ESTATE-002, UC-NET-002, UC-NET-003 consent gate, UC-ESTATE-003 gift transfer, UC-CREDIT-001, UC-SETT-001) + 2 background process diagrams |
| `03_Domain_Glossary.md` | 71 terms in 8 sections: Assets & Valuation, Performance & Return, Estate & Legal, Connections & Consent, Advisory & Marketplace, Credit, Financial Planning, System & Infrastructure |

## 10. Phase 3 Summary (What Was Created)

| Document | Key Content |
|---|---|
| `01_Architecture_Overview.md` | 5-tier Mermaid flowchart, 7 subsystem decomposition, request lifecycle sequence, local/Railway/AWS hardware mapping, synchronous vs. async operation split, RBAC + ABAC access control architecture, V2 adapter extension points |
| `02_API_Design.md` | 22 endpoint groups covering all FRs, every `METHOD /path` with auth requirement, complete JSON request/response examples for key endpoints, rate limits, field naming conventions, pagination design, provenance response structure |
| `03_Database_Schema.md` | Full DDL for: `users`, `portfolios`, `assets` (base), `liquid_assets`, `real_estate_assets`, `alternative_assets`, `liabilities`, `transactions` (append-only + rules), `financial_snapshots` (append-only), `connections`, `inheritance_allocations` (trigger for 100% cap), `gift_rules`, `documents`; ER diagram; all 30+ enums; abbreviated column specs for 14 additional tables; migration strategy |
| `04_Auth_and_Authorization.md` | Supabase Auth delegation flow (full Mermaid sequence), JWT claims structure, token storage security (in-memory not localStorage), RBAC FastAPI dependency code, RBAC matrix flowchart, ABAC decision flowchart with Python filter code, 2FA state diagram, session lifecycle, admin access scope, security headers, CORS config |
| `05_Event_and_Background_Jobs.md` | 10 Celery jobs fully specced: `capture_financial_snapshot`, `invalidate_performance_cache`, `expire_stale_consents`, `send_consent_expiry_warning`, `check_stale_valuations`, `send_in_app_notification`, `send_email_notification`, `compile_user_data_export`, `generate_peer_benchmarks`, `anonymise_closed_account`; Celery Beat schedule config; staleness thresholds table; monitoring metrics and alert thresholds; idempotency design |
| `06_Data_Room_Architecture.md` | Storage key conventions, document upload flow with ClamAV scan (Mermaid sequence), signed URL download flow (Mermaid sequence), allowed MIME types, consent audit log immutability design (S3 Object Lock, 7-year COMPLIANCE mode), soft-delete lifecycle, estate plan document checklist |

---

## 11. Phase 4 Summary (What Was Created)

| Document | Key Content |
|---|---|
| `Phase4/01_Calculation_Engine_Contracts.md` | Contract IDs, mathematical formulas in precise notation for all 8 engines: WealthAndOwnershipEngine (attributed value floor, net worth identity), ValuationAndVerificationEngine (verified wealth %, staleness thresholds table), CashFlowAndDebtEngine (surplus, DSR, reducing-balance EMI), PerformanceAndAttributionEngine (XIRR via Brent's method pseudocode, TWRR geometric linking, max drawdown running-peak algorithm, attribution reconciliation), PlanningAndScenarioEngine (SIP future value, funding gap, invest-vs-prepay NPV crossover), ConsentAndMarketplaceEngine (3-gate ABAC, re-identification risk scoring), EstatePlanningControl (estate coverage %, nominee mismatch), PeerBenchmarkingControl (cohort criteria, why median not mean, min-10 anonymity) |
| `Phase4/02_Design_Patterns.md` | 7 patterns with Mermaid `classDiagram` and Python code skeletons: Strategy (interchangeable XIRR/TWRR and valuation algorithms), Protection Proxy (ConsentAndMarketplaceEngine strips fields before return), Facade (DashboardFacade runs 5 engines in `asyncio.gather`), Observer (portfolio write → Celery task → FinancialSnapshot), Adapter (ManualEntryAdapter V1 → NSEMarketDataAdapter V2 via Protocol), Template Method (BaseCalculationEngine: validate → execute → attach_provenance), Repository (all DB access behind Protocol; SQLAlchemy as default implementation) |
| `Phase4/03_Class_Interfaces.md` | Shared types module (`MinorUnits`, `Percentage`, all `StrEnum` definitions), Python `Protocol` classes for all 10 Control/Facade objects, Protocol classes for 6 repositories (`AssetRepository`, `TransactionRepository` append-only, `FinancialSnapshotRepository` insert-only, `ConnectionRepository`, `GiftRuleRepository`, `DocumentRepository`), key Pydantic schemas: `DashboardPayload`, `NetWorthResult`, `XirrResult`, `TwrrResult`, `FundingGapResult`, `PrepayScenarioResult`, `GiftEvaluationResult`, `AccessDecision`, `ConsentUpdateRequest`, `AssetCreateRequest`, `TransactionCreateRequest`, `AllocationValidation`, `BorrowerProfile`, domain dataclasses (`Asset`, `HouseholdMember`, `IndianFinancialYear`, `DateRange`, `YearMonth`), exception hierarchy (`VittavaanError`, `CalculationError`, `PermissionDenied`, `ValidationError`, `NotFoundError`) |
| `Phase4/04_Legal_Rules_Engine_Design.md` | Why a rules engine (vs hardcoded), `gift_rules` table full column semantics, seed SQL for initial rules (S.56(2)(x) relative/non-relative/specific-occasion, Maharashtra stamp duty), complete Section 56(2)(x) relative definition with Mermaid flowchart, gift eligibility decision tree (BLOCKED if pledged/title-disputed/inactive), gift tax evaluation decision tree (occasion → relative → ₹50k cumulative check → TAXABLE_PARTIAL/FULL), stamp duty state-lookup algorithm with flowchart, rule lookup algorithm with fallback hierarchy (exact → ANY relationship → central law), annual cumulative gift check SQL, cost basis carryover logic, Finance Act version management procedure (expire old + insert new row), UI legal disclaimer text, 7 open questions flagged for professional review |

---

## 12. Phase 5 — What To Do Next

Phase 5 is **Implementation Planning**. It converts the OOSE design documents into actionable developer artifacts: a sprint-by-sprint roadmap, the exact monorepo layout, and coding standards.

Create the following 3 documents in `docs/v2/Phase5/`:

---

### Document 1: `01_Sprint_Roadmap.md`

**What it should contain:**

A feature-gated sprint plan. The key principle: **each sprint must produce a working, testable, deployable increment** — not a partial feature.

**Sprint sequencing rationale:**
- Start with auth + settings (everything depends on being able to log in)
- Then portfolio core (assets + transactions — the data backbone)
- Then dashboard (first user-visible value)
- Then estate planning (depends on portfolio being complete)
- Then connections + consent (depends on user base having data)
- Credit and marketplace last (lowest priority in V1)

**Sprint definitions should include:**
- Sprint number and name
- Objectives (1-3 sentences)
- User stories covered (referencing `FR-[DOMAIN]-[NNN]` IDs from Phase 1)
- Backend endpoints to implement (from Phase 3/02)
- Frontend pages/components to build (referencing wireframe HTML files)
- Database migrations required (from Phase 3/03)
- Background jobs activated (from Phase 3/05)
- Definition of Done (specific tests/checks that must pass)
- Staging deployment milestone (Y/N for each sprint)

**Suggested sprint breakdown (7 sprints for V1):**
1. Sprint 1: Project scaffolding, auth flow, user + settings CRUD
2. Sprint 2: Portfolio — asset CRUD (all 3 types), liability CRUD
3. Sprint 3: Transactions + FinancialSnapshot (WealthEngine + daily snapshot job)
4. Sprint 4: Dashboard — net worth, trend chart, asset breakdown, alerts
5. Sprint 5: Estate planning — household, estate plan, inheritance allocation, gift transfers
6. Sprint 6: Connections, consent, peer view (ABAC gate)
7. Sprint 7: Advisory queries, market insights, credit profile

---

### Document 2: `02_Project_Structure.md`

**What it should contain:**

The exact directory layout for the monorepo, with a description of what goes in each folder.

```
vittavaan/
├── backend/
│   └── app/
│       ├── api/          ← FastAPI route handlers (thin — no business logic)
│       ├── services/     ← All 8 engines + Facade (business logic here)
│       │   ├── strategies/  ← Strategy pattern implementations
│       │   └── protocols.py ← All Protocol definitions
│       ├── repositories/ ← Repository implementations (SQLAlchemy)
│       ├── models/       ← SQLAlchemy ORM models
│       │   └── domain.py ← Pure domain dataclasses (no ORM)
│       ├── schemas/      ← Pydantic v2 input/output schemas
│       ├── jobs/         ← Celery task definitions
│       ├── adapters/     ← MarketDataAdapter (and future adapters)
│       ├── core/
│       │   ├── auth.py       ← JWT verification, UserContext
│       │   ├── config.py     ← Settings (pydantic-settings)
│       │   ├── dependencies.py ← FastAPI DI wiring
│       │   ├── exceptions.py ← VittavaanError hierarchy
│       │   └── types.py      ← MinorUnits, Percentage, all enums
│       └── tests/        ← pytest-asyncio tests, mirrors app/ structure
├── frontend/
│   └── src/
│       ├── pages/        ← One folder per page (Dashboard, Portfolio, etc.)
│       ├── components/   ← Shared reusable components
│       │   ├── ui/       ← shadcn/ui base components (do not edit)
│       │   └── domain/   ← Vittavaan-specific components (Charts, AssetCard, etc.)
│       ├── hooks/        ← Custom React hooks (usePortfolio, useNetWorth, etc.)
│       ├── lib/
│       │   ├── api.ts    ← Typed API client (generated from OpenAPI)
│       │   ├── formatters.ts ← formatINR(), formatPct(), formatDate()
│       │   └── utils.ts
│       └── types/        ← TypeScript types (mirroring backend schemas)
├── packages/
│   └── types/            ← Shared TypeScript types (frontend + future mobile)
├── infrastructure/
│   └── terraform/
│       ├── modules/      ← Reusable modules (rds, ecs, s3, etc.)
│       ├── staging/      ← staging env vars
│       └── production/   ← production env vars
├── docs/v2/              ← All spec docs
├── docker-compose.yml
├── Makefile              ← Common commands: make dev, make test, make migrate
└── .github/workflows/    ← CI/CD pipelines
```

Also include:
- File naming conventions (snake_case for Python, PascalCase for React components, camelCase for hooks)
- Module import rules (services never import from api; repositories never import from services)
- `__init__.py` strategy (explicit imports only — no wildcard `*`)

---

### Document 3: `03_Code_Standards.md`

**What it should contain:**

**Backend (Python):**
- `ruff` configuration (line length 100, select E/F/I/N/UP/RUF, ignore list)
- `mypy` strict mode settings (`strict = true`, known exceptions)
- Required docstring format (Google style, not NumPy or reStructuredText)
- Import order (stdlib → third-party → local, enforced by ruff)
- Type annotation rules (no bare `dict`, no `Any` without `# type: ignore` comment explaining why)
- Money handling rules (no float arithmetic on monetary values — `MinorUnits` type alias everywhere)
- Git commit format: `type(scope): message` — types: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`

**Frontend (TypeScript):**
- `tsconfig.json` strict mode settings
- ESLint rules (react-hooks, import order, no-implicit-any)
- Component file structure (exports at bottom, hooks above JSX, types at top)
- Indian number formatting: always use `Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' })` — never custom formatter
- Tailwind class ordering (enforced by `prettier-plugin-tailwindcss`)
- API call pattern: always via TanStack Query hooks — never raw `fetch` in components

**Testing standards:**
- Minimum coverage targets (80% backend, 70% frontend)
- One test file per source file, mirroring directory structure
- Test naming: `test_<what>_<when>_<expected>` e.g., `test_calculate_xirr_insufficient_data_returns_error`
- All engine tests must use `InMemory*Repository` — no DB in unit tests
- Integration tests use a dedicated test database (separate schema, rolled back after each test)

---

## 13. After Phase 5 — Remaining Work

### Phase 6 — Testing
- `Phase6/01_Test_Strategy.md` — testing pyramid (unit: engines/services, integration: API+DB, E2E: Playwright), coverage targets, CI gate
- `Phase6/02_Test_Personas.md` — 3 realistic investor profiles with specific portfolio data for seeding test scenarios
- `Phase6/03_Security_Test_Plan.md` — ABAC bypass attempts, JWT manipulation, SQL injection, rate limit checks, IDOR tests

### Phase 7 — Deployment
- `Phase7/01_Infrastructure_as_Code.md` — full `docker-compose.yml`, Terraform modules for AWS ECS + RDS + ElastiCache + S3
- `Phase7/02_CI_CD_Pipeline.md` — GitHub Actions: lint → test → build → push image → deploy to Railway (staging) / ECS (prod)
- `Phase7/03_Monitoring_and_Observability.md` — structured logging format, Celery metric emission, CloudWatch alarms, error alerting



Phase 4 is **Object Design**. It fills the gap between Phase 3 (system-level design) and Phase 5 (implementation). It specifies the exact mathematical contracts of each calculation engine, the design pattern implementations with code skeletons, and the final class interfaces that developers will implement directly.

Create the following 4 documents in `docs/v2/Phase4/`:

---

### Document 1: `01_Calculation_Engine_Contracts.md`

**What it should contain:**

For each of the 8 calculation engines, define:
1. **Mathematical formula** (in LaTeX where appropriate) — exact algorithm, not just "compute XIRR"
2. **Input preconditions** — what the caller must ensure before calling (e.g., "at least one external cash flow must exist")
3. **Output guarantees** — what the caller can rely on (e.g., "always returns integer minor units", "returns null with error code if convergence fails")
4. **Error cases** — specific named error codes (e.g., `INSUFFICIENT_DATA`, `CONVERGENCE_FAILED`, `NO_VALUATIONS_IN_PERIOD`)
5. **Calculation version** — the version tag embedded in every output

Engines to cover:
- `WealthAndOwnershipEngine` — net worth, attributed value, household aggregation, asset class breakdown, waterfall
- `ValuationAndVerificationEngine` — verified wealth %, staleness calculation, verification level elevation logic
- `CashFlowAndDebtEngine` — surplus, DSR, savings rate, amortization (reducing balance method — standard in India)
- `PerformanceAndAttributionEngine` — XIRR (Newton-Raphson/Brent), TWRR (sub-period geometric linking), max drawdown, attribution
- `PlanningAndScenarioEngine` — future value with inflation (FV formula), funding gap, invest-vs-prepay NPV comparison, crossover return
- `ConsentAndMarketplaceEngine` — ABAC filter, re-identification risk score, advisor match relevance
- `EstatePlanningControl` — estate coverage %, will coverage, default intestacy share (HSA Class I)
- `GiftRuleEngine` — gift tax eligibility, stamp duty calculation, annual cumulative check, cost basis carryover

**Key formulas to include precisely:**
- `AttributedValue = GrossValue × (ownership_pct / 100)` → **integer**, floor at end
- `XIRR`: solve `Σ(Cₜ / (1+r)^(tₜ-t₀)) = 0` using Brent's method
- `TWRR`: `(1+r₁) × (1+r₂) × ... × (1+rₙ) - 1` where each `rᵢ = (Eᵢ - Bᵢ - Cᵢ) / Bᵢ`
- `MaxDrawdown = (Trough - Peak) / Peak × 100`
- `FundingGap = TargetAmountNominal - ProjectedPortfolioValue`
- `DSR = (TotalMonthlyEMI / MonthlyGrossIncome) × 100`
- `EstateCoverage = AllocatedAssetValue / TotalAttributedNetWorth × 100`

---

### Document 2: `02_Design_Patterns.md`

**What it should contain:**

Specify each design pattern used, with:
1. **Which pattern** (name)
2. **Where it's applied** (specific class or interface)
3. **Why this pattern** (problem it solves here)
4. **Python code skeleton** showing the interface and key method signatures
5. **Mermaid diagram** showing the pattern structure in Vittavaan's context

Patterns to document:
- **Strategy** — `PerformanceAndAttributionEngine` and `ValuationAndVerificationEngine` use interchangeable calculation strategies (e.g., `XirrStrategy`, `TwrrStrategy`; `CircleRateValuation`, `ComparableValuation`)
- **Protection Proxy** — `ConsentAndMarketplaceEngine` as the proxy for all cross-user data access
- **Facade** — `DashboardFacade` aggregates 5+ engine calls into one response
- **Observer** — Asset write → triggers `FinancialSnapshot` capture (via Celery event)
- **Adapter** — `ManualEntryAdapter` (V1) vs `NSEMarketDataAdapter` (V2) — same interface, swappable
- **Template Method** — `BaseCalculationEngine` defines the `calculate()` template with `validate_inputs()`, `execute()`, `attach_provenance()` steps
- **Repository** — `AssetRepository`, `TransactionRepository` abstract all DB access; services never query SQLAlchemy directly

---

### Document 3: `03_Class_Interfaces.md`

**What it should contain:**

Full Python type-annotated interface definitions for every class in the system. This is what a developer opens when implementing a class — it tells them exactly what the class must expose.

Structure:
1. **Service layer interfaces** — one for each of the 12 Control objects from Phase 2
2. **Repository interfaces** — one for each aggregate root (Portfolio, EstatePlan, Connection, Document)
3. **Schema definitions** — key Pydantic v2 input/output schemas for the most complex operations
4. **Enum definitions** — consolidated list of all Python enums (these map to DB CHECK constraints)

Format for each interface:
```python
class WealthAndOwnershipEngineProtocol(Protocol):
    """
    Contract for the WealthAndOwnershipEngine.
    All monetary return values are in minor units (paise).
    All percentage values are floats in [0.0, 100.0].
    """

    async def calculate_net_worth(
        self,
        portfolio_id: UUID,
        *,
        as_of: datetime | None = None,
    ) -> NetWorthResult: ...

    async def calculate_attributed_value(
        self,
        asset: Asset,
    ) -> int: ...  # always paise, always integer
```

Key schemas to include:
- `DashboardPayload` (full structure of `/dashboard` response)
- `NetWorthResult` (with provenance)
- `GiftEvaluationResult` (eligibility, tax_status, stamp_duty, checklist)
- `ConsentDecision` (allowed, reason, permitted_fields)
- `FundingGapResult` (target, projected, gap, goal_status)
- `XirrResult` and `TwrrResult` (with PerformanceBasis and provenance)
- `BorrowerProfile` (anonymised credit profile)

---

### Document 4: `04_Legal_Rules_Engine_Design.md`

**What it should contain:**

A detailed design of the `GiftRuleEngine` and how it evaluates Indian law rules at runtime. This is a critical design because rules change on every Finance Act amendment.

1. **Rule table data model** — how `GiftRule` records are structured, what the columns mean
2. **Rule lookup algorithm** — how the engine picks the right rule for a given transfer (jurisdiction + date + relationship + occasion)
3. **Rule evaluation flow** — step-by-step decision tree for:
   - Is the asset eligible for gifting? (Check pledge, asset type restrictions)
   - Is the recipient a "relative" under Section 56(2)(x)?
   - Is the gift occasion exempt?
   - If non-relative: is the cumulative annual value below ₹50,000?
   - Stamp duty: which state, which rate, donor/donee relationship applies?
   - Cost basis carryover: what acquisition cost does the recipient inherit?
4. **Version management** — how new Finance Act changes are added without breaking existing transfers
5. **The "relative" definition** — complete list of relationships that qualify as "relative" under Section 56(2)(x) (spouse, siblings, parents, siblings of parents, siblings of spouse, lineal ascendants/descendants and their spouses — NOT cousins, NOT friends)
6. **Mermaid flowchart** of the full gift eligibility decision tree

---

## 12. After Phase 4 — Planned Work

### Phase 5 — Implementation Planning
- Sprint roadmap (what to build in which order — start with auth + asset CRUD + dashboard, NOT estate first)
- Monorepo project structure with exact file naming conventions
- Code standards: ruff config, mypy strict mode settings, TypeScript strict config, commit message format

### Phase 6 — Testing
- Test strategy: unit (engines), integration (API + DB), E2E (Playwright)
- Test personas: 3 realistic investor profiles with specific portfolios for testing
- Security test plan: ABAC bypass attempts, SQL injection, JWT tampering

### Phase 7 — Deployment
- Docker Compose for local dev (full file)
- Railway deployment config
- GitHub Actions CI/CD pipeline
- Terraform modules for AWS production

---

## 13. Files to Read First (Priority Order)

If you have limited context budget, read in this order:

1. **This file** — you're reading it ✅
2. [`docs/v2/Phase4/03_Class_Interfaces.md`](./Phase4/03_Class_Interfaces.md) — all Protocol definitions, Pydantic schemas, enums
3. [`docs/v2/Phase2/01_ECB_Object_Model.md`](./Phase2/01_ECB_Object_Model.md) — all classes and their relationships
4. [`docs/v2/Phase3/03_Database_Schema.md`](./Phase3/03_Database_Schema.md) — DB tables and types
5. [`docs/v2/Phase3/02_API_Design.md`](./Phase3/02_API_Design.md) — API contracts
6. [`docs/v2/Phase4/01_Calculation_Engine_Contracts.md`](./Phase4/01_Calculation_Engine_Contracts.md) — exact math for all 8 engines
7. [`docs/v2/Phase2/03_Domain_Glossary.md`](./Phase2/03_Domain_Glossary.md) — exact term definitions
8. [`docs/metric_dictionary_by_page.md`](../metric_dictionary_by_page.md) — financial metric definitions (original reference)
9. [`docs/v2/Phase1/04_India_Legal_Rules_Catalogue.md`](./Phase1/04_India_Legal_Rules_Catalogue.md) — before working on estate/gift features

---

## 14. Tone and Working Style

- **Autonomous:** Yatish has explicitly asked the agent to make educated decisions and not wait for input on non-crucial matters. Only stop and ask if something is architecturally breaking or contradicts a stated preference.
- **Detailed:** Solo developer; documents must be detailed enough to serve as team-level specs. No hand-waving.
- **India-first:** All examples, monetary figures, legal references, date formats use Indian conventions.
- **Mermaid-first:** All diagrams use Mermaid syntax. No ASCII art, no external tools.
- **No mobile yet:** Desktop-first V1. Do not design for mobile unless explicitly asked.
- **Document location:** ALL new files go in `docs/v2/`. NEVER modify `docs/` (root).
- **Update the README:** After creating any new Phase directory and documents, update [`docs/v2/README.md`](./README.md) to mark them as `✅ Draft`.
- **Update this file:** After completing a phase, add a summary section here and update the Phase Next field and phase map at the top.

---

## 15. Open Items (Known Gaps to Be Aware Of)

| Item | Status | Notes |
|---|---|---|
| Tech Stack approval | Pending Yatish's explicit sign-off | `Tech_Stack.md` ends with "Approved by: [pending]" — continue anyway as the stack is well-reasoned and Yatish chose not to object when presented |
| India Legal Rules — professional review | Not done yet | `04_India_Legal_Rules_Catalogue.md` has a CAUTION block — items flagged `professional_review_required = true` need CA/Advocate review before implementation of those features |
| Use Cases for Planning, Will, Peers, Marketplace | Partial | `05_Use_Cases.md` notes at the bottom that UC-PLAN-001 through UC-NET-004 etc. are not yet written. These should be added in the next iteration before Phase 5 begins. |
| Notification table schema | Not in Phase 3 schema | `notifications` table is referenced in Phase 3 but not defined — add in sprint 3 as noted |
| Peer benchmark table schema | Not in Phase 3 schema | `peer_benchmarks` table referenced — add in sprint 4 as noted |
| ClamAV integration | Referenced in Data Room doc | Implementation detail for Phase 5 — referenced as async scan job |
| Gift tax — 7 open legal questions | Flagged in Phase 4 | See `Phase4/04_Legal_Rules_Engine_Design.md` Section 12 — unlisted equity FMV, crypto VDA treatment, and joint ownership scenarios need CA review before implementation |

---

*This document should be read completely before starting any work. Then proceed to Phase 5 — create `docs/v2/Phase5/` and follow the instructions in Section 12 above.*
