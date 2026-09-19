# Phase 1 — India Legal Rules Catalogue

> **OOSE Phase:** Requirements Elicitation
> **Purpose:** Documents every Indian legal and tax rule that the Vittavaan system must encode, evaluate, or display. This is the "business rules source of truth" — the reference that engineers and the calculation engines will implement.
> **Why this document exists:** Wealth management is not a generic SaaS application. Many features (gift tax, inheritance allocation, credit profiles, stamp duty, succession) depend on specific provisions of Indian law. Encoding these incorrectly creates legal risk for users. This catalogue ensures every rule is traceable to its legal source, versioned for regulatory changes, and flagged where professional review is required.
> **Status:** Draft — requires review by a qualified CA or legal advisor before implementation

---

> [!CAUTION]
> **THIS IS NOT LEGAL ADVICE.** This document is an engineering specification for encoding publicly available Indian legal provisions into a software system. It does not constitute legal, tax, or financial advice. Users of Vittavaan should be advised to consult qualified professionals for their specific situations. Rules encoded here must be reviewed by a qualified CA / Advocate before the relevant features are launched.

---

## How Rules Are Stored in the System

All rules in this catalogue will be stored in database tables with the following mandatory fields on every rule record:

```
jurisdiction          TEXT        -- e.g., 'INDIA', 'MAHARASHTRA', 'KARNATAKA'
law_reference         TEXT        -- e.g., 'Income Tax Act 1961, Section 56(2)(x)'
rule_effective_date   DATE        -- date from which this version of the rule applies
rule_version          TEXT        -- e.g., 'FA2024' (Finance Act 2024 version)
calculation_date      DATE        -- date on which a specific evaluation was performed
professional_review_required  BOOLEAN  -- true = this rule has interpretation ambiguity
notes                 TEXT        -- plain-language explanation
```

**Engineering principle:** A rule change (e.g., new Finance Act budget changes a threshold) requires a new database record with an updated `rule_effective_date`. The old record is retained permanently for historical evaluations.

---

## Rule Set 1: Gift Tax Rules

### Legal Source
- Income Tax Act 1961, Section 56(2)(x), as amended by successive Finance Acts
- Income Tax Act 1961, Section 47 (transfers not regarded as transfers for capital gains)

### Purpose in Vittavaan
Used by the **Gift Rules page**, the **Gift Transfer tracker**, and the `GiftRule` entity to:
1. Determine whether a proposed gift is exempt or taxable in the recipient's hands
2. Calculate the taxable amount if the gift is above the threshold
3. Display the applicable exemption basis (relationship-based vs. threshold-based)

---

### Rule 1.1 — Gifts Between "Relatives" Are Fully Exempt

**Statement:** Under Section 56(2)(x), a gift received from a "relative" as defined in the Explanation to Section 56(2)(vii) is fully exempt from income tax in the recipient's hands, regardless of amount.

**Definition of "relative" for this purpose:**
- Spouse of the individual
- Brother or sister of the individual
- Brother or sister of the spouse of the individual
- Brother or sister of either of the parents of the individual
- Any lineal ascendant or descendant of the individual
- Any lineal ascendant or descendant of the spouse of the individual
- Spouse of a person referred to above

**System encoding required:**
- A `RelationshipType` enum in the `HouseholdMember` model with values that map to this exemption list
- A `evaluate_gift_tax_status(donor_user_id, recipient_member_id)` function that returns `EXEMPT_RELATIVE` for matching relationships
- Display of the specific relationship that qualifies as the exemption basis

**Status:** Settled law — `professional_review_required = false`

---

### Rule 1.2 — Non-Relative Gift Threshold

**Statement:** Gifts received from non-relatives are taxable in the recipient's hands if the **aggregate value of all gifts received in a financial year exceeds ₹50,000**. The entire amount (not just the excess) becomes taxable as "Income from Other Sources."

**Key parameters (as of FY 2024-25):**
- Annual threshold: ₹50,000 (minor units: `5000000` paise)
- Taxable amount: Full aggregate value (not just excess above threshold)
- Tax treatment: Added to recipient's income, taxed at applicable slab rate

**System encoding required:**
- The `GiftRule` table stores `annual_exemption_limit_minor_units = 5000000`
- The system tracks cumulative non-relative gifts received by the user in the current financial year (April 1 to March 31)
- Warning displayed when a new gift would push the cumulative total above the threshold
- `TaxableGiftAmount` calculation: if aggregate > threshold, taxable = full aggregate

**Status:** Settled law — `professional_review_required = false`

---

### Rule 1.3 — Gifts Received on Certain Occasions Are Exempt

