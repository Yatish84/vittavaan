# Phase 1 — Functional Requirements

> **OOSE Phase:** Requirements Elicitation
> **Purpose:** A complete, verifiable inventory of what the system MUST do. Every requirement maps to one or more wireframe screens and is written as a testable statement.
> **Notation:** `FR-[DOMAIN]-[NNN]` — e.g., `FR-AUTH-001`
> **Status:** Draft

---

## Reading This Document

Each requirement follows the format:
- **ID** — unique, stable identifier
- **Priority** — `MUST` (V1 launch blocker), `SHOULD` (V1 desirable), `COULD` (V2+)
- **Source** — the wireframe page(s) that evidences this requirement
- **Statement** — what the system must do, written precisely enough to be tested

---

## Domain 1: Authentication & Session Management

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-AUTH-001 | MUST | All pages | The system SHALL accept a cryptographically signed JWT from the external Auth provider and extract the user identity from it before granting access to any protected resource. |
| FR-AUTH-002 | MUST | All pages | The system SHALL create a local `User` record the first time a valid JWT is received for an identity that does not yet exist in the database. |
| FR-AUTH-003 | MUST | All pages | The system SHALL reject any request to a protected endpoint that does not carry a valid, non-expired JWT with a `401 Unauthorized` response. |
| FR-AUTH-004 | MUST | Settings | The system SHALL allow a user to enable two-factor authentication (TOTP or SMS OTP) as an additional layer on top of the external auth provider's session. |
| FR-AUTH-005 | MUST | All pages | The system SHALL maintain a `LocalSession` record per active login, tracking the session expiry. |
| FR-AUTH-006 | MUST | Settings | The system SHALL allow a user to terminate all active sessions (logout everywhere). |
| FR-AUTH-007 | SHOULD | Settings | The system SHOULD allow a user to view a list of their active sessions (device, IP, login time). |
| FR-AUTH-008 | MUST | Platform | The system SHALL support both email+password and phone OTP as login methods, delegated to the auth provider. |
| FR-AUTH-009 | MUST | Platform | A single user account SHALL be able to hold both an `InvestorProfile` and an `AdvisorProfile` simultaneously (dual role). |
| FR-AUTH-010 | MUST | Platform | The system SHALL provide a UI mechanism for a dual-role user to switch their active context between `Investor` view and `Advisor` view without logging out. |

---

## Domain 2: User Profiles & Settings

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-PROF-001 | MUST | Investor Profile, Profiling | The system SHALL allow an Investor to complete a structured profiling questionnaire capturing: education level, city tier, stated annual income, risk tolerance, investment horizon, liquidity needs, and behavioral bias indicators. |
| FR-PROF-002 | MUST | Investor Profile | The system SHALL derive a multi-dimensional investor classification (not a single score) from questionnaire responses, with each dimension (risk capacity, risk tolerance, liquidity need, investment knowledge) calculated separately. |
| FR-PROF-003 | MUST | Investor Profile | The system SHALL flag a conflict if a user's stated risk tolerance materially exceeds their calculated risk capacity based on objective financial factors. |
| FR-PROF-004 | MUST | Investor Profile | The system SHALL record the date the investor profile was created and last reviewed, and display the number of days since the last review. |
| FR-PROF-005 | MUST | Advisors | The system SHALL allow a user with the Advisor role to create and maintain an `AdvisorProfile` with: firm name, certifications (from a fixed validated list), specialty areas, and a professional bio. |
| FR-PROF-006 | MUST | Advisors | The system SHALL restrict the list of valid certifications to a defined enumeration: `CA`, `SEBI_RIA`, `CFP`, `CFA`, `IBBI_VALUER`, `ADVOCATE`, `CS`, `MBA_FINANCE`. No free-text credential entry is permitted. |
| FR-PROF-007 | MUST | Advisors | The system SHALL allow the System Administrator to mark each credential on an AdvisorProfile as `VERIFIED` or `UNVERIFIED` after checking against the relevant authoritative register. |
| FR-PROF-008 | MUST | Advisors | The system SHALL display a clear `UNVERIFIED` badge on any advisor profile whose credentials have not been administrator-verified. |
| FR-PROF-009 | MUST | Settings | The system SHALL allow a user to set their base display currency. All portfolio values SHALL be displayed in this currency with appropriate conversion if assets are held in other currencies. |
| FR-PROF-010 | MUST | Settings | The system SHALL display all Indian Rupee values using the Indian numbering system (lakh/crore, e.g., ₹1,47,32,500) rather than the international million/billion system. |
| FR-PROF-011 | MUST | Settings | The system SHALL allow a user to configure notification preferences: which types of alerts trigger email, in-app, or no notification. |
| FR-PROF-012 | MUST | Settings | The system SHALL display a transparency dashboard showing: subscription fees paid to platform, and any other platform revenue generated from the user's activity (marketplace fees, lender referrals). |

