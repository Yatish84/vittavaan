# vittavaan-class-architecture.md

## Project Overview
Vittavaan is a comprehensive wealth management and networking application designed to help users track net worth, manage specialized assets (like real estate and alternative collections), and structure estate planning. Beyond individual portfolio management, it serves as a collaborative networking zone where investors and professional advisors can connect, compare benchmarks, and share relevant financial intelligence.

## Document Purpose & Module Summary
This document serves as the foundational Object-Oriented architectural blueprint for the application. By defining the core domain classes, subclasses, attributes, and functions, it bridges the gap between conceptual prototype features and the physical data architecture. This structured approach establishes the database tables and API boundaries required for backend implementation. 

The architecture is divided into the following core modules:
*   **Module 1 & 1.5:** Handles role-based user profiles, peer connections, global settings, and the zero-trust authentication gateway relying on Entity-Boundary-Control principles.
*   **Module 2:** The financial engine aggregating portfolios, tracking liquid, real estate, and alternative assets, and calculating net worth.
*   **Module 3:** Structures the complex logic surrounding family wealth transfer, legal documentation (wills), and inter-vivos gifting compliance.
*   **Module 4:** Facilitates the networking, community, and analytical aspects, providing dynamic market data, peer-comparison reports, and direct advisor queries.

---

