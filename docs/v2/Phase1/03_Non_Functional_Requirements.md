# Phase 1 — Non-Functional Requirements (NFRs)

> **OOSE Phase:** Requirements Elicitation
> **Purpose:** Defines the quality constraints — how well the system must do what it does. These are engineering constraints that span all functional areas.
> **Notation:** `NFR-[CATEGORY]-[NNN]`
> **Status:** Draft

---

## Overview

Non-functional requirements are organized into eight categories. Each requirement is tagged with a priority:
- **MUST** — a launch blocker; if not met, the system is not acceptable for production
- **SHOULD** — important; must be met within the first operational quarter
- **COULD** — desirable for long-term excellence

---

## 1. Performance

| ID | Priority | Requirement |
|---|---|---|
| NFR-PERF-001 | MUST | The Net Worth Dashboard SHALL render with complete data (net worth, asset allocation, top movers, alerts) in under **2 seconds** on a standard broadband connection (>10 Mbps), measured from the API response to first interactive paint. |
| NFR-PERF-002 | MUST | All CRUD operations (add asset, log transaction, update liability) SHALL respond with a success or error within **1 second** under normal load (≤100 concurrent users). |
| NFR-PERF-003 | MUST | The XIRR and TWRR calculations SHALL complete within **3 seconds** for portfolios with up to 1,000 transactions. For portfolios with >1,000 transactions, results MAY be served from a pre-computed cache (refreshed on portfolio change). |
| NFR-PERF-004 | MUST | `FinancialSnapshot` capture (background job triggered on portfolio change) SHALL complete within **30 seconds** of the triggering event. |
| NFR-PERF-005 | SHOULD | Stale valuation and consent expiry background jobs SHALL complete a full sweep in under **5 minutes** regardless of the total user count at V1 scale. |
| NFR-PERF-006 | MUST | The document (Data Room) upload process SHALL support files up to **25 MB** per file. Uploads SHALL display progress feedback in the UI. |
| NFR-PERF-007 | SHOULD | API responses for paginated list endpoints (asset list, transaction history) SHALL respond in under **500ms** for pages of up to 50 records. |
| NFR-PERF-008 | SHOULD | The mobile app (V2) SHALL achieve Lighthouse performance scores of ≥85 on a simulated mid-range Android device on a 4G connection. This is a forward constraint on API payload design. |

---

## 2. Scalability

| ID | Priority | Requirement |
|---|---|---|
| NFR-SCALE-001 | MUST | The V1 architecture SHALL support up to **1,000 registered users** and **10,000 assets** without database schema changes or re-architecture. |
| NFR-SCALE-002 | SHOULD | The system SHALL be designed so that the Calculation Engine layer (FastAPI + Celery workers) can be **horizontally scaled** (adding more worker instances) to handle increased load without modifying application code. |
| NFR-SCALE-003 | SHOULD | The database schema SHALL avoid table designs that cause lock contention on high-frequency operations (e.g., the `FinancialSnapshot` append-only table must not block asset reads). |
| NFR-SCALE-004 | COULD | The system COULD support multi-region deployment in V2 to reduce latency for users outside the primary India AWS region (`ap-south-1`). |

---

## 3. Reliability & Availability

| ID | Priority | Requirement |
|---|---|---|
| NFR-REL-001 | MUST | The production system SHALL target **99.5% monthly uptime** (≤3.6 hours downtime/month). Planned maintenance windows SHALL be communicated at least 24 hours in advance. |
| NFR-REL-002 | MUST | All database transactions involving financial data (asset updates, transaction logging, inheritance allocation) SHALL be **ACID-compliant**. Partial writes that leave the database in an inconsistent state are not acceptable. |
| NFR-REL-003 | MUST | The `Transaction` and `FinancialSnapshot` tables SHALL be **append-only**. No `DELETE` or `UPDATE` operations are permitted on these tables in normal operation. Any corrective action is done via a new correcting record. |
| NFR-REL-004 | MUST | The system SHALL perform **daily automated database backups** in production. Backups SHALL be retained for a minimum of 30 days. Point-in-time recovery SHALL be available for the preceding 7 days. |
| NFR-REL-005 | MUST | If the external Authentication Provider (Supabase Auth) is unavailable, the system SHALL fail gracefully — displaying a clear error message and preventing access, rather than degrading to an insecure bypass. |
| NFR-REL-006 | MUST | If the object storage service (Data Room) is unavailable, the system SHALL continue to serve all portfolio data. Document download/upload functionality SHALL be disabled with a clear user-facing message. Uploads SHALL NOT be silently discarded. |
| NFR-REL-007 | SHOULD | The system SHOULD implement a **circuit breaker pattern** for all external dependencies (auth provider, future market data APIs). If a dependency fails repeatedly, the circuit opens and the fallback behavior activates without further retries causing cascading load. |
| NFR-REL-008 | MUST | Background jobs (snapshot capture, consent expiry, stale valuation check) SHALL implement **retry logic** with exponential backoff. Failed jobs SHALL be logged with sufficient detail to diagnose the cause. |

