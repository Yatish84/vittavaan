# Phase 1 — Actors & System Boundary

> **OOSE Phase:** Requirements Elicitation
> **Purpose:** Formally defines every entity that interacts with Vittavaan and draws the precise boundary of what the system is responsible for.
> **Status:** Draft

---

## 1. System Context Statement

Vittavaan is a **wealth management and financial networking platform** that allows individuals and households to manually record, track, analyse, and plan their financial lives. It provides structured tools for portfolio management, estate planning, peer networking with privacy controls, and access to verified financial professionals.

**Version 1 Scope:** All data is manually entered by users. No real-time feeds or external account connections exist in V1. The system boundary excludes any data that is not explicitly provided by the user or the platform.

---

## 2. System Boundary Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           VITTAVAAN SYSTEM                                 │
│                                                                            │
│  ┌─────────────────┐   ┌─────────────────┐   ┌──────────────────────────┐ │
│  │  Identity &     │   │  Wealth &       │   │  Estate & Legal          │ │
│  │  Networking     │   │  Portfolio      │   │  Planning                │ │
│  └─────────────────┘   └─────────────────┘   └──────────────────────────┘ │
│                                                                            │
│  ┌─────────────────┐   ┌─────────────────┐   ┌──────────────────────────┐ │
│  │  Financial      │   │  Advisory       │   │  Calculation &           │ │
│  │  Planning       │   │  Marketplace    │   │  Analysis Engines        │ │
│  └─────────────────┘   └─────────────────┘   └──────────────────────────┘ │
│                                                                            │
└───────▲────────────────────▲───────────────────────────▲───────────────────┘
        │                    │                           │
        │ Auth Tokens         │ API Requests              │ Future: Market Data
        │                    │                           │
