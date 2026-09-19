# Analysis: Object Model

According to OOSE principles, the Analysis phase translates the functional requirements and use cases into an **Analysis Object Model**. This model abstracts the system into three distinct types of objects (the Entity-Control-Boundary pattern) to ensure the architecture remains modular, resilient to UI changes, and strictly aligned with the business logic.

To ensure the exact functionality of the 25 wireframes is fully supported, **no object has been omitted**. Every screen, data point, and calculation engine has a corresponding object below.

---

## 1. Entity Objects
Entity objects represent the persistent, long-lived information tracked by the system. These map directly to the underlying database tables and abstract concepts of the financial domain.

*   **Identity & Network Entities**
    *   `User`: The core identity representing a human being on the platform.
    *   `InvestorProfile`: The financial persona, tracking demographics, risk tolerance, and investment horizon.
    *   **`AdvisorProfile`:** The professional persona, tracking firm details and verified certifications.
    *   **`Connection`:** The relationship state between two users, storing strict, time-bound, field-level access consent rules.
    *   **`Setting`:** User preferences for base currency, 2FA, and notifications.
    *   **`Document`:** Secure data room file records (e.g., wills, deeds, valuation reports).
    *   **`LocalSession`:** Active authentication tokens and expiry states.

*   **Wealth & Portfolio Entities**
    *   **`Portfolio`:** The container for a user's ledger.
    *   **`Asset` (Abstract):** The base class for holdings, tracking ownership split, purchase price, current value, and data provenance (verification level).
    *   **`LiquidAsset`:** Specialized asset for equities, mutual funds, and bank accounts.
    *   **`RealEstateAsset`:** Specialized asset tracking square footage, localized pricing, and property types.
    *   **`AlternativeAsset`:** Specialized asset for passion investments, tracking manual appraisal dates.
    *   **`Liability`:** Debt obligations, tracking principal, current balance, interest rates, and due dates.
    *   **`Transaction`:** The immutable ledger of cash flows (inflows, outflows, buys, sells).
    *   **`FinancialSnapshot`:** A permanent historical record of net worth at a specific point in time.

*   **Estate Planning Entities**
    *   **`HouseholdMember`:** Dependents, spouses, or beneficiaries.
    *   **`EstatePlan`:** The overarching blueprint, naming primary and secondary executors.
    *   **`Will`:** The legal document state (Draft, Executed, Revoked).
    *   **`InheritanceAllocation`:** The specific percentage share of a designated asset granted to a `HouseholdMember`.
    *   **`GiftRule`:** Jurisdictional tax exemption limits and effective dates.
    *   **`GiftTransfer`:** Logged inter-vivos (living) wealth transfers.

*   **Advisory & Market Entities**
    *   **`AdvisoryQuery`:** A consultation thread between an investor and an advisor.
    *   **`MarketInsight`:** An article or trend report published by an advisor.
    *   **`PeerBenchmark`:** Aggregated, anonymized cohort data for comparative rankings.

---

## 2. Boundary Objects
Boundary objects represent the system's interface with the actors. These map directly to the provided HTML wireframes, data input forms, and system notifications.

