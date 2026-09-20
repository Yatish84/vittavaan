# Phase 2 — Analysis: Sequence Diagrams

> **OOSE Phase:** Analysis
> **Purpose:** Shows how Entity, Control, and Boundary objects collaborate — in time — to fulfil the key use cases from Phase 1. Each diagram uses the Cockburn use case ID as its reference.
> **Status:** Draft

---

## How to Read These Diagrams

- **Actors** (Investor, Advisor, Admin) appear on the left.
- **Boundary** objects (`Page`, `Form`, `Warning`) are blue boxes.
- **Control** objects (`Engine`, `Control`, `Facade`, `Gateway`) are green boxes.
- **Entity** objects (`Portfolio`, `Asset`, `Connection`, etc.) are yellow boxes.
- **External systems** (Auth Provider, Object Storage) are grey boxes.

All monetary interactions enforce the integer minor-units contract. No floating-point money crosses any object boundary.

---

## UC-AUTH-001: Register and Authenticate

```mermaid
sequenceDiagram
    actor Investor
    participant LoginPage as LoginPage\n(Boundary)
    participant AuthGW as AuthGatewayControl\n(Control)
    participant AuthProv as Supabase Auth\n(External)
    participant UserDB as User Entity\n(Entity)
    participant Session as LocalSession Entity\n(Entity)
    participant Portfolio as Portfolio Entity\n(Entity)

    Investor->>LoginPage: Submit credentials (email + pw / OTP)
    LoginPage->>AuthProv: Authenticate user
    AuthProv-->>LoginPage: Return signed JWT
    LoginPage->>AuthGW: POST /api/v1/auth/session {jwt_token}
    AuthGW->>AuthProv: Verify JWT signature (public key)
    AuthProv-->>AuthGW: JWT claims {sub, email, ...}

    alt New User (no User record for this sub)
        AuthGW->>UserDB: CREATE User {sub, email, is_investor=true}
        UserDB-->>AuthGW: User record
        AuthGW->>Portfolio: CREATE Portfolio {user_id}
        Portfolio-->>AuthGW: Portfolio record
    else Existing User
        AuthGW->>UserDB: FETCH User WHERE jwt_sub = sub
        UserDB-->>AuthGW: User record
    end

    AuthGW->>Session: CREATE LocalSession {user_id, jwt_sub, expires_at}
    Session-->>AuthGW: Session record
    AuthGW-->>LoginPage: 200 OK {user_id, session_token, redirect_to: /dashboard}
    LoginPage->>Investor: Redirect to Net Worth Dashboard
```

---

## UC-PORT-001: Add Liquid Asset

```mermaid
sequenceDiagram
    actor Investor
    participant ALPage as AssetsAndLiabilitiesPage\n(Boundary)
    participant AddForm as AddAssetForm\n(Boundary)
    participant WOE as WealthAndOwnershipEngine\n(Control)
    participant VVE as ValuationAndVerificationEngine\n(Control)
    participant AssetDB as LiquidAsset Entity\n(Entity)
    participant Portfolio as Portfolio Entity\n(Entity)
    participant SnapJob as FinancialSnapshot\nBackground Job

    Investor->>ALPage: Select "Add Asset → Liquid"
    ALPage->>AddForm: Render AddAssetForm (liquid subtype)
    Investor->>AddForm: Fill and submit form\n{name, sub_type, quantity, purchase_price,\ncurrent_value, purchase_date, ownership_pct}

    Note over AddForm: Client-side validation\n(non-blocking pre-check)
    AddForm->>WOE: POST /api/v1/assets {asset_data}

    Note over WOE: Validate:\nownnership_pct ∈ [0,100]\namounts ≥ 0 (integers)\nrequired fields present

    alt Validation fails
        WOE-->>AddForm: 422 Unprocessable Entity\n{field_errors: [...]}
        AddForm->>Investor: Show inline validation errors
    else Validation passes
        WOE->>AssetDB: INSERT liquid_asset {all fields}
        AssetDB-->>WOE: asset_id
        WOE->>WOE: calculate_attributed_value()\n= current_value × (ownership_pct / 100)
        WOE->>VVE: check_staleness(asset)
        VVE-->>WOE: StalenessResult {is_stale: false}
        WOE->>Portfolio: update_last_updated_at()
        WOE->>SnapJob: queue_snapshot_job(portfolio_id)\n[async — returns immediately]
        WOE-->>AddForm: 201 Created {asset_id, attributed_value, staleness_status}
        AddForm->>ALPage: Navigate to asset list
        ALPage->>Investor: Show asset card with success toast
    end
```

