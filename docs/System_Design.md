# System Design Document (SDD)

According to OOSE principles, the System Design phase defines the software architecture. It focuses on how the analysis objects are grouped into deployable subsystems, how they map to hardware, and the overarching policies for data, security, and control flow.

## 1. Design Goals
Derived from the requirements and the financial nature of the application, the following design goals drive the architecture:
*   **Absolute Accuracy:** Floating-point calculation errors are unacceptable. All monetary values must be stored and calculated as integers (minor units/paise/cents).
*   **Zero-Trust Security:** Privacy is paramount. The system must support highly granular, time-bound, field-level access controls between peers and advisors.
*   **Extensibility:** While the V1 launch relies on manual data entry, the architecture must support seamless "plug-and-play" integration with external Account Aggregators and Financial APIs in future versions.
*   **Cross-Platform Consistency:** The backend APIs must be strictly decoupled from the UI to support both the initial Desktop Browser release and the future Mobile App releases simultaneously.

---

## 2. Subsystem Decomposition
To manage complexity, Vittavaan is decomposed into loosely coupled subsystems. This follows a classic N-Tier / Service-Oriented Architecture (SOA).

### 2.1 Presentation Subsystems (Client-Side)
*   **Desktop Web Client:** The responsive browser application rendering the 25 HTML wireframes.
*   **Mobile App Client (Future):** The iOS/Android application.

### 2.2 Application Logic Subsystems (Server-Side)
*   **Identity & Access Subsystem:** Validates Auth-Core tokens, manages `LocalSession`, and enforces `Connection` data-sharing rules.
*   **Ledger & Wealth Subsystem:** Manages `Portfolio`, `Asset`, `Liability`, and `Transaction` CRUD operations.
*   **Estate & Legal Subsystem:** Manages `HouseholdMember`, `EstatePlan`, `Will`, and `InheritanceAllocation` logic.
*   **Advisory Marketplace Subsystem:** Manages professional directories, `AdvisoryQuery` workflows, and `MarketInsight` publishing.
*   **Calculation Engine Subsystem (App Service Layer):** The heavy-lifting mathematical engines (`PerformanceAndAttributionEngine`, `CashFlowAndDebtEngine`, `WealthAndOwnershipEngine`).

### 2.3 Storage & Infrastructure Subsystems
*   **Data Room Subsystem:** Secure object storage (e.g., AWS S3) for `Document` entities (Wills, Deeds).
*   **Persistent Storage Subsystem:** The relational database storing all core entities.

---

## 3. Hardware/Software Mapping
Vittavaan utilizes a **Client-Server Architectural Style**.
*   **Client Nodes:** User workstations running standard Web Browsers (and eventually smartphones).
*   **API Gateway Node:** A reverse-proxy server that routes incoming HTTPS requests to the appropriate Application Subsystems.
*   **Application Server Nodes:** Scalable computing nodes hosting the stateless Calculation Engines and Business Logic subsystems.
*   **Database Server Node:** A dedicated, highly secure node hosting the Relational Database Management System.
*   **External Nodes:** The independent Auth-Core system and future External Financial APIs.

---

## 4. Persistent Data Management
Given the strict requirements for financial accuracy and complex entity relationships, Vittavaan will use a **Relational Database Management System (RDBMS)** (e.g., PostgreSQL).
*   **ACID Compliance:** Essential for the `Transaction` ledger to guarantee data integrity during cash flow logging.
*   **Referential Integrity:** Strict foreign key constraints will be utilized. For example, the database must prevent the deletion of an `Asset` if it is actively linked to an `InheritanceAllocation` or a `FinancialGoal`.
*   **Immutability:** `FinancialSnapshot` and `Transaction` records are designed to be append-only ledgers to preserve historical accuracy.

---

## 5. Access Control Policy
Vittavaan requires a hybrid access control model:
*   **Authentication:** Delegated to the external Auth-Core system. Vittavaan only accepts cryptographically signed tokens.
*   **Static Access Control (RBAC):** Base permissions are determined by the `User` boolean flags (`is_investor`, `is_advisor`). For example, only users with `is_advisor = true` can execute the `publish_insight()` operation.
*   **Dynamic Access Control (ABAC):** The *ConsentAndMarketplaceEngine* acts as a Protection Proxy. When an Advisor requests to view an Investor's portfolio, this engine dynamically reads the `Connection.permissions` JSON and the `consent_expires_at` timestamp. If the current time is past expiry, or the specific field is not whitelisted, the engine scrubs the data from the API response before it reaches the Boundary Object.

---

## 6. Global Control Flow
*   **Synchronous Flow:** Standard CRUD operations (e.g., submitting an `AddAssetForm`) use a request-response model (REST or GraphQL) where the client waits for confirmation.
*   **Event-Driven Flow:** Heavy calculations are decoupled via an event bus. For example, when an `Asset` is updated, the system fires an `AssetUpdatedEvent`. A background worker listens for this event and triggers the `capture_periodic_metrics()` operation to generate a new `FinancialSnapshot` asynchronously, preventing the UI from freezing.

---

## 7. Boundary Conditions (Exception Handling)
*   **External Dependency Failure:** If the Auth-Core system goes offline, the `AuthGatewayControl` will fail gracefully, alerting the user to try again later, rather than crashing the frontend.
*   **Stale Data Graceful Degradation:** If a user attempts to view the `AttributionPage` but has no `Transactions` logged, the `PerformanceAndAttributionEngine` throws an `InsufficientDataException`. The UI catches this and renders an empty state component with a call-to-action ("Log a transaction to see returns"), rather than showing `NaN` or `0%`.
*   **Data Room Outage:** If the object storage system (S3) is unreachable, the system allows the user to view their `EstatePlan` text data but disables the "Download Will" button, showing an appropriate warning.