---

## Domain 3: Portfolio — Assets

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-ASSET-001 | MUST | Assets & Liabilities | The system SHALL allow an Investor to add, edit, and remove assets in three categories: `LIQUID`, `REAL_ESTATE`, and `ALTERNATIVE`. |
| FR-ASSET-002 | MUST | Assets & Liabilities | Every asset record SHALL store: name, category, ownership percentage (0–100%), purchase price in minor units (paise), current value in minor units, purchase date, currency, valuation method, valuation-as-of date, and verification level. |
| FR-ASSET-003 | MUST | Assets & Liabilities | The system SHALL enforce that ownership percentage is always between 0% and 100% (inclusive) at both the API and database constraint level. |
| FR-ASSET-004 | MUST | Assets & Liabilities | All monetary values SHALL be stored as non-negative integers representing paise (minor units). The API SHALL reject any monetary input that is not a non-negative integer. |
| FR-ASSET-005 | MUST | Assets & Liabilities | The system SHALL calculate the `AttributedAssetValue` for each asset as `current_value_minor_units × (ownership_split_pct / 100)`. This attributed value SHALL be used in all net worth calculations. |
| FR-ASSET-006 | MUST | Assets & Liabilities | The system SHALL support the following Liquid Asset sub-types (as source data): bank savings account, bank FD, equity (direct stocks), mutual fund, ETF, PPF, EPF, NPS, crypto, bonds, and unlisted company shares. |
| FR-ASSET-007 | MUST | Karjat Plot (Real Estate) | For Real Estate assets, the system SHALL store: property type (`LAND`, `RESIDENTIAL`, `COMMERCIAL`), location address, area (sq ft or sq meters), and price per area unit. The system SHALL automatically calculate gross valuation as `area × price_per_unit`. |
| FR-ASSET-008 | MUST | Karjat Plot | The system SHALL allow a Real Estate asset to store comparable transaction data (low, median, high comparable values) to contextualise the user's valuation. |
| FR-ASSET-009 | MUST | Karjat Plot | The system SHALL track title verification status (`UNCHECKED`, `IN_PROGRESS`, `VERIFIED`, `DISPUTED`), encumbrance status, and mutation status for Real Estate assets. |
| FR-ASSET-010 | MUST | Stamp Collection (Alternative) | For Alternative assets, the system SHALL store: collection/asset type (e.g., `PHILATELY`, `FINE_ART`, `NUMISMATICS`, `GOLD_PHYSICAL`), last appraisal date, and appraiser name. |
| FR-ASSET-011 | MUST | Assets & Liabilities | The system SHALL track a `verification_level` for every asset: `SELF_DECLARED`, `DOCUMENTED`, `VERIFIED`, `ACCEPTED`. The level is updated by the administrator or through document upload evidence. |
| FR-ASSET-012 | MUST | Assets & Liabilities | The system SHALL calculate `ValuationAgeDays` (current date minus valuation-as-of date) for every asset and flag assets as stale based on asset-class-specific thresholds (configurable by platform). |
| FR-ASSET-013 | MUST | Assets & Liabilities | The system SHALL calculate and display: total assets by class, percentage share of each asset class, and gain/loss per asset (current value minus cost basis). |
| FR-ASSET-014 | MUST | Assets & Liabilities | The system SHALL allow a user to upload documents linked to a specific asset (e.g., title deed linked to a real estate asset, purchase receipt linked to an alternative asset). |
| FR-ASSET-015 | SHOULD | Assets & Liabilities | The system SHOULD allow assets to be tagged with custom labels (e.g., "Retirement Corpus", "Children's Education") in addition to the formal asset categories. |