---

## UC-PORT-004: Log a Cash Flow Transaction

```mermaid
sequenceDiagram
    actor Investor
    participant ALPage as AssetsAndLiabilitiesPage\n(Boundary)
    participant TxnForm as LogTransactionForm\n(Boundary)
    participant CFE as CashFlowAndDebtEngine\n(Control)
    participant TxnDB as Transaction Entity\n(Entity)
    participant SnapJob as FinancialSnapshot\nBackground Job

    Investor->>ALPage: Select "Log Transaction"
    ALPage->>TxnForm: Render LogTransactionForm
    Investor->>TxnForm: Fill form\n{date, amount_inr, type, category, notes}

    Note over TxnForm: Convert INR → paise\namount_minor_units = amount_inr × 100

    TxnForm->>CFE: POST /api/v1/transactions {transaction_data}

    Note over CFE: Validate:\ndate ≤ today\namount_minor_units > 0\ntype ∈ TransactionTypeEnum\ncategory provided

    alt Date is in the future
        CFE-->>TxnForm: 422 {error: "Transaction date cannot be in the future"}
        TxnForm->>Investor: Show error
    else Amount is zero or negative
        CFE-->>TxnForm: 422 {error: "Amount must be greater than zero"}
        TxnForm->>Investor: Show error
    else Valid
        Note over CFE: Append-only — no UPDATE/DELETE ever
        CFE->>TxnDB: INSERT transaction\n{all fields, is_correction_for: null}
        TxnDB-->>CFE: transaction_id

        Note over CFE: Invalidate cached\ncash flow aggregates

        CFE->>SnapJob: queue_snapshot_job(portfolio_id)\n[async]
        CFE-->>TxnForm: 201 Created {transaction_id}
        TxnForm->>Investor: Success toast "Transaction logged"
    end
```

---

## UC-DASH-001: View Net Worth Dashboard

```mermaid
sequenceDiagram
    actor Investor
    participant NWPage as NetWorthPage\n(Boundary)
    participant Facade as DashboardFacade\n(Control)
    participant WOE as WealthAndOwnershipEngine\n(Control)
    participant VVE as ValuationAndVerificationEngine\n(Control)
    participant CFE as CashFlowAndDebtEngine\n(Control)
    participant PAE as PerformanceAndAttributionEngine\n(Control)
    participant CME as ConsentAndMarketplaceEngine\n(Control)
    participant SnapDB as FinancialSnapshot Entity\n(Entity)
    participant AssetDB as Asset Entity\n(Entity)

    Investor->>NWPage: Navigate to /dashboard
    NWPage->>Facade: GET /api/v1/dashboard {user_id}

    par Parallel computation
        Facade->>WOE: calculate_net_worth(portfolio_id)
        WOE->>AssetDB: Fetch all assets (attributed values)
        AssetDB-->>WOE: List~Asset~
        WOE-->>Facade: NetWorthResult {total_assets, total_liabilities, net_worth}
    and
        Facade->>SnapDB: fetch_historical_trend(12 months)
        SnapDB-->>Facade: List~FinancialSnapshot~
    and
        Facade->>VVE: get_stale_assets(portfolio_id)
        VVE->>AssetDB: Fetch assets with valuation_as_of
        AssetDB-->>VVE: List~Asset~
        VVE-->>Facade: List~StaleAsset~
    and
        Facade->>CFE: calculate_monthly_surplus(portfolio_id, current_month)
        CFE-->>Facade: SurplusResult
    end

    Facade->>WOE: calculate_net_worth_waterfall(portfolio_id, 1_month)
    WOE-->>Facade: WaterfallResult

    Facade->>VVE: calculate_verified_wealth_pct(portfolio_id)
    VVE-->>Facade: Float (verified_wealth_pct)

    Note over Facade: Compute alerts:\n- Stale assets\n- Expiring consents\n- Concentration risks

    CME->>CME: check_expiring_consents(user_id)

    Note over Facade: Assemble DashboardPayload\nwith provenance metadata:\n{as_of, calculation_version,\nverification_summary, is_partial}

    Facade-->>NWPage: 200 OK DashboardPayload
    NWPage->>Investor: Render full dashboard

    alt Empty portfolio (no assets logged)
        Facade-->>NWPage: 200 OK {net_worth: 0, empty_state: true}
        NWPage->>Investor: Render onboarding empty state
    end
```

