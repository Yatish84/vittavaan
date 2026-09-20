# Requirements Elicitation

## 1. System Boundary and Actors
The Vittavaan system interacts with the following actors:
*   **Investor:** The primary user who aggregates their portfolio, tracks assets and liabilities, manages estate plans, and connects with peers and advisors.
*   **Advisor:** A professional user (who may also be an Investor) who maintains a public profile with verified credentials, answers financial queries, and publishes market insights.
*   **Household Member/Beneficiary:** A tracked entity receiving inheritance allocations or gifts. 
*   **System Administrator:** An internal actor responsible for verifying advisor credentials, managing global settings, and monitoring system integrity.
*   **External Auth-Core System:** An external authentication provider that manages user registration and password verification, passing tokens to Vittavaan.
*   **External Financial API (Future):** An external system actor that will eventually feed real-time valuation and account aggregation data into Vittavaan.

---

## 2. High-Level Use Cases

### 2.1 User Identity & Session Management (Auth-Core Integration)
*   **Process Authentication Handshake:** Receive the token from the external Auth-Core, verify the handshake, and extract the user identity.
*   **Manage Local Session:** Create, validate, and terminate the user's active session within Vittavaan.
*   **Initialize Local Identity:** Create the baseline user record in Vittavaan if the identity provided by the Auth-Core token is logging in for the first time.
*   **Switch Context:** Toggle the application interface between the personal "Investor" view and the professional "Advisor" view.
*   **Manage Preferences:** Update base currency, notification settings, and local security preferences (e.g., 2FA enforcement).

### 2.2 Profile & Network Management
*   **Update Investor Profile:** Set or modify financial demographics, risk tolerance, and investment horizon.
*   **Update Advisor Profile:** Add or verify professional certifications and areas of specialty.
*   **Generate Financial Resume:** Compile and view a summary of the user's financial standing and profile.
*   **Search Network:** Query the platform to find peers for comparison or certified advisors for consultation.
*   **Manage Connections:** Send, accept, reject, or terminate connection requests with other users.
*   **Manage Data Consents:** Define, update, or revoke strict, time-bound, field-level data sharing permissions for specific connections.

### 2.3 Wealth & Portfolio Management
*   **Manage Liquid Assets:** Add, update, or remove traditional financial instruments.
*   **Manage Real Estate Assets:** Add, update, or remove properties, including calculating valuations based on square footage and pricing.
*   **Manage Alternative Assets:** Add, update, or remove passion assets, and track manual appraisal expiry dates.
*   **Manage Liabilities:** Add or remove loans, track interest rates, and record principal/interest payments.
*   **Log Transactions:** Manually record cash flow events against specific assets or the general portfolio.
*   **View Net Worth Dashboard:** View aggregated, real-time totals of assets, liabilities, and overall net worth.
*   **View Performance & Attribution:** Analyze historical snapshots, money-weighted returns (XIRR), and time-weighted returns (TWRR).

### 2.4 Financial Planning & Estate Structuring
*   **Manage Financial Goals:** Create future objectives, link them to specific assets, and calculate the funding gap.
*   **Manage Household:** Add and update demographic details for family members and dependents.
*   **Structure Estate Plan:** Appoint and manage primary and secondary executors for the estate.
*   **Manage Wills:** Upload will documents, verify execution status, or revoke them.
*   **Allocate Inheritance:** Assign percentage shares of specific assets to household beneficiaries.
*   **Log Gift Transfers:** Record inter-vivos wealth transfers and evaluate tax compliance against jurisdictional gift rules.
*   **Manage Data Room (Documents):** Upload, view, and link secure documents to specific assets or estate plans.

### 2.5 Advisory & Market Intelligence
*   **Submit Advisory Query:** As an investor, open a consultation thread with an advisor.
*   **Manage Advisory Queries:** As an advisor, view open queries, provide responses, and resolve queries.
*   **Publish Market Insight:** As an advisor, author and publish market trends or economic news.
*   **Consume Market Feed:** View a personalized feed of market insights and news.
*   **View Peer Benchmarks:** Compare personal financial metrics against anonymized data from similar demographic cohorts.

## 3. Detailed Core Use Cases

To drive the system design and architecture, we have selected three core use cases that represent the most essential and complex functionality of Vittavaan: Asset Management, Estate Planning, and Secure Networking.

### 3.1 Use Case: Add Real Estate Asset
*   **Use Case Name:** AddRealEstateAsset
*   **Initiating Actor:** Investor
*   **Entry Condition:** The Investor is authenticated and is viewing their active Portfolio.
*   **Flow of Events:**
    1. The Investor selects the option to add a new Real Estate asset.
    2. The System presents a form requesting property type (e.g., Land, Residential), location address, square footage, price per square foot (in minor units), and the user's ownership split percentage.
    3. The Investor inputs the required information and submits the form.
    4. The System's *Application Service Layer* calculates the gross valuation (`square_footage` * `price_per_sqft`).
    5. The System calculates the attributed value based on the `ownership_split_pct`.
    6. The System saves the new `RealEstateAsset` to the database, linked to the Investor's `Portfolio`.
    7. The System triggers a background job to capture a new `FinancialSnapshot`, updating the user's total net worth.
    8. The System confirms the addition to the Investor.