---

## Domain 4: Portfolio — Liabilities

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-LIAB-001 | MUST | Assets & Liabilities, Credit | The system SHALL allow an Investor to add, edit, and remove liabilities with the following types: `HOME_LOAN`, `LAP` (Loan Against Property), `PERSONAL_LOAN`, `CAR_LOAN`, `BUSINESS_LOAN`, `CREDIT_CARD`, `EDUCATION_LOAN`, `GOLD_LOAN`, `MARGIN_FACILITY`. |
| FR-LIAB-002 | MUST | Assets & Liabilities | Every liability record SHALL store: name, type, original principal (minor units), current outstanding balance (minor units), interest rate, rate type (`FIXED`/`FLOATING`), remaining tenure, lender name, and next payment due date. |
| FR-LIAB-003 | MUST | Credit | The system SHALL calculate and display an amortization schedule showing: monthly EMI, principal component, interest component, and cumulative principal paid for each month of the loan tenure. |
| FR-LIAB-004 | MUST | Assets & Liabilities | The system SHALL calculate `LiabilitySharePct` for each liability as `outstanding_balance / total_liabilities`. |
| FR-LIAB-005 | MUST | Assets & Liabilities | The system SHALL calculate `PrincipalPaidToDate` and `InterestPaidToDate` from the transaction ledger for each linked liability. |
| FR-LIAB-006 | MUST | Credit | The system SHALL calculate the `DebtServiceRatio` as the sum of all monthly debt payments divided by the user's defined monthly income base. |
| FR-LIAB-007 | MUST | Assets & Liabilities | The system SHALL allow a liability to be linked to a specific asset as collateral (e.g., a home loan linked to a residential property). The system SHALL calculate `LoanToLinkedAssetValue` for such linked pairs. |
| FR-LIAB-008 | SHOULD | Credit | The system SHOULD warn the user if a pledged/encumbered asset is attempted to be listed on the marketplace or designated in a gift transfer. |

---

## Domain 5: Portfolio — Cash Flow & Transactions

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-TXN-001 | MUST | Assets & Liabilities (Cash Flow tab) | The system SHALL allow an Investor to manually log cash flow transactions with: date, amount (minor units), type (`INFLOW`/`OUTFLOW`/`BUY`/`SELL`/`RENT`/`DIVIDEND`/`INTEREST`/`GIFT`), category, and optional link to a specific asset. |
| FR-TXN-002 | MUST | Assets & Liabilities | The system SHALL not allow historical transactions to be edited or deleted (append-only ledger). If an error is made, the user must log a correcting transaction. |
| FR-TXN-003 | MUST | Assets & Liabilities | The system SHALL calculate and display monthly inflows, outflows, surplus (`Inflows - Outflows`), and savings rate (`Surplus / Inflows`) from the transaction ledger. |
| FR-TXN-004 | MUST | Assets & Liabilities | The system SHALL group income by source (salary, rent, dividends, interest, other) and expenses by category (housing, EMI, food, transport, medical, other) for the cash flow view. |
| FR-TXN-005 | MUST | Assets & Liabilities | The system SHALL calculate and display the Debt Service Ratio using transaction data. |
| FR-TXN-006 | MUST | Analysis | The system SHALL flag any transaction that has not been assigned a category as an "Unclassified Transaction" and display the count of unclassified transactions as a data quality indicator. |
| FR-TXN-007 | MUST | Net Worth | The system SHALL trigger a background job to capture a new `FinancialSnapshot` whenever a material change occurs to the portfolio (asset added/updated, liability changed, transaction logged). |
| FR-TXN-008 | MUST | Net Worth | `FinancialSnapshot` records SHALL be immutable and append-only. They SHALL record total assets, total liabilities, net worth, and asset class breakdowns — all in minor units — at the moment of capture. |

---

