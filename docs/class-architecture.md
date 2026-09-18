# Vittavaan: System Architecture & Domain Model

## Project Overview
Vittavaan is a comprehensive wealth management and networking application designed to help users track net worth, manage specialized assets (like real estate and alternative collections), and structure estate planning. Beyond individual portfolio management, it serves as a collaborative networking zone where investors and professional advisors can connect, compare benchmarks, and share relevant financial intelligence. 

All monetary values are strictly stored as integers (minor units, e.g., paise/cents) to prevent floating-point calculation errors[cite: 1].

## Document Purpose & Module Summary
This document serves as the foundational Object-Oriented architectural blueprint for the application. The architecture is divided into the following core modules:
*   **Module 1 & 1.5:** Role-based user profiles, peer connections with time-bound consents[cite: 1], universal document storage[cite: 1], and the zero-trust authentication gateway.
*   **Module 2:** The financial engine aggregating portfolios, tracking assets, managing transactional cash flows[cite: 1], and mapping financial goals[cite: 1].
*   **Module 3:** Structures family wealth transfer, legal documentation, and inter-vivos gifting compliance.
*   **Module 4:** Facilitates networking, market data, peer-comparison reports, and advisor queries.
*   **Module 5:** The Application Service Layer, grouped into functional calculation engines to aggregate database queries and compute complex dashboard metrics[cite: 1].

---