*   **Exceptional Flows:**
    *   *Invalid Ownership Split:* If the Investor inputs an ownership split > 100% or < 0%, the System rejects the input and prompts for correction.
    *   *Missing Data:* If required fields (like square footage) are missing, the System prompts the Investor to complete the form.
*   **Exit Condition:** The asset is successfully added to the portfolio, and the user's net worth snapshot is updated.

### 3.2 Use Case: Allocate Inheritance
*   **Use Case Name:** AllocateInheritance
*   **Initiating Actor:** Investor
*   **Entry Condition:** The Investor has an active `EstatePlan`, at least one `HouseholdMember` registered, and assets in their `Portfolio`.
*   **Flow of Events:**
    1. The Investor navigates to the Estate Planning module and selects a specific `Asset` to allocate.
    2. The System retrieves and displays the list of registered `HouseholdMembers`.
    3. The Investor selects a `HouseholdMember` and inputs a percentage share and any specific distribution conditions (text).
    4. The System validates that the sum of all `percentage_share` allocations for this specific `Asset` across all beneficiaries does not exceed 100%.
    5. The System saves the `InheritanceAllocation` record.
    6. The System displays the updated allocation summary for the Asset.
*   **Exceptional Flows:**
    *   *Allocation Exceeds 100%:* If the new allocation pushes the total over 100% for the asset, the System rejects the submission and displays an error indicating the remaining available percentage.
*   **Exit Condition:** The inheritance allocation is legally recorded within the system's Estate Plan for the chosen beneficiary.

### 3.3 Use Case: Grant Advisor Data Consent
*   **Use Case Name:** GrantAdvisorDataConsent
*   **Initiating Actor:** Investor
*   **Communicating Actor:** Advisor
*   **Entry Condition:** The Investor has an existing, accepted `Connection` with the Advisor.
*   **Flow of Events:**
    1. The Investor selects the Advisor from their network and chooses to update data-sharing permissions.
    2. The System presents a granular checklist of portfolio components (e.g., total net worth, specific real estate assets, liability details), a field for "Consent Purpose", and a date picker for "Consent Expiry".
    3. The Investor selects the desired fields, enters the purpose, sets an expiry date (e.g., 30 days from now), and submits.
    4. The System updates the `permissions` JSON/Dictionary and the expiry timestamps on the `Connection` object.
    5. The System generates a `ConsentForm` document in the Data Room as an immutable log of this action.
    6. The System sends a notification to the Advisor indicating that new data access has been granted.
*   **Exceptional Flows:**
    *   *Invalid Expiry Date:* If the selected expiry date is in the past, the System rejects the submission and prompts for a valid future date.
*   **Exit Condition:** The Advisor can now view the specifically permitted data points until the exact expiry timestamp is reached.

### 3.4 Use Case: View Portfolio Performance & Metrics
*   **Use Case Name:** ViewPortfolioPerformance
*   **Initiating Actor:** Investor
*   **Entry Condition:** The Investor is authenticated, has existing assets and transactions, and navigates to the "Analysis" or "Attribution" dashboard.
*   **Flow of Events:**
    1. The Investor requests to view their portfolio performance and metric breakdown for a specific time horizon.
    2. The System queries the database to retrieve the Investor's `Portfolio` along with all linked `Assets`, `Liabilities`, and historical `Transactions`.
    3. The System passes the transaction ledger to the *PerformanceAndAttributionEngine* to calculate complex derived metrics, such as time-weighted returns (TWRR) and money-weighted returns (XIRR).
    4. The System passes the asset data to the *WealthAndOwnershipEngine* to aggregate total asset values, strictly applying the `ownership_split_pct` to ensure accurate household representation.
    5. The System retrieves historical `FinancialSnapshots` to generate time-series trend data.
    6. The System aggregates these Source, Derived, and Hidden metrics and formats them for the user interface.
    7. The System renders the Dashboard displaying the charts, net worth totals, return percentages, and asset allocation breakdown.
*   **Exceptional Flows:**
    *   *Insufficient Data:* If the user has not logged enough transactions to calculate XIRR/TWRR, the System gracefully degrades the UI, displaying an empty state or "N/A" with a prompt to "Log your first transaction."
    *   *Stale Valuations:* If the system detects that an alternative asset's `valuation_as_of` date is older than the configured threshold (e.g., > 1 year), the System flags the specific metric on the dashboard with a "Stale Data / Needs Appraisal" warning.
*   **Exit Condition:** The Investor successfully views their up-to-date, accurately calculated performance metrics and trends.