## Domain 6: Dashboard & Analysis

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-DASH-001 | MUST | Net Worth | The system SHALL display the user's current net worth, total assets, total liabilities, and month-over-month and 12-month change for each, with both absolute (minor units) and percentage changes. |
| FR-DASH-002 | MUST | Net Worth | The system SHALL display a net worth waterfall chart showing what drove the change in net worth: equity gains, real estate revaluation, fresh investment, loan repayment, crypto change. The sum of components MUST reconcile to the total net worth change. |
| FR-DASH-003 | MUST | Net Worth | The system SHALL display a `VerifiedWealthPct` — the percentage of net worth supported by verified (not self-declared) valuations. |
| FR-DASH-004 | MUST | Net Worth | The system SHALL display a time-series chart of net worth over the user's history using `FinancialSnapshot` data. The chart SHALL NOT interpolate missing data points when a source feed is unavailable; missing periods are shown as a gap. |
| FR-DASH-005 | MUST | Net Worth | The system SHALL display a monthly income vs. expense breakdown with source/category grouping. |
| FR-DASH-006 | MUST | Net Worth | The system SHALL surface "Worth a Look" alerts — data quality and portfolio health signals — including: stale valuations, fund overlaps, concentration risks, upcoming consent expiries, and financial events. |
| FR-DASH-007 | MUST | Analysis | The system SHALL calculate and display `PortfolioXIRR` (money-weighted return) for user-selectable time windows (1Y, 3Y, 5Y, since inception). |
| FR-DASH-008 | MUST | Analysis | The system SHALL calculate and display `PortfolioTWRR` (time-weighted return) for user-selectable time windows. |
| FR-DASH-009 | MUST | Analysis | The system SHALL display XIRR and TWRR separately and clearly label the difference between them. The two SHALL NOT be presented as interchangeable. |
| FR-DASH-010 | MUST | Analysis | The system SHALL calculate and display maximum drawdown percentage, drawdown start date, trough date, and recovery time in months. |
| FR-DASH-011 | MUST | Attribution | The system SHALL attribute portfolio return to each asset class (Liquid, Real Estate, Alternative) showing: start-of-period weight, period return, rupee gain, and percentage contribution. The sum of class contributions SHALL reconcile to the portfolio's total return. |
| FR-DASH-012 | MUST | Attribution | The system SHALL display the return relative to a relevant benchmark (e.g., Nifty 500 TRI for the equity component). |
| FR-DASH-013 | SHOULD | Net Worth | The system SHOULD flag if the user has a high concentration in a single issuer/employer (direct + look-through exposure via funds). |
| FR-DASH-014 | MUST | Analysis | The system SHALL display a `PerformanceBasis` indicator (Verified / Estimated / Self-declared) alongside all performance metrics, reflecting the quality of underlying valuations. |

---

## Domain 7: Financial Planning

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-PLAN-001 | MUST | Planning | The system SHALL allow an Investor to create financial goals with: name, target amount (minor units), target year, and a list of earmarked assets/holdings. |
| FR-PLAN-002 | MUST | Planning | The system SHALL calculate `GoalProjectedValue` — the projected future value of earmarked holdings under user-specified return assumptions (equity return %, debt return %, inflation %). |
| FR-PLAN-003 | MUST | Planning | The system SHALL calculate and display the `GoalFundingGap` (`GoalProjectedValue - GoalNeededThen`, where `GoalNeededThen` is the inflation-adjusted target amount). |
| FR-PLAN-004 | MUST | Planning | The system SHALL display `GoalStatus` for each goal: `ON_TRACK`, `SHORT`, `FUNDED`, or `AT_RISK`. |
| FR-PLAN-005 | MUST | Planning | The system SHALL calculate and display the timing mismatch for each goal — the portion of earmarked funding that will not be liquid or accessible by the goal date. |
| FR-PLAN-006 | MUST | Planning | The system SHALL display upcoming financial events with days-until countdown: lease renewals, ESOP vesting windows, insurance renewals, and loan maturity dates. |
| FR-PLAN-007 | MUST | Planning | The system SHALL provide an "invest vs. prepay" calculator: given a prepayment amount, current loan rate, and assumed investment return, compute the economic end-position for both scenarios and the crossover return at which they are equal. |
| FR-PLAN-008 | MUST | Financial Resume | The system SHALL generate a structured Financial Resume including: individual net worth, verified vs. unverified net worth, income by source, debt service ratio, liquidity buckets (3-day, 1-year), credit metrics, investment track record summary, and data quality indicators. |
| FR-PLAN-009 | MUST | Financial Resume | The system SHALL allow a user to create a recipient-specific version of the Financial Resume — choosing exactly which fields are included/excluded before sharing. |
| FR-PLAN-010 | SHOULD | Financial Resume | The system SHOULD allow an Advisor to attest the Financial Resume by adding their name, credential, and attestation date as a digitally linked record. |

