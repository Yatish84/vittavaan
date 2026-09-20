# Domain Glossary

## Identity, people and households

| Term | Canonical definition |
|---|---|
| Authenticated Principal | Vittavaan-local reference to an identity proven by auth-core. It authenticates a caller but does not itself own financial assets. |
| Person | A natural person represented in the ledger. A person may have no login, for example a dependant or minor. |
| Principal–Person Link | Controlled association identifying which person an authenticated principal may act as for self-service purposes. |
| Household | A user-organized grouping of people used for permitted consolidated views. A household is not automatically a legal or tax entity. |
| Household Membership | Effective-dated relationship between a person and household, including role and state. |
| Owner | A person with an economic ownership allocation in a holding. Ownership authority is separate from household administration. |
| Administrator | A person permitted to maintain specified records/processes for others. Administration never implies power to dispose of another owner’s assets. |
| Viewer | A principal/person with an active grant to read a defined scope. |
| Dependant | A person whose financial support is relevant to the household; dependency does not imply ownership or access. |
| Guardian | A person permitted to administer a minor’s specified records under an approved relationship. Majority triggers review, not automatic transfer. |
| Professional | A future CA, advocate, valuer or registered advisor whose credential, engagement, purpose, scope and expiry are separately verified. |

## Authorization and consent

| Term | Canonical definition |
|---|---|
| Access Grant | Explicit, effective-dated authority from a grantor to a grantee over a scope at a defined level and purpose. |
| Scope | The exact household, person, holding, document or field group to which an authorization applies. |
| Access Level | `TOTALS_ONLY`, `READ`, `READ_DOCUMENTS` or `MANAGE`; action-specific ownership rules may still prohibit an operation. |
| Consent | Purpose-bound permission for a specific processing or external disclosure. Consent and household access are related but not interchangeable. |
| Authority Context | The person, role, grant and purpose under which an action is attempted; recorded with material audit evidence. |
| Feature Gate | Disabled-by-default control preventing a capability from operating until product, legal, security, privacy and operational approvals exist. |
| Break Glass | Future exceptional access workflow with named trigger, bounded recipient, delayed/verified release and complete auditing. Not part of beta. |

## Holdings and ownership

| Term | Canonical definition |
|---|---|
| Holding | One canonical record of an owned asset or economic interest. A holding is never duplicated merely because multiple people own it. |
| Asset Class | Stable top-level classification used for policy, aggregation and presentation. |
| Asset Subtype | Versioned classification selecting class-specific attributes and validation. |
| Ownership Allocation | Effective-dated percentage assigning a holding’s economic value to a person. Active allocations total exactly 100%. |
| Attributed Value | Holding value multiplied by a person’s applicable ownership percentage using deterministic fixed-precision rounding. |
| Cost Basis Lot | Acquisition amount/date/quantity for a separable lot, preserved independently from current valuation. |
| Quantity | Decimal amount in the subtype’s unit, such as units, grams, acres, square feet or options. |
| Liquidity Class | Availability category such as same-day, settlement-dated, window-dated, rule-bound, illiquid or no-market. |
| Exit Window | Date/range and restrictions within which a holding may become transferable or realizable. |
| Pledge/Lien | Restriction linking a holding to an obligation or third-party interest. It does not remove ownership but constrains permitted actions. |
| Commitment | Future or contingent funding obligation, such as an AIF drawdown or ESOP exercise cost. It is disclosed but not automatically netted as a liability. |
| Contingent Exposure | Potential obligation, such as a guarantee, shown separately until crystallized under policy. |

## Valuation, source and verification