---

## 4. Security

| ID | Priority | Requirement |
|---|---|---|
| NFR-SEC-001 | MUST | All network communication between the client and server SHALL use **TLS 1.2 or higher**. HTTP-only endpoints SHALL redirect to HTTPS and SHALL NOT serve financial data. |
| NFR-SEC-002 | MUST | All data at rest in the database and object storage SHALL be **encrypted**. For PostgreSQL on AWS RDS, this means AES-256 encryption at the storage level. |
| NFR-SEC-003 | MUST | **No monetary values SHALL be stored or transmitted as floating-point numbers.** All monetary fields in the API, database, and calculation engines SHALL use integers (minor units in paise). This is enforced by Pydantic validators and database CHECK constraints. |
| NFR-SEC-004 | MUST | The system SHALL implement **Row-Level Security** logic at the application service layer: a user can only read or write their own data. No user can read another user's portfolio, estate plan, or transactions unless an active, non-expired, field-level consent grant exists. |
| NFR-SEC-005 | MUST | **Field-level consent evaluation** SHALL occur server-side before any data is included in an API response. The client SHALL never receive data and decide whether to display it; all access control decisions are made at the server. |
| NFR-SEC-006 | MUST | API keys, database credentials, and JWT secrets SHALL NEVER be committed to version control. Environment-specific secrets SHALL be managed via a secrets manager (AWS Secrets Manager in production; `.env` file for local development with `.env` in `.gitignore`). |
| NFR-SEC-007 | MUST | The system SHALL implement **rate limiting** on all authentication and high-impact write endpoints to mitigate brute-force and denial-of-service attacks. |
| NFR-SEC-008 | MUST | Documents stored in the Data Room SHALL never be accessible via a direct, permanent public URL. All document access SHALL require a **time-limited signed URL** (≤60 minutes by default). |
| NFR-SEC-009 | MUST | The system SHALL implement **CORS** policy, allowing API requests only from known frontend origins (the web app domain in staging and production). |
| NFR-SEC-010 | MUST | All user-facing input SHALL be **validated and sanitized** on the server side. The frontend may validate for UX, but the API SHALL NOT trust client-side validation. SQL injection, XSS, and CSRF protections SHALL be active. |
| NFR-SEC-011 | SHOULD | The system SHOULD log all access attempts to sensitive data (Financial Resume generation, consent grant/revoke, will document access) with: actor, action, timestamp, and outcome — in an immutable audit log. |
| NFR-SEC-012 | MUST | Credit module borrower profiles SHALL be verified for **re-identification risk** before being shared with any lender. The system SHALL not share information if the combination of fields makes the user uniquely identifiable within the platform's user base. |
| NFR-SEC-013 | SHOULD | The system SHOULD implement **dependency vulnerability scanning** in the CI pipeline (e.g., `pip audit` for Python, `npm audit` for JavaScript) and block deployments if high-severity vulnerabilities are detected in production dependencies. |

---

## 5. Privacy & Data Governance

| ID | Priority | Requirement |
|---|---|---|
| NFR-PRIV-001 | MUST | The system SHALL maintain an **immutable consent audit log** for every data sharing event: grantor user ID, grantee user ID, exact fields permitted, consent purpose, granted-at timestamp, expires-at timestamp, and any revocation timestamp. This log is the legal evidence of consent. |
| NFR-PRIV-002 | MUST | Users SHALL be able to **export all their personal and financial data** in a structured, machine-readable format (JSON) within 72 hours of a request. This supports compliance with India's Digital Personal Data Protection (DPDP) Act 2023 right-of-access obligations. |
| NFR-PRIV-003 | MUST | The system SHALL support **account deletion with data retention** handling: personal identifiers (name, email, phone, PAN) are purged immediately upon verified account closure; financial transaction records are retained for 7 years as required by Indian income tax regulations; all records are fully anonymised post-retention. |
| NFR-PRIV-004 | MUST | Financial data of Indian users SHALL be stored in servers **located within India** (`ap-south-1` AWS region, Mumbai) from the production launch. Staging environments may use non-India regions during internal testing only. |
| NFR-PRIV-005 | MUST | The system SHALL NOT use or share user financial data for any commercial purpose (targeted advertising, third-party data sales) without explicit, separate, revocable consent that is distinct from the service agreement. |
| NFR-PRIV-006 | MUST | Advisor-matched recommendations SHALL be based **solely on the user's actual portfolio data and stated needs**. Commercial payments from advisors SHALL NOT influence which advisors appear in search results or what `AdvisorMatchReason` is shown. Any commercial arrangement shall be disclosed separately. |
| NFR-PRIV-007 | MUST | The Credit module's anonymous borrower profile SHALL pass through a **re-identification risk check** (see FR-CREDIT-007). The system SHALL not share profiles that fail this check without the user acknowledging the risk. |

