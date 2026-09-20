# Phase 2 — Analysis: Domain Glossary

> **OOSE Phase:** Analysis
> **Purpose:** Defines every domain term precisely, in the Indian financial context, establishing the "ubiquitous language" used consistently across all documentation, code identifiers, API field names, database column names, and UI copy.
> **Rule:** If a term appears in code or documentation without matching a definition here, it must be added. No synonyms or informal abbreviations in code.
> **Status:** Draft

---

## How to Use This Glossary

- **Code names** — the exact identifier used in Python classes, TypeScript types, API JSON fields, and database column names
- **UI label** — the exact label shown to users in the interface (may differ from code name for readability)
- **Context** — the domain area this term belongs to

Terms are sorted alphabetically within each section.

---

## Section A — Asset & Valuation Terms

---

**Allocated Beneficiary Value**
`code: allocated_beneficiary_value_minor_units`
`UI: Allocated to Beneficiaries`
The portion of an asset's attributed value that has been designated to registered beneficiaries through `InheritanceAllocation` records. Calculated as `attributed_value × (sum_of_allocated_percentages / 100)`.

---

**Alternative Asset**
`code: AlternativeAsset (entity)`
`UI: Alternative Assets`
Assets that do not fit the standard liquid or real estate categories. Includes: philately, fine art, numismatics, physical gold (coins/bars, not jewellery ETF), unlisted company shares, vintage watches, wine, and other collectibles. Values are inherently subjective and require periodic appraisal.

---

**Annual Exemption Limit**
`code: annual_exemption_limit_minor_units`
`UI: Annual Gift Exemption`
The Indian Income Tax Act threshold (₹50,000 per financial year) below which gifts from non-relatives are exempt from income tax in the recipient's hands. Stored in minor units in the `GiftRule` table.

---

**Appraisal**
`code: last_appraisal_date, appraiser_name`
`UI: Last Appraised`
A professional evaluation of an asset's value by a qualified appraiser or valuer. For alternative assets, this is the primary mechanism for establishing a `DOCUMENTED` or `VERIFIED` valuation. Appraisals expire after asset-class-specific periods (platform-configurable).

---

**Asset Category**
`code: AssetCategoryEnum {LIQUID, REAL_ESTATE, ALTERNATIVE}`
`UI: Asset Class`
The top-level classification of an asset. All portfolio calculations are grouped by this category for asset allocation, attribution, and net worth breakdown.

---

**Attributed Asset Value**
`code: attributed_value_minor_units`
`UI: Your Share (₹)`
The portion of an asset's gross current value that belongs to this user, calculated as `current_value_minor_units × (ownership_split_pct / 100)`. **This is the only value used in net worth calculations.** Gross value is never added directly to net worth.

---

**Cost Basis**
`code: purchase_price_minor_units`
`UI: Cost / Purchase Price`
The original total acquisition cost of an asset, in paise. For real estate, this includes purchase price plus stamp duty, registration fees, legal costs, and any verified improvement costs. The cost basis is used to calculate unrealised gain/loss and forms the carried-over basis for gift recipients.

---

**Encumbrance**
`code: encumbrance_status: EncumbranceStatusEnum {CLEAR, PARTIAL, PLEDGED}`
`UI: Encumbrance Status`
A legal claim against a property asset — typically a mortgage or pledge in favour of a lender. An encumbered property cannot be gifted or listed on the marketplace without the lender's prior written consent. See also: `Pledged Asset`.

---

**Financial Snapshot**
`code: FinancialSnapshot (entity)`
`UI: (internal, not user-visible as a term)`
An immutable, point-in-time record of the user's complete portfolio metrics: total assets, total liabilities, net worth, asset class breakdown, and verified wealth — all in minor units — captured at a specific datetime. The foundation of all trend charts. Append-only: records are never edited or deleted.

---

