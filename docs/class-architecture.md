# Vittavaan: System Architecture & Domain Model

## Project Overview
Vittavaan is a comprehensive wealth management and networking application designed to help users track net worth, manage specialized assets (like real estate and alternative collections), and structure estate planning. Beyond individual portfolio management, it serves as a collaborative networking zone where investors and professional advisors can connect, compare benchmarks, and share relevant financial intelligence. 

All monetary values are strictly stored as integers (minor units, e.g., paise/cents) to prevent floating-point calculation errors.

## Document Purpose & Module Summary
This document serves as the foundational Object-Oriented architectural blueprint for the application. The architecture is divided into the following core modules:
*   **Module 1 & 1.5:** Dual-role user identities, demographic profiles, peer connections with time-bound consents, universal document storage, and the zero-trust authentication gateway.
*   **Module 2:** The financial engine aggregating portfolios, tracking assets, managing transactional cash flows, and mapping financial goals.
*   **Module 3:** Structures family wealth transfer, legal documentation, and inter-vivos gifting compliance.
*   **Module 4:** Facilitates networking, market data, peer-comparison reports, and advisor queries.
*   **Module 5:** The Application Service Layer, grouped into functional calculation engines to aggregate database queries and compute complex dashboard metrics.

---

## Table of Contents
1. [Entity-Relationship (ER) Diagram](#entity-relationship-er-diagram)
2. [Module 1: User, Profile & Data Room Classes](#module-1-user-profile--data-room-classes)
3. [Module 1.5: Security & Session (Auth-Core Gateway)](#module-15-security--session-auth-core-gateway)
4. [Module 2: Wealth, Portfolio & Planning Classes](#module-2-wealth-portfolio--planning-classes)
5. [Module 3: Estate & Legal Planning Classes](#module-3-estate--legal-planning-classes)
6. [Module 4: Advisory & Market Intelligence Classes](#module-4-advisory--market-intelligence-classes)
7. [Module 5: Application Service Layer (Calculation Engines)](#module-5-application-service-layer-calculation-engines)

---

## Entity-Relationship (ER) Diagram

The following Mermaid diagram visualizes the relational database connections between the core persistent domain classes. *(Note: Stateless boundaries, calculation engines, and generic lookup tables like `GiftRule` are excluded to maintain structural clarity).*

```mermaid
erDiagram
    USER ||--o| INVESTOR_PROFILE : "has"
    USER ||--o| ADVISOR_PROFILE : "has"
    USER ||--o{ CONNECTION : "initiates / receives"
    USER ||--|| SETTING : "has"
    USER ||--o{ DOCUMENT : "owns"
    USER ||--o{ LOCAL_SESSION : "authenticates"
    USER ||--|| PORTFOLIO : "owns"
    USER ||--o{ HOUSEHOLD_MEMBER : "registers"
    USER ||--o| ESTATE_PLAN : "creates"
    USER ||--o{ FINANCIAL_GOAL : "sets"
    USER ||--o{ ADVISORY_QUERY : "asks / answers"
    USER ||--o{ GIFT_TRANSFER : "sends"
    USER ||--o{ MARKET_INSIGHT : "publishes"

    PORTFOLIO ||--o{ ASSET : "contains"
    PORTFOLIO ||--o{ LIABILITY : "contains"
    PORTFOLIO ||--o{ TRANSACTION : "logs"
    PORTFOLIO ||--o{ FINANCIAL_SNAPSHOT : "snapshots"

    ASSET ||--o{ TRANSACTION : "subject_of"
    ASSET ||--o{ DOCUMENT : "provenance_link"
    ASSET ||--o{ INHERITANCE_ALLOCATION : "allocated_in"

    ESTATE_PLAN ||--o| WILL : "contains"
    ESTATE_PLAN ||--o{ INHERITANCE_ALLOCATION : "specifies"

    WILL ||--o| DOCUMENT : "backed_by"

    HOUSEHOLD_MEMBER ||--o{ INHERITANCE_ALLOCATION : "receives"
    HOUSEHOLD_MEMBER ||--o{ GIFT_TRANSFER : "receives"

    FINANCIAL_GOAL ||--o{ ASSET : "funded_by"


## Module 1: User, Profile & Data Room Classes

### 1. `User`
The core identity class handling basic account management and immutable human demographics. Acts as the root for dual-role users (investors who are also advisors).
*   **Attributes:**
    *   `user_id` (String/UUID) - Primary Key
    *   `email` (String) - Unique identifier
    *   `first_name` (String)
    *   `last_name` (String)
    *   `date_of_birth` (Date) - Used to dynamically calculate age for cohorts/credit
    *   `gender` (Enum) - e.g., `MALE`, `FEMALE`, `NON_BINARY`, `PREFER_NOT_TO_SAY`
    *   `is_investor` (Boolean) - True if the user has an attached `InvestorProfile` and personal ledger
    *   `is_advisor` (Boolean) - True if the user has an attached `AdvisorProfile` for the marketplace
    *   `created_at` (DateTime)
    *   `last_login` (DateTime)
*   **Functions:**
    *   `get_user_details()`: Fetches the consolidated identity payload.
    *   `switch_active_context(target_role)`: Toggles the UI state between personal wealth and professional advisory views.
    *   `search_network(search_criteria)`: Queries the database for peers or advisors.
    *   `send_connection_request(recipient_id)`: Creates the initial `Connection` object.
    *   `get_network_connections(status_filter=None)`: Fetches a list of linked `Connection` objects.

### 2. `InvestorProfile`
The financial persona linked to a user. Separates self-declared financial demographics from core identity.
*   **Attributes:**
    *   `profile_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to `User`
    *   `education_level` (Enum) - e.g., `BACHELORS`, `MASTERS`, `DOCTORATE`, `PROFESSIONAL`
    *   `city_tier` (Enum) - e.g., `TIER_1`, `TIER_2`, `TIER_3`
    *   `stated_annual_income_minor_units` (Integer) - Self-declared demographic income
    *   `risk_tolerance` (Enum) - `CONSERVATIVE`, `MODERATE`, `AGGRESSIVE`
    *   `investment_horizon_years` (Integer)
    *   `financial_resume_summary` (Text) 
*   **Functions:**
    *   `update_risk_profile(new_tolerance)`: Adjusts the user's risk settings.
    *   `get_resume_data()`: Packages the profile info for the frontend UI.

### 3. `AdvisorProfile`
Manages professional credentials for the network, using strict finite lists to ensure regulatory integrity.
*   **Attributes:**
    *   `profile_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to `User`
    *   `firm_name` (String)
    *   `certifications` (List of Enums) - Strict subset of recognized credentials (e.g., `CFP`, `SEBI_RIA`, `CA`, `IBBI_VALUER`, `ADVOCATE`, `CFA`).
    *   `specialty_areas` (List of Strings) - e.g., Estate Planning, Equities, Crypto Taxation
*   **Functions:**
    *   `add_certification(cert_name)`
    *   `get_public_profile()`

### 4. `Connection`
Manages the relationship, state, and strict time-bound permissions between users.
*   **Attributes:**
    *   `connection_id` (String/UUID) - Primary Key
    *   `requester_id` (Foreign Key) 
    *   `recipient_id` (Foreign Key) 
    *   `status` (Enum) - `PENDING`, `ACCEPTED`, `REJECTED`, `REVOKED`
    *   `permissions` (Dictionary/JSON) - Field-level access control list
    *   `consent_scope` (String) - Data/actions the source is allowed to provide/view
    *   `consent_purpose` (String) - Recorded purpose for the data share
    *   `consent_granted_at` (DateTime) - Consent start
    *   `consent_expires_at` (DateTime) - Consent expiry enforcing time-bound rules
    *   `created_at` (DateTime)
    *   `updated_at` (DateTime)
*   **Functions:**
    *   `accept_connection()`
    *   `reject_connection()`
    *   `update_permissions(new_permissions_dict)`
    *   `terminate_connection()`
    *   `get_connection_details()`

### 5. `Setting`
*   **Attributes:**
    *   `setting_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) 
    *   `two_factor_enabled` (Boolean)
    *   `base_currency` (String) 
    *   `email_notifications` (Boolean)
*   **Functions:**
    *   `get_user_settings()`
    *   `toggle_2fa(status)`
    *   `update_base_currency(new_currency)`

### 6. `Document` (Data Room)
Universal document storage supporting verification, estate planning, and consents.
*   **Attributes:**
    *   `document_id` (String/UUID) - Primary Key
    *   `owner_id` (Foreign Key) - Links to `User`
    *   `linked_asset_id` (Foreign Key, Optional) - Links to `Asset` if applicable
    *   `document_type` (Enum) - e.g., `WILL`, `VALUATION_REPORT`, `CONSENT_FORM`, `TITLE_DEED`
    *   `storage_url` (String) - Secure cloud reference
    *   `document_date` (Date)
    *   `document_expiry` (Date, Optional)
*   **Functions:**
    *   `upload_document()`
    *   `verify_document()`

---

## Module 1.5: Security & Session (Auth-Core Gateway)

### 1. `AuthGateway` (Boundary/Control Class)
*   **Attributes:**
    *   `public_key` (String) 
    *   `issuer_url` (String) 
*   **Functions:**
    *   `verify_handshake(token)`
    *   `extract_user_identity(token)`

### 2. `LocalSession`
*   **Attributes:**
    *   `session_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key)
    *   `access_token` (String) 
    *   `expires_at` (DateTime)
    *   `is_active` (Boolean)
*   **Functions:**
    *   `create_session(user_id, token)`
    *   `validate_session()`
    *   `terminate_session()`

---

## Module 2: Wealth, Portfolio & Planning Classes

### 1. `Portfolio`
*   **Attributes:**
    *   `portfolio_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) 
    *   `created_at` (DateTime)
    *   `last_updated` (DateTime)
*   **Functions:**
    *   `add_asset(asset_data)`
    *   `remove_asset(asset_id)`
    *   `add_liability(liability_data)`
    *   `get_net_worth_history(timeframe)`

### 2. `Asset` (Abstract Base Class)
Foundational blueprint incorporating fractional ownership and strict data provenance.
*   **Attributes:**
    *   `asset_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key)
    *   `name` (String) 
    *   `asset_category` (Enum) - `LIQUID`, `REAL_ESTATE`, `ALTERNATIVE`
    *   `ownership_split_pct` (Float) - Legal/economic ownership share enabling proper household deduplication
    *   `purchase_price_minor_units` (Integer) - Initial cost basis stored in minor units
    *   `current_value_minor_units` (Integer) - Latest valuation stored in minor units
    *   `purchase_date` (Date)
    *   `currency` (String) 
    *   `verification_level` (Enum) - `SELF_DECLARED`, `DOCUMENTED`, `VERIFIED`, `ACCEPTED` tracking data actionability
    *   `valuation_method` (String) - e.g., "market feed", "appraisal", "manual estimate"
    *   `valuation_as_of` (DateTime) - Explicit timestamp of the valuation
    *   `notes` (Text)
*   **Functions:**
    *   `update_details(updated_data_dict)`
    *   `update_valuation(new_value_minor_units, method)`
    *   `calculate_attributed_value()`: Multiplies gross value by ownership split.

### 3. `LiquidAsset`, 4. `RealEstateAsset`, 5. `AlternativeAsset` 
*(Subclasses inheriting from Asset, storing specific attributes like `ticker_symbol`, `square_footage`, `collection_type`)*

### 6. `Liability`
*   **Attributes:**
    *   `liability_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key) 
    *   `name` (String) 
    *   `liability_type` (Enum) 
    *   `principal_amount_minor_units` (Integer) - Original loan size
    *   `current_balance_minor_units` (Integer) - Amount currently owed
    *   `interest_rate` (Float)
    *   `due_date` (Date)
*   **Functions:**
    *   `update_details(updated_data_dict)`
    *   `record_payment(amount_minor_units)`

### 7. `Transaction` (Cash Flow Ledger)
Records individual historical cash flows, required for generating time-weighted (TWRR) and money-weighted (XIRR) returns.
*   **Attributes:**
    *   `transaction_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key)
    *   `asset_id` (Foreign Key, Optional) - Links to specific asset if applicable
    *   `transaction_date` (DateTime)
    *   `amount_minor_units` (Integer)
    *   `transaction_type` (Enum) - e.g., `INFLOW`, `OUTFLOW`, `BUY`, `SELL`, `RENT`
    *   `category` (String) - e.g., "salary", "dividend", "repair"
*   **Functions:**
    *   `log_transaction()`
    *   `get_period_cashflows(start_date, end_date)`

### 8. `FinancialGoal` (Planning)
Maps user objectives against current portfolio funding.
*   **Attributes:**
    *   `goal_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key)
    *   `name` (String)
    *   `target_year` (Date) - Date goal requires funds
    *   `target_amount_minor_units` (Integer) - Expected need at target date
    *   `linked_asset_ids` (List of Strings) - Holdings assigned to fund this goal
*   **Functions:**
    *   `calculate_funding_gap()`: Computes difference between projected value and needed value.

### 9. `FinancialSnapshot` (Time-Series Ledger)
Immutable historical ledger using explicit integer columns.
*   **Attributes:**
    *   `snapshot_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key) 
    *   `snapshot_date` (Date) 
    *   `total_assets_value_minor_units` (Integer)
    *   `total_liabilities_value_minor_units` (Integer)
    *   `net_worth_value_minor_units` (Integer)
    *   `liquid_assets_value_minor_units` (Integer)
    *   `real_estate_value_minor_units` (Integer)
    *   `alternative_assets_value_minor_units` (Integer)
*   **Functions:**
    *   `capture_periodic_metrics()`
    *   `fetch_historical_trend(start_date, end_date)`

---

## Module 3: Estate & Legal Planning Classes

### 1. `HouseholdMember`
*   **Attributes:**
    *   `member_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) 
    *   `first_name` (String)
    *   `last_name` (String)
    *   `relationship` (Enum) 
    *   `date_of_birth` (Date)
    *   `contact_email` (String, Optional)

### 2. `EstatePlan`
*   **Attributes:**
    *   `plan_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) 
    *   `primary_executor_name` (String)
    *   `primary_executor_contact` (String)
    *   `secondary_executor_name` (String, Optional)
    *   `last_reviewed_date` (Date)

### 3. `Will`
*   **Attributes:**
    *   `will_id` (String/UUID) - Primary Key
    *   `plan_id` (Foreign Key) 
    *   `document_id` (Foreign Key) - Links to `Document` storage
    *   `signature_date` (Date)
    *   `status` (Enum) - `DRAFT`, `EXECUTED`, `REVOKED`

### 4. `InheritanceAllocation`
*   **Attributes:**
    *   `allocation_id` (String/UUID) - Primary Key
    *   `plan_id` (Foreign Key) 
    *   `asset_id` (Foreign Key) 
    *   `beneficiary_id` (Foreign Key) 
    *   `percentage_share` (Float) 
    *   `distribution_conditions` (Text) 
*   **Functions:**
    *   `validate_total_allocation(asset_id)`

### 5. `GiftRule`
*   **Attributes:**
    *   `rule_id` (String/UUID) - Primary Key
    *   `jurisdiction` (String) 
    *   `rule_effective_date` (Date) - Version control for tax/legal rules
    *   `annual_exemption_limit_minor_units` (Integer)

### 6. `GiftTransfer`
*   **Attributes:**
    *   `transfer_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) 
    *   `recipient_id` (Foreign Key) 
    *   `asset_id` (Foreign Key, Optional) 
    *   `cash_value_minor_units` (Integer)
    *   `transfer_date` (Date)
    *   `tax_filed_status` (Boolean)

---

## Module 4: Advisory & Market Intelligence Classes

### 1. `AdvisoryQuery` (The "Ask" Module)
*   **Attributes:**
    *   `query_id` (String/UUID) - Primary Key
    *   `asker_id` (Foreign Key)
    *   `advisor_id` (Foreign Key, Optional)
    *   `subject` (String)
    *   `content_body` (Text)
    *   `status` (Enum)
    *   `created_at` (DateTime)
    *   `updated_at` (DateTime)
*   **Functions:**
    *   `submit_query()`
    *   `get_open_queries(advisor_id=None)`
    *   `add_response(advisor_id, response_text)`
    *   `resolve_query()`

### 2. `MarketInsight` (Trends & News)
*   **Attributes:**
    *   `insight_id` (String/UUID) - Primary Key
    *   `author_id` (Foreign Key)
    *   `title` (String)
    *   `content` (Text)
    *   `category` (Enum)
    *   `tags` (List of Strings)
    *   `published_date` (DateTime)
*   **Functions:**
    *   `publish_insight()`
    *   `fetch_feed(user_preferences)`

### 3. `PeerBenchmark` (Peers)
*   **Attributes:**
    *   `benchmark_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key)
    *   `cohort_criteria` (Dictionary)
    *   `user_metric_value` (Float)
    *   `cohort_average` (Float)
    *   `percentile_rank` (Integer)
    *   `generated_at` (DateTime)
*   **Functions:**
    *   `generate_cohort_comparison(metric_type)`
    *   `get_historical_benchmarks()`

---

## Module 5: Application Service Layer (Calculation Engines)

This module represents stateless backend service classes mapping to the recommended engineering taxonomy. They orchestrate SQL queries and Python math, strictly outputting JSON payloads with robust provenance (e.g., `value_minor_units`, `as_of`, `calculation_version`).

### 1. `WealthAndOwnershipEngine`
*   **Functions:** Aggregates assets, liabilities, and net worth, rigorously applying `ownership_split_pct` before household aggregation to prevent double-counting.

### 2. `ValuationAndVerificationEngine`
*   **Functions:** Evaluates `verification_level` across the portfolio, calculating `VerifiedWealthPct` and monitoring `ValuationAgeDays` to flag stale data states.

### 3. `CashFlowAndDebtEngine`
*   **Functions:** Queries `Transaction` and `Liability` tables to compute `MonthlySurplus`, amortization schedules, and the `DebtServiceRatio`.

### 4. `PerformanceAndAttributionEngine`
*   **Functions:** Calculates money-weighted returns (`PortfolioXIRR`), time-weighted returns (`PortfolioTWRR`), and asset class contributions over defined time windows using historical transactions.

### 5. `PlanningAndScenarioEngine`
*   **Functions:** Projects future values for `FinancialGoal` records, calculates timing mismatches, and models "invest vs. prepay" scenarios based on dynamic assumptions.

### 6. `ConsentAndMarketplaceEngine`
*   **Functions:** Evaluates `Document` and `Connection` grants to determine field-level access decisions, preventing exposure of withheld datapoints.