---

## 6. Regulatory & Compliance

| ID | Priority | Requirement |
|---|---|---|
| NFR-REG-001 | MUST | The system SHALL ensure that **only users with verified advisor credentials** (`CredentialVerificationStatus = VERIFIED`) can receive field-level consent grants from Investors for the purpose of providing financial advice. Unverified advisors can only receive a connection, not data access. |
| NFR-REG-002 | MUST | All **gift tax exemption and taxability calculations** SHALL be based on the current version of the Indian Income Tax Act (Section 56(2)(x)) as configured by the System Administrator. The system SHALL store the rule version and effective date alongside every gift evaluation. |
| NFR-REG-003 | MUST | All **inheritance default share calculations** SHALL reference the applicable Indian personal law (Hindu Succession Act, Indian Succession Act, or personal law as determined by the user's declared religion/community). The system SHALL disclose which law is being applied. |
| NFR-REG-004 | MUST | The Credit module's **lender matching** SHALL only include RBI-regulated institutions (scheduled commercial banks, RBI-registered NBFCs). The system SHALL not facilitate lending by unregistered entities. |
| NFR-REG-005 | SHOULD | The system SHOULD implement record-keeping that satisfies Section 285BA of the Income Tax Act requirements for Statement of Financial Transactions (SFT) if the platform is classified as a reporting financial institution in future. |
| NFR-REG-006 | SHOULD | All **legal and tax rule data** (gift rules, stamp duty rates, succession shares) SHALL be stored with: jurisdiction, `rule_effective_date`, `rule_version`, and a `professional_review_required` flag indicating whether the rule is settled law or subject to interpretation. |
| NFR-REG-007 | MUST | The system SHALL NOT present any **investment recommendation** to users. Analysis, benchmarks, and peer comparisons are informational tools. The system SHALL include appropriate disclaimers that it is not providing SEBI-regulated investment advice. |

---

## 7. Usability & Accessibility

| ID | Priority | Requirement |
|---|---|---|
| NFR-UX-001 | MUST | All currency values displayed in the UI SHALL use the **Indian numbering format**: ₹1,47,32,500 for large values, ₹75,000 for smaller values. The lakh (1,00,000) and crore (1,00,00,000) conventions SHALL be used in all labels and charts. |
| NFR-UX-002 | MUST | All dates displayed SHALL use the **DD MMM YYYY** format (e.g., 19 Sep 2026) to avoid DD/MM/YYYY vs. MM/DD/YYYY ambiguity. |
| NFR-UX-003 | MUST | The system SHALL display all monetary changes with **colour coding**: green for positive (net worth increase, inflow), red for negative (net worth decrease, outflow). Colour shall never be the only differentiator — a symbol (+/-) or label shall also be used (accessibility). |
| NFR-UX-004 | MUST | The system SHALL provide **meaningful empty states** on all data-driven pages. An Investor who has just registered and has no assets SHALL see instructional UI, not blank or error states. |
| NFR-UX-005 | MUST | When a calculation cannot be completed due to insufficient data (e.g., XIRR requires at least one transaction), the system SHALL display an explicit message explaining what data is needed and provide a direct call to action (e.g., "Log your first transaction to see returns"). |
| NFR-UX-006 | MUST | The UI SHALL display **staleness warnings** whenever data used in a displayed metric is older than the configured threshold for that asset class. The warning SHALL identify which specific data is stale, not just a generic alert. |
| NFR-UX-007 | SHOULD | The UI SHALL meet **WCAG 2.1 Level AA** accessibility standards: sufficient colour contrast ratios, keyboard navigability of all interactive elements, ARIA labels on all form controls and charts. |
| NFR-UX-008 | MUST | The UI SHALL be fully functional on the following desktop browsers: Chrome (latest), Firefox (latest), Safari (latest), Edge (latest). |
| NFR-UX-009 | SHOULD | The UI SHOULD be **responsive** — while optimized for desktop (1280px+), it should be usable on tablet screens (768px+) without horizontal scrolling. |
| NFR-UX-010 | MUST | Error messages shown to the user SHALL be written in plain English, describing what went wrong and what the user can do. Technical error codes or stack traces SHALL NEVER be shown to end users. |

---

## 8. Maintainability & Extensibility

| ID | Priority | Requirement |
|---|---|---|
| NFR-MAINT-001 | MUST | The system SHALL enforce a **strict separation of concerns**: API route handlers contain no business logic; all business logic lives in service/engine classes; ORM models contain no business logic. Route handlers call services; services call engines and repositories. |
| NFR-MAINT-002 | MUST | All **financial calculation functions** (XIRR, TWRR, amortization, funding gap, etc.) SHALL have dedicated unit tests with known inputs and expected outputs. Tests SHALL cover: normal case, minimum data case, edge cases (zero transactions, 100% ownership, 0% ownership), and error cases (insufficient data for XIRR). |
| NFR-MAINT-003 | MUST | The database schema SHALL use **Alembic migrations**. No manual schema modifications are permitted. Every schema change must be captured in a versioned migration file and applied via the migration tool. |
| NFR-MAINT-004 | MUST | The system SHALL use **Conventional Commits** for all commit messages. The CI pipeline SHALL reject commits that do not follow the `type(scope): subject` format. |
| NFR-MAINT-005 | MUST | All API endpoints SHALL be **documented in OpenAPI 3.0** format, auto-generated by FastAPI. The OpenAPI spec SHALL be the single source of truth for frontend developers and future mobile developers. |
| NFR-MAINT-006 | SHOULD | The backend code SHALL achieve a **minimum test coverage of 80%** (line coverage) across the service/engine layer. The CI pipeline SHALL fail if coverage drops below this threshold. |
| NFR-MAINT-007 | MUST | All **legal rules** (gift rules, stamp duty rates, succession defaults) SHALL be stored in the database (the `GiftRule` and `LegalRule` tables), NOT hardcoded in application logic. Updating a tax rule SHALL require only a database record change, not a code deployment. |
| NFR-MAINT-008 | MUST | The **V2 API integration points** (External Financial APIs: AA, CDSL, market feeds) SHALL be represented as defined service interfaces (abstract classes/protocols in Python, interfaces in TypeScript). The V1 manual-entry implementation fulfils these interfaces. V2 implementation replaces them without changing callers. |
| NFR-MAINT-009 | SHOULD | The project SHALL maintain a `CHANGELOG.md` following the Keep a Changelog format, updated with every release. |
| NFR-MAINT-010 | MUST | The entire local development environment SHALL be startable with a single command (`make dev` or `docker compose up`) with no pre-installed dependencies beyond Docker and Git. |

---

## 9. Deployment & Operations

| ID | Priority | Requirement |
|---|---|---|
| NFR-OPS-001 | MUST | Every commit to the `develop` branch SHALL automatically trigger the CI pipeline (lint, type check, test, build). No broken builds are allowed to persist on `develop` for more than 2 hours. |
| NFR-OPS-002 | MUST | Deployment to the **staging environment** SHALL be fully automated on successful merge to `develop`. No manual steps required beyond code review and merge. |
| NFR-OPS-003 | MUST | Deployment to the **production environment** SHALL require a manual approval gate (via GitHub Actions environment approval), even when CI passes. |
| NFR-OPS-004 | MUST | **Database migrations** in staging and production SHALL be applied as part of the automated deployment process, before the new application version starts serving traffic. Failed migrations SHALL halt the deployment automatically. |
| NFR-OPS-005 | MUST | The system SHALL log all API errors at ERROR level with: timestamp, endpoint, HTTP method, status code, user ID (anonymized), and a request correlation ID. Logs SHALL NOT contain sensitive financial data (amounts, account numbers). |
| NFR-OPS-006 | SHOULD | The system SHOULD integrate with an error tracking service (Sentry) to capture and alert on unhandled exceptions in both the backend and the frontend. |
| NFR-OPS-007 | MUST | Application secrets (database credentials, JWT secrets, Supabase keys, AWS credentials) SHALL be injected as environment variables at runtime. They SHALL NEVER be embedded in Docker images, application code, or configuration files committed to version control. |
| NFR-OPS-008 | SHOULD | The system SHOULD implement health check endpoints (`GET /health` returning `200 OK` with service status) for use by the cloud platform's load balancer and monitoring tools. |

---

*Next document: [04_India_Legal_Rules_Catalogue.md](./04_India_Legal_Rules_Catalogue.md)*
