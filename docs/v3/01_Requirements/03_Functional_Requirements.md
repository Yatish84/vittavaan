# Functional Requirements

## Conventions

- `MUST` is required for the first customer beta unless marked `GATED`.
- `SHOULD` is expected unless a documented trade-off defers it.
- Every requirement will later link to use cases, API/schema elements and automated acceptance evidence.

## Identity and application authorization

| ID | Priority | Requirement |
|---|---|---|
| FR3-IAM-001 | MUST | Every protected request shall carry an auth-core access token validated for signature, issuer, audience, time claims and revocation. |
| FR3-IAM-002 | MUST | The system shall idempotently map an authenticated subject to one local principal without copying credentials, factors or refresh tokens. |
| FR3-IAM-003 | MUST | The bootstrap response shall contain only the principal’s permitted people, households, scopes, preferences and enabled features. |
| FR3-IAM-004 | MUST | Authentication alone shall never grant access to another person’s financial records. |
| FR3-IAM-005 | MUST | The system shall distinguish owner, administrator, viewer, dependant/guardian and future professional authority. |
| FR3-IAM-006 | MUST | Denials shall avoid confirming the existence of resources outside the caller’s scope. |
| FR3-IAM-007 | MUST | Logout, session management, MFA, recovery and identity closure UI shall link to or invoke auth-core contracts rather than duplicate them. |

## People, households, ownership and grants

| ID | Priority | Requirement |
|---|---|---|
| FR3-HH-001 | MUST | A user shall create a household and add people who may or may not have logins. |
| FR3-HH-002 | MUST | A holding shall be recorded once with one or more effective-dated person ownership allocations totaling exactly 100%. |
| FR3-HH-003 | MUST | Household totals shall count a shared holding once; person views shall use the applicable ownership allocation. |
| FR3-HH-004 | MUST | Household relationship shall not grant visibility; access shall require an explicit scoped grant. |
| FR3-HH-005 | MUST | Grants shall record grantor, grantee, scope, level, purpose, start, expiry and revocation. |
| FR3-HH-006 | MUST | Only an owner may authorize an action committing that owner’s holding share. |
| FR3-HH-007 | MUST | A household administrator may maintain only the records and processes permitted by their active grant. |
| FR3-HH-008 | MUST | The system shall support totals-only, read, document-read and manage levels without exposing hidden data to the client. |
| FR3-HH-009 | SHOULD | A minor approaching majority shall generate a dated review checklist, not an automatic authority transfer. |

## Catalogue, holdings and valuations

| ID | Priority | Requirement |
|---|---|---|
| FR3-HOLD-001 | MUST | Every asset class and subtype listed in the operator PDF shall be selectable and recordable. |
| FR3-HOLD-002 | MUST | Priority-1 types shall capture and validate the rich class-specific fields defined by the v3 coverage catalogue. |
| FR3-HOLD-003 | MUST | Long-tail types shall use versioned validated subtype attributes while retaining all universal holding invariants. |
| FR3-HOLD-004 | MUST | Monetary values shall use integer minor units and ISO currency; rates and percentages shall use fixed-precision decimals. |
| FR3-HOLD-005 | MUST | Valuations shall be append-only events containing value, method, source, as-of time, confidence and verification level. |
| FR3-HOLD-006 | MUST | The current displayed value shall be selected from valuation history by a documented policy rather than stored as an unaudited overwrite. |
| FR3-HOLD-007 | MUST | Staleness shall be evaluated by class/method policy and shown with the last valid as-of time. |
| FR3-HOLD-008 | MUST | Pledge, lien, collateral, exit restriction and liquidity-window facts shall appear consistently wherever the holding is used. |
| FR3-HOLD-009 | MUST | Derivative notional and contingent exposure shall not be included in net worth as if they were market value. |
| FR3-HOLD-010 | MUST | User estimates shall be labelled and excluded from verified-only totals. |
| FR3-HOLD-011 | MUST | Holdings shall link to documents, transactions, income streams, commitments, liabilities and goals without duplicating the underlying fact. |