**Statement:** Gifts received on specific occasions are exempt regardless of amount or relationship:
1. On the occasion of the marriage of the individual
2. Under a will or by way of inheritance
3. In contemplation of death of the donor
4. From a local authority (Section 10(20))
5. From a fund, foundation, university, hospital, or institution referred to in Section 10(23C)
6. From a trust or institution registered under Section 12A or 12AA

**System encoding required:**
- `GiftOccasionType` enum with values: `MARRIAGE`, `INHERITANCE`, `CONTEMPLATION_OF_DEATH`, `OTHER`
- When `occasion = MARRIAGE` or `INHERITANCE`, the gift evaluation returns `EXEMPT_OCCASION`
- Note: Vittavaan tracks gifts between living persons — the `INHERITANCE` case is covered separately by the Estate Planning module

**Status:** Settled law — `professional_review_required = false`

---

### Rule 1.4 — Immovable Property Gifts

**Statement:** For gifted immovable property (real estate), the taxable value in the recipient's hands is the **stamp duty value** of the property, not the consideration paid (which is zero for a gift).

**Key parameters:**
- If stamp duty value > ₹50,000 (for non-relatives), the full stamp duty value is taxable
- Safe harbour: if the difference between stamp duty value and actual consideration does not exceed the higher of ₹50,000 or 10% of consideration — not applicable for gifts (consideration = zero)

**System encoding required:**
- For real estate gifts, use `StampDutyValue` (not `CurrentMarketValue`) as the basis for gift tax calculation
- The system should prompt the user to enter the stamp duty circle rate value for tax computation purposes
- `GiftValue` for real estate = stamp duty value at the time of registration

**Status:** Settled law — `professional_review_required = false`

---

### Rule 1.5 — Gift Asset Eligibility Restrictions

**Statement:** Certain assets cannot be gifted despite being legally owned:

| Restriction | Affected Asset | Reason |
|---|---|---|
| `PLEDGED_ASSET` | Any asset pledged as loan collateral | Legal encumbrance; lender consent required |
| `JOINT_ASSET_NO_CONSENT` | Joint asset where co-owner consent not obtained | Fractional interest can be gifted; full asset cannot |
| `EPF_BALANCE` | EPF accumulations | EPFO rules prohibit assignment or transfer |
| `UNVESTED_ESOP` | ESOPs not yet vested | No legal ownership of unvested options |
| `NPS_ACCUMULATION` | NPS Tier-I balance | PFRDA rules prohibit transfer |
| `NOMINEE_NOT_OWNER` | Assets where user is nominee but not legal owner | Nominee holds in trust for legal heirs; cannot gift |
| `PPF_BALANCE` | PPF balance | PPF rules prohibit transfer (can only be pledged) |

**System encoding required:**
- `GiftEligibilityStatus` enum per asset type
- Pre-gift checklist that evaluates each restriction before allowing a gift to be logged
- Warning + block on gift transfer initiation for ineligible assets
- For `JOINT_ASSET`, display the maximum giftable value = `GrossAssetValue × UserOwnershipPct`

**Status:** Settled law for most; some ESOP cases require professional review — `professional_review_required = true` for ESOP

---

## Rule Set 2: Inheritance & Succession Rules

### Legal Source
- Hindu Succession Act 1956 (as amended 2005)
- Indian Succession Act 1925 (for non-Hindu users)
- Transfer of Property Act 1882

### Purpose in Vittavaan
Used by the **Inheritance page** and **Will page** to:
1. Show the default intestacy (no-will) distribution for each asset
2. Flag conflicts between the user's intended allocation and legal defaults
3. Model what happens to assets not covered by the will

---

### Rule 2.1 — Hindu Succession Act — Class I Heirs

**Statement:** For a Hindu male dying intestate (without a will), the estate passes equally to Class I heirs simultaneously:

**Class I Heirs:**
1. Son
2. Daughter
3. Widow (spouse)
4. Mother
5. Son of a predeceased son
6. Daughter of a predeceased son
7. Son of a predeceased daughter
8. Daughter of a predeceased daughter
9. Widow of a predeceased son
10. Son of a predeceased son's predeceased son
11. Daughter of a predeceased son's predeceased son
12. Widow of a predeceased son's predeceased son

**System encoding required:**
- The Household Member's `relationship` field determines which Class I category they belong to
- `DefaultInheritanceSharePct = 1 / (count of surviving Class I heirs)`
- Display "Hindu Succession Act 1956 — Class I" as the legal basis
- Flag if the user has no Class I heirs (estate would pass to Class II heirs — show a warning to seek legal advice)