**Gross Asset Value**
`code: current_value_minor_units`
`UI: Gross Value (₹)`
The total market or appraised value of an asset without applying the ownership percentage. A property worth ₹1 crore owned 60% by the user has a gross value of ₹1,00,00,000 but an attributed value of ₹60,00,000.

---

**Liquid Asset**
`code: LiquidAsset (entity), LiquidSubTypeEnum`
`UI: Liquid Assets`
Assets that are readily convertible to cash within a short timeframe. Sub-types include: bank savings accounts, FDs, direct equity (stocks), mutual funds, ETFs, PPF, EPF, NPS, crypto, bonds, and unlisted company shares. Liquidity varies by sub-type; PPF has lock-in periods, for example.

---

**Minor Units / Paise**
`code: *_minor_units (suffix convention on all monetary fields)`
`UI: displayed as ₹ with Indian formatting (e.g., ₹1,47,32,500)`
The integer representation of a monetary amount in the smallest denomination of the currency. For INR, this is paise: 1 INR = 100 paise. **All monetary values in the system are stored and calculated as integers in minor units.** No floating-point arithmetic is ever used for money.

---

**Mutation**
`code: mutation_status: MutationStatusEnum {PENDING, IN_PROGRESS, COMPLETED}`
`UI: Mutation Status`
The process of updating property records at the local municipal or revenue authority (tahsildar's office) to reflect a change of ownership. Required after purchase or gift of real estate. Without mutation, the new owner has legal title but the official property records still show the previous owner.

---

**Ownership Split Percentage**
`code: ownership_split_pct: Float`
`UI: Your Ownership (%)`
The percentage of an asset that is legally owned by this user, expressed as a decimal from 0 to 100 (inclusive). A property jointly owned equally between spouses has `ownership_split_pct = 50.0` for each. The system enforces this is never negative and never exceeds 100.

---

**Performance Basis**
`code: PerformanceBasisEnum {VERIFIED, ESTIMATED, MIXED, PARTIAL}`
`UI: Return Data Quality`
A metadata tag on all performance metrics (XIRR, TWRR, net worth trend) indicating the quality of the underlying valuations. `VERIFIED` means all constituent assets have at least `DOCUMENTED` verification. `ESTIMATED` means some assets use self-declared values. `MIXED` means some are verified and some estimated. `PARTIAL` means data for the full period is missing.

---

**Pledged Asset**
`code: is_pledged: Boolean (derived from encumbrance_status)`
`UI: Pledged (loan collateral)`
An asset that has been offered as security for a loan. Pledged assets cannot be gifted or listed on the marketplace while the pledge is active. The system displays a hard block on any gift or listing initiation for pledged assets.

---

**Real Estate Asset**
`code: RealEstateAsset (entity), PropertyTypeEnum {LAND, RESIDENTIAL, COMMERCIAL}`
`UI: Real Estate`
Immovable property owned by the user. Three sub-types: land plots, residential properties (flats, houses), and commercial properties (offices, shops). Each requires title verification, encumbrance checking, and mutation tracking. Valuation methods include: circle rate (government-set), comparable sales, appraisal, or user estimate.

---

**Staleness / Stale Valuation**
`code: StalenessStatusEnum {CURRENT, APPROACHING_STALE, STALE}`
`code: ValuationAgeDays`
`UI: Last Updated [N] days ago ⚠️`
The condition where an asset's recorded `current_value_minor_units` was set based on a valuation date (`valuation_as_of`) that is beyond the platform's freshness threshold for that asset class. Stale assets are flagged on the dashboard and in the "Worth a Look" alerts. Net worth figures derived from stale valuations are marked with a `PARTIAL_DATA` badge.

---

**Stamp Duty Value**
`code: stamp_duty_value_minor_units`
`UI: Stamp Duty Value / Circle Rate Value`
The government-mandated minimum value of a property for the purpose of computing stamp duty and registration fees. For properties, this is the value at the **circle rate** — not the actual transaction price. Gift tax for immovable property is also computed on the stamp duty value (not market value), per the Income Tax Act.

---

**Unverified / Self-Declared**
`code: VerificationLevelEnum.SELF_DECLARED`
`UI: Self-Declared 🔵`
An asset whose value is based solely on the user's own input, with no supporting documentation uploaded. All newly created assets start as `SELF_DECLARED`. Self-declared valuations contribute to gross net worth but reduce the `VerifiedWealthPct` metric.

---

**Verification Level**
`code: VerificationLevelEnum {SELF_DECLARED, DOCUMENTED, VERIFIED, ACCEPTED}`
`UI: Verification Status`
A four-tier indicator of how well an asset's value is supported by evidence:
- `SELF_DECLARED` — user's own figure, no documents
- `DOCUMENTED` — user has uploaded supporting document (e.g., purchase agreement, FD receipt)
- `VERIFIED` — a platform-trusted source (advisor, valuer) has confirmed the value
- `ACCEPTED` — the value has been reviewed and accepted by the System Administrator

---

**Verified Wealth Percentage**
`code: verified_wealth_pct`
`UI: Verified Wealth (%)`
The proportion of total net worth supported by assets with verification level `DOCUMENTED` or above. Calculated as: `sum(attributed_value for assets where verification_level in [DOCUMENTED, VERIFIED, ACCEPTED]) / total_net_worth`. A key data quality metric displayed prominently on the dashboard.

---

## Section B — Performance & Return Terms

---

**Attribution**
`code: AttributionResult`
`UI: Return Attribution`
The decomposition of a portfolio's total return into contributions from each asset class (and within equity, by individual holding). Each class's contribution = `(class_return × class_weight)`. The sum of all class contributions must reconcile exactly to the total portfolio return.

---

**Benchmark Return**
`code: benchmark_return`
`UI: Benchmark (e.g., Nifty 500 TRI)`
The return of a reference index over the same period as the portfolio return calculation. Used to contextualise whether the portfolio has outperformed or underperformed. In V1, benchmark returns are manually maintained in the database. In V2, they will be fed from a market data API.

---

**Excess Return (Alpha)**
`code: excess_return_pct`
`UI: vs. Benchmark (±%)`
The difference between the portfolio's return (XIRR or TWRR) and the benchmark return over the same period. Positive excess return means the portfolio outperformed the benchmark; negative means underperformance.

---

**Maximum Drawdown**
`code: max_drawdown_pct, drawdown_start_date, drawdown_trough_date, recovery_months`
`UI: Max Drawdown`
The largest peak-to-trough decline in portfolio value over the measurement period, expressed as a percentage. Accompanied by the drawdown start date (peak), trough date, and number of months to full recovery (if recovered). A key risk metric.

---

**TWRR — Time-Weighted Rate of Return**
`code: portfolio_twrr`
`UI: Time-Weighted Return (TWRR)`
The geometric mean of sub-period returns, where each sub-period is bounded by an external cash flow event. TWRR eliminates the effect of the timing and size of cash flows, making it the correct metric to evaluate **investment manager skill** — how well the underlying assets performed, independent of when money was added or withdrawn. **Must never be presented as interchangeable with XIRR.**

---

**XIRR — Extended Internal Rate of Return**
`code: portfolio_xirr`
`UI: Money-Weighted Return (XIRR)`
The rate of return that sets the net present value of all actual cash flows (investments, withdrawals) and the terminal portfolio value to zero. XIRR accounts for the timing and size of each cash flow, making it the correct metric to evaluate **actual wealth creation** for the investor — how much their money grew given when it was deployed. **Must never be presented as interchangeable with TWRR.** Requires at least one external cash flow transaction to compute; returns `null` with an error code if insufficient data.

---

## Section C — Estate & Legal Planning Terms

---

**Beneficiary**
`code: beneficiary_id (references HouseholdMember)`
`UI: Beneficiary`
A household member designated to receive a specific percentage of an asset through an `InheritanceAllocation`. Distinguished from **Nominee** (who holds in trust) — a beneficiary has the legal entitlement to the asset.

---

**EstateCoveragePct**
`code: estate_coverage_pct`
`UI: Estate Coverage (%)`
The percentage of the user's total attributed net worth that has been allocated to beneficiaries through the Will or inheritance allocations. Calculated as `WillCoveredEstateValue / TotalAttributedNetWorth × 100`. Assets with no allocation reduce this percentage.

---

**Estate Plan**
`code: EstatePlan (entity)`
`UI: Estate Plan`
The comprehensive record of a user's instructions for the distribution of their estate after death. Comprises the Will document, executor designation, inheritance allocations, and asset-beneficiary mappings. The system analyses this against the current portfolio to identify gaps.

---

**Executor**
`code: primary_executor_name, primary_executor_contact`
`UI: Will Executor`
The person legally appointed by the testator (will maker) to administer the estate after death: collecting assets, paying debts, and distributing the estate to beneficiaries. Vittavaan stores the executor's name and contact details but does not itself validate executor eligibility.

---

**Gift Deed**
`code: gift_deed_status: DeedStatusEnum {NOT_PREPARED, DRAFT, EXECUTED, REGISTERED}`
`UI: Gift Deed Status`
The legal document that evidences the transfer of an asset as a gift, without any consideration. For immovable property, a gift deed must be registered with the Sub-Registrar of Assurances and stamped with the applicable stamp duty. Vittavaan tracks the lifecycle of this document.

---

**Gift Occasion**
`code: GiftOccasionEnum {MARRIAGE, INHERITANCE, GENERAL, CONTEMPLATION_OF_DEATH}`
`UI: Gift Occasion`
The context of the gift, which may affect its tax treatment. Gifts on the occasion of marriage or by inheritance are exempt regardless of amount or relationship.

---

**Gift Rule**
`code: GiftRule (entity)`
`UI: Gift Tax Rule`
A versioned, jurisdiction-specific database record encoding a provision of the Indian Income Tax Act (or state law) that governs whether a gift is exempt or taxable. Rules are never hardcoded — they live in the database with an `rule_effective_date` and `rule_version` so that Finance Act changes can be captured without a code deployment.

---

**Hindu Succession Act (HSA)**
`code: succession_law: SuccessionLawEnum.HINDU_SUCCESSION_ACT`
`UI: Applicable Law: Hindu Succession Act`
The Indian legislation that governs the distribution of a Hindu's estate when they die without a valid will (intestate). The Act defines Class I and Class II heirs and their relative shares. The 2005 amendment gave daughters equal coparcenary rights.

---

**Inheritance Allocation**
`code: InheritanceAllocation (entity)`
`UI: Inheritance Allocation`
A record specifying that a particular household member should receive a defined percentage of a specific asset from the user's estate. The system enforces that the sum of all allocations for a single asset does not exceed 100%. The sum may be less than 100% — the unallocated portion falls to the default succession rules.

---

**Intestacy**
`code: is_intestate_portion: Boolean (derived)`
`UI: Default Succession (no will)`
The legal condition of dying without a valid will, causing the estate to be distributed according to applicable personal law (Hindu Succession Act, Indian Succession Act, or personal law). The system models the default intestacy position for any asset that lacks an inheritance allocation or will disposition.

---

**Mutation**
*(see Assets section above — same term, critical in the estate context)*

---

**Nominee**
`code: (implicit in platform warnings — not a primary entity in V1)`
`UI: Nominee`
A person designated by a financial instrument holder to receive the instrument's proceeds upon death (e.g., a mutual fund nominee, bank account nominee). A nominee is NOT the legal owner — they hold the asset in trust for the legal heirs determined by the will or succession law. The system detects and warns when a nominee differs from the intended beneficiary.

---

**Probate**
`code: probate_required: Boolean (derived from asset location)`
`UI: Probate Required`
A court-granted permission to execute a will, mandatory in some Indian jurisdictions. In Mumbai, Chennai, and Kolkata (the three Presidency Towns), probate is mandatory for wills involving immovable property. The system flags the requirement based on the location of Real Estate assets.

---

**Stamp Duty (Gift)**
`code: stamp_duty_paid_minor_units, stamp_duty_rule_id`
`UI: Stamp Duty`
The tax payable on the gift deed document for immovable property, calculated as a percentage of the stamp duty value (circle rate value) of the property. Rates vary by state and by the relationship between donor and recipient. Stored in the `GiftRule` table per jurisdiction.

---

**Testator**
`code: (maps to User who owns the EstatePlan)`
`UI: You (Will Maker)`
The person who creates and signs a will. In Vittavaan, this is always the authenticated Investor user associated with the Estate Plan.

---

## Section D — Connections & Consent Terms

---

**Consent Scope**
`code: permissions: JSON, consent_scope: String`
`UI: Shared Data`
The explicit, user-defined list of data fields that an Investor has permitted a connected user (typically an Advisor) to view. Expressed as a JSON array of field identifiers. Every data access request is evaluated against this list by the `ConsentAndMarketplaceEngine`. The Advisor sees nothing outside this list, regardless of what other data the Investor has.

---

**Connection**
`code: Connection (entity), ConnectionStatusEnum {PENDING, ACCEPTED, REJECTED, REVOKED}`
`UI: Connection`
A mutual relationship between two users on the platform. Connections must be accepted before any data sharing can occur. Connections can be revoked by either party at any time; revocation immediately terminates all active data consents.

---

**Consent Audit Log**
`code: Document (type: CONSENT_FORM), immutable`
`UI: (internal — visible in Data Room as a record)`
An immutable record of every consent grant and revocation event, written to the Data Room at the moment of the event. Contains: grantor ID, grantee ID, permitted fields, purpose, timestamps. This is the legal evidence of consent under DPDP Act requirements.

---

**Data Access Grant**
`code: Connection.permissions (non-empty), consent_expires_at`
`UI: Data Access`
The configuration of a `Connection` where the Investor has specified which data fields the connected user may view, why, and until when. A connection without a data access grant is a social connection only.

---

**Protection Proxy**
`code: ConsentAndMarketplaceEngine (implements proxy pattern)`
`UI: (invisible to users — an enforcement mechanism)`
The design pattern implementation that intercepts every request for one user's data by another user and evaluates whether the requesting user holds a valid, unexpired, field-specific consent. Only the approved fields are included in the response. No access decision is ever made on the client side.

---

**Re-identification Risk**
`code: RiskLevelEnum {LOW, MEDIUM, HIGH}`
`UI: Privacy Risk`
The risk that a combination of disclosed characteristics in an anonymous borrower profile is specific enough to identify the user within the platform's user population. Assessed before submitting any profile to lenders. If risk is HIGH, the system warns the user and suggests reducing disclosed fields.

---

## Section E — Advisory & Marketplace Terms

---

**Advisor Match Reason**
`code: AdvisorMatch.match_reason`
`UI: Why this advisor`
A transparent, plain-language explanation of why a specific advisor appears in a user's search results. Based solely on the user's actual portfolio data (e.g., "Specialises in ESOP planning — you have unvested ESOPs"). Never based on paid placement or undisclosed commercial arrangements.

---

**Advisory Query**
`code: AdvisoryQuery (entity), QueryTypeEnum {TAX, ESTATE, INVESTMENT, VALUATION, LEGAL}`
`UI: Query`
A question submitted by an Investor to a specific connected Advisor, with a defined type. Queries progress through a lifecycle: `OPEN → IN_PROGRESS → RESOLVED → CLOSED`. Only queries of type `INVESTMENT` are restricted to advisors with verified `SEBI_RIA` certification.

---

**Data Freshness**
`code: data_freshness_days`
`UI: Data freshness`
The number of days since the investor's portfolio data was last updated by the investor. Displayed per connection to give both parties context on how current the shared data is.

---

**Market Insight**
`code: MarketInsight (entity)`
`UI: Market Insight`
A financial commentary article published by a verified Advisor on the platform. Insights are filtered for each Investor based on relevance to their actual holdings — an insight only appears in an Investor's feed if there is a traceable path from the insight's topic to a specific holding in the portfolio.

---

**Peer Benchmark**
`code: PeerBenchmark (entity)`
`UI: Peer Comparison`
An anonymised, aggregate comparison of one user's financial metrics against a cohort of users with similar characteristics (age band, city tier, income category, risk profile). **Never a ranking or leaderboard.** The cohort must have a minimum size (platform-configurable, default: 10 users) before the benchmark is surfaced to prevent de-anonymisation.

---

## Section F — Credit Terms

---

**Anonymous Borrower Profile**
`code: BorrowerProfile`
`UI: Credit Profile (Anonymous)`
A structured summary of an Investor's creditworthiness, constructed using only anonymised attributes (age band, city tier, income type — not amount, verified net worth band, security coverage multiple, DSR, on-time payment record). **No personally identifiable information (name, PAN, email, phone, employer)** is included. Submitted to empanelled lenders anonymously; the Investor's identity is disclosed only after they explicitly consent to a specific lender's bid.

---

**Debt Service Ratio (DSR)**
`code: debt_service_ratio`
`UI: Debt Service Ratio`
The ratio of the user's total monthly debt obligations (sum of all EMIs) to their stated monthly gross income. Expressed as a percentage: `(total_monthly_EMI / monthly_gross_income) × 100`. A DSR above 40–50% is generally considered high-risk by Indian lenders.

---

**Security Coverage Multiple**
`code: security_coverage_multiple`
`UI: Security Coverage`
The ratio of the value of assets offered as security for a loan to the loan amount requested: `eligible_security_value / requested_credit_amount`. A multiple of 2.0× means the offered security is worth twice the loan requested. Lenders typically require a coverage multiple well above 1.0× for comfort.

---

## Section G — Financial Planning Terms

---

**Financial Event**
`code: FinancialEvent`
`UI: Upcoming Events`
A time-bounded milestone in the user's financial life that the planning module tracks with a countdown. Examples: lease renewal date, insurance policy expiry, ESOP vesting window, FD maturity, loan balloon payment.

---

**Financial Resume**
`code: FinancialResumePayload`
`UI: Financial Resume`
A structured, shareable summary of the user's financial standing, analogous to a CV but for wealth. Contains: individual net worth (verified vs. total), income sources, DSR, liquidity buckets, investment track record, credit profile summary, and data quality indicators. The user can create a recipient-specific version that controls exactly which fields are disclosed.

---

**Funding Gap**
`code: funding_gap_minor_units`
`UI: Funding Gap`
For a financial goal, the difference between the `inflation_adjusted_target_amount` and the `projected_value_of_earmarked_assets` at the target year: `Funding Gap = GoalNeededThen - GoalProjectedValue`. A positive gap means the user is short; a negative gap means the goal is overfunded.

---

**Goal Status**
`code: GoalStatusEnum {ON_TRACK, SHORT, FUNDED, AT_RISK}`
`UI: Goal Status`
A derived classification of a financial goal's health:
- `ON_TRACK` — funding gap < 10% of target
- `SHORT` — funding gap 10–30% of target
- `AT_RISK` — funding gap > 30% of target
- `FUNDED` — gap is zero or negative (overfunded)

---

**Inflation-Adjusted Target Amount**
`code: inflation_adjusted_target_minor_units`
`UI: Target Amount in Today's Money`
The amount needed at the goal's target year, expressed in today's purchasing power — and also computed in future nominal terms using the user's specified `inflation_assumption_pct`. The Funding Gap is calculated using the future nominal target, not the today's amount.

---

**Invest vs. Prepay Crossover Return**
`code: crossover_return_pct`
`UI: Crossover Return`
In the invest-vs-prepay scenario calculator: the investment return rate at which the financial outcome of investing the surplus amount equals the outcome of prepaying the loan. Below this rate, prepayment wins; above it, investing wins.

---

**Liquidity Bucket**
`code: liquidity_bucket: LiquidityBucketEnum {T_PLUS_3_DAYS, T_PLUS_30_DAYS, T_PLUS_1_YEAR, ILLIQUID}`
`UI: Liquidity`
A classification of an asset by how quickly it can be converted to cash without significant loss. Bank savings accounts are `T_PLUS_3_DAYS`; listed equity is `T_PLUS_3_DAYS` (settlement T+1 but practical withdrawal); FDs with penalty clauses may be `T_PLUS_30_DAYS`; real estate is `ILLIQUID`. Used in the Financial Resume and Planning page to assess short-term financial resilience.

---

## Section H — System & Infrastructure Terms

---

**Calculation Version**
`code: calculation_version: String`
`UI: (internal metadata — shown in Data Room audit records)`
A version tag appended to every `FinancialSnapshot` and performance calculation result, identifying which version of the calculation engine produced it. Enables investigation when a formula is updated — historical snapshots are not retroactively recalculated, and the version tag shows which formula applied.

---

**Financial Year (FY)**
`code: financial_year_start: Month.APRIL, financial_year_end: Month.MARCH`
`UI: FY 2024–25 (Apr 2024 – Mar 2025)`
The Indian financial year runs from **April 1 to March 31** of the following calendar year. All tax-related calculations (gift tax thresholds, LTCG/STCG classification, tax-loss harvesting windows) use the Indian FY, not the calendar year. The system's transaction aggregation for annual summaries respects this convention.

---

**Indian Numbering System**
`code: formatters.ts:formatINR()`
`UI: ₹1,47,32,500 (not ₹14,732,500)`
The Indian convention for grouping digits in large numbers: the rightmost three digits form the first group, then groups of two digits (not three) to the left. One lakh = 1,00,000. One crore = 1,00,00,000. All currency display in the UI must use this convention.

---

**Immutable Ledger**
`code: Transaction, FinancialSnapshot (both append-only)`
`UI: (invisible convention — users cannot edit/delete these records)`
The design principle that financial records (`Transaction` and `FinancialSnapshot`) are permanent once written. No UPDATE or DELETE SQL is ever executed on these tables. Errors are corrected by logging correcting entries (for transactions) or by allowing the background snapshot job to write a new snapshot (for performance data).

---

**Is Partial**
`code: is_partial: Boolean`
`UI: Estimated ⚠️ or Partial Data`
A metadata flag on any calculated metric indicating that the calculation could not use complete, current data for all inputs. For example, if XIRR is computed for a 3-year window but the portfolio has stale valuations for one year, `is_partial = true`. **Partial data is always disclosed to the user — it is never silently presented as complete.**

---

**Provenance**
`code: {as_of: DateTime, calculation_version: String, source_ids: List[UUID], is_partial: Boolean}`
`UI: Data as of [date] · [Verified / Estimated]`
The metadata attached to every derived metric that documents: when the metric was calculated, which version of the calculation engine produced it, which source records were used, and whether the data is complete. Provenance is the system's mechanism for transparency — users always know the basis for what they see.

---

**Ubiquitous Language**
`(this document is the definition)`
The shared vocabulary agreed upon by all stakeholders (product, engineering, design, advisors) and used consistently in every artefact: code variables, API fields, database columns, UI labels (with allowed display name variations), and documentation. Deviations must update this glossary.

---

*This glossary covers the core domain. Additional terms will be added as Phase 3 and Phase 4 introduce implementation-specific concepts (e.g., specific API field names, migration terminology, CI/CD pipeline terms).*

*← Previous: [02_Sequence_Diagrams.md](./02_Sequence_Diagrams.md)*