---

## Domain 8: Estate & Legal Planning

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-ESTATE-001 | MUST | Household | The system SHALL allow an Investor to register household members with: first name, last name, relationship (`SPOUSE`, `CHILD`, `PARENT`, `SIBLING`, `IN_LAW`, `OTHER`), date of birth, and optional contact email. |
| FR-ESTATE-002 | MUST | Household | The system SHALL display a consolidated household balance sheet that counts jointly held assets exactly once (not once per member), using the `ownership_split_pct` to attribute portions to each member. |
| FR-ESTATE-003 | MUST | Household | The system SHALL calculate and display `HouseholdNetWorth`, `MemberAttributedNetWorth` per member, and `MemberHouseholdNetWorthShare` for each member. |
| FR-ESTATE-004 | MUST | Household | The system SHALL calculate household income (inflows), outflows, surplus, passive income, debt service ratio, and dependent support amounts at the household level. |
| FR-ESTATE-005 | MUST | Will | The system SHALL allow an Investor to create an `EstatePlan` by appointing a primary executor (name and contact) and optionally a secondary executor. |
| FR-ESTATE-006 | MUST | Will | The system SHALL allow an Investor to upload a will document and record its signature date and status (`DRAFT`, `EXECUTED`, `REVOKED`). |
| FR-ESTATE-007 | MUST | Will | The system SHALL analyse the estate plan against the current portfolio and display: assets with effective will disposition (`WillCoveredEstateValue`), assets without disposition (`WillUncoveredEstateValue`), and the `EstateCoveragePct`. |
| FR-ESTATE-008 | MUST | Will | The system SHALL flag assets acquired after the will's execution date, assets referenced in the will that are no longer owned, and nomination/beneficiary conflicts. |
| FR-ESTATE-009 | MUST | Inheritance | The system SHALL allow an Investor to allocate a percentage share of any asset to any registered household member. |
| FR-ESTATE-010 | MUST | Inheritance | The system SHALL enforce at the API and database level that the sum of all `InheritanceAllocation.percentage_share` values for a single asset never exceeds 100%. Any attempt to exceed 100% SHALL return a validation error showing the remaining available percentage. |
| FR-ESTATE-011 | MUST | Inheritance | The system SHALL model the default intestacy position for unallocated assets under the applicable Indian succession law (Hindu Succession Act for Hindu users, relevant personal law otherwise) and display it alongside the user's intended allocation. |
| FR-ESTATE-012 | MUST | Gift Rules | The system SHALL provide a Gift Rules Engine that, given a donor, recipient, relationship, and asset, determines: whether the gift is tax-exempt or taxable, the applicable exemption limit, and the maximum legally giftable value. |
| FR-ESTATE-013 | MUST | Gift Rules | The system SHALL check whether the proposed gift asset has restrictions: pledged/encumbered, joint-owned without co-owner consent, or product-type restrictions (EPF, unvested ESOPs). |
| FR-ESTATE-014 | MUST | Gift Transfer | The system SHALL allow an Investor to log a gift transfer tracking the full lifecycle: gift deed status, registration date, mutation status, stamp duty paid, and whether the portfolio ownership has been updated post-transfer. |
| FR-ESTATE-015 | MUST | Gift Transfer | The system SHALL calculate stamp duty, registration fee, and total transfer cost for a gift, using the applicable rate for the asset type and jurisdiction. |

---