## Table of Contents
1. [Module 1: User & Profile Classes](#module-1-user--profile-classes)
2. [Module 1.5: Security & Session (Auth-Core Gateway)](#module-15-security--session-auth-core-gateway)
3. [Module 2: Wealth & Portfolio Classes](#module-2-wealth--portfolio-classes)
4. [Module 3: Estate & Legal Planning Classes](#module-3-estate--legal-planning-classes)
5. [Module 4: Advisory & Market Intelligence Classes](#module-4-advisory--market-intelligence-classes)

---

## Module 1: User & Profile Classes

### 1. `User`
The core identity class handling role assignment and basic account management. *(Note: Credential storage is delegated to the external auth-core service).*
*   **Attributes:**
    *   `user_id` (String/UUID) - Primary Key
    *   `email` (String) - Unique identifier
    *   `first_name` (String)
    *   `last_name` (String)
    *   `role` (Enum) - e.g., `INVESTOR`, `ADVISOR`
    *   `created_at` (DateTime)
    *   `last_login` (DateTime)
*   **Functions:**
    *   `get_user_details()`: Fetches the consolidated profile and settings payload for the logged-in user.
    *   `get_role_dashboard()`: Routes the user to the appropriate UI based on their role.
    *   `search_network(search_criteria)`: Queries the database for peers or advisors by specialty, firm name, or location.
    *   `send_connection_request(recipient_id)`: Creates the initial `Connection` object with a `PENDING` status.
    *   `get_network_connections(status_filter=None)`: Fetches a list of all `Connection` objects linked to this user, optionally filtering by status (e.g., pending vs. accepted).

### 2. `InvestorProfile`
Linked to a User with the `INVESTOR` role. Manages data for the Investor Profile and Financial Resume views.
*   **Attributes:**
    *   `profile_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to `User`
    *   `risk_tolerance` (Enum) - `CONSERVATIVE`, `MODERATE`, `AGGRESSIVE`
    *   `investment_horizon_years` (Integer)
    *   `financial_resume_summary` (Text) - Summary of financial background
*   **Functions:**
    *   `update_risk_profile(new_tolerance)`: Adjusts the user's risk settings.
    *   `get_resume_data()`: Packages the profile info for the frontend UI.

### 3. `AdvisorProfile`
Linked to a User with the `ADVISOR` role. Manages professional credentials for the network.
*   **Attributes:**
    *   `profile_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to `User`
    *   `firm_name` (String)
    *   `certifications` (List of Strings) - e.g., CFA, CPA
    *   `specialty_areas` (List of Strings) - e.g., Estate Planning, Equities
*   **Functions:**
    *   `add_certification(cert_name)`: Appends a new qualification to the profile.
    *   `get_public_profile()`: Returns the sanitized data for investors to view.

### 4. `Connection`
Manages the relationship, state, and permissions between two users on the platform.
*   **Attributes:**
    *   `connection_id` (String/UUID) - Primary Key
    *   `requester_id` (Foreign Key) - User who sent the invite
    *   `recipient_id` (Foreign Key) - User who received the invite
    *   `status` (Enum) - `PENDING`, `ACCEPTED`, `REJECTED`, `REVOKED`
    *   `permissions` (Dictionary/JSON) - Access control list (e.g., `{"market_insights": true, "net_worth": false}`)
    *   `created_at` (DateTime)
    *   `updated_at` (DateTime)
*   **Functions:**
    *   `accept_connection()`: Changes status from `PENDING` to `ACCEPTED`.
    *   `reject_connection()`: Changes a `PENDING` request status to `REJECTED`.
    *   `update_permissions(new_permissions_dict)`: Modifies the access control list.
    *   `terminate_connection()`: Changes status to `REVOKED` and instantly nullifies shared data access.
    *   `get_connection_details()`: Returns a packaged dictionary of a specific peer's shared data, status, and current permissions for the frontend UI to render.

### 5. `Setting`
Stores global system preferences for the user account. Designed with a universal framework to support multiple regions and currencies.
*   **Attributes:**
    *   `setting_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to `User`
    *   `two_factor_enabled` (Boolean)
    *   `base_currency` (String) - Global currency standard (e.g., USD, EUR, INR)
    *   `email_notifications` (Boolean)
*   **Functions:**
    *   `get_user_settings()`: Returns the full dictionary of the user's current preferences.
    *   `toggle_2fa(status)`: Enables or disables multi-factor authentication.
    *   `update_base_currency(new_currency)`: Changes the default currency for all wealth calculations.

---

## Module 1.5: Security & Session (Auth-Core Gateway)

Since primary credential verification and user management are delegated to the standalone `auth-core` microservice, this module acts as the localized boundary. It handles the secure handshake, validates incoming tokens, and manages the local application state utilizing Entity-Boundary-Control architecture principles.

### 1. `AuthGateway` (Boundary/Control Class)
The boundary layer responsible for communicating with `auth-core` and validating the entry handshake.
*   **Attributes:**
    *   `public_key` (String) - Used to verify the cryptographic signature of the token sent by auth-core.
    *   `issuer_url` (String) - The trusted URL of the auth-core service.
*   **Functions:**
    *   `verify_handshake(token)`: Validates the signature, audience, and expiration of the incoming token to ensure it genuinely originated from auth-core.
    *   `extract_user_identity(token)`: Decodes the token payload to map the auth-core identity to the local Vittavaan `User` record.

### 2. `LocalSession`
Manages the active state and access rights of the user within the main Vittavaan application once the handshake passes.
*   **Attributes:**
    *   `session_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to the local `User`
    *   `access_token` (String) - The validated token structure
    *   `expires_at` (DateTime)
    *   `is_active` (Boolean)
*   **Functions:**
    *   `create_session(user_id, token)`: Initializes the local session and grants entry to the app.
    *   `validate_session()`: Middleware check to ensure the session is active before loading any protected modules or UI dashboards.
    *   `terminate_session()`: Logs the user out locally and optionally pings `auth-core` to kill the global session.

---

## Module 2: Wealth & Portfolio Classes

This module serves as the core financial engine of Vittavaan. It utilizes a centralized `Portfolio` to group individual holdings and separates assets into specific subclasses to handle the unique data structures required for liquid capital, real estate, and alternative collections.

### 1. `Portfolio`
The aggregator class that groups all financial holdings and obligations for a specific user, acting as the primary point of entry for dashboard metrics.
*   **Attributes:**
    *   `portfolio_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to `User`
    *   `created_at` (DateTime)
    *   `last_updated` (DateTime)
*   **Functions:**
    *   `add_asset(asset_data)`: Instantiates a new asset subclass and links it to the portfolio.
    *   `remove_asset(asset_id)`: Deletes or archives an asset from the portfolio.
    *   `add_liability(liability_data)`: Links a new debt to the portfolio.
    *   `get_total_assets()`: Sums the `current_value` of all linked Asset records.
    *   `get_total_liabilities()`: Sums the `current_balance` of all linked Liability records.
    *   `calculate_net_worth()`: Subtracts total liabilities from total assets to yield the overarching net worth.
    *   `get_net_worth_history(timeframe)`: Fetches a time-series array of past net worth valuations to render historical trend charts.

### 2. `Asset` (Abstract Base Class)
The foundational blueprint for anything of value owned by the user. Subclasses will inherit these core properties.
*   **Attributes:**
    *   `asset_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key) - Links back to `Portfolio`
    *   `name` (String) - e.g., "HDFC Savings Account", "Karjat Land"
    *   `asset_category` (Enum) - `LIQUID`, `REAL_ESTATE`, `ALTERNATIVE`
    *   `purchase_price` (Float) - Initial cost basis
    *   `current_value` (Float) - Latest valuation
    *   `purchase_date` (Date)
    *   `currency` (String) - Local currency of the asset
    *   `notes` (Text)
*   **Functions:**
    *   `update_details(updated_data_dict)`: Allows the user to change the name, notes, or category without altering the financial valuation.
    *   `update_valuation(new_value)`: Overwrites `current_value` and updates the timestamp.
    *   `calculate_roi()`: Computes the percentage yield based on purchase price versus current value.
    *   `get_asset_summary()`: Returns a standardized JSON object for the "All Listings" UI.

### 3. `LiquidAsset` (Subclass of Asset)
Handles traditional financial instruments like bank accounts, mutual funds, or equities.
*   **Attributes:**
    *   `institution_name` (String) - e.g., "Chase Bank", "Zerodha"
    *   `ticker_symbol` (String, Optional) - For publicly traded assets
    *   `quantity_held` (Float) - Number of shares or units
*   **Functions:**
    *   `fetch_live_price()`: Pings an external API to automatically update the `current_value`.

### 4. `RealEstateAsset` (Subclass of Asset)
Tailored for property and land holdings, specifically accommodating views like the *Karjat Plot* prototype.
*   **Attributes:**
    *   `property_type` (Enum) - `LAND`, `RESIDENTIAL`, `COMMERCIAL`
    *   `location_address` (String)
    *   `square_footage` (Float)
    *   `price_per_sqft` (Float)
*   **Functions:**
    *   `calculate_sqft_valuation()`: Multiplies `square_footage` by `price_per_sqft` to dynamically update the `current_value`.

### 5. `AlternativeAsset` (Subclass of Asset)
Designed for passion assets and niche collections, such as the *Stamp Collection* view.
*   **Attributes:**
    *   `collection_type` (String) - e.g., "Philately", "Fine Art", "Numismatics"
    *   `authenticity_cert_id` (String, Optional) - Reference to provenance documents
    *   `last_appraisal_date` (Date)
    *   `appraiser_name` (String)
*   **Functions:**
    *   `check_appraisal_status()`: Flags the asset if the `last_appraisal_date` is older than a specified threshold (e.g., 3 years).

### 6. `Liability`
Tracks all debts, loans, and financial obligations required to calculate true net worth.
*   **Attributes:**
    *   `liability_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key) - Links back to `Portfolio`
    *   `name` (String) - e.g., "Home Mortgage", "Auto Loan"
    *   `liability_type` (Enum) - `MORTGAGE`, `PERSONAL_LOAN`, `CREDIT_CARD`
    *   `principal_amount` (Float) - Original loan size
    *   `current_balance` (Float) - Amount currently owed
    *   `interest_rate` (Float)
    *   `due_date` (Date)
*   **Functions:**
    *   `update_details(updated_data_dict)`: Allows the user to change non-financial attributes like name or liability type.
    *   `record_payment(amount)`: Deducts the payment from the `current_balance`.
    *   `get_liability_summary()`: Packages debt data for the balance sheet UI.

---

## Module 3: Estate & Legal Planning Classes

This module structures the complex logic surrounding family wealth transfer, legal documentation, and tax compliance. It maps directly to the *Household*, *Will*, *Inheritance*, and *Gift* views, ensuring assets are properly assigned to beneficiaries while adhering to jurisdictional rules.

### 1. `HouseholdMember`
Represents family members, dependents, or external beneficiaries who are relevant to the user's estate plan.
*   **Attributes:**
    *   `member_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to the primary `User`
    *   `first_name` (String)
    *   `last_name` (String)
    *   `relationship` (Enum) - e.g., `SPOUSE`, `CHILD`, `SIBLING`, `TRUST`
    *   `date_of_birth` (Date)
    *   `contact_email` (String, Optional)
*   **Functions:**
    *   `update_details()`: Modifies basic contact or relationship information.
    *   `get_age()`: Dynamically computes current age for trust or inheritance age-restriction logic.

### 2. `EstatePlan`
The high-level container that groups all end-of-life directives, executors, and linked documents for a user.
*   **Attributes:**
    *   `plan_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - Links back to `User`
    *   `primary_executor_name` (String)
    *   `primary_executor_contact` (String)
    *   `secondary_executor_name` (String, Optional)
    *   `last_reviewed_date` (Date)
*   **Functions:**
    *   `add_household_member(member_data)`: Creates a new `HouseholdMember` and links them to the estate plan.
    *   `get_household_members()`: Retrieves the list of family members linked to the estate.
    *   `remove_household_member(member_id)`: Removes a family member from the estate plan.
    *   `update_executors()`: Replaces the designated legal executors.
    *   `check_review_status()`: Flags the estate plan with an alert if it hasn't been reviewed in over a year.

### 3. `Will`
Manages the structured data and digital storage references for the legal will document.
*   **Attributes:**
    *   `will_id` (String/UUID) - Primary Key
    *   `plan_id` (Foreign Key) - Links back to `EstatePlan`
    *   `document_storage_url` (String) - Secure cloud link to the PDF/Scanned document
    *   `signature_date` (Date)
    *   `notary_details` (String)
    *   `status` (Enum) - `DRAFT`, `EXECUTED`, `REVOKED`
*   **Functions:**
    *   `upload_document(file_url)`: Attaches a new digital copy of the will.
    *   `verify_execution_status()`: Checks if the document is formally signed and active.
    *   `revoke_will()`: Changes the status to `REVOKED` and archives the document link.

### 4. `InheritanceAllocation`
The connective tissue that links specific `Asset` records to specific `HouseholdMember` beneficiaries.
*   **Attributes:**
    *   `allocation_id` (String/UUID) - Primary Key
    *   `plan_id` (Foreign Key) - Links back to `EstatePlan`
    *   `asset_id` (Foreign Key) - Links to a specific `Asset`
    *   `beneficiary_id` (Foreign Key) - Links to a `HouseholdMember`
    *   `percentage_share` (Float) - e.g., 50.0 for 50%
    *   `distribution_conditions` (Text) - e.g., "Payable upon 25th birthday"
*   **Functions:**
    *   `update_share(new_percentage)`: Adjusts the distribution weight.
    *   `validate_total_allocation(asset_id)`: Sums all shares for a single asset to ensure they equal exactly 100%.

### 5. `GiftRule`
Stores the jurisdictional limits and tax-free thresholds for inter-vivos (living) wealth transfers.
*   **Attributes:**
    *   `rule_id` (String/UUID) - Primary Key
    *   `jurisdiction` (String) - e.g., "Canada", "USA", "India"
    *   `fiscal_year` (Integer)
    *   `annual_exemption_limit` (Float) - Maximum tax-free amount per year
    *   `lifetime_exemption_limit` (Float, Optional)
*   **Functions:**
    *   `update_annual_limit(new_limit)`: Modifies the threshold based on new government tax laws.
    *   `evaluate_compliance(transfer_amount)`: Compares a proposed transfer against the limits and returns a boolean or warning flag.

### 6. `GiftTransfer`
Logs the actual historical or planned movement of assets or cash to family members while the user is still living.
*   **Attributes:**
    *   `transfer_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - The sender
    *   `recipient_id` (Foreign Key) - Links to `HouseholdMember`
    *   `asset_id` (Foreign Key, Optional) - Populated if a specific physical asset was transferred
    *   `cash_value` (Float) - The monetary value of the gift
    *   `transfer_date` (Date)
    *   `tax_filed_status` (Boolean)
*   **Functions:**
    *   `log_transfer()`: Records a completed transaction.
    *   `generate_annual_report(fiscal_year)`: Aggregates all transfers to generate a schedule for tax reporting purposes.

---

## Module 4: Advisory & Market Intelligence Classes

This final module facilitates the networking, community, and analytical aspects of Vittavaan. It leverages the role-based profiles to connect investors with advisors, while providing dynamic market data and peer-comparison reports.

### 1. `AdvisoryQuery` (The "Ask" Module)
Manages direct questions and consultation threads between investors and professional advisors on the network.
*   **Attributes:**
    *   `query_id` (String/UUID) - Primary Key
    *   `asker_id` (Foreign Key) - Links to the `User` (Investor) who asked the question
    *   `advisor_id` (Foreign Key, Optional) - Links to a specific `User` (Advisor). If null, the query is broadcast to the open network.
    *   `subject` (String)
    *   `content_body` (Text)
    *   `status` (Enum) - `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`
    *   `created_at` (DateTime)
    *   `updated_at` (DateTime)
*   **Functions:**
    *   `submit_query()`: Opens a new thread and notifies relevant advisors.
    *   `get_open_queries(advisor_id=None)`: Fetches a list of `OPEN` or `IN_PROGRESS` threads. If `advisor_id` is null, it fetches public community questions.
    *   `add_response(advisor_id, response_text)`: Appends an answer to the thread.
    *   `resolve_query()`: Marks the thread as closed once the investor is satisfied.

### 2. `MarketInsight` (Trends & News)
Handles the publishing and aggregation of financial news, tax updates, or advisor-authored articles on the platform.
*   **Attributes:**
    *   `insight_id` (String/UUID) - Primary Key
    *   `author_id` (Foreign Key) - Links to a `User` (usually an Advisor or System Admin)
    *   `title` (String)
    *   `content` (Text)
    *   `category` (Enum) - e.g., `MACRO_ECONOMICS`, `REAL_ESTATE`, `TAX_POLICY`
    *   `tags` (List of Strings) - e.g., ["crypto", "compliance", "interest rates"]
    *   `published_date` (DateTime)
*   **Functions:**
    *   `publish_insight()`: Makes the article live on the network feed.
    *   `fetch_feed(user_preferences)`: Returns a curated list of insights based on the user's tags or risk profile.

### 3. `PeerBenchmark` (Peers)
A snapshot entity that stores anonymized, aggregated comparison metrics, allowing users to see how their wealth distribution stacks up against similar demographics.
*   **Attributes:**
    *   `benchmark_id` (String/UUID) - Primary Key
    *   `user_id` (Foreign Key) - The user requesting the comparison
    *   `cohort_criteria` (Dictionary) - The filters used for the peer group (e.g., `{"age_range": "35-45", "net_worth_tier": "1M-5M"}`)
    *   `user_metric_value` (Float) - The user's specific data point (e.g., % of wealth in real estate)
    *   `cohort_average` (Float) - The peer group's average for that same data point
    *   `percentile_rank` (Integer) - Where the user ranks within the cohort (1-99)
    *   `generated_at` (DateTime)
*   **Functions:**
    *   `generate_cohort_comparison(metric_type)`: Queries anonymized system data to calculate the peer average and the user's percentile rank.
    *   `get_historical_benchmarks()`: Retrieves past snapshots to show how the user's ranking has evolved over time.

### 4. `PortfolioAnalytics` (Analysis)
A dynamic reporting class that analyzes the user's `Portfolio` and `Asset` allocation to generate risk assessments and diversification scores.
*   **Attributes:**
    *   `analysis_id` (String/UUID) - Primary Key
    *   `portfolio_id` (Foreign Key) - Links back to `Portfolio`
    *   `liquidity_ratio` (Float) - Ratio of liquid assets to total net worth
    *   `debt_to_asset_ratio` (Float)
    *   `diversification_score` (Integer) - A computed health metric (0-100)
    *   `top_heavy_warning` (Boolean) - True if a single asset dominates the portfolio (e.g., > 50% of total wealth)
    *   `evaluated_at` (DateTime)
*   **Functions:**
    *   `run_full_analysis()`: Executes the algorithms that scan the portfolio and calculate the ratios.
    *   `generate_visual_chart_data()`: Packages the analytics into a JSON payload formatted specifically for rendering frontend charts.