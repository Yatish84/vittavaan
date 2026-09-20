# Object Design Document (ODD)

Following OOSE principles, the Object Design phase bridges the gap between our abstract Analysis model and the actual codebase. This document details the exact class interfaces, mathematical contracts (preconditions, postconditions, invariants), and the Design Patterns that will ensure the Vittavaan codebase is robust, secure, and extensible.

---

## 1. Applied Design Patterns

To solve recurring architectural challenges in Vittavaan, we will utilize the following standard Design Patterns:

### 1.1 Strategy Pattern (Calculation Engines)
*   **Problem:** Vittavaan needs to calculate complex metrics (like XIRR or TWRR) for portfolios, but the exact algorithms might change based on future regulatory updates or different asset classes.
*   **Solution:** We encapsulate the calculation algorithms within specific Strategy classes (e.g., `PerformanceAndAttributionEngine`). The core `Portfolio` object simply passes its data to the engine without knowing *how* the math is done.
*   **Benefit:** We can swap or upgrade financial calculation algorithms at runtime without modifying the core data structures.

### 1.2 Protection Proxy Pattern (Zero-Trust Security)
*   **Problem:** Advisors should only see Investor data if explicit, time-bound consent has been granted.
*   **Solution:** We use the `ConsentAndMarketplaceEngine` as a Protection Proxy. When an Advisor's UI requests a client's portfolio, the request hits the Proxy first. The Proxy evaluates the `Connection` object's `consent_expires_at` timestamp and `permissions` JSON. If access is denied or expired, the Proxy throws an `UnauthorizedAccessException` before the real `Portfolio` object is ever touched.
*   **Benefit:** Enforces strict, centralized access control without cluttering the data classes with security logic.

### 1.3 Observer Pattern (Event-Driven Updates)
*   **Problem:** When a user updates the value of a `RealEstateAsset` (e.g., changes the price per sqft), the system must generate a new `FinancialSnapshot` to track the net worth trend.
*   **Solution:** The `Asset` acts as a *Subject*. When its value changes, it fires an event. The `WealthAndOwnershipEngine` acts as an *Observer*. It listens for this event and automatically calculates and saves the new snapshot.
*   **Benefit:** Decouples the UI form submission from the heavy background calculation, ensuring the app remains responsive.

### 1.4 Facade Pattern (API Simplification)
*   **Problem:** The `NetWorthPage` wireframe requires data from Assets, Liabilities, pending Advisory Queries, and Estate Plans all at once.
*   **Solution:** We create a `DashboardFacade` control object. The frontend makes a single API call to `getDashboardMetrics()`. The Facade internally queries the various tables and engines, formats the data, and returns a single clean JSON payload.
*   **Benefit:** Reduces network calls and simplifies frontend development.

---

## 2. Interface Specifications & Contracts

To guarantee absolute data integrity, we define strict contracts for our core classes.

### 2.1 Class: `Asset` (Abstract Entity)
*   **Visibility:** Public methods, Private attributes.
*   **Attributes:**
    *   `- current_value_minor_units: Integer`
    *   `- ownership_split_pct: Float`
*   **Invariant Contract:** 
    *   `ownership_split_pct >= 0.0 AND ownership_split_pct <= 100.0` (A user cannot own more than 100% of an asset).
*   **Operations:**
    *   `+ updateValuation(newValueMinorUnits: Integer): void`
        *   *Precondition:* `newValueMinorUnits >= 0` (Asset values cannot be negative; liabilities are tracked separately).
        *   *Postcondition:* `current_value_minor_units == newValueMinorUnits`
    *   `+ calculateAttributedValue(): Integer`
        *   *Return:* `current_value_minor_units * (ownership_split_pct / 100)`

### 2.2 Class: `EstatePlanningControl` (Control Object)
*   **Operations:**
    *   `+ allocateInheritance(assetId: UUID, beneficiaryId: UUID, percentage: Float): void`
        *   *Precondition:* `percentage > 0`
        *   *Precondition:* `(currentTotalAllocated(assetId) + percentage) <= 100.0`
        *   *Postcondition:* A new `InheritanceAllocation` record is successfully saved to the database.
        *   *Exception:* Throws `AllocationExceededException` if the user tries to assign more than the remaining unallocated percentage.

### 2.3 Class: `Connection` (Entity Object)
*   **Attributes:**
    *   `- consent_expires_at: DateTime`
    *   `- permissions: List<String>`
*   **Operations:**
    *   `+ isDataAccessible(requestingUserId: UUID, dataField: String): Boolean`
        *   *Postcondition:* Returns `True` ONLY IF (`requestingUserId == recipient_id`) AND (`consent_expires_at > CURRENT_TIMESTAMP`) AND (`permissions.includes(dataField)`).

---

## 3. Mapping Associations to Collections (Data Structures)

How we map UML associations into actual programming language collections:

*   **1-to-Many (Portfolio to Assets):** A single `Portfolio` contains multiple `Assets`. In the `Portfolio` class, this is mapped as a private List/Array: `private List<Asset> assets`. We expose safe methods like `+ addAsset(Asset a)` rather than making the list public.
*   **Qualified Associations (User to Connections):** A `User` has many `Connections` with other peers. For rapid O(1) lookups during security checks, this is mapped as a Hash Map (Dictionary) rather than a flat list: `private Map<UUID, Connection> connections`, where the key is the peer's `user_id`.
