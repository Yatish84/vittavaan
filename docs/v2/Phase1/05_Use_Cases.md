# Phase 1 — Use Cases

> **OOSE Phase:** Requirements Elicitation
> **Purpose:** Detailed use cases for all major workflows in Vittavaan V1. Each use case specifies the actor, preconditions, complete happy path, exception flows, and exit condition.
> **Notation:** `UC-[DOMAIN]-[NNN]` — e.g., `UC-PORT-001`
> **Status:** Draft

---

## Reading This Document

Each use case follows the Cockburn format:
- **Use Case ID & Name** — stable identifier
- **Initiating Actor** — who starts this use case
- **Communicating Actors** — other actors involved
- **Priority** — `CORE` (V1 launch required), `IMPORTANT` (V1 desirable), `EXTENSION` (V2)
- **Entry Condition** — what must be true before this use case begins
- **Happy Path** — the steps when everything goes right
- **Exception Flows** — what happens when something goes wrong
- **Exit Condition** — what is true when the use case ends successfully
- **Business Rules** — which FR/legal rules govern this use case
- **System Objects Involved** — which entities, controls, and boundaries participate

---

## Domain 1: Authentication & Session

---

### UC-AUTH-001: Register and Authenticate

**Initiating Actor:** Unregistered User (becomes Investor or Advisor)
**Priority:** CORE

**Entry Condition:** The user has navigated to the Vittavaan application and is not authenticated.

**Happy Path:**
1. The user is presented with the Supabase Auth-provided registration/login screen.
2. The user registers using email + password, OR authenticates using phone OTP.
3. Supabase Auth validates the credentials and issues a signed JWT.
4. The JWT is sent to the Vittavaan API (`POST /api/v1/auth/session`).
5. The `AuthGatewayControl` verifies the JWT signature using the Supabase public key.
6. The system checks whether a `User` record exists for the `sub` (user ID) in the JWT.
   - **6a. New user:** A `User` record is created with `is_investor = true`, `is_advisor = false`. A blank `Portfolio`, `Setting`, and `EstatePlan` shell are created automatically.
   - **6b. Existing user:** The existing `User` record is fetched.
7. A `LocalSession` record is created with the session token and expiry.
8. The user is redirected to the Net Worth Dashboard.

**Exception Flows:**
- **E1 — Invalid JWT:** If the JWT signature verification fails (tampered token), the system returns `401 Unauthorized`. The user is returned to the login screen with an error message.
- **E2 — Supabase Auth unavailable:** If the auth provider cannot be reached, the system returns a `503 Service Unavailable` response with a user-facing message: "Authentication is temporarily unavailable. Please try again in a few minutes."
- **E3 — Expired JWT:** If the JWT has expired, the system returns `401 Unauthorized`. The frontend redirects the user to re-authenticate.

**Exit Condition:** The user is authenticated, a `LocalSession` is active, and the user's dashboard is loaded.

**Business Rules:** FR-AUTH-001, FR-AUTH-002, FR-AUTH-003, FR-AUTH-008

**Objects Involved:**
- Boundary: `LoginPage` (Supabase-hosted or SDK)
- Control: `AuthGatewayControl`
- Entity: `User`, `LocalSession`, `Portfolio`, `Setting`

---

### UC-AUTH-002: Switch Active Role Context

**Initiating Actor:** Dual-Role User (Investor + Advisor)
**Priority:** CORE

**Entry Condition:** The user is authenticated and has both `is_investor = true` and `is_advisor = true`.

**Happy Path:**
1. The user selects the "Switch to Advisor View" toggle in the navigation.
2. The system updates the active context in the `LocalSession` (no separate API call required — context is a UI state stored in the session).
3. The navigation changes to show Advisor-specific sections (marketplace listing management, open queries, published insights).
4. The user's personal portfolio data is still accessible but not the primary view.
5. To switch back, the user selects "Switch to Investor View."