---

## UC-DASH-002: View Portfolio Performance (XIRR & TWRR)

```mermaid
sequenceDiagram
    actor Investor
    participant AnalPage as AnalysisPage\n(Boundary)
    participant PAE as PerformanceAndAttributionEngine\n(Control)
    participant TxnDB as Transaction Entity\n(Entity)
    participant SnapDB as FinancialSnapshot Entity\n(Entity)

    Investor->>AnalPage: Navigate to Analysis, select "3 Years"
    AnalPage->>PAE: GET /api/v1/performance?window=3Y

    PAE->>TxnDB: fetch_period_transactions(start, end)
    TxnDB-->>PAE: List~Transaction~

    PAE->>SnapDB: fetch_snapshot(start_date)
    SnapDB-->>PAE: FinancialSnapshot (start of period value)

    PAE->>SnapDB: fetch_snapshot(end_date)
    SnapDB-->>PAE: FinancialSnapshot (end of period value)

    Note over PAE: XIRR: Solve for r where\nNPV of all cashflows +\nterminal value = 0\n(Newton-Raphson / Brent method)

    alt Insufficient transactions for XIRR
        PAE-->>AnalPage: 200 OK\n{xirr: null, error: "INSUFFICIENT_DATA",\nxirr_message: "Log transactions to see XIRR"}
        AnalPage->>Investor: Show InsufficientDataNotice for XIRR
    else XIRR solver does not converge
        PAE-->>AnalPage: 200 OK\n{xirr: null, error: "CONVERGENCE_FAILED"}
        AnalPage->>Investor: Show convergence error notice
    else XIRR computed
        Note over PAE: TWRR: Geometrically link\nsub-period returns between\neach external cash flow\n(neutralises timing effects)

        PAE->>PAE: calculate_max_drawdown(portfolio_id, period)

        Note over PAE: Build PerformanceBasis:\nVERIFIED / ESTIMATED / MIXED\nbased on asset verification levels

        PAE-->>AnalPage: 200 OK\n{xirr, twrr, max_drawdown, performance_basis}
        AnalPage->>Investor: Render XIRR & TWRR side-by-side\nwith methodology labels and PerformanceBasis badge
    end
```

---

## UC-ESTATE-002: Allocate Inheritance

```mermaid
sequenceDiagram
    actor Investor
    participant InhPage as InheritancePage\n(Boundary)
    participant AllocForm as AllocationForm\n(Boundary)
    participant EPC as EstatePlanningControl\n(Control)
    participant AllocDB as InheritanceAllocation Entity\n(Entity)
    participant AssetDB as Asset Entity\n(Entity)
    participant MemberDB as HouseholdMember Entity\n(Entity)

    Investor->>InhPage: Navigate to Inheritance
    InhPage->>EPC: GET /api/v1/estate/allocations {user_id}
    EPC->>AllocDB: Fetch all allocations for user
    EPC->>AssetDB: Fetch all assets with their totals
    EPC->>MemberDB: Fetch household members
    EPC-->>InhPage: AllocationOverview\n{assets with current allocation %, members list}
    InhPage->>Investor: Render allocation matrix

    Investor->>InhPage: Select asset + "Add Allocation"
    InhPage->>AllocForm: Render AllocationForm\n{asset, members, remaining %}

    Investor->>AllocForm: Select member, enter 40%, add conditions
    AllocForm->>EPC: POST /api/v1/estate/allocations\n{asset_id, beneficiary_id, pct: 40, conditions}

    EPC->>AllocDB: calculate_current_total(asset_id)
    AllocDB-->>EPC: currently_allocated: 35%

    Note over EPC: Validate:\n35 + 40 = 75 ≤ 100 ✅

    alt Allocation would exceed 100%
        EPC-->>AllocForm: 422\n{error: "Exceeds 100%. Remaining: X%"}
        AllocForm->>Investor: Show AllocationExceededError\n"Remaining available: X%"
    else Valid allocation
        EPC->>AllocDB: INSERT InheritanceAllocation\n{asset_id, beneficiary_id, pct: 40}
        AllocDB-->>EPC: allocation_id

        EPC->>EPC: calculate_estate_coverage(user_id)
        EPC-->>InhPage: 201 Created\n{allocation_id, updated_coverage_pct}
        InhPage->>Investor: Update allocation display\nShow updated EstateCoveragePct
    end
```