**Status:** Settled law — `professional_review_required = false` for standard cases; complex family structures require professional advice

---

### Rule 2.2 — Hindu Succession Act 2005 Amendment — Daughters' Rights

**Statement:** The Hindu Succession (Amendment) Act 2005 gives daughters equal rights as sons (coparcenary rights in HUF property). Daughters have the same rights regardless of whether they were born before or after the 2005 amendment.

**System encoding required:**
- The system SHALL NOT distinguish between sons and daughters in inheritance share calculations
- Retrospective effect: applies even to daughters born before 2005
- Note: HUF-specific coparcenary property is out of V1 scope, but this principle applies to standard estate calculations

**Status:** Settled law (confirmed by Supreme Court in Vineeta Sharma v. Rakesh Sharma, 2020) — `professional_review_required = false`

---

### Rule 2.3 — Nomination vs. Legal Ownership

**Statement:** A nominee for a financial asset (bank account, mutual fund, equity demat) is NOT the legal owner of the asset on the account holder's death. The nominee holds the asset **in trust for the legal heirs**. Legal title passes to heirs as determined by the will or succession law.

**Critical exception:** Under the Companies Act 2013 and the Depositories Act 1996, nominees of demat accounts in a company's register of members DO acquire full ownership (they are not merely custodians).

**System encoding required:**
- Flag a `NomineeBeneficiaryMismatch` when the user-specified nominee differs from the will beneficiary or intended heir
- Display a warning: "Your nominee for [asset] is [name], but your will/allocation designates [name]. A nominee may only hold in trust for legal heirs — this may lead to a dispute."
- For equity demat specifically: flag the Companies Act exception separately

**Status:** Settled law but frequently misunderstood — `professional_review_required = false` for display; user should consult advisor for resolution

---

### Rule 2.4 — Will Registration — Optional but Advisable

**Statement:** Registration of a will in India is NOT mandatory under the Registration Act 1908. An unregistered will is legally valid. However, a registered will is more difficult to challenge and easier to probate.

**System encoding required:**
- `WillRegistrationStatus` field: `UNREGISTERED`, `REGISTERED`, `NOTARISED`
- Display advisory note: "Your will is not registered. While valid, registering it at the Sub-Registrar's office makes it harder to contest and easier to execute."
- No legal consequence encoded in V1 for unregistered status (it is a recommendation, not a requirement)

**Status:** Settled law — `professional_review_required = false`

---

### Rule 2.5 — Probate Requirements by Jurisdiction

**Statement:** Probate (court-granted permission to execute a will) is mandatory in some jurisdictions:
- **Mumbai, Chennai, Kolkata (Presidency Towns):** Probate is mandatory for wills of immovable property
- **Rest of India:** Probate is NOT mandatory (the will can be executed without probate)
- **Immovable property outside the three Presidency Towns:** Succession certificate or Letters of Administration may be needed instead

**System encoding required:**
- `ProbateRequired` flag set based on the location of assets covered by the will
- If any Real Estate asset is in Mumbai, Chennai, or Kolkata: display a specific `PROBATE_REQUIRED` warning
- Otherwise: display `SUCCESSION_CERTIFICATE_MAY_BE_NEEDED` advisory

**Status:** Settled law — `professional_review_required = false` for display; professional advice required for execution

---

## Rule Set 3: Stamp Duty on Gift Deeds

### Legal Source
- Indian Stamp Act 1899
- State-specific Stamp Acts (Bombay Stamp Act 1958, Karnataka Stamp Act 1957, etc.)

### Purpose in Vittavaan
Used by the **Gift Transfer page** to calculate `StampDutyAmount` and `TotalTransferCost`.

---

### Rule 3.1 — Stamp Duty on Gift Deed (Immovable Property)

**Statement:** Stamp duty on a gift deed for immovable property varies by state. The following are illustrative rates (must be verified and updated annually by the System Administrator):

| State | Stamp Duty on Gift to Relative | Stamp Duty on Gift to Non-Relative |
|---|---|---|
| Maharashtra | 3% of stamp duty value | 5% of stamp duty value |
| Karnataka | ₹5,000 (fixed, to blood relative) | 5.65% of market value |
| Delhi | 2% of value (female donee) / 4% (male donee) | 4–6% of value |
| Tamil Nadu | 1% of value (to relatives) | 7% of value |

**System encoding required:**
- `StampDutyRule` table: `state`, `relationship_category` (`RELATIVE`/`NON_RELATIVE`), `duty_type` (`PERCENTAGE`/`FIXED`), `duty_rate`, `rule_effective_date`, `law_reference`
- The Gift Transfer page queries this table based on the asset's state and the donor-recipient relationship
- **All stamp duty rates are configured by the System Administrator — they are NEVER hardcoded in application logic**
- Display the full rate table to the user for transparency