## Domain 9: Connections & Networking

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-NET-001 | MUST | Connections | The system SHALL allow a user to search for other platform users by name or profession and send a connection request. |
| FR-NET-002 | MUST | Connections | The system SHALL allow a user to accept, reject, or revoke a connection. A revoked connection SHALL immediately terminate all active data consents. |
| FR-NET-003 | MUST | Connections | The system SHALL allow an Investor to grant a connected user (typically an Advisor) access to specific data fields from their portfolio, with: a defined consent scope (list of permitted fields), a consent purpose (free text), and a consent expiry date. |
| FR-NET-004 | MUST | Connections | The system SHALL enforce that no connected user can access data beyond their explicit consent scope. The ConsentAndMarketplaceEngine SHALL evaluate `Connection.permissions` and `consent_expires_at` on every data request. |
| FR-NET-005 | MUST | Connections | The system SHALL automatically revoke data access when `consent_expires_at` is reached, via a background job that runs at least every 15 minutes. |
| FR-NET-006 | MUST | Connections | The system SHALL log every consent grant and revocation as an immutable record in the Data Room with: grantor, grantee, fields permitted, purpose, granted-at, expires-at. |
| FR-NET-007 | MUST | Connections | The system SHALL display data freshness metrics for each connection: days since last sync, connection health status. |
| FR-NET-008 | MUST | Peers | The system SHALL allow users to view data shared by connected peers, restricted to exactly the fields the peer has granted access to. |
| FR-NET-009 | MUST | Peers | The system SHALL display peer data using privacy-preserving representations for sensitive fields: `NetWorthBand` (e.g., "₹1–5 Cr") instead of exact figures, unless the peer has granted exact-value access. |
| FR-NET-010 | MUST | Peers | The system SHALL NOT implement any peer ranking, leaderboard, "better than X% of peers" metric, or comparative scoring. The Peers module is for consensual sharing only. |
| FR-NET-011 | MUST | Connections | The system SHALL display pending access requests with their age in days and auto-expire unanswered requests after a configurable period (default: 30 days). |

---

## Domain 10: Advisory Marketplace

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-MKT-001 | MUST | Advisors | The system SHALL display a searchable directory of Advisor profiles. Search SHALL support filtering by: certification type, specialty area, city, fee range, and rating. |
| FR-MKT-002 | MUST | Advisors | The system SHALL display an "Advisor Match Reason" for each advisor result, explaining in plain language why the advisor appears for the user (e.g., "Matches your real estate holdings + ESOP planning need"). Match reasons SHALL be based on actual portfolio data, not undisclosed commercial placement. |
| FR-MKT-003 | MUST | Ask | The system SHALL allow an Investor to submit an advisory query to a specific advisor with a subject, body, and optional attached documents. |
| FR-MKT-004 | MUST | Ask | The system SHALL support multi-turn advisory query threads (question → response → follow-up). |
| FR-MKT-005 | MUST | Ask | Advisory queries SHALL support natural-language questions grounded in the user's ledger (e.g., "How much did my Karjat plot return?"). The system SHALL display the answer alongside: the sources used, the as-of dates of each source, and a confidence disclosure noting any estimated or missing data used in the answer. |
| FR-MKT-006 | MUST | Ask | Query status SHALL progress through defined states: `OPEN` → `IN_PROGRESS` → `RESOLVED` → `CLOSED`. The Investor can re-open a resolved query. |
| FR-MKT-007 | MUST | Trends & News | The system SHALL display a feed of market insights and financial news published by Advisors, filtered to the user's actual holdings. A news item SHALL only appear if it has a traceable relevance path to the user's portfolio (holding → fund → sector). |
| FR-MKT-008 | MUST | Trends & News | For each news item, the system SHALL display: the portfolio exposure affected (value and percentage), the relevance path (e.g., "Affects HDFC Bank → which is in your Mirae Asset MF"), and the publication date. |
| FR-MKT-009 | SHOULD | Advisors | The system SHOULD display advisor ratings and completed engagement counts. A `RatingParticipationPct` (rated / total engagements) SHALL be shown. |
| FR-MKT-010 | MUST | Marketplace | The system SHALL allow users to browse marketplace listings of assets (real estate, collectibles) for sale or transfer on the platform. |
| FR-MKT-011 | MUST | Marketplace | Listings SHALL display a verification status showing which required checks have passed, how many are pending, and the completion percentage. |
| FR-MKT-012 | MUST | Marketplace Browse | The system SHALL allow filtering listings by asset class, price range, verification status, yield, and listing age. |
| FR-MKT-013 | SHOULD | Marketplace | The system SHOULD allow a user to open a purchase/interest thread on a listing, tracking the buyer's offers and the listing's agree price negotiation. |