---

## UC-NET-002: Grant Data Consent to an Advisor

```mermaid
sequenceDiagram
    actor Investor
    participant ConxPage as ConnectionsPage\n(Boundary)
    participant ConsentForm as ConsentConfigurationForm\n(Boundary)
    participant CME as ConsentAndMarketplaceEngine\n(Control)
    participant ConnDB as Connection Entity\n(Entity)
    participant DocDB as Document Entity\n(Entity)
    participant Storage as Supabase Storage\n(External)
    actor Advisor

    Investor->>ConxPage: Navigate to Connections → select Advisor → "Manage Data Access"
    ConxPage->>CME: GET /api/v1/connections/{connection_id}/consent
    CME->>ConnDB: Fetch Connection {connection_id}
    ConnDB-->>CME: Connection {status: ACCEPTED, current permissions}
    CME-->>ConxPage: ConsentPayload {current_fields, expiry}
    ConxPage->>ConsentForm: Render ConsentConfigurationForm\nwith available field checklist

    Investor->>ConsentForm: Select fields, enter purpose, set 90-day expiry
    ConsentForm->>CME: PATCH /api/v1/connections/{connection_id}/consent\n{permitted_fields: [...], purpose: "Tax review", expires_at: "2027-01-01"}

    Note over CME: Validate:\nexpires_at > now\nlen(permitted_fields) > 0\npurpose not empty

    alt Expiry date in the past
        CME-->>ConsentForm: 422 {error: "Expiry must be in future"}
        ConsentForm->>Investor: Show validation error
    else No fields selected
        CME-->>ConsentForm: 422 {error: "Select at least one field"}
        ConsentForm->>Investor: Show validation error
    else Valid
        CME->>ConnDB: UPDATE Connection\n{permissions: [...], consent_purpose, consent_granted_at: now, consent_expires_at}
        ConnDB-->>CME: Updated Connection

        Note over CME: Write immutable audit record
        CME->>Storage: Upload ConsentAuditLog JSON
        Storage-->>CME: storage_key
        CME->>DocDB: INSERT Document\n{type: CONSENT_FORM, storage_key}

        CME->>Advisor: Send notification\n"[Investor] granted data access. Expires [date]"
        CME-->>ConsentForm: 200 OK {connection_id, expires_at}
        ConsentForm->>Investor: Show "Access granted until [date]"
    end
```

---

## UC-NET-003: Advisor Accesses Investor Data (Consent Gating)

This is the most security-critical sequence. The Protection Proxy pattern is implemented here.