**Status:** Varies by state; rates change — `professional_review_required = true`; administrator must update annually

---

### Rule 3.2 — Registration Fee on Gift Deed

**Statement:** Gift deeds for immovable property must be registered with the Sub-Registrar of Assurances. Registration fee is typically 1% of the property value, subject to a state-specific cap.

**System encoding required:**
- `RegistrationFeeRule` table per state: `fee_rate`, `fee_cap_minor_units`, `rule_effective_date`
- Calculated as: `min(property_value × fee_rate, fee_cap_minor_units)`

**Status:** Varies by state — `professional_review_required = true`

---

## Rule Set 4: Capital Gains on Asset Transfers

### Legal Source
- Income Tax Act 1961, Sections 45, 47, 48, 54, 54F

### Purpose in Vittavaan
Used by the **Gift Transfer page** and **Marketplace listing** to flag capital gains implications for the donor/seller.

---

### Rule 4.1 — Gift is Not a "Transfer" for the Donor — Capital Gains Not Triggered

**Statement:** Under Section 47(iii) of the Income Tax Act, a gift is not regarded as a "transfer" for the purpose of capital gains tax. Therefore, the **donor does not pay capital gains tax** at the time of the gift.

**However:** The **recipient's cost basis** carries over from the donor's original acquisition cost (stepped-up to the donor's cost, not the market value on gift date).

**System encoding required:**
- Display to donor: "No capital gains triggered for you on this gift."
- `RecipientCarriedCostBasis = DonorOriginalCostBasis` (not current market value)
- `RecipientHoldingPeriodStart = DonorOriginalAcquisitionDate` (holding period carries over for certain assets)

**Status:** Settled law — `professional_review_required = false`

---

### Rule 4.2 — Holding Period Classification (for Recipient's Future Sale)

**Statement:** When the recipient eventually sells the gifted asset, the holding period includes the donor's holding period for the same asset. The classification (`SHORT_TERM` vs. `LONG_TERM`) depends on the combined holding period:

| Asset Type | Long-Term Threshold |
|---|---|
| Listed equity, equity MFs, units (STT paid) | > 12 months |
| Unlisted equity, REITs | > 24 months |
| Immovable property | > 24 months |
| Debt MFs (post April 2023) | No LTCG benefit; always taxed as STCG |
| Gold ETFs, Fund of Funds | > 24 months |

**System encoding required:**
- `AssetHoldingPeriodRule` table per asset subtype: `long_term_months_threshold`
- `RecipientHoldingPeriodStart` calculated from gift transfer record
- Display to user at gift logging time: the recipient's cost basis, holding period start, and the tax classification they will inherit

**Status:** Mostly settled; debt MF change is post-April 2023 new regime — `professional_review_required = false` for display

---

## Rule Set 5: Credit Profile Rules

### Legal Source
- RBI Guidelines on Credit Information Companies
- Credit Information Companies (Regulation) Act 2005
- SEBI (Investment Advisers) Regulations 2013

### Purpose in Vittavaan
Used by the **Credit module** to build and share an anonymous borrower profile.

---

### Rule 5.1 — Regulated Lender Constraint

**Statement:** Vittavaan's credit facilitation module may only match users with RBI-regulated entities: Scheduled Commercial Banks, RBI-registered NBFCs, or Housing Finance Companies regulated by the National Housing Bank.

**System encoding required:**
- `LenderRegistry` table with: `entity_name`, `entity_type` (`BANK`/`NBFC`/`HFC`), `rbi_registration_number`, `registration_status` (`ACTIVE`/`SUSPENDED`)
- Lender matching filters out any lender not in this registry or with `registration_status != 'ACTIVE'`

**Status:** Regulatory requirement — `professional_review_required = false`

---

### Rule 5.2 — Credit Bureau Score Interpretation (CIBIL)

**Statement:** TransUnion CIBIL scores range from 300 to 900. The following bands are commonly used in Indian lending (not a formal regulatory definition — lender-specific):

| Band | Score Range | Typical Lender Response |
|---|---|---|
| EXCELLENT | 750–900 | Best rates; minimal documentation |
| GOOD | 700–749 | Good rates; standard documentation |
| FAIR | 650–699 | Possible approval; higher rates |
| POOR | 600–649 | Difficult; limited lenders |
| VERY_POOR | 300–599 | Likely rejection by most lenders |

**System encoding required:**
- `CibilScoreBand` enum and labelling in the Credit module UI
- No automated credit decision — the score band is displayed informationally
- CIBIL score is user-input in V1; bureau API integration is V2

**Status:** Illustrative market convention — `professional_review_required = false` (display only, no enforcement)

---

## Rule Set 6: Advisor Regulatory Framework

### Legal Source
- SEBI (Investment Advisers) Regulations 2013 (as amended 2020)
- Institute of Chartered Accountants of India (ICAI) Act 1949
- Insolvency and Bankruptcy Board of India (IBBI) Valuer Regulations 2017
- Bar Council of India Rules

### Purpose in Vittavaan
Used by the **Advisor Marketplace** to validate credentials and restrict what unverified advisors can do.

---

### Rule 6.1 — SEBI RIA Restriction

**Statement:** Only SEBI-registered Investment Advisers (RIAs) are permitted to provide personalised investment advice for a fee under Indian law. A CA or CFA providing investment advice without SEBI RIA registration is potentially in violation of the SEBI IA Regulations.

**System encoding required:**
- Investment advice-related actions (e.g., portfolio recommendation, asset allocation suggestions) are restricted in the platform to users with `certification = 'SEBI_RIA'` and `CredentialVerificationStatus = 'VERIFIED'`
- Non-SEBI-RIA advisors may: publish market insights (general information), answer estate or tax queries, provide valuation reports
- System disclaimer: "Vittavaan is not a SEBI-registered investment adviser. Personalised investment advice is provided only by SEBI-RIA-certified advisors on this platform."

**Status:** Regulatory requirement — `professional_review_required = false` (restriction enforcement); content of advice is outside system scope

---

### Rule 6.2 — CA / CS Practice Limitations

**Statement:** Chartered Accountants and Company Secretaries are regulated by ICAI and ICSI respectively. They may provide tax, accounting, and compliance advice. However, a CA who also wishes to provide investment advice must have a separate SEBI RIA registration.

**System encoding required:**
- `AdvisorProfile.certifications` is a list — a user can hold both `CA` and `SEBI_RIA`
- The platform tags advisory queries with a type: `TAX`, `ESTATE`, `INVESTMENT`, `VALUATION`, `LEGAL`
- Only `SEBI_RIA` advisors receive `INVESTMENT`-type query routing

**Status:** Regulatory — `professional_review_required = false`

---

## Rule Set 7: Data Retention Rules

### Legal Source
- Income Tax Act 1961, Section 44AA and Rule 6F (record retention for 6 years from end of assessment year)
- Companies Act 2013 (for business records — out of V1 scope)
- Reserve Bank of India KYC Master Directions 2016

### Purpose in Vittavaan
Used by the **Account Closure** process in Settings.

---

### Rule 7.1 — Financial Record Retention Period

**Statement:** Section 44AA of the Income Tax Act requires that books of account and financial records be retained for **6 years from the end of the relevant assessment year** (i.e., effectively 6–7 years from the financial year in which the transaction occurred).

**System encoding required:**
- On account closure request: calculate `RetentionExpiryDate = max(6 years from last transaction date, 7 years from account registration date)`
- Personal identifiers (name, email, phone, PAN) are purged immediately upon closure confirmation
- Financial records (transactions, assets, snapshots) are retained until `RetentionExpiryDate`
- At `RetentionExpiryDate`, all remaining records are deleted via a scheduled purge job

**Status:** Settled law — `professional_review_required = false`

---

## Appendix: Rules Requiring Future Research / Professional Input

The following areas require further input from a qualified CA or Advocate before the corresponding features are built:

| Rule Area | Uncertainty | Recommended Action |
|---|---|---|
| HUF gifting rules | Complex interaction between Hindu law and Income Tax Act for HUF property | Obtain formal legal opinion before implementing HUF gifting |
| NRI gift exemptions | Different rules apply when donor or recipient is NRI (FEMA implications) | Defer to V2 with NRI-specific flag |
| Will contestation grounds | Grounds on which a will can be challenged (lack of testamentary capacity, undue influence) | Add informational content with `professional_review_required = true` |
| ESOP gift/transfer | Whether unvested ESOPs can be nominated or willed | Obtain ESOP-specific legal opinion |
| Agricultural land succession | Special rules in many states (e.g., Karnataka Land Reforms Act restricts non-agriculturalist ownership) | Flag all agricultural land with `professional_review_required = true` |
| Benami Transactions Prohibition Act | Implications when ownership and beneficial ownership differ | Display warning on any asset with < 100% ownership split involving non-relatives |

---

*Next document: [05_Use_Cases.md](./05_Use_Cases.md)*