| Term | Canonical definition |
|---|---|
| Valuation Event | Immutable assertion that a holding had a stated value at an as-of time under a method and source. |
| Valuation Method | How value was established, for example market close, NAV, statement, appraisal, circle rate or owner estimate. |
| Current Valuation | Valuation selected by versioned policy for a scope/as-of request; not a mutable field overwritten on the holding. |
| Source | Origin of a fact: manual, import file, document, institution, depository, registrar, professional or approved reference provider. |
| Provenance | Source IDs, as-of times, calculation/policy versions, verification composition, completeness and lineage supporting a result. |
| Verification Level 1 | Self-declared fact without independent documentary support. |
| Verification Level 2 | Documented fact supported by evidence, not independently verified merely by upload. |
| Verification Level 3 | Fact independently verified or obtained from an approved authoritative source. |
| Verification Level 4 | Verified conduct or professionally attested evidence under an approved policy. |
| Staleness | State where a fact exceeds the class/method-specific age tolerance. Stale facts remain visible as last-known unless policy excludes them. |
| Completeness | Whether required inputs for the requested result and period are present; `PARTIAL` names material omissions. |
| Reconciliation | Process of matching staged/imported facts to canonical records and resolving duplicates/conflicts. |

## Ledger and obligations

| Term | Canonical definition |
|---|---|
| Transaction | Immutable dated economic event classified as external flow, income, expense, buy, sell, debt service, gift or internal transfer. |
| Correcting Entry | New transaction that reverses or adjusts a prior transaction while preserving both records. |
| Internal Transfer | Movement between included accounts/scopes that does not constitute household income or expense. |
| Income Stream | Description and observed receipt history for salary, rent, dividend, coupon, pension, royalty or similar inflow; not automatically a forecast. |
| Liability | Present obligation included in liabilities/net worth under policy. |
| Amortization Schedule | Versioned expected payment/principal/interest schedule derived from explicit terms and reconciled with observed payments. |
| Financial Snapshot | Immutable calculated projection of wealth at a point in time, reproducible from fact and engine versions. |
| Projection | Derived read model optimized for viewing; it is disposable/rebuildable and never the system of record. |

## Performance and planning

| Term | Canonical definition |
|---|---|
| XIRR | Money-weighted annualized return solving discounted dated external cash flows. Withheld if the required cash-flow history is incomplete. |
| TWRR | Time-weighted return geometrically linking sub-period returns to reduce the effect of external cash-flow timing. |
| Benchmark Return | Return from an approved, licensed comparison series for the same relevant period/basis. |
| Attribution Contribution | Portion of total return explained by a class/holding under the approved attribution method; not the same as that class’s standalone return. |
| Performance Basis | Verification/completeness characterization of inputs, such as verified, mixed, estimated, stale or partial. |
| Goal | Versioned target amount/date linked to specific funding holdings and assumptions. |
| Funding Gap | Difference between the inflation-adjusted target and projected available funding under versioned assumptions. |
| Liquidity Mismatch | Funding value unavailable by the goal date because of maturity, lock-in, exit window, pledge or other restriction. |
| Saved Scenario | Immutable calculator inputs, assumptions, exclusions, outputs and engine version retained for later comparison. |
| Life-Event Prompt | Prompt derived only from an explicit dated ledger fact, never an inferred private event. |

## Documents, imports and operations

| Term | Canonical definition |
|---|---|
| Document | Metadata record referencing encrypted object bytes and linked domain records. Folder presentation is derived. |
| Quarantine | Storage/access state before an upload passes malware and policy checks. |
| Supersession | Link from a replacement document/fact to the prior version while preserving history. |
| Import Job | Idempotent workflow that parses a file into staging, validation, reconciliation and confirmed ledger commits. |
| Staged Row | Uncommitted parsed proposal that cannot affect calculations until validated and confirmed. |
| Outbox Event | Transactionally recorded intent to publish domain work after a successful database commit. |
| Audit Evidence | Append-only record of actor, authority, subject, action, purpose, outcome, time and correlation without prohibited secrets/content. |
| Correlation ID | Identifier connecting one request/workflow across API, jobs, events and audit evidence. |
| Calculation Version | Immutable identifier for an engine/policy implementation used to reproduce a derived result. |

## Terms intentionally rejected

- **User-owned asset:** authentication user and financial owner are not interchangeable.
- **Verified badge:** verification is evidence/policy-specific, not a universal guarantee.
- **Current value field:** value is selected from immutable valuation events.
- **Delete transaction:** corrections preserve the historical entry.
- **Household permission:** household membership alone grants no financial visibility.
- **Portfolio return:** ambiguous unless explicitly labelled XIRR, TWRR, benchmark or attribution.