```mermaid
sequenceDiagram
    actor Advisor
    participant PeersPage as PeersPage\n(Boundary)
    participant CME as ConsentAndMarketplaceEngine\n[Protection Proxy]\n(Control)
    participant ConnDB as Connection Entity\n(Entity)
    participant WOE as WealthAndOwnershipEngine\n(Control)
    participant AssetDB as Asset Entity\n(Entity)

    Advisor->>PeersPage: Navigate to Connected Investor view
    PeersPage->>CME: GET /api/v1/users/{investor_id}/portfolio\n[Authorization: Bearer {advisor_jwt}]

    Note over CME: INTERCEPT every request\nbefore reaching data layer

    CME->>ConnDB: Fetch Connection\n{requester=advisor_id, recipient=investor_id}

    alt No accepted connection exists
        CME-->>PeersPage: 403 Forbidden\n{error: "No connection to this user"}
        PeersPage->>Advisor: Show "Not connected" message
    else Connection is REVOKED
        CME-->>PeersPage: 403 Forbidden\n{error: "Connection revoked"}
    else Connection ACCEPTED but consent expired
        Note over CME: consent_expires_at ≤ now
        CME-->>PeersPage: 403 Forbidden\n{error: "Consent expired. Ask user to renew."}
        PeersPage->>Advisor: Show ConsentExpiredNotice
    else Connection ACCEPTED, consent valid
        CME->>ConnDB: Read permissions list\n["total_net_worth", "real_estate_assets"]
        ConnDB-->>CME: permitted_fields: [...]

        CME->>WOE: get_portfolio_data(investor_id)
        WOE->>AssetDB: Fetch all assets
        AssetDB-->>WOE: Full portfolio payload
        WOE-->>CME: Full portfolio payload

        Note over CME: FILTER payload:\nStrip all fields NOT in permitted_fields\nOnly {total_net_worth, real_estate_assets}\nremain in the response

        CME-->>PeersPage: 200 OK\n{filtered_portfolio_data}
        PeersPage->>Advisor: Render only permitted data
    end
```

---

## UC-ESTATE-003: Log a Gift Transfer

```mermaid
sequenceDiagram
    actor Investor
    participant GTPage as GiftTransferPage\n(Boundary)
    participant GTForm as GiftTransferForm\n(Boundary)
    participant GRE as GiftRuleEngine\n(Control)
    participant EPC as EstatePlanningControl\n(Control)
    participant GiftDB as GiftTransfer Entity\n(Entity)
    participant RuleDB as GiftRule Entity\n(Entity)
    participant AssetDB as Asset Entity\n(Entity)

    Investor->>GTPage: Navigate to Gift Transfer → "New Gift"
    GTPage->>GTForm: Render GiftTransferForm

    Investor->>GTForm: Select asset, select recipient member
    GTForm->>GRE: GET /api/v1/gifts/evaluate\n{asset_id, recipient_member_id}

    GRE->>AssetDB: Fetch asset {pledged_status, asset_type, ownership_pct}
    AssetDB-->>GRE: Asset

    alt Asset is pledged
        GRE-->>GTForm: 400 Bad Request\n{eligibility: BLOCKED, reason: "PLEDGED_ASSET"}
        GTForm->>Investor: Show GiftEligibilityError\n"Cannot gift — asset is pledged"

    else Asset type is restricted (EPF/PPF/ESOP)
        GRE-->>GTForm: 400 Bad Request\n{eligibility: BLOCKED, reason: "ASSET_TYPE_RESTRICTED"}
        GTForm->>Investor: Show GiftEligibilityError\n"This asset type cannot be legally transferred"

    else Asset is eligible
        GRE->>RuleDB: Fetch applicable GiftRule\n{jurisdiction, rule_effective_date}
        RuleDB-->>GRE: GiftRule {exemption_limit, law_reference}
        GRE->>GRE: evaluate_gift_tax_status(donor, recipient, asset)
        GRE->>GRE: calculate_stamp_duty(asset, jurisdiction, relationship)

        GRE-->>GTForm: 200 OK GiftEvaluation\n{tax_status, applicable_rule, stamp_duty,\nregistration_fee, total_transfer_cost, warnings}

        GTForm->>Investor: Show evaluation summary with tax guidance

        Investor->>GTForm: Confirm and submit gift
        GTForm->>GRE: POST /api/v1/gifts {gift_transfer_data}

        GRE->>GiftDB: INSERT GiftTransfer\n{donor_id, recipient_id, asset_id,\ntax_treatment, stamp_duty, status: INITIATED}
        GiftDB-->>GRE: transfer_id

        Note over GRE: Generate checklist:\n☐ Prepare gift deed\n☐ Register with sub-registrar\n☐ Complete mutation\n☐ Update portfolio

        GRE-->>GTForm: 201 Created {transfer_id, checklist}
        GTForm->>GTPage: Navigate to transfer tracker
        GTPage->>Investor: Show Gift Transfer checklist

    end
```