┌───────┴──────┐   ┌─────────┴──────────┐   ┌───────────┴─────────────────┐
│  External    │   │  Investors &       │   │  External Financial APIs    │
│  Auth        │   │  Advisors          │   │  (V2 only — AA, CDSL, etc.) │
│  Provider    │   │  (Human Users)     │   │                             │
└──────────────┘   └────────────────────┘   └─────────────────────────────┘
```

---

## 3. Actor Definitions

### Primary Actors
Actors who directly initiate use cases with the system.

---

#### 3.1 Investor
**Description:** The primary user of the platform. An Investor is an individual who uses Vittavaan to track and manage their personal and household financial portfolio.

**Characteristics:**
- Has a personal `Portfolio` containing assets, liabilities, and transactions
- May have household members (family) registered under their account
- Has an `InvestorProfile` capturing financial demographics and risk tolerance
- May connect with peers and advisors on the platform
- May also be an `Advisor` simultaneously (dual role)

**V1 Capabilities:**
- Manually enter and manage all assets (liquid, real estate, alternative)
- Record liabilities and cash flow transactions
- Define financial goals and track progress
- Register household members and manage estate planning
- Log gift transfers to family members
- Connect with other users (peers and advisors)
- Grant field-level, time-bound data access to connected advisors
- View dashboard metrics (net worth, analysis, attribution)
- Submit advisory queries to advisors on the platform
- Generate and share a financial resume

**Technical Identity:** A `User` record with `is_investor = true` and an associated `InvestorProfile`.

---

#### 3.2 Advisor
**Description:** A financial professional who provides services to Investors through the platform. May offer portfolio analysis, estate planning, tax advisory, or credit facilitation services.

**Characteristics:**
- Has verified professional credentials (CA, SEBI RIA, IBBI Valuer, Advocate, CFA)
- Has a public-facing `AdvisorProfile` on the marketplace
- May also be an Investor themselves (most common real-world scenario)
- Credentials are verified by the System Administrator before the advisor profile is visible

**V1 Capabilities:**
- Maintain a public advisor profile with specialties and credentials
- Respond to advisory queries from connected Investors
- Publish market insights and articles visible to the platform community
- Access Investor data only within explicitly granted, time-bound consent scopes
- List professional services on the marketplace

**Technical Identity:** A `User` record with `is_advisor = true` and an associated `AdvisorProfile`.

---

#### 3.3 Household Member / Beneficiary
**Description:** A family member or dependent registered by an Investor. Not an independent platform user in V1 — they are data entities managed by the Investor.

**Characteristics:**
- Does not have an independent login account in V1
- Represents dependents (children, parents) or co-owners (spouse, siblings)
- May be designated as a beneficiary for inheritance allocations or gift recipients
- In V2, a Household Member may optionally be invited to create their own Investor account and link to the household

**V1 Role:** Passive data entity; appears in household aggregation, inheritance allocation, and gift transfer records.

**Technical Identity:** A `HouseholdMember` record linked to an `Investor`'s `User` record.

---

### Supporting Actors
Actors who are involved in use cases but do not initiate them directly.

---

#### 3.4 System Administrator
**Description:** An internal Vittavaan platform operator with elevated access for platform management.

**Responsibilities:**
- Verify advisor credentials against authoritative registers (ICAI, SEBI, IBBI)
- Manage platform-level settings (gift rule updates, jurisdiction rules)
- Monitor system health and audit logs
- Handle account closure and data export requests
- Manage marketplace listing approvals

**Access:** Direct database access + admin-only API endpoints. Never accesses end-user financial data for commercial purposes.

**Technical Identity:** A `User` record with `is_admin = true` and a separate admin API role.

---

#### 3.5 External Authentication Provider (Auth-Core)
**Description:** The external identity and authentication service that manages user registration, password handling, and token issuance. Vittavaan delegates all authentication to this provider.

**V1 Choice:** Supabase Auth

**Responsibilities:**
- Manage user registration (email + password, or phone OTP)
- Issue cryptographically signed JWT tokens upon successful login
- Handle password resets and 2FA (TOTP or SMS OTP)
- Maintain session revocation lists

**What Vittavaan does NOT own:**
- Passwords (never stored in Vittavaan's database)
- The authentication flow (login page is Supabase-hosted or Supabase SDK)

**What Vittavaan owns:**
- All financial data and domain records
- The mapping from Supabase's `auth.users.id` to Vittavaan's `User.user_id`

---

#### 3.6 External Financial API Provider *(V2 Actor — defined now for architectural readiness)*
**Description:** External services that will eventually provide real-time or near-real-time financial data feeds.

**Examples:**
- **Account Aggregators (AA)**: RBI-licensed AAs (Setu, Onemoney, Finvu) that pull bank account, FD, and loan data via the AA framework.
- **CDSL/NSDL**: Depository feeds for equity and mutual fund holdings.
- **Market Data Providers**: NSE/BSE data feeds for live equity prices.
- **Credit Bureaus**: CIBIL and CRIF for credit scores (already referenced in Credit module).

**V1 Status:** This actor exists in the architecture as a defined integration point (the Adapter pattern) but is not active. All V1 equivalents are replaced by manual user input forms.

**Architectural impact on V1:** The `LiquidAsset` model has a `fetch_live_price()` method stub. The `FinancialSnapshot` capture is event-driven (not a manual button). These are designed to work both with manual inputs and future API feeds.

---

## 4. Actor-Use Case Matrix

The following matrix shows which actor initiates or participates in each high-level use case group.

| Use Case Group | Investor | Advisor | HH Member | Admin | Auth Provider |
|---|:---:|:---:|:---:|:---:|:---:|
| Register & Authenticate | ✅ | ✅ | — | — | ✅ |
| Manage Investor Profile | ✅ | — | — | — | — |
| Manage Advisor Profile | — | ✅ | — | ✅ (verify) | — |
| Manage Portfolio (Assets) | ✅ | — | — | — | — |
| Manage Portfolio (Liabilities) | ✅ | — | — | — | — |
| Log Transactions (Cash Flow) | ✅ | — | — | — | — |
| View Dashboard & Analytics | ✅ | — | — | — | — |
| Manage Financial Goals | ✅ | — | — | — | — |
| Register Household Members | ✅ | — | — | — | — |
| Manage Estate Plan & Will | ✅ | — | — | — | — |
| Allocate Inheritance | ✅ | — | — | — | — |
| Log Gift Transfer | ✅ | — | — | — | — |
| Manage Connections | ✅ | ✅ | — | — | — |
| Grant/Revoke Data Consent | ✅ | — | — | — | — |
| Submit Advisory Query | ✅ | — | — | — | — |
| Answer Advisory Query | — | ✅ | — | — | — |
| Publish Market Insight | — | ✅ | — | — | — |
| Browse Advisor Marketplace | ✅ | — | — | — | — |
| Browse Asset Marketplace | ✅ | — | — | — | — |
| List Asset on Marketplace | ✅ | — | — | — | — |
| Generate Financial Resume | ✅ | — | — | — | — |
| Manage Platform Settings | ✅ | ✅ | — | ✅ | — |
| Apply for Credit (V1 basic) | ✅ | — | — | — | — |
| View Peer Benchmarks | ✅ | — | — | — | — |

---

## 5. What Is INSIDE the System Boundary (V1)

The following are Vittavaan's V1 responsibilities:

1. **User identity and session management** — using JWT tokens from the external auth provider
2. **Portfolio data storage and management** — assets, liabilities, transactions (manual input)
3. **Financial calculation and analysis** — all derived metrics (net worth, XIRR, TWRR, etc.)
4. **Estate planning** — household members, wills, inheritance allocations, gift tracking
5. **Privacy-controlled social networking** — connections, consent management
6. **Advisory marketplace** — advisor profiles, queries, market insights
7. **Asset marketplace** — listing, browsing, basic transaction facilitation
8. **Document storage (Data Room)** — secure upload and retrieval of financial documents
9. **Notifications** — in-platform alerts (stale data, expiring consents, upcoming events)
10. **Settings and preferences** — currency, notifications, privacy, export

---

## 6. What Is OUTSIDE the System Boundary (V1)

The following are explicitly NOT Vittavaan's responsibility in V1:

| Excluded Capability | Planned Phase |
|---|---|
| Real-time bank account balance reading (AA APIs) | V2 |
| Live equity/MF portfolio sync (CDSL/NSDL) | V2 |
| Live market price feeds (NSE/BSE) | V2 |
| Tax filing or ITR generation | V2+ |
| Actual trade execution (buy/sell orders) | Out of scope — Vittavaan is a tracker, not a broker |
| Insurance policy management | V2+ |
| EMI payment collection | Out of scope |
| Actual legal will drafting/notarisation | Vittavaan stores documents; it does not draft or notarise |
| KYC/AML compliance (beyond basic platform KYC) | Platform handles basic identity; does not perform RBI-mandated FI KYC |
| Corporate/HUF portfolio management | V2+ (V1 is individual + household only) |
| Credit underwriting / loan disbursement | Vittavaan facilitates lender matching; lending is performed by empanelled institutions |

---

## 7. Key Boundary Conditions

These are scenarios where the system boundary creates explicit design constraints:

### 7.1 Authentication Token Validity
- If the Supabase Auth service is unreachable, Vittavaan must fail gracefully (error page, not crash).
- If a JWT has expired, the API returns `401 Unauthorized` and the frontend prompts re-authentication. Vittavaan never attempts to refresh tokens on behalf of the user without the user's action.

### 7.2 Advisor Credential Verification
- Vittavaan does not directly connect to SEBI or ICAI APIs in V1. Credential verification is a manual admin process.
- An `AdvisorProfile` with unverified credentials is visible in search but marked with an explicit `UNVERIFIED` badge. The system enforces that unverified advisors cannot receive data consent grants.

### 7.3 Data Export
- Vittavaan must provide a structured data export (JSON or CSV) of all user data on request (Settings page). This is the user's right under privacy principles and the anticipated DPDP Act requirements.
- Export covers all financial data. It does NOT include documents stored in Supabase Storage (user must download those separately).

### 7.4 Account Closure
- When a user closes their account, Vittavaan retains transaction records for a legally required period (7 years, per Indian income tax record-keeping obligations), then purges all personal data. The retention policy must be disclosed at registration.

---

*Next document: [02_Functional_Requirements.md](./02_Functional_Requirements.md)*