## Liabilities, transactions and cash flow

| ID | Priority | Requirement |
|---|---|---|
| FR3-LEDGER-001 | MUST | Every liability type in the operator PDF shall be recordable, including contingent guarantees and court/tax obligations. |
| FR3-LEDGER-002 | MUST | Direct liabilities shall be separated from contingent obligations in totals and presentation. |
| FR3-LEDGER-003 | MUST | A liability shall support principal/outstanding, rate type, benchmark/reset, schedule, lender, dates, security and source where applicable. |
| FR3-LEDGER-004 | MUST | Transactions shall be append-only; correction shall use a reversing/correcting entry linked to the original. |
| FR3-LEDGER-005 | MUST | Cash flow shall distinguish external contributions/withdrawals from income, expense, purchase, sale, debt service and internal transfer. |
| FR3-LEDGER-006 | MUST | Internal transfers shall not double-count household income or spending. |
| FR3-LEDGER-007 | MUST | Income streams shall support observed receipts, cadence, payer, linked holding/person and reliability without presenting forecasts as facts. |
| FR3-LEDGER-008 | MUST | Amortization schedules shall be generated from explicit inputs and reconciled against observed payments. |

## Imports, sources and reconciliation

| ID | Priority | Requirement |
|---|---|---|
| FR3-IMPORT-001 | MUST | Beta shall support manual entry and controlled CSV/document-assisted imports. |
| FR3-IMPORT-002 | MUST | Imported rows shall enter an isolated staging area and require validation/mapping before ledger commit. |
| FR3-IMPORT-003 | MUST | Import jobs shall be idempotent and detect exact and probable duplicates. |
| FR3-IMPORT-004 | MUST | Partial failures shall identify failed rows without discarding valid staged work or prior ledger facts. |
| FR3-IMPORT-005 | MUST | Ownership, classification, currency and source must be resolved before a staged financial fact can commit. |
| FR3-IMPORT-006 | MUST | OCR/extraction may propose values but shall never change the ledger without human confirmation. |
| FR3-IMPORT-007 | MUST | Connector consent, health, last success and failure fields shall exist even while live connector adapters are disabled. |
| FR3-IMPORT-008 | GATED | Live connectors may activate only after vendor, consent, reconciliation, security and operations approval. |

## Documents and provenance

| ID | Priority | Requirement |
|---|---|---|
| FR3-DOC-001 | MUST | Documents shall attach to domain records; any folder presentation shall be derived. |
| FR3-DOC-002 | MUST | Uploads shall remain quarantined until malware scanning completes successfully. |
| FR3-DOC-003 | MUST | Downloads shall require authorization and a short-lived signed URL; object keys shall not authorize access. |
| FR3-DOC-004 | MUST | Document metadata shall include owner, type, checksum, source, dates, verification state, linked records and supersession. |
| FR3-DOC-005 | MUST | Superseded documents shall remain traceable under retention policy rather than being silently overwritten. |
| FR3-DOC-006 | MUST | Every read, copy, grant and download of sensitive documents shall create authorized audit evidence. |

## Net worth and wealth experience

| ID | Priority | Requirement |
|---|---|---|
| FR3-WEALTH-001 | MUST | Net worth shall equal attributed current assets minus included attributed liabilities for the selected scope and as-of policy. |
| FR3-WEALTH-002 | MUST | Every displayed aggregate shall include as-of, scope, source/provenance summary, completeness and verification basis. |
| FR3-WEALTH-003 | MUST | Trend charts shall preserve gaps where required and shall not silently interpolate failed/missing source periods. |
| FR3-WEALTH-004 | MUST | Movement components shall reconcile to the total change or disclose an explicit unreconciled remainder. |
| FR3-WEALTH-005 | MUST | Verified share shall be weighted by attributed value, not record count. |
| FR3-WEALTH-006 | MUST | The application shall provide the Net worth, Assets, Liabilities, Cash flow, Data room, Consents, Holding, First run and Account setup states represented in the Assets and liabilities wireframe. |
| FR3-WEALTH-007 | MUST | Liquidity views shall use availability windows/restrictions and shall not equate illiquid estimated value with accessible cash. |
| FR3-WEALTH-008 | MUST | Empty, partial, stale, failed, negative and insufficient-data states shall be explicit and actionable. |