---

## Domain 11: Credit Module

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-CREDIT-001 | MUST | Credit | The system SHALL allow an Investor to initiate a credit request by specifying: requested amount, purpose, desired tenure, and which asset classes they are willing to offer as security. |
| FR-CREDIT-002 | MUST | Credit | The system SHALL construct an anonymous borrower profile (no name, no PAN, no direct identifiers) using: age band, city tier, verified net worth, verified income, CIBIL/CRIF scores (user-input in V1), debt service ratio, on-time payment record, and security coverage. |
| FR-CREDIT-003 | MUST | Credit | The system SHALL NOT share the Investor's identity with any lender until the Investor explicitly consents to identity disclosure for a specific bid. |
| FR-CREDIT-004 | MUST | Credit | The system SHALL calculate the Security Coverage Multiple (`EligibleSecurityValue / RequestedCreditAmount`) and display it in the borrower profile. |
| FR-CREDIT-005 | SHOULD | Credit | The system SHOULD display a count of matching empanelled lenders (bank, NBFC, private bank) for the submitted credit request. |
| FR-CREDIT-006 | SHOULD | Credit | For each lender bid received, the system SHOULD calculate: Bid APR (rate + mandatory fees), Bid EMI, total interest, and total repayment. |
| FR-CREDIT-007 | MUST | Credit | The system SHALL perform a re-identification risk check before sharing the anonymized profile — if the combination of disclosed characteristics makes the user identifiable (small cohort risk), the system SHALL warn the user and suggest reducing disclosed fields. |

---

## Domain 12: Data Room (Documents)

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-DOCS-001 | MUST | Assets & Liabilities | The system SHALL allow users to upload documents with types: `WILL`, `TITLE_DEED`, `VALUATION_REPORT`, `PURCHASE_AGREEMENT`, `CONSENT_FORM`, `APPRAISAL_REPORT`, `LOAN_AGREEMENT`, `TAX_DOCUMENT`, `INSURANCE_POLICY`, `OTHER`. |
| FR-DOCS-002 | MUST | Assets & Liabilities | Documents SHALL be stored in secure object storage. Direct public URLs to documents SHALL never be exposed. All document access SHALL use time-limited signed URLs (default: 60 minutes). |
| FR-DOCS-003 | MUST | Assets & Liabilities | A document MAY be linked to a specific asset or estate plan element. Unlinked documents are stored in the general Data Room. |
| FR-DOCS-004 | MUST | Assets & Liabilities | The system SHALL record for every document: owner, document type, linked asset (if any), document date, expiry date (if applicable), and upload timestamp. |
| FR-DOCS-005 | SHOULD | Assets & Liabilities | The system SHOULD scan uploaded documents for malware/viruses before making them accessible. Documents SHALL be quarantined until the scan completes. |

---

## Domain 13: Settings & Platform Administration

| ID | Priority | Source | Requirement |
|---|---|---|---|
| FR-SETT-001 | MUST | Settings | The system SHALL allow a user to update: display name, base currency, notification preferences, security settings (2FA). |
| FR-SETT-002 | MUST | Settings | The system SHALL allow a user to request a full data export of their financial data in a structured format (JSON). The export SHALL include: all assets, liabilities, transactions, estate plan data, connections, and consents. |
| FR-SETT-003 | MUST | Settings | The system SHALL allow a user to initiate account closure. The system SHALL confirm the closure request, retain data per legal requirements (7 years for financial records), and purge personal identifiers after the retention period. |
| FR-SETT-004 | MUST | Settings | The system SHALL maintain an immutable audit log of all material settings changes (e.g., 2FA toggle, base currency change, account closure request). |
| FR-SETT-005 | MUST | Settings | The system SHALL display the user's household role (`OWNER`, `ADMIN`, `GUARDIAN`, `DEPENDANT`) and the date the role began. |

---

*Next document: [03_Non_Functional_Requirements.md](./03_Non_Functional_Requirements.md)*