**Exception Flows:**
- **E1 — Missing AdvisorProfile:** If `is_advisor = true` but no `AdvisorProfile` exists, the system prompts the user to complete the Advisor Profile setup before switching.

**Exit Condition:** The user is viewing the application in their selected role context.

**Business Rules:** FR-AUTH-009, FR-AUTH-010

---

## Domain 2: Portfolio — Assets

---

### UC-PORT-001: Add Liquid Asset

**Initiating Actor:** Investor
**Priority:** CORE

**Entry Condition:** The Investor is authenticated and viewing their Portfolio.

**Happy Path:**
1. The Investor selects "Add Asset" → "Liquid Asset."
2. The system presents the `AddAssetForm` with fields for: asset name, sub-type (bank account, equity, MF, FD, etc.), institution name, ticker/scheme code (optional), quantity, purchase price (in INR — converted to paise by the form), current value (if different from purchase price), purchase date, ownership percentage, currency, verification level (defaults to `SELF_DECLARED`), and notes.
3. The Investor completes and submits the form.
4. The system validates all inputs:
   - `ownership_split_pct` is between 0 and 100
   - `purchase_price_minor_units >= 0`
   - `current_value_minor_units >= 0`
   - Required fields are present (name, sub-type, purchase date)
5. A new `LiquidAsset` record is created and linked to the Investor's `Portfolio`.
6. The `WealthAndOwnershipEngine` calculates the attributed value: `current_value × (ownership_pct / 100)`.
7. A background job is queued to capture a new `FinancialSnapshot`.
8. The system returns the new asset record with its calculated attributed value.
9. The UI shows the asset in the Assets list with a success notification.

**Exception Flows:**
- **E1 — Invalid ownership percentage:** The system returns a `422 Unprocessable Entity` error: "Ownership percentage must be between 0% and 100%."
- **E2 — Negative monetary value:** The system returns a `422` error: "Asset values cannot be negative."
- **E3 — Missing required fields:** The system returns a `422` error identifying the missing field(s).
- **E4 — Snapshot job failure:** The background job fails. The asset is still saved. A retry is scheduled. The user sees the asset immediately; the dashboard may show a slightly stale net worth for up to 30 seconds.

**Exit Condition:** The new asset is saved, the portfolio is updated, and a net worth snapshot is queued.

**Business Rules:** FR-ASSET-001, FR-ASSET-002, FR-ASSET-003, FR-ASSET-004, FR-ASSET-005, FR-ASSET-006, NFR-SEC-003

---

### UC-PORT-002: Add Real Estate Asset

**Initiating Actor:** Investor
**Priority:** CORE

**Entry Condition:** The Investor is authenticated and viewing their Portfolio.

**Happy Path:**
1. The Investor selects "Add Asset" → "Real Estate Asset."
2. The system presents the `AddAssetForm` with Real Estate specific fields: property type (`LAND`, `RESIDENTIAL`, `COMMERCIAL`), location address, area (sq ft), price per sq ft (in INR), ownership percentage, purchase date, total acquisition cost (purchase price + stamp duty + registration + legal costs), valuation method (`CIRCLE_RATE`, `APPRAISAL`, `COMPARABLE`, `USER_ESTIMATE`), valuation as-of date, title verification status, encumbrance status, mutation status.
3. The Investor inputs the area and price per sq ft.
4. The system calculates gross valuation automatically: `gross_value = area_sqft × price_per_sqft_minor_units`.
5. The Investor confirms or overrides the calculated value.
6. The Investor submits the form.
7. Validation runs (same monetary and ownership checks as UC-PORT-001, plus area must be > 0).
8. The system creates a `RealEstateAsset` record.
9. Snapshot job is queued.

**Exception Flows:**
- **E1 — Zero area:** The system returns a `422` error: "Property area must be greater than zero."
- **E2 — Pledged asset flagged:** If the Investor marks the property as encumbered (pledged), the system displays a warning: "This property is encumbered. It cannot be gifted or listed on the marketplace while the encumbrance is active."