## Analysis and planning

| ID | Priority | Requirement |
|---|---|---|
| FR3-AN-001 | MUST | XIRR, TWRR, benchmark return and attribution contribution shall be calculated and labelled separately. |
| FR3-AN-002 | MUST | XIRR shall be withheld when complete dated external cash flows are unavailable. |
| FR3-AN-003 | MUST | Attribution components shall reconcile to the displayed total under a documented method. |
| FR3-AN-004 | MUST | Performance shall disclose whether inputs are verified, documented, self-declared, stale or partial. |
| FR3-AN-005 | MUST | Where shown in the wireframe, the system shall compare outcomes including and excluding Level-1 holdings. |
| FR3-AN-006 | MUST | Benchmark/news data shall not display without an approved source, licence and as-of provenance. |
| FR3-AN-007 | SHOULD | Look-through exposure shall combine direct holdings, fund constituents, employer equity and related income without prescribing action. |
| FR3-PLAN-001 | MUST | A goal shall link to specific holdings and preserve versioned target, date, contribution and assumption facts. |
| FR3-PLAN-002 | MUST | Goal status shall account for both projected amount and liquidity availability by the target date. |
| FR3-PLAN-003 | MUST | Selling/unlinking a funding holding shall identify affected goals before confirmation. |
| FR3-PLAN-004 | MUST | Calculators shall prefill from permitted ledger facts, expose every input/assumption and state exclusions. |
| FR3-PLAN-005 | MUST | Saved scenarios shall preserve immutable inputs, assumptions, output version and calculation date. |
| FR3-PLAN-006 | MUST | Life-event prompts shall arise only from recorded dated facts, never inferred private events. |

## Settings, privacy and audit

| ID | Priority | Requirement |
|---|---|---|
| FR3-SET-001 | MUST | Users shall configure display currency/format, accessibility preferences and notification choices without changing stored financial facts. |
| FR3-SET-002 | MUST | The system shall display who can access each relevant scope and when that access expires. |
| FR3-SET-003 | MUST | Users shall request a structured export covering all data owned by Vittavaan and receive status/completion evidence. |
| FR3-SET-004 | MUST | Account closure shall coordinate immediate access revocation with retention, anonymization and auth-core identity workflows. |
| FR3-SET-005 | MUST | Material actions shall create immutable audit evidence containing actor, authority, subject, action, purpose, outcome, time and correlation ID. |
| FR3-SET-006 | MUST | Audit/log payloads shall exclude passwords, tokens, full identifiers, document contents and unnecessary financial values. |
| FR3-SET-007 | SHOULD | Revenue transparency shall show fees attributable to the user when gated commercial modules eventually activate. |

## Gated future capabilities

| ID | Requirement |
|---|---|
| FR3-GATE-001 | Financial-resume claims shall be recipient-specific, banded, expiring, revocable and derived only from permitted verification levels. |
| FR3-GATE-002 | Ask shall retrieve only authorized ledger/document facts, delegate arithmetic to deterministic engines, cite sources and refuse advice/prediction. |
| FR3-GATE-003 | Credit shall release identity only to one selected regulated lender after explicit purpose-bound consent and successful re-identification controls. |
| FR3-GATE-004 | Marketplace workflows shall never represent Vittavaan as valuer or custodian and shall use approved external escrow/payment arrangements. |
| FR3-GATE-005 | Estate/gift/inheritance workflows shall use versioned professionally reviewed legal rules and owner/executor authority. |
| FR3-GATE-006 | Advisor discovery/ratings/payments shall activate only under approved credential, conflict, engagement and regulatory policies. |