---

## UC-CREDIT-001: Submit a Credit Request (Anonymous Profile)

```mermaid
sequenceDiagram
    actor Investor
    participant CredPage as CreditPage\n(Boundary)
    participant CME as ConsentAndMarketplaceEngine\n(Control)
    participant WOE as WealthAndOwnershipEngine\n(Control)
    participant CFE as CashFlowAndDebtEngine\n(Control)
    participant VVE as ValuationAndVerificationEngine\n(Control)
    participant AssetDB as Asset Entity\n(Entity)
    participant TxnDB as Transaction Entity\n(Entity)

    Investor->>CredPage: Navigate to Credit → "Request Credit"
    Investor->>CredPage: Input: requested_amount, purpose, tenure, security_asset_classes

    CredPage->>CME: POST /api/v1/credit/evaluate {request_data}

    CME->>VVE: get_eligible_security_value(portfolio_id, asset_classes)
    VVE->>AssetDB: Fetch assets with verification_level ≥ DOCUMENTED
    AssetDB-->>VVE: List~VerifiedAsset~
    VVE-->>CME: eligible_security_value_minor_units

    CME->>WOE: calculate_net_worth(portfolio_id) [verified only]
    WOE-->>CME: verified_net_worth_minor_units

    CME->>CFE: calculate_debt_service_ratio(portfolio_id)
    CFE->>TxnDB: Fetch EMI payments and income
    TxnDB-->>CFE: Cashflow data
    CFE-->>CME: debt_service_ratio

    Note over CME: Build anonymous borrower profile:\n- Age band (not exact age)\n- City tier (not city name)\n- Verified net worth band\n- Income type (not amount)\n- Security coverage multiple\n- DSR\n- On-time payment record\nNO: name, PAN, email, phone, employer

    CME->>CME: check_reidentification_risk(borrower_profile)

    alt Re-identification risk is HIGH
        CME-->>CredPage: 200 OK\n{risk_level: HIGH, suggested_removals: [...]}\nwith warning
        CredPage->>Investor: Show re-identification warning\n"Your profile may be identifiable. Remove [field] to improve privacy."
        Investor->>CredPage: Acknowledge risk and confirm OR modify profile
    else Risk is LOW / MEDIUM
        CME-->>CredPage: 200 OK {borrower_profile, matching_lender_count}
        CredPage->>Investor: Show anonymous profile preview + lender count
        Investor->>CredPage: Confirm submission
        CredPage->>CME: POST /api/v1/credit/submit {confirmed_profile}
        CME-->>CredPage: 200 OK {credit_request_id, status: SUBMITTED}
        CredPage->>Investor: "Profile submitted anonymously. Awaiting bids."
    end
```

---

## UC-SETT-001: Export All User Data

```mermaid
sequenceDiagram
    actor Investor
    participant SettPage as SettingsPage\n(Boundary)
    participant ExportJob as DataExportJob\n(Background Worker)
    participant AssetDB as Asset Entity\n(Entity)
    participant TxnDB as Transaction Entity\n(Entity)
    participant EstateDB as EstatePlan Entity\n(Entity)
    participant ConnDB as Connection Entity\n(Entity)
    participant Storage as Supabase Storage\n(External)

    Investor->>SettPage: Navigate to Settings → Privacy → "Export My Data"
    SettPage->>SettPage: Prompt 2FA confirmation (if enabled)
    Investor->>SettPage: Confirm

    SettPage->>ExportJob: POST /api/v1/users/me/export\n[queued background job]
    SettPage-->>Investor: "Export started. You'll receive a notification when it's ready."

    Note over ExportJob: Running asynchronously (Celery task)

    ExportJob->>AssetDB: Fetch all assets
    ExportJob->>TxnDB: Fetch all transactions
    ExportJob->>EstateDB: Fetch estate plan, allocations, gift transfers
    ExportJob->>ConnDB: Fetch all connections + consent logs

    Note over ExportJob: Compile structured JSON:\n{user_profile, portfolio, transactions,\nestate_plan, connections, snapshots}

    ExportJob->>Storage: Upload export JSON (owner: investor, type: USER_EXPORT)
    Storage-->>ExportJob: storage_key

    ExportJob->>Investor: Send notification\n"Your data export is ready. [Download link — valid 60 min]"

    Investor->>SettPage: Click download link
    SettPage->>Storage: Generate signed URL (60 min expiry)
    Storage-->>SettPage: Signed URL
    SettPage->>Investor: Redirect to file download
```