**Exit Condition:** The real estate asset is saved with its calculated valuation.

**Business Rules:** FR-ASSET-007, FR-ASSET-008, FR-ASSET-009, FR-LIAB-007

---

### UC-PORT-003: Add Alternative Asset

**Initiating Actor:** Investor
**Priority:** CORE

**Entry Condition:** The Investor is authenticated and viewing their Portfolio.

**Happy Path:**
1. The Investor selects "Add Asset" → "Alternative Asset."
2. The system presents the `AddAssetForm` with Alternative-specific fields: collection type (`PHILATELY`, `FINE_ART`, `NUMISMATICS`, `GOLD_PHYSICAL`, `UNLISTED_EQUITY`, `WINE`, `WATCHES`, `OTHER`), last appraisal date, appraiser name, purchase price, current estimated value, and notes.
3. The Investor submits the form.
4. Validation runs.
5. The system creates an `AlternativeAsset` record with `verification_level = SELF_DECLARED` (since alternative assets are inherently self-declared until an appraisal document is uploaded).
6. The `ValuationAndVerificationEngine` immediately checks: if `last_appraisal_date` is more than 365 days ago (or absent), the asset is flagged with `StalenessStatus = STALE`.
7. A `StaleDataWarning` is displayed on the asset card immediately upon creation if stale.

**Exception Flows:**
- **E1 — No appraisal date:** If the Investor leaves the appraisal date blank, the system accepts the asset but immediately flags it as requiring appraisal.

**Exit Condition:** The alternative asset is saved with its staleness status evaluated.

**Business Rules:** FR-ASSET-010, FR-ASSET-011, FR-ASSET-012

---

### UC-PORT-004: Log a Cash Flow Transaction

**Initiating Actor:** Investor
**Priority:** CORE

**Entry Condition:** The Investor is authenticated. (Assets and/or liabilities may or may not exist yet.)

**Happy Path:**
1. The Investor selects "Log Transaction."
2. The system presents the `LogTransactionForm` with: date, amount (INR, converted to paise), type (`INFLOW`, `OUTFLOW`, `BUY`, `SELL`, `RENT`, `DIVIDEND`, `INTEREST`, `EMI_PAYMENT`, `GIFT_OUT`, `GIFT_IN`), category (predefined list), optional link to a specific asset, and notes.
3. The Investor completes and submits the form.
4. The system validates: date is not in the future, amount > 0, type and category are valid enums.
5. A new `Transaction` record is appended to the ledger. The record is **immutable** — no future UPDATE or DELETE is permitted.
6. The cash flow aggregates (monthly inflow, outflow, surplus) are updated in the cached summary.
7. If the transaction is linked to an asset (e.g., a `BUY` for an equity holding), the system suggests updating the asset's cost basis and quantity.
8. A `FinancialSnapshot` background job is triggered.

**Exception Flows:**
- **E1 — Future date:** The system returns a `422` error: "Transaction date cannot be in the future."
- **E2 — Zero or negative amount:** The system returns a `422` error: "Transaction amount must be greater than zero."
- **E3 — Correction required:** If the Investor made an error, they cannot edit the transaction. The system presents a "Log a correcting entry" helper that pre-fills a reversing transaction.

**Exit Condition:** The transaction is permanently appended to the ledger, and the cash flow summary is updated.

**Business Rules:** FR-TXN-001, FR-TXN-002, NFR-REL-002, NFR-REL-003

---

## Domain 3: Dashboard & Analysis

---

### UC-DASH-001: View Net Worth Dashboard

**Initiating Actor:** Investor
**Priority:** CORE

**Entry Condition:** The Investor is authenticated.

**Happy Path:**
1. The Investor navigates to the Net Worth Dashboard.
2. The system's `DashboardFacade` makes a single aggregated API call.
3. The `WealthAndOwnershipEngine` computes:
   - `TotalAssets = Sum(attributed_value for all assets)`
   - `TotalLiabilities = Sum(outstanding_balance for all liabilities)`
   - `NetWorth = TotalAssets - TotalLiabilities`