*   **Dashboard & View Boundaries (Pages)**
    *   **`NetWorthPage`:** The primary dashboard displaying total aggregated wealth.
    *   **`AssetsAndLiabilitiesPage`:** The master list of all holdings and debts.
    *   **`KarjatPlotPage`:** A specialized view for a specific `RealEstateAsset`.
    *   **`StampCollectionPage`:** A specialized view for a specific `AlternativeAsset`.
    *   **`AnalysisPage`:** High-level trends and asset allocation charts.
    *   **`AttributionPage`:** Detailed performance metrics (TWRR, XIRR).
    *   **`CreditPage`:** Liability amortization and debt service ratios.
    *   **`PlanningPage`:** Financial goal tracking and funding gaps.
    *   **`HouseholdPage`:** Management of family members and dependents.
    *   **`InheritancePage`:** View of asset allocations and beneficiaries.
    *   **`WillPage`:** View of executor appointments and document status.
    *   **`GiftRulesPage`:** Display of compliance and exemption limits.
    *   **`GiftTransferPage`:** Interface for logging a new gift.
    *   **`ConnectionsPage`:** Interface for managing network peers and data sharing.
    *   **`FinancialResumePage`:** A compiled summary of the investor's standing.
    *   **`InvestorProfilePage` & `ProfilingPage`:** Screens for onboarding and updating risk/demographics.
    *   **`SettingsPage`:** User preferences UI.
    *   **`AdvisorsPage` & `MarketplacePage`:** Directories of professional advisors.
    *   **`MarketplaceBrowsePage` & `MarketplaceLandPage`:** specialized views for navigating advisory services.
    *   **`AskPage`:** Interface for submitting a new `AdvisoryQuery`.
    *   **`TrendsAndNewsPage`:** The feed of `MarketInsights`.
    *   **`PeersPage`:** Interface for comparing against `PeerBenchmarks`.
    *   *(Note: `Schema.dc.html`, `User Flow.dc.html`, `User Story.dc.html`, `Platform Map.dc.html`, `Platform.dc.html`, and `Pages.dc.html` are architectural/design documentation files, not run-time user interfaces).*

*   **Form & Action Boundaries**
    *   **`AddAssetForm`:** UI component for data entry of new holdings.
    *   **`ConsentConfigurationForm`:** UI component for selecting specific fields and expiry dates for a `Connection`.
    *   **`AllocationForm`:** UI component for assigning percentage shares to beneficiaries.
    *   **`LogTransactionForm`:** UI component for recording cash flows.

*   **Notice Boundaries**
    *   **`StaleDataWarning`:** Alert shown when an appraisal is outdated.
    *   **`ValidationErrorNotice`:** Alert shown when business rules fail (e.g., allocation > 100%).
    *   **`NotificationAlert`:** System messages indicating new connections or answered queries.

---

## 3. Control Objects
Control objects orchestrate the use cases. They contain the complex business logic, mathematical calculations, and workflow validations. They sit between the Boundary objects (UI) and the Entity objects (Database).

*   **`WealthAndOwnershipEngine`:** Calculates absolute net worth by multiplying gross asset values against the `ownership_split_pct` to ensure fractional ownership is accurately represented.
*   **`PerformanceAndAttributionEngine`:** Consumes the `Transaction` ledger to calculate complex time-weighted (TWRR) and money-weighted (XIRR) returns for the `AttributionPage`.
*   **`ValuationAndVerificationEngine`:** Monitors the `valuation_as_of` dates on alternative assets and triggers `StaleDataWarning` boundary objects when thresholds are exceeded.
*   **`CashFlowAndDebtEngine`:** Calculates amortization schedules and Debt Service Ratios for the `CreditPage`.
*   **`PlanningAndScenarioEngine`:** Evaluates current portfolio trajectories against `FinancialGoal` target amounts to calculate funding gaps.
*   **`ConsentAndMarketplaceEngine`:** The gatekeeper that intercepts requests on the `ConnectionsPage`, evaluates the `Connection.permissions` JSON, and strips out unauthorized data fields before rendering.
*   **`EstatePlanningControl`:** Orchestrates the `InheritancePage`, validating that new `InheritanceAllocations` do not exceed 100% of an asset's value.
*   **`AuthGatewayControl`:** Verifies incoming tokens from the external Auth-Core system and manages the lifecycle of the `LocalSession`.
*   **`PeerBenchmarkingControl`:** Aggregates and anonymizes portfolio data from users within the same demographic constraints to generate dynamic `PeerBenchmarks`.
*   **`AdvisoryControl`:** Manages the state transitions of `AdvisoryQuery` threads (Open -> In Progress -> Resolved) and orchestrates the distribution of `MarketInsights` to the `TrendsAndNewsPage`.