---

## Background Process: Financial Snapshot Capture

This is an internal background workflow, not a direct actor-initiated use case. It runs asynchronously after every portfolio-changing operation.

```mermaid
sequenceDiagram
    participant Trigger as Event Trigger\n(Asset/Liability/Txn write)
    participant CeleryQ as Celery Queue\n(Redis)
    participant SnapWorker as SnapshotWorker\n(Celery Task)
    participant WOE as WealthAndOwnershipEngine\n(Control)
    participant VVE as ValuationAndVerificationEngine\n(Control)
    participant AssetDB as Asset Entity\n(Entity)
    participant SnapDB as FinancialSnapshot Entity\n(Entity)

    Trigger->>CeleryQ: queue_task("capture_snapshot", {portfolio_id})

    Note over CeleryQ: Deduplication: if a snapshot\njob for this portfolio_id is\nalready queued, skip duplicate

    CeleryQ->>SnapWorker: Execute task

    SnapWorker->>WOE: calculate_total_assets(portfolio_id)
    WOE->>AssetDB: Fetch all assets (attributed values)
    AssetDB-->>WOE: List~Asset~
    WOE-->>SnapWorker: total_assets_minor_units

    SnapWorker->>WOE: calculate_asset_class_breakdown(portfolio_id)
    WOE-->>SnapWorker: ClassBreakdown {liquid, real_estate, alternative}

    SnapWorker->>VVE: calculate_verified_wealth_pct(portfolio_id)
    VVE-->>SnapWorker: verified_wealth_minor_units

    Note over SnapWorker: Assemble FinancialSnapshot:\n{total_assets, total_liabilities,\nnet_worth, asset_class_breakdown,\nverified_wealth, as_of: now,\ncalculation_version: "v1.3"}

    SnapWorker->>SnapDB: INSERT FinancialSnapshot\n[Append-only — no UPDATE ever]
    SnapDB-->>SnapWorker: snapshot_id

    Note over SnapWorker: Job complete.\nDashboard next load will\npick up fresh snapshot.

    alt Task fails
        SnapWorker->>CeleryQ: Retry with exponential backoff\n(max 3 attempts)
        Note over SnapWorker: After 3 failures:\nLog ERROR with portfolio_id\nand failure reason
    end
```

---

## Background Process: Consent Expiry Check

```mermaid
sequenceDiagram
    participant Scheduler as Celery Beat Scheduler\n(Every 15 minutes)
    participant ExpiryJob as ConsentExpiryJob\n(Celery Task)
    participant CME as ConsentAndMarketplaceEngine\n(Control)
    participant ConnDB as Connection Entity\n(Entity)
    participant DocDB as Document Entity\n(Entity)
    participant Storage as Supabase Storage\n(External)

    Scheduler->>ExpiryJob: Trigger "expire_stale_consents" every 15 min

    ExpiryJob->>CME: expire_stale_consents()
    CME->>ConnDB: SELECT connections\nWHERE consent_expires_at ≤ NOW()\nAND permissions != '[]'

    loop For each expired connection
        CME->>ConnDB: UPDATE Connection\nSET permissions = '[]'\nconsent_expired_at = NOW()
        ConnDB-->>CME: Updated

        Note over CME: Write immutable expiry audit log
        CME->>Storage: Upload ConsentExpiryLog JSON
        Storage-->>CME: storage_key
        CME->>DocDB: INSERT Document {type: CONSENT_EXPIRY_LOG}

        CME->>CME: Send notification to both\nInvestor (your consent expired)\nAdvisor (access has expired)
    end

    ExpiryJob-->>Scheduler: Task complete\nExpired N consents
```

---

*Next document: [03_Domain_Glossary.md](./03_Domain_Glossary.md)*
