# Project Overview: Vittavaan

> **Document Status:** Living specification — to be updated as the project evolves.
> **Primary Audience:** All stakeholders — product, design, engineering, and QA.

---

## 1. The Vision

**Vittavaan** (Sanskrit: *vittam* = wealth/money; *vaan* = carrier/vessel) is a **comprehensive, India-first wealth management and financial networking platform**. It gives individuals and families a single, structured place to see, understand, manage, and eventually transfer their wealth — across every asset class they actually own.

The long-term ambition is to be the **"source of truth" for a household's financial life**: a living ledger connected to banks, mutual fund registrars, and stock exchanges, with the intelligence to help users plan their future, benchmark themselves against peers, and work with professional advisors — all without surrendering privacy.

**Version 1 (the focus of this initial build):** All data entry is manual. The user is in full control of every number they put in. No external API connections exist yet. The architecture must, however, be designed so that plugging in Account Aggregators (AA), SEBI market feeds, and banking APIs in V2 requires minimal refactoring.

---

## 2. Who Is This For?

Vittavaan serves the **affluent and aspirationally affluent Indian household** — typically urban professionals, business owners, or HNI (High Net-worth Individuals) families who:

- Hold assets across multiple classes: equities, mutual funds, real estate, gold, alternative collections, unlisted shares, EPF, FDs.
- Have joint ownership structures, family trusts, or partial ownerships (e.g., a plot co-owned with siblings).
- Need to track liabilities just as carefully as assets.
- Are beginning to think about estate planning, gifts to family, and wealth succession.
- Want to engage professional advisors (CAs, SEBI RIAs, advocates, valuers) without losing control of their financial data.

### Primary Actors

| Actor | Description |
|---|---|
| **Investor** | The primary user managing their personal and household portfolio |
| **Advisor** | A professional user (CA, SEBI RIA, advocate, valuer, CFA) who may also be an Investor |
| **Household Member / Beneficiary** | A tracked family member who may receive assets or inheritance |
| **System Administrator** | Internal platform admin managing credential verification and system health |
| **External Auth Provider** | The authentication service issuing verified tokens to the platform |
| **External Financial API** *(Future V2)* | Account Aggregators, CDSL/NSDL, market data feeds |

---

## 3. What Problem Does It Solve?

Most Indian households with significant assets face a **fragmented wealth picture**:

- Equity portfolio in one app (Zerodha, Groww), mutual funds in another (MF Central), property records in a physical file, gold in a locker, FDs in a bank branch, and a will written a decade ago that references assets they no longer own.
- No single view of **net worth** that accounts for fractional ownership correctly.
- No systematic way to see if they are **on track for their goals** (retirement, children's education, house purchase).
- No structured way to **share financial data** with a CA for tax filing or an advisor for planning, without handing over complete access.
- No platform that understands the **Indian legal and tax context**: gift tax exemptions between relatives, Hindu Undivided Family (HUF) structures, succession under the Hindu Succession Act, stamp duty on property transfers.

Vittavaan solves all of this in one integrated, privacy-first platform.

---

## 4. Core Features & Platform Map

Vittavaan is organized into **six functional domains**, each mapping to one or more screens in the wireframe:

### 4.1 Dashboard & Net Worth (`Net Worth`, `Assets & Liabilities`, `Analysis`, `Attribution`)
The central view every user sees after login. It shows:
- **Total Assets, Total Liabilities, Net Worth** — updated whenever any holding changes.
- **Month-over-month and 12-month change** in net worth, broken down by what drove the change (equity gains, real estate revaluation, new investment, loan repayment).
- **Asset class breakdown**: Liquid (equities, MFs, FDs, cash), Real Estate, Alternative (gold, stamps, art, unlisted shares).
- **Verification status**: what percentage of wealth is verified vs. self-declared — a trust signal for the platform and for advisors.
- **Performance Analysis (XIRR, TWRR)**: money-weighted and time-weighted returns over selectable windows.
- **Attribution**: which asset class, sector, or holding contributed how much to the portfolio's return.
- **"Worth a Look" alerts**: stale valuations, fund overlaps, concentration risks, upcoming financial events.

### 4.2 Portfolio Ledger (`Assets & Liabilities`, `Karjat Plot`, `Stamp Collection`, `Credit`)
The user's full portfolio in detail:

**Assets — three types:**
- **Liquid Assets**: bank accounts, FDs, equities, mutual funds, ETFs, crypto, EPF, PPF. Identified by institution, ticker, or scheme. Ready for live price feeds in V2.
- **Real Estate Assets**: residential, commercial, land. Tracked by address, area (sqft), price per sqft, ownership percentage (critical for co-owned plots). The *Karjat Plot* wireframe is the prototype for this view.
- **Alternative Assets**: stamp collections, art, numismatics, gold (physical), unlisted company stakes. Tracked by last appraisal date and appraiser. The *Stamp Collection* wireframe is the prototype.

**Liabilities:**
- Home loans, personal loans, car loans, credit cards, business loans.
- Tracked by outstanding principal, interest rate (fixed/floating), EMI, due date.
- Amortization schedule and Debt Service Ratio calculated automatically.

**Cash Flow Ledger:**
- Every inflow (salary, rent, dividends, interest) and outflow (EMIs, expenses, repairs) is logged.
- Monthly surplus, savings rate, and income-by-source are derived here.

**Data Room (Documents):**
- Secure document uploads linked to specific assets or estate plan elements.
- Document types: title deeds, valuation reports, purchase agreements, will copies, consent forms.

**Credit Module:**
- A structured facility to build an anonymous borrower profile and submit it to empanelled lenders for credit bids.
- The user's verified net worth, income, and repayment history feed into a black-box profile shared with lenders only after explicit consent.

### 4.3 Financial Planning (`Planning`, `Investor Profile`, `Profiling`)
- **Financial Goals**: retirement corpus, children's education, house purchase, foreign trip — anything with a target amount and a target year.
- Each goal can have specific assets "earmarked" for it.
- The system calculates the **funding gap**: what the user needs vs. what their current portfolio will grow to under stated return assumptions.
- **Invest vs. Prepay Calculator**: should you pay down a loan early or invest that money instead?
- **Investor Profiling**: a structured questionnaire that determines risk capacity, risk tolerance, liquidity needs, investment horizon, and behavioral biases — without collapsing everything into one opaque "risk score."
- **Financial Resume**: a shareable, recipient-specific summary of a user's financial standing — like a credit report, but richer and under the user's control. Can be attested by a professional.

### 4.4 Estate & Legal Planning (`Household`, `Inheritance`, `Will`, `Gift Rules`, `Gift Transfer`)
This is a differentiator few wealth apps tackle:

- **Household**: register all family members (spouse, children, parents, siblings). Each member has a role, DOB, and relationship. The household view shows a **consolidated balance sheet** that counts jointly held assets only once.
- **Will & Estate Plan**: appoint primary and secondary executors. Upload the will document. Track which assets are covered by the will, which are not, and where nominations conflict with will instructions.
- **Inheritance Allocation**: for each asset, assign percentage shares to beneficiaries. The system enforces that allocations don't exceed 100% of an asset.
- **Gift Rules Engine**: a rules database encoding the Indian Income Tax Act's gift exemptions — gifts between "relatives" (as defined) are exempt; gifts above ₹50,000 from non-relatives are taxable in the recipient's hands. Checks whether an asset can legally be gifted (e.g., pledged assets cannot be gifted).
- **Gift Transfer Tracker**: log a specific gift (asset or cash), track the deed status, registration, mutation, stamp duty paid, and update the ledger when legal transfer completes.

### 4.5 Connections & Networking (`Connections`, `Peers`)
Privacy-first social graph:
- **Connections**: connect with other platform users — friends, family, or professionals.
- **Granular Consent**: when you connect with an advisor, you choose *exactly* what they can see (total net worth only? specific real estate? no liabilities?), and for *how long* (consent expires automatically).
- **Peers module**: see what connected peers have chosen to share. Not a leaderboard or ranking system — no "better/worse" signals. Just structured, consensual peer financial sharing.
- **Consent Audit Trail**: every grant and revocation is logged immutably in the Data Room as a consent document.

### 4.6 Advisor Marketplace (`Advisors`, `Marketplace`, `Marketplace Browse`, `Marketplace Land`, `Ask`, `Trends & News`)
- **Advisor Directory**: browse verified CAs, SEBI RIAs, advocates, valuers, and CFAs. Advisors are matched to users based on actual holdings and detected needs, not paid placement.
- **Advisor Credentials**: certifications are verified against authoritative registers (ICAI, SEBI RIA registry, IBBI valuer registry).
- **Ask Module**: send a consultation query to a specific advisor. Natural-language questions grounded in the user's actual ledger (e.g., "How much did my Karjat plot actually return in the last 3 years?").
- **Trends & News**: a curated feed of market insights, tax policy updates, and economic news — filtered to what is actually relevant to the user's holdings, not generic clickbait.
- **Marketplace Listings**: a platform where users can list assets (property, collectibles, unlisted stakes) for sale or transfer, with structured verification checks before a listing goes live.

---

## 5. Key Design Principles

### 5.1 Absolute Financial Accuracy
All monetary values are stored and calculated as **integers in minor units (paise)**. Floating-point arithmetic is explicitly prohibited for money. This prevents rounding errors in net worth, returns, and inheritance calculations.

### 5.2 Ownership-Attributed Aggregation
Jointly owned assets are a common reality in Indian households. **Every asset carries an ownership percentage**. Net worth, household aggregation, and inheritance calculations always apply this percentage before summing — preventing double-counting.

### 5.3 Verification-Gated Actions
Data has a **verification level** (Self-declared → Documented → Verified → Accepted). More sensitive actions (credit applications, formal financial resumes, marketplace listings) require higher verification levels. The platform nudges users to document and verify their holdings over time.

### 5.4 Zero-Trust Privacy by Design
The platform operates on an explicit-consent model. **No data is shared without a time-bound, field-level grant**. Advisors see only what the investor explicitly permits, only for as long as permitted. Every consent is logged.

### 5.5 India-Specific Legal & Tax Context
Calculations, rules, and terminology are grounded in Indian law: the Income Tax Act (gift exemptions, capital gains), Hindu Succession Act, Transfer of Property Act, SEBI regulations for advisors. Legal rules are **versioned** so that regulatory changes can be tracked and prior calculations explained.

### 5.6 Extensibility for V2 API Integrations
The architecture uses an **adapter/abstraction layer** between the data entry layer and the domain model. In V1, the "adapter" is manual user input. In V2, it will be replaced by Account Aggregator (AA) APIs, CDSL/NSDL portfolio feeds, and market data streams — with zero changes to the core domain logic.

### 5.7 Cross-Platform (Desktop & Mobile)
V1 targets the **desktop web browser**. The backend API is designed as a **platform-agnostic service layer** — all business logic lives server-side. The mobile app (V2 roadmap) will consume the same APIs. Shared calculation engines, shared data model, separate UI implementations.

---

## 6. The 25 Wireframe Screens — Full Map

| # | Screen / File | Domain | Purpose |
|---|---|---|---|
| 1 | Net Worth Dashboard (v3) | Dashboard | Primary overview: net worth, asset allocation, alerts |
| 2 | Assets & Liabilities | Portfolio | Multi-tab ledger: holdings, debts, cash flow, data room |
| 3 | Analysis | Dashboard | Portfolio return analysis (XIRR, TWRR, drawdown) |
| 4 | Attribution | Dashboard | Return attribution by asset class, sector, holding |
| 5 | Karjat Plot | Portfolio | Prototype real estate asset detail view |
| 6 | Stamp Collection | Portfolio | Prototype alternative asset detail & marketplace listing |
| 7 | Credit | Portfolio | Anonymous credit profile builder & lender bid dashboard |
| 8 | Planning | Planning | Goals, funding gap, investment vs. prepay calculator |
| 9 | Investor Profile | Planning | Risk/behavioral profiling questionnaire |
| 10 | Financial Resume | Planning | Shareable, recipient-specific financial standing summary |
| 11 | Household | Estate | Consolidated household balance sheet & member registry |
| 12 | Inheritance | Estate | Asset-level beneficiary allocation & succession modeling |
| 13 | Will | Estate | Will coverage analysis, executor management |
| 14 | Gift Rules | Estate | India gift tax rules engine & compliance checker |
| 15 | Gift Transfer | Estate | Gift execution tracker (deed → registration → mutation) |
| 16 | Connections | Network | Data-sharing connections with consent management |
| 17 | Peers | Network | Consensual peer financial sharing (not a leaderboard) |
| 18 | Advisors | Marketplace | Advisor directory with verified credentials & matching |
| 19 | Marketplace | Marketplace | Asset listings overview |
| 20 | Marketplace Browse | Marketplace | Filtered listing search & discovery |
| 21 | Marketplace Land | Marketplace | Land/real estate specific marketplace view |
| 22 | Ask | Marketplace | Advisor query module grounded in user's ledger |
| 23 | Trends & News | Marketplace | Holdings-filtered market intelligence feed |
| 24 | Settings | Platform | Identity, privacy, notifications, export, security |
| 25 | Profiling | Planning | Onboarding flow for investor profiling |

> **Note:** `Schema.dc.html`, `User Flow.dc.html`, `User Story.dc.html`, `Platform Map.dc.html`, and `Platform.dc.html` are **architectural reference documents**, not end-user screens.

---

## 7. Technical Architecture Summary

```
┌─────────────────────────────────────────────────┐
│               PRESENTATION LAYER                │
│  Desktop Web App (V1)  │  Mobile App (V2)        │
└───────────────────┬─────────────────────────────┘
                    │ HTTPS / REST or GraphQL
┌───────────────────▼─────────────────────────────┐
│                 API GATEWAY                      │
│  Auth verification · Rate limiting · Routing     │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│          APPLICATION LOGIC LAYER                 │
│                                                  │
│  Identity & Access   │  Ledger & Wealth          │
│  Estate & Legal      │  Advisory Marketplace     │
│                                                  │
│  ┌─────────────────────────────────────────────┐ │
│  │         CALCULATION ENGINE LAYER            │ │
│  │  Wealth & Ownership   │  Performance & Attr  │ │
│  │  Cash Flow & Debt     │  Planning & Scenarios │ │
│  │  Valuation & Verif.   │  Estate & Transfer    │ │
│  │  Consent & Marketplace│  Exposure & Conc.     │ │
│  └─────────────────────────────────────────────┘ │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│              STORAGE LAYER                       │
│  PostgreSQL (RDBMS) │  Object Storage (Docs)     │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│         EXTERNAL SYSTEMS (V2)                    │
│  Account Aggregators  │  CDSL/NSDL Feeds         │
│  Market Data APIs     │  Credit Bureaus (CIBIL)  │
└─────────────────────────────────────────────────┘
```

**Key architectural decisions:**
- **RDBMS (PostgreSQL)**: ACID compliance for the transaction ledger; referential integrity for asset-liability-inheritance links.
- **Event-driven background processing**: asset updates fire events; calculation engines run asynchronously to keep the UI responsive.
- **Design patterns in use**: Strategy (calculation engines), Protection Proxy (consent gating), Observer (snapshot generation), Facade (dashboard aggregation).
- **Immutable records**: `Transaction` and `FinancialSnapshot` are append-only ledgers.

---

## 8. Data Model Highlights

| Entity | Key Insight |
|---|---|
| `User` | Dual-role: same person can be Investor AND Advisor |
| `Asset` (abstract) | Three subclasses: `LiquidAsset`, `RealEstateAsset`, `AlternativeAsset` |
| `Portfolio` | One per user; contains assets, liabilities, transactions, snapshots |
| `FinancialSnapshot` | Immutable daily/periodic freeze of net worth — the basis for all trend charts |
| `Transaction` | Every cash flow event, dated and categorized — the basis for XIRR/TWRR |
| `Connection` | Relationship + consent: `permissions` JSON + `consent_expires_at` timestamp |
| `InheritanceAllocation` | Asset × Beneficiary × percentage — validated not to exceed 100% |
| `GiftRule` | Versioned Indian tax law rules — jurisdiction + effective date + threshold |

---

## 9. What We Are Deliberately NOT Building in V1

| Out of Scope (V1) | Reason |
|---|---|
| External account aggregation / AA API | Architecture is ready; not activated until V2 |
| Live market price feeds | Valuations are manual in V1 |
| Tax filing integration | Complex regulatory scope; planned for V2+ |
| Trading / order execution | This is a tracking platform, not a brokerage |
| Mobile app UI | Desktop-first; mobile app uses same APIs in V2 |
| AI / ML financial advice engine | "Ask" module in V1 is human-advisor-mediated |
| HUF / Corporate entity portfolios | V1 is individual + household only |

---

## 10. Open Questions & Decisions Needed

The following items require stakeholder input before detailed implementation begins:

1. **Technology Stack**: Which backend framework (Python/Django, Node.js, Go)? Which frontend framework (React, Vue, Next.js)? Which mobile target in V2 (Flutter, React Native, native)?
2. **Authentication Provider**: Which Auth-Core system? (Auth0, Supabase Auth, Firebase Auth, custom TOTP?)
3. **Hosting & Infrastructure**: Self-hosted or managed cloud (AWS, GCP, Azure)?
4. **Data Residency**: Given the sensitive financial nature, is India-only data residency required from day one?
5. **Monetization Model**: Subscription tiers, marketplace transaction fees, or freemium? This affects what features are gated.
6. **Advisor Verification Process**: How are credentials verified in V1 — manual admin process or API to SEBI/ICAI registries?
7. **Credit Bureau Integration (Credit Module)**: Is CIBIL/CRIF integration planned for V1 or V2?
8. **Mobile Wireframes**: When will mobile wireframes be ready, so API design can account for mobile-specific interaction patterns?

---

*Last updated: September 2026 — Initial version based on wireframe analysis and class architecture review.*