## Table of Contents
1. [Module 1: User, Profile & Data Room Classes](#module-1-user-profile--data-room-classes)
2. [Module 1.5: Security & Session (Auth-Core Gateway)](#module-15-security--session-auth-core-gateway)
3. [Module 2: Wealth, Portfolio & Planning Classes](#module-2-wealth-portfolio--planning-classes)
4. [Module 3: Estate & Legal Planning Classes](#module-3-estate--legal-planning-classes)
5. [Module 4: Advisory & Market Intelligence Classes](#module-4-advisory--market-intelligence-classes)
6. [Module 5: Application Service Layer (Calculation Engines)](#module-5-application-service-layer-calculation-engines)

---

## Module 1: User, Profile & Data Room Classes

### 1. `User`
The core identity class handling role assignment and basic account management. 
*   **Attributes:**
    *   `user_id` (String/UUID) - Primary Key
    *   `email` (String) - Unique identifier
    *   `first_name` (String)
    *   `last_name` (String)
    *   `role` (Enum) - e.g., `INVESTOR`, `ADVISOR`
    *   `created_at` (DateTime)
    *   `last_login` (DateTime)
*   **Functions:**
    *   `get_user_details()`: Fetches the consolidated profile and settings payload.
    *   `get_role_dashboard()`: Routes the user to the appropriate UI based on their role.
    *   `search_network(search_criteria)`: Queries the database for peers or advisors.
    *   `send_connection_request(recipient_id)`: Creates the initial `Connection` object.
    *   `get_network_connections(status_filter=None)`: Fetches a list of linked `Connection` objects.

### 2. `InvestorProfile`
*   **Attributes:**
    *   `profile_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to `User`
    *   `risk_tolerance` (Enum) - `CONSERVATIVE`, `MODERATE`, `AGGRESSIVE`
    *   `investment_horizon_years` (Integer)
    *   `financial_resume_summary` (Text) 
*   **Functions:**
    *   `update_risk_profile(new_tolerance)`: Adjusts the user's risk settings.
    *   `get_resume_data()`: Packages the profile info for the frontend UI.

### 3. `AdvisorProfile`
*   **Attributes:**
    *   `profile_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to `User`
    *   `firm_name` (String)
    *   `certifications` (List of Strings) 
    *   `specialty_areas` (List of Strings) 
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
    *   `consent_scope` (String) - Data/actions the source is allowed to provide/view[cite: 1]
    *   `consent_purpose` (String) - Recorded purpose for the data share[cite: 1]
    *   `consent_granted_at` (DateTime) - Consent start[cite: 1]
    *   `consent_expires_at` (DateTime) - Consent expiry enforcing time-bound rules[cite: 1]
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
Universal document storage supporting verification, estate planning, and consents[cite: 1].
*   **Attributes:**
    *   `document_id` (String/UUID) - Primary Key
    *   `owner_id` (Foreign Key) - Links to `User`[cite: 1]
    *   `linked_asset_id` (Foreign Key, Optional) - Links to `Asset` if applicable[cite: 1]
    *   `document_type` (Enum) - e.g., `WILL`, `VALUATION_REPORT`, `CONSENT_FORM`, `TITLE_DEED`[cite: 1]
    *   `storage_url` (String) - Secure cloud reference
    *   `document_date` (Date)[cite: 1]
    *   `document_expiry` (Date, Optional)[cite: 1]
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
Foundational blueprint incorporating fractional ownership and strict data provenance[cite: 1].
*   **Attributes:**
    *   `asset_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key)
    *   `name` (String) 
    *   `asset_category` (Enum) - `LIQUID`, `REAL_ESTATE`, `ALTERNATIVE`
    *   `ownership_split_pct` (Float) - Legal/economic ownership share enabling proper household deduplication[cite: 1]
    *   `purchase_price_minor_units` (Integer) - Initial cost basis stored in minor units[cite: 1]
    *   `current_value_minor_units` (Integer) - Latest valuation stored in minor units[cite: 1]
    *   `purchase_date` (Date)
    *   `currency` (String) 
    *   `verification_level` (Enum) - `SELF_DECLARED`, `DOCUMENTED`, `VERIFIED`, `ACCEPTED` tracking data actionability[cite: 1]
    *   `valuation_method` (String) - e.g., "market feed", "appraisal", "manual estimate"[cite: 1]
    *   `valuation_as_of` (DateTime) - Explicit timestamp of the valuation[cite: 1]
    *   `notes` (Text)
*   **Functions:**
    *   `update_details(updated_data_dict)`
    *   `update_valuation(new_value_minor_units, method)`
    *   `calculate_attributed_value()`: Multiplies gross value by ownership split[cite: 1].

### 3. `LiquidAsset`, 4. `RealEstateAsset`, 5. `AlternativeAsset` 
*(Subclasses inheriting from Asset, storing specific attributes like `ticker_symbol`, `square_footage`, `collection_type`)*

### 6. `Liability`
*   **Attributes:**
    *   `liability_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key) 
    *   `name` (String) 
    *   `liability_type` (Enum) 
    *   `principal_amount_minor_units` (Integer) - Original loan size[cite: 1]
    *   `current_balance_minor_units` (Integer) - Amount currently owed[cite: 1]
    *   `interest_rate` (Float)
    *   `due_date` (Date)
*   **Functions:**
    *   `update_details(updated_data_dict)`
    *   `record_payment(amount_minor_units)`

### 7. `Transaction` (Cash Flow Ledger)
Records individual historical cash flows, required for generating time-weighted (TWRR) and money-weighted (XIRR) returns[cite: 1].
*   **Attributes:**
    *   `transaction_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key)
    *   `asset_id` (Foreign Key, Optional) - Links to specific asset if applicable
    *   `transaction_date` (DateTime)[cite: 1]
    *   `amount_minor_units` (Integer)[cite: 1]
    *   `transaction_type` (Enum) - e.g., `INFLOW`, `OUTFLOW`, `BUY`, `SELL`, `RENT`[cite: 1]
    *   `category` (String) - e.g., "salary", "dividend", "repair"[cite: 1]
*   **Functions:**
    *   `log_transaction()`
    *   `get_period_cashflows(start_date, end_date)`

### 8. `FinancialGoal` (Planning)
Maps user objectives against current portfolio funding[cite: 1].
*   **Attributes:**
    *   `goal_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key)
    *   `name` (String)
    *   `target_year` (Date) - Date goal requires funds[cite: 1]
    *   `target_amount_minor_units` (Integer) - Expected need at target date[cite: 1]
    *   `linked_asset_ids` (List of Strings) - Holdings assigned to fund this goal[cite: 1]
*   **Functions:**
    *   `calculate_funding_gap()`: Computes difference between projected value and needed value[cite: 1].

### 9. `FinancialSnapshot` (Time-Series Ledger)
Immutable historical ledger using explicit integer columns.
*   **Attributes:**
    *   `snapshot_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key) 
    *   `snapshot_date` (Date) 
    *   `total_assets_value_minor_units` (Integer)[cite: 1]
    *   `total_liabilities_value_minor_units` (Integer)[cite: 1]
    *   `net_worth_value_minor_units` (Integer)[cite: 1]
    *   `liquid_assets_value_minor_units` (Integer)[cite: 1]
    *   `real_estate_value_minor_units` (Integer)[cite: 1]
    *   `alternative_assets_value_minor_units` (Integer)[cite: 1]
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
    *   `document_id` (Foreign Key) - Links to `Document` storage[cite: 1]
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
    *   `rule_effective_date` (Date) - Version control for tax/legal rules[cite: 1]
    *   `annual_exemption_limit_minor_units` (Integer)[cite: 1]

### 6. `GiftTransfer`
*   **Attributes:**
    *   `transfer_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) 
    *   `recipient_id` (Foreign Key) 
    *   `asset_id` (Foreign Key, Optional) 
    *   `cash_value_minor_units` (Integer)[cite: 1]
    *   `transfer_date` (Date)
    *   `tax_filed_status` (Boolean)

---

## Module 4: Advisory & Market Intelligence Classes

*(Contains `AdvisoryQuery`, `MarketInsight`, and `PeerBenchmark` mapping community network features, threads, and peer comparison parameters.)*

---

## Module 5: Application Service Layer (Calculation Engines)

This module represents stateless backend service classes mapping to the recommended engineering taxonomy[cite: 1]. They orchestrate SQL queries and Python math, strictly outputting JSON payloads with robust provenance (e.g., `value_minor_units`, `as_of`, `calculation_version`)[cite: 1].

### 1. `WealthAndOwnershipEngine`
*   **Functions:** Aggregates assets, liabilities, and net worth, rigorously applying `ownership_split_pct` before household aggregation to prevent double-counting[cite: 1].

### 2. `ValuationAndVerificationEngine`
*   **Functions:** Evaluates `verification_level` across the portfolio, calculating `VerifiedWealthPct` and monitoring `ValuationAgeDays` to flag stale data states[cite: 1].

### 3. `CashFlowAndDebtEngine`
*   **Functions:** Queries `Transaction` and `Liability` tables to compute `MonthlySurplus`, amortization schedules, and the `DebtServiceRatio`[cite: 1].

### 4. `PerformanceAndAttributionEngine`
*   **Functions:** Calculates money-weighted returns (`PortfolioXIRR`), time-weighted returns (`PortfolioTWRR`), and asset class contributions over defined time windows using historical transactions[cite: 1].

### 5. `PlanningAndScenarioEngine`
*   **Functions:** Projects future values for `FinancialGoal` records, calculates timing mismatches, and models "invest vs. prepay" scenarios based on dynamic assumptions[cite: 1].

### 6. `ConsentAndMarketplaceEngine`
*   **Functions:** Evaluates `Document` and `Connection` grants to determine field-level access decisions, preventing exposure of withheld datapoints[cite: 1].