4. The system retrieves the most recent and prior-month `FinancialSnapshot` to compute MoM changes.
5. The `ValuationAndVerificationEngine` calculates `VerifiedWealthPct` and identifies stale assets.
6. The system computes the net worth waterfall (equity gain, RE revaluation, fresh investment, loan repayment contribution).
7. Income and expense aggregates are computed from the current month's `Transaction` records.
8. "Worth a Look" alerts are generated: stale assets, fund overlaps, concentration risks, expiring consents.
9. All data is returned as a single JSON payload with provenance metadata (`as_of`, `calculation_version`, `verification_summary`).
10. The UI renders the dashboard with all sections.

**Exception Flows:**
- **E1 — No portfolio data:** If the Investor has no assets logged, the system displays an empty state with a "Get started" prompt and a link to add their first asset.
- **E2 — Stale valuations present:** The dashboard renders but the net worth figure is accompanied by a `PARTIAL_DATA` badge and a list of stale assets contributing to the figure.
- **E3 — FinancialSnapshot gap:** If there is no prior-month snapshot (e.g., the user just registered), MoM change is shown as "N/A — first month."
- **E4 — Background job backlog:** If the last snapshot is more than 1 hour old (job backlog), the dashboard shows the snapshot value with a "as of [time]" label and triggers a fresh recalculation in the background.

**Exit Condition:** The Investor views their current net worth with provenance, change data, verification status, and alerts.

**Business Rules:** FR-DASH-001, FR-DASH-002, FR-DASH-003, FR-DASH-004, FR-DASH-005, FR-DASH-006, NFR-PERF-001

---

### UC-DASH-002: View Portfolio Performance (XIRR & TWRR)

**Initiating Actor:** Investor
**Priority:** CORE

**Entry Condition:** The Investor is authenticated and has at least one `Transaction` record logged.

**Happy Path:**
1. The Investor navigates to the Analysis page and selects a time window (e.g., "3 Years").
2. The system queries all `Transaction` records in the window, plus the portfolio value at the start and end.
3. The `PerformanceAndAttributionEngine`:
   - Computes `PortfolioXIRR`: solves for the rate `r` such that the NPV of all cash flows and terminal value = 0 (Newton-Raphson or Brent's method).
   - Computes `PortfolioTWRR`: geometrically links sub-period returns neutralising external flow timing.
4. The engine also computes: max drawdown, drawdown start, trough date, recovery months.
5. A `BenchmarkReturn` for the selected benchmark (e.g., Nifty 500 TRI) is fetched (in V1, this is a manually maintained table; in V2, it is a market data feed).
6. The system returns both metrics with the `PerformanceBasis` flag (Verified / Estimated / Mixed).
7. The UI displays XIRR and TWRR side-by-side with labels explaining the difference.

**Exception Flows:**
- **E1 — Insufficient data for XIRR:** XIRR requires at least one external cash flow. If the user has only asset valuations but no `Transaction` records, the `PerformanceAndAttributionEngine` throws `InsufficientDataException`. The UI displays: "Log your first transaction to see money-weighted returns (XIRR)."
- **E2 — XIRR does not converge:** If the Newton-Raphson solver fails to converge (pathological cash flow pattern), the system returns `XIRR = null` with a flag `XIRR_CONVERGENCE_FAILED` and displays: "XIRR could not be calculated for this period. This can happen with unusual cash flow patterns — please contact support."
- **E3 — Estimated valuations present:** The performance is calculated but `PerformanceBasis = ESTIMATED`. The UI displays: "Return includes estimated property values. [View breakdown]" linking to Attribution.

**Exit Condition:** The Investor views XIRR and TWRR with their correct methodology labels and performance basis disclosure.

**Business Rules:** FR-DASH-007, FR-DASH-008, FR-DASH-009, FR-DASH-010, FR-DASH-014

---

## Domain 4: Estate Planning

---

### UC-ESTATE-001: Register a Household Member

**Initiating Actor:** Investor
**Priority:** CORE

**Entry Condition:** The Investor is authenticated and navigates to the Household page.

**Happy Path:**
1. The Investor selects "Add Household Member."
2. The system presents the form: first name, last name, relationship (enum), date of birth, optional contact email, optional PAN (masked for display).
3. The Investor submits.
4. Validation: relationship is a valid enum value; date of birth is not in the future and not unrealistically old (>120 years).
5. A new `HouseholdMember` record is created and linked to the Investor's `User`.
6. The household balance sheet is recalculated to include this member in the household view.

**Exception Flows:**
- **E1 — Duplicate member:** If a member with the same first name, last name, and date of birth already exists, the system warns: "This member may already be registered. Do you want to add them again?" (soft duplicate check — does not block).

**Exit Condition:** The household member is registered and appears in the household balance sheet and beneficiary selection lists.

**Business Rules:** FR-ESTATE-001, FR-ESTATE-002

---

### UC-ESTATE-002: Allocate Inheritance

**Initiating Actor:** Investor
**Priority:** CORE

**Entry Condition:** The Investor has an `EstatePlan`, at least one `HouseholdMember`, and at least one `Asset` in their portfolio.

**Happy Path:**
1. The Investor navigates to the Inheritance page and selects an asset to allocate.
2. The system displays the asset's current gross value and attributed value, and the current total allocation (initially 0%).
3. The Investor selects a household member from the list.
4. The Investor enters a percentage share and optional distribution conditions (text).
5. The system's `EstatePlanningControl` validates:
   - `percentage > 0`
   - `current_total_allocated(asset_id) + new_percentage <= 100.0`
6. If validation passes, a new `InheritanceAllocation` record is saved.
7. The system displays the updated allocation summary: which members have been allocated what percentage, and the remaining unallocated percentage.
8. The system recalculates the estate coverage: `EstateCoveragePct` updates.

**Exception Flows:**
- **E1 — Allocation exceeds 100%:** The system returns a `422` error: "This allocation would exceed 100% for this asset. Remaining unallocated: [X]%. Please enter a value of [X]% or less."
- **E2 — No household members registered:** The system displays an empty state: "No household members registered. [Add a household member] to begin allocating your estate."
- **E3 — Asset is jointly owned (ownership < 100%):** The system displays a warning: "You own [X]% of this asset. The allocation percentages apply to your [X]% share — beneficiaries receive their stated percentage of your ownership share."

**Exit Condition:** The `InheritanceAllocation` is recorded, the asset's allocation total is updated, and the estate coverage percentage is recalculated.

**Business Rules:** FR-ESTATE-009, FR-ESTATE-010, FR-ESTATE-011, Rule 2.3 (Nominee vs. Beneficiary)

---

### UC-ESTATE-003: Log a Gift Transfer

**Initiating Actor:** Investor
**Priority:** IMPORTANT

**Entry Condition:** The Investor has at least one asset eligible for gifting and at least one registered household member (or a specified external recipient).

**Happy Path:**
1. The Investor navigates to Gift Transfer and selects "New Gift."
2. The Investor selects the asset to be gifted (or specifies a cash amount).
3. The system's `GiftRuleEngine` immediately evaluates:
   - Is the asset eligible for gifting? (Checks pledged status, EPF/PPF restrictions, unvested ESOPs)
   - What is the relationship to the recipient?
   - Is the gift exempt or taxable under Section 56(2)(x)?
   - What stamp duty applies (for real estate)?
4. The system displays the gift evaluation: exemption status, applicable rule, stamp duty, registration fee, total transfer cost.
5. The Investor confirms the gift details and submits.
6. A `GiftTransfer` record is created with status `INITIATED`.
7. The system generates a Gift Transfer checklist: deed status → registration → mutation → portfolio update.
8. As the Investor completes each step, they update the checklist in the system.
9. When the Investor marks the transfer as legally complete (mutation done), the system prompts: "Would you like to update [asset name] ownership percentage to reflect the gift?"
10. If confirmed, the asset's `ownership_split_pct` is updated (or the asset is removed if 100% gifted).

**Exception Flows:**
- **E1 — Pledged asset:** The system blocks the gift initiation with a hard error: "This asset is pledged against a loan. It cannot be gifted while the encumbrance is active. Please clear the encumbrance first."
- **E2 — EPF/PPF/Unvested ESOP:** The system blocks with: "This asset type cannot be legally transferred by gift. [See rules]"
- **E3 — Non-relative above threshold:** The system warns (not blocks): "This gift to a non-relative may be taxable in the recipient's hands. Gift value: ₹[X]. Annual threshold: ₹50,000. Taxable amount: ₹[X]. The recipient should report this in their income tax return."
- **E4 — Incomplete checklist at month end:** The system sends an alert (if notifications enabled): "Your gift transfer for [asset] has a pending checklist item: [item]. Please update the status."

**Exit Condition:** The gift transfer is logged, the checklist is active, and the system tracks the transfer lifecycle until portfolio ownership is updated.

**Business Rules:** FR-ESTATE-012, FR-ESTATE-013, FR-ESTATE-014, FR-ESTATE-015, Rules 1.1–1.5, Rule 4.1

---

## Domain 5: Connections & Consent

---

### UC-NET-001: Send a Connection Request

**Initiating Actor:** Investor (or Advisor)
**Priority:** CORE

**Entry Condition:** The user is authenticated.

**Happy Path:**
1. The user searches the platform for another user by name or profession.
2. The search results display: name, role (Investor/Advisor), credential verification status (for advisors), and a "Connect" button.
3. The user selects "Connect" on a result.
4. A `Connection` record is created with `status = PENDING`, `requester_id = current_user`, `recipient_id = selected_user`.
5. A notification is sent to the recipient.
6. The requester's connection list shows the connection as "Pending."

**Exception Flows:**
- **E1 — Duplicate request:** If a `PENDING` or `ACCEPTED` connection already exists between these two users, the system displays: "You already have a connection with this user."
- **E2 — Blocked user:** If either user has blocked the other (future feature), the system displays a generic "User not found" message (to prevent enumeration).

**Exit Condition:** A pending connection exists and the recipient has been notified.

**Business Rules:** FR-NET-001

---

### UC-NET-002: Grant Data Consent to an Advisor

**Initiating Actor:** Investor
**Communicating Actor:** Advisor (receives notification)
**Priority:** CORE

**Entry Condition:** An `ACCEPTED` connection exists between the Investor and the Advisor.

**Happy Path:**
1. The Investor selects the Advisor from their Connections list and chooses "Manage Data Access."
2. The system presents the `ConsentConfigurationForm` with:
   - A checklist of available data fields (e.g., "Total Net Worth," "Real Estate Assets," "Liquid Assets," "Liabilities," "Cash Flow Summary," "Financial Goals," "Individual asset details")
   - A text field for Consent Purpose (mandatory)
   - A date picker for Consent Expiry (mandatory; must be in the future)
3. The Investor selects the desired fields, enters a purpose (e.g., "Annual tax filing review"), and sets an expiry (e.g., 90 days from today).
4. The Investor submits.
5. Validation: expiry date is in the future; at least one field is selected; purpose is not empty.
6. The system updates the `Connection` record: `permissions = [selected_fields]`, `consent_purpose = entered_purpose`, `consent_granted_at = now`, `consent_expires_at = selected_expiry`.
7. An immutable consent log record is written to the Data Room as a `ConsentForm` document.
8. A notification is sent to the Advisor: "New data access granted by [Investor name]. Expires [date]."

**Exception Flows:**
- **E1 — Past expiry date:** The system returns `422`: "Consent expiry date must be in the future."
- **E2 — No fields selected:** The system returns `422`: "Please select at least one data field to share."
- **E3 — Unverified advisor:** If the Advisor's credentials are `UNVERIFIED`, the system returns a warning (not a block) at the consent selection step: "This advisor's credentials have not been verified by Vittavaan. Proceed with caution."

**Exit Condition:** The Advisor can now access exactly the permitted fields until the consent expires. An immutable consent record exists in the Data Room.

**Business Rules:** FR-NET-003, FR-NET-004, FR-NET-005, FR-NET-006, NFR-SEC-004, NFR-SEC-005, NFR-PRIV-001

---

### UC-NET-003: Advisor Accesses Investor Data (Consent Gating)

**Initiating Actor:** Advisor (indirectly — triggered when Advisor requests Investor data)
**Priority:** CORE

**Entry Condition:** An Advisor with an accepted connection to an Investor requests portfolio data.

**Happy Path:**
1. The Advisor navigates to a connected Investor's shared view.
2. The API request carries the Advisor's JWT (identifying the Advisor as the requesting user).
3. The `ConsentAndMarketplaceEngine` (Protection Proxy) intercepts the request:
   - Fetches the `Connection` between the Advisor and the Investor.
   - Checks `status = ACCEPTED`.
   - Checks `consent_expires_at > current_timestamp`.
   - Reads the `permissions` list from the `Connection`.
4. The engine filters the portfolio data payload: only fields listed in `permissions` are included. All other fields are stripped before the response is returned.
5. The Advisor receives only the permitted data.

**Exception Flows:**
- **E1 — Consent expired:** `consent_expires_at <= current_timestamp`. The engine returns `403 Forbidden`: "Your data access consent for this user has expired. Please request the user to renew access."
- **E2 — No consent granted:** `permissions = []` or no consent has been granted. The engine returns `403 Forbidden`: "No data access has been granted for this user."
- **E3 — Connection revoked:** `status = REVOKED`. The engine returns `403 Forbidden`.

**Exit Condition:** The Advisor receives only the data the Investor explicitly permitted. No access decision is made client-side.

**Business Rules:** FR-NET-004, FR-NET-005, NFR-SEC-004, NFR-SEC-005

---

## Domain 6: Advisory Marketplace

---

### UC-MKT-001: Submit an Advisory Query

**Initiating Actor:** Investor
**Communicating Actor:** Advisor (receives query)
**Priority:** IMPORTANT

**Entry Condition:** The Investor is authenticated and has an accepted connection with at least one Advisor.

**Happy Path:**
1. The Investor navigates to "Ask" and selects an advisor.
2. The Investor types their question (e.g., "How much did my Karjat plot actually return after costs in the last 3 years?").
3. The Investor optionally attaches documents from the Data Room.
4. The Investor submits the query.
5. An `AdvisoryQuery` record is created with `status = OPEN`.
6. The system parses the question and, if it references portfolio data (e.g., "Karjat plot"), links the relevant asset to the query context.
7. The Advisor receives a notification with the question.
8. The Advisor navigates to the query, views the question and the portfolio context data (subject to the active consent scope), and provides a response.
9. The query status transitions to `IN_PROGRESS` when the Advisor first responds.
10. The response is stored as a thread message in the `AdvisoryQuery`.
11. The Investor receives a notification that their query has been answered.
12. The Investor can follow up or mark the query as `RESOLVED`.

**Exception Flows:**
- **E1 — Query requires data the Advisor cannot access:** If the question references a part of the portfolio not covered by the Advisor's consent scope, the system displays a warning to the Investor: "This question references [asset name], which is not currently shared with this advisor. [Update consent] to allow them to see this data."
- **E2 — Advisor unresponsive:** If the query remains `OPEN` for more than 5 days, the system sends a reminder notification to the Advisor.

**Exit Condition:** The query is submitted, the Advisor is notified, and a conversation thread exists.

**Business Rules:** FR-MKT-003, FR-MKT-004, FR-MKT-005, FR-MKT-006

---

## Domain 7: Credit Module

---

### UC-CREDIT-001: Submit a Credit Request

**Initiating Actor:** Investor
**Priority:** IMPORTANT

**Entry Condition:** The Investor is authenticated. The Investor has portfolio data with a verification level of at least `DOCUMENTED` for the assets they wish to offer as security.

**Happy Path:**
1. The Investor navigates to the Credit page and selects "Request Credit."
2. The Investor inputs: requested amount, purpose, desired tenure, and selects which asset classes to offer as security.
3. The system computes the anonymous borrower profile:
   - `VerifiedNetWorth` (verified assets only)
   - `VerifiedAnnualIncome` (from documented income transactions)
   - `EligibleSecurityValue` (verified/accepted asset value for selected asset classes)
   - `SecurityCoverMultiple`
   - `ExistingDebtServiceRatio`
   - `OnTimePaymentPct` (from transaction history)
4. The system performs a re-identification risk check: can the combination of age band, city tier, income type, and security class uniquely identify the user within the platform? If risk is HIGH, the system warns the Investor and suggests reducing disclosed fields.
5. The Investor reviews the anonymized profile and confirms submission.
6. The profile is shared (anonymously) with matching empanelled lenders.
7. The system displays: `MatchingLenderCount`, broken down by bank, NBFC, private bank.
8. Lenders review the profile and submit bids with rate, fees, and terms.
9. The Investor reviews bids and selects one.
10. Upon bid selection, the Investor consents to identity disclosure to the selected lender only.

**Exception Flows:**
- **E1 — Insufficient verified assets:** If all assets are `SELF_DECLARED`, the system returns: "Your credit request cannot be submitted. Lenders require at least some assets to be documented or verified. [How to verify your assets]"
- **E2 — High re-identification risk:** The system warns: "The combination of characteristics you've selected may make you identifiable. We recommend removing [specific field] to improve your privacy." The Investor may override and proceed with acknowledgment.

**Exit Condition:** The anonymous credit profile is shared with lenders and the Investor awaits bids.

**Business Rules:** FR-CREDIT-001, FR-CREDIT-002, FR-CREDIT-003, FR-CREDIT-004, FR-CREDIT-007, Rules 5.1, 5.2, NFR-PRIV-007

---

## Domain 8: Settings

---

### UC-SETT-001: Export All User Data

**Initiating Actor:** Investor
**Priority:** MUST (regulatory — DPDP Act compliance)

**Entry Condition:** The Investor is authenticated.

**Happy Path:**
1. The Investor navigates to Settings → Privacy → "Export My Data."
2. The Investor confirms the export request (2FA confirmation if 2FA is enabled).
3. The system queues a background export job.
4. The job compiles: all `Asset` records, all `Liability` records, all `Transaction` records, all `InheritanceAllocation` records, all `Connection` records (excluding other users' data), all consent logs, all `FinancialSnapshot` records, and all `HouseholdMember` records.
5. The job generates a JSON file and stores it in the Investor's secure Data Room folder.
6. The Investor receives a notification: "Your data export is ready. [Download]"
7. The download link generates a time-limited signed URL (60 minutes).

**Exception Flows:**
- **E1 — Large dataset (>72-hour SLA breach):** If the job has not completed within 72 hours, the Investor receives a notification: "Your export is taking longer than expected. We'll notify you as soon as it's ready."

**Exit Condition:** A structured JSON file containing all the user's data is available for download.

**Business Rules:** FR-SETT-002, NFR-PRIV-002, Rule 7.1

---

*This document covers the primary use cases. Use cases for Financial Planning goals, Financial Resume generation, Peer sharing, Will management, and Marketplace listing are to be added in the next iteration.*
