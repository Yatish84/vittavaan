# Phase 4 — Object Design: Calculation Engine Contracts

> **OOSE Phase:** Object Design
> **Purpose:** Defines the exact mathematical contracts for every calculation engine. This is the implementation blueprint — developers open this file when coding an engine and follow it precisely. Deviating from these contracts without updating this document is a breaking change.
> **Unit convention:** All monetary inputs and outputs are in **paise (minor units)** unless explicitly stated otherwise. All percentages are floats in `[0.0, 100.0]`.
> **Status:** Draft

---

## How to Read This Document

Each engine section defines:

| Field | Meaning |
|---|---|
| **Contract ID** | Stable identifier for this contract version |
| **Preconditions** | What the caller guarantees before calling — the engine may raise if violated |
| **Algorithm** | The precise mathematical formula or procedure |
| **Postconditions** | What the caller can rely on from the return value |
| **Error Codes** | Named error strings returned when computation is impossible |
| **Calculation Version** | Embedded in every output's provenance; increment on any formula change |
| **Edge Cases** | Inputs that require special handling (not errors, but special paths) |

---

## Engine 1 — WealthAndOwnershipEngine

**Contract ID:** `WOE-v1`  
**Calculation Version:** `v1.0`  
**Module:** `backend/app/services/wealth_engine.py`

### 1.1 `calculate_attributed_value(asset)`

**Purpose:** Compute the owner's economic interest in a single asset.

$$\text{AttributedValue} = \left\lfloor \text{GrossValue} \times \frac{\text{ownershipPct}}{100} \right\rfloor$$

Where:
- $\text{GrossValue}$ = `asset.current_value_minor_units` (integer, paise)
- $\text{ownershipPct}$ = `asset.ownership_split_pct` (float, 0.0–100.0)
- $\lfloor \cdot \rfloor$ = integer floor (never round up — never report more than you own)

**Preconditions:**
- `current_value_minor_units >= 0`
- `0.0 <= ownership_split_pct <= 100.0`
- `is_active == True`

**Postconditions:**
- Return type: `int` (paise), always `>= 0`
- Result is always `<= current_value_minor_units`

**Error Codes:** None — this operation always produces a valid result given valid preconditions.

**Edge Cases:**
- `ownership_split_pct = 0.0` → returns `0` (user has a record of the asset but no economic interest)
- `ownership_split_pct = 100.0` → returns `current_value_minor_units` exactly

---

### 1.2 `calculate_net_worth(portfolio_id, *, as_of=None)`

$$\text{NetWorth} = \sum_{a \in \text{ActiveAssets}} \text{AttributedValue}(a) - \sum_{l \in \text{ActiveLiabilities}} l.\text{currentBalance}$$

**Preconditions:**
- Portfolio must exist
- All `current_value_minor_units` must be `>= 0`

**Postconditions:**
- Return type: `NetWorthResult` with fields:
  - `total_assets_minor_units: int` (always `>= 0`)
  - `total_liabilities_minor_units: int` (always `>= 0`)
  - `net_worth_minor_units: int` (may be negative if liabilities exceed assets)
  - `provenance: ProvenanceMetadata`
- `net_worth = total_assets - total_liabilities` — callers can rely on this identity exactly

**Error Codes:**
- `PORTFOLIO_NOT_FOUND` — no portfolio for this `portfolio_id`

**Edge Cases:**
- Empty portfolio (no assets, no liabilities) → returns `{total_assets: 0, total_liabilities: 0, net_worth: 0}`
- All assets stale → result is returned with `provenance.is_partial = True` and `provenance.performance_basis = "ESTIMATED"`

---

### 1.3 `calculate_asset_class_breakdown(portfolio_id)`

$$\text{LiquidPct} = \frac{\sum_{a \in \text{LIQUID}} \text{AttributedValue}(a)}{\text{TotalAssets}} \times 100$$

$$\text{RealEstatePct} = \frac{\sum_{a \in \text{REAL\_ESTATE}} \text{AttributedValue}(a)}{\text{TotalAssets}} \times 100$$

$$\text{AlternativePct} = 100 - \text{LiquidPct} - \text{RealEstatePct}$$

**Postconditions:**
- `liquid_pct + real_estate_pct + alternative_pct == 100.0` (within floating-point tolerance of `1e-6`)
- Each percentage is in `[0.0, 100.0]`

**Edge Cases:**
- `TotalAssets == 0` → all percentages are `0.0`, no division; `is_partial = True`

---

### 1.4 `calculate_net_worth_waterfall(portfolio_id, period)`

Produces the month-over-month breakdown of net worth change into its components.

$$\Delta\text{NetWorth} = \Delta\text{Liquid} + \Delta\text{RealEstate} + \Delta\text{Alternative} + \Delta\text{Liabilities} + \text{OtherAdjustments}$$

Where each $\Delta$ = `current_attributed_value - prior_period_attributed_value`.

**Preconditions:**
- At least two `FinancialSnapshot` records exist for this portfolio spanning `period`

**Postconditions:**
- Sum of all waterfall bar values equals `net_worth_current - net_worth_prior` exactly (reconciles perfectly)
- Each bar value may be positive (gain) or negative (loss/increase in debt)

**Error Codes:**
- `INSUFFICIENT_HISTORY` — fewer than 2 snapshots exist for the requested period

---

### 1.5 `calculate_household_net_worth(user_id)`

$$\text{HouseholdNetWorth} = \text{UserNetWorth} + \sum_{m \in \text{Members}} \text{SharedAssetAttributed}(m)$$

**Note:** Joint assets are counted **once** (attributed to the user's ownership percentage). Assets fully owned by a member that the user has declared are counted once at the member's declared share. No double-counting.

**Preconditions:**
- V1: Household net worth is computed from the user's own portfolio only (household member portfolios are not linked in V1; this is V2 scope). The method exists but returns `user_net_worth` until V2.

---

## Engine 2 — ValuationAndVerificationEngine

**Contract ID:** `VVE-v1`  
**Calculation Version:** `v1.0`  
**Module:** `backend/app/services/valuation_engine.py`

### 2.1 `calculate_verified_wealth_pct(portfolio_id)`

$$\text{VerifiedWealthPct} = \frac{\sum_{a : \text{level} \geq \text{DOCUMENTED}} \text{AttributedValue}(a)}{\text{TotalAttributedAssets}} \times 100$$

Where verification levels are ordered: `SELF_DECLARED (0) < DOCUMENTED (1) < VERIFIED (2) < ACCEPTED (3)`.  
"Verified" for this metric means level $\geq 1$ (DOCUMENTED or above).

**Postconditions:**
- Result is in `[0.0, 100.0]`
- `0.0` if all assets are `SELF_DECLARED`
- `100.0` if all assets are `DOCUMENTED` or above

**Edge Cases:**
- `TotalAttributedAssets == 0` → returns `0.0` with `is_partial = True`

---

### 2.2 `check_staleness(asset)`

$$\text{ValuationAgeDays} = \left\lfloor \frac{\text{Now} - \text{asset.valuation\_as\_of}}{\text{1 day}} \right\rfloor$$

Staleness classification by `ValuationAgeDays` against per-asset-type thresholds (stored in config, not hardcoded):

| Asset Sub-type | `APPROACHING_STALE` | `STALE` |
|---|---|---|
| `BANK_SAVINGS`, `BANK_FD` | ≥ 180 days | ≥ 365 days |
| `EQUITY`, `MUTUAL_FUND`, `ETF` | ≥ 30 days | ≥ 60 days |
| `CRYPTO` | ≥ 7 days | ≥ 30 days |
| `BONDS`, `NPS`, `PPF`, `EPF` | ≥ 90 days | ≥ 180 days |
| `REAL_ESTATE` (all types) | ≥ 180 days | ≥ 365 days |
| `ALTERNATIVE` (all types) | ≥ 180 days | ≥ 365 days |

**Postconditions:**
- Returns `StalenessResult {status: StalenessStatusEnum, valuation_age_days: int, threshold_warning: int, threshold_stale: int}`

**Edge Cases:**
- `valuation_as_of` is `null` (asset created without explicit valuation date) → treat as stale immediately (`status = STALE`, `valuation_age_days = ∞`)
- Newly created asset with `valuation_as_of = now()` → `CURRENT`

---

### 2.3 `evaluate_verification_level(asset, documents)`

Given an asset and its linked documents, return the highest achievable verification level:

```
SELF_DECLARED (default)
  → if len(relevant_docs) > 0 and any doc.scan_status == "CLEAN":
      DOCUMENTED
      → if any doc.document_type in PROFESSIONAL_VALUATION_TYPES:
          VERIFIED
          → if admin has reviewed and approved:
              ACCEPTED
```

Where `PROFESSIONAL_VALUATION_TYPES = {VALUATION_REPORT, APPRAISAL_REPORT}`.

**Note:** This method does not UPDATE the asset — it returns the level the asset is entitled to. The API endpoint calls this and updates `asset.verification_level` if it has changed.

---

## Engine 3 — CashFlowAndDebtEngine

**Contract ID:** `CFE-v1`  
**Calculation Version:** `v1.0`  
**Module:** `backend/app/services/cashflow_engine.py`

### 3.1 `calculate_monthly_surplus(portfolio_id, month)`

$$\text{Surplus} = \sum_{t \in \text{INFLOW}} t.\text{amount} - \sum_{t \in \text{OUTFLOW}} t.\text{amount} - \sum_{t \in \text{EMI\_PAYMENT}} t.\text{amount}$$

Where the sum is over all transactions in the given calendar month with `transaction_date` in `[first_day_of_month, last_day_of_month]`.

**Postconditions:**
- `surplus_minor_units: int` — may be negative (spending exceeded income)
- `income_minor_units: int` — always `>= 0`
- `expenses_minor_units: int` — always `>= 0`
- `savings_rate_pct: float` — `(surplus / income) × 100` if `income > 0`, else `null`

**Edge Cases:**
- Month with no transactions → all values `0`, `savings_rate_pct = null`
- Month with only outflows (no income) → `surplus < 0`, `savings_rate_pct = null`

---

### 3.2 `calculate_debt_service_ratio(portfolio_id)`

$$\text{DSR} = \frac{\sum_{l \in \text{ActiveLiabilities}} l.\text{monthlyEMI}}{\text{MonthlyGrossIncome}} \times 100$$

Where:
- `monthlyEMI` for each liability = derived from `current_balance`, `interest_rate`, `remaining_tenure_months` using the reducing-balance EMI formula (see 3.4 below)
- `MonthlyGrossIncome` = average monthly INFLOW over the last 3 full months

**Postconditions:**
- `dsr_pct: float` in `[0.0, ∞)` (theoretically unbounded above 100)
- Risk classification: `{LOW: DSR < 30, MEDIUM: 30 ≤ DSR < 50, HIGH: DSR ≥ 50}`

**Error Codes:**
- `NO_INCOME_DATA` — no INFLOW transactions in last 3 months; cannot compute DSR

---

### 3.3 `calculate_savings_rate(portfolio_id, period)`

$$\text{SavingsRate} = \frac{\text{TotalSurplus}}{\text{TotalIncome}} \times 100$$

Where totals are over the entire `period` (not monthly averages).

**Edge Cases:**
- `TotalIncome == 0` → returns `null` with `error: NO_INCOME_DATA`
- Negative surplus (spent more than earned) → returns negative savings rate (valid, not an error)

---

### 3.4 `calculate_amortization_schedule(liability)`

Uses the **standard Indian reducing-balance (flat-rate) EMI formula**:

$$\text{EMI} = \frac{P \cdot r \cdot (1+r)^n}{(1+r)^n - 1}$$

Where:
- $P$ = `current_balance_minor_units` (outstanding principal in paise)
- $r$ = `interest_rate / 100 / 12` (monthly rate as decimal)
- $n$ = `remaining_tenure_months`

Each period row:
$$\text{InterestComponent}_k = \text{OpeningBalance}_k \times r$$
$$\text{PrincipalComponent}_k = \text{EMI} - \text{InterestComponent}_k$$
$$\text{ClosingBalance}_k = \text{OpeningBalance}_k - \text{PrincipalComponent}_k$$

**Postconditions:**
- Schedule rows: exactly `remaining_tenure_months` entries
- `ClosingBalance` of last row = 0 (within ±1 paise rounding)
- All values in paise (integer floor per row)

**Edge Cases:**
- `interest_rate == 0.0` → EMI = `P / n` exactly; no interest component
- Floating-rate loan (`rate_type = FLOATING`) → schedule is indicative only; first row uses current rate with a `is_indicative: True` flag

---

## Engine 4 — PerformanceAndAttributionEngine

**Contract ID:** `PAE-v1`  
**Calculation Version:** `v1.0`  
**Module:** `backend/app/services/performance_engine.py`

### 4.1 `calculate_xirr(portfolio_id, start, end)`

**Definition:** XIRR is the rate $r$ such that:

$$\sum_{k=0}^{n} \frac{C_k}{(1+r)^{d_k}} = 0$$

Where:
- $C_k$ = cash flow amount at event $k$ (positive for inflows, negative for outflows/investments made)
- $d_k$ = $(t_k - t_0)$ in fractional years (using Actual/365 day count convention)
- $C_0$ = negative of the portfolio value at `start` (initial investment equivalent)
- $C_n$ = portfolio value at `end` (terminal value, positive)
- All intermediate cash flows from `Transaction` records

**Solver:** Brent's method (guaranteed convergence for continuous functions on a bracketed interval). Bracket: search in $r \in (-0.9999, 100.0)$.

```python
# Pseudocode
def _solve_xirr(cashflows: list[tuple[date, int]]) -> float:
    def npv(r: float) -> float:
        t0 = cashflows[0][0]
        return sum(
            c / (1 + r) ** ((t - t0).days / 365)
            for t, c in cashflows
        )
    return brentq(npv, a=-0.9999, b=100.0, xtol=1e-6, maxiter=1000)
```

**Preconditions:**
- At least 2 cash flow events (including start and end portfolio values)
- Terminal portfolio value must be known (i.e., at least one `FinancialSnapshot` exists at or near `end`)

**Postconditions:**
- `xirr_pct: float | None` — annualised rate as percentage (e.g., `14.2` = 14.2% p.a.)
- `provenance.performance_basis: PerformanceBasisEnum` — derived from asset verification levels

**Error Codes:**
- `INSUFFICIENT_DATA` — fewer than 2 events; no XIRR possible
- `NO_SNAPSHOT_AT_PERIOD_END` — cannot establish terminal value
- `CONVERGENCE_FAILED` — Brent's method did not converge within tolerance

**Edge Cases:**
- Portfolio with only one transaction (initial purchase, no subsequent events) → `INSUFFICIENT_DATA`
- All transactions in a single day → degenerate case; `CONVERGENCE_FAILED`
- Very high intra-period returns (>10,000%) → may produce multiple roots; Brent's method uses narrower bracket, returns first positive root

---

### 4.2 `calculate_twrr(portfolio_id, start, end)`

**Definition:** TWRR links sub-period returns geometrically, eliminating cash flow timing effects:

$$\text{TWRR} = \left[\prod_{k=1}^{n} (1 + r_k)\right] - 1$$

Where each sub-period return $r_k$ is bounded by an external cash flow event:

$$r_k = \frac{E_k - B_k - C_k}{B_k}$$

Where:
- $B_k$ = portfolio value at beginning of sub-period $k$ (after previous cash flow)
- $E_k$ = portfolio value at end of sub-period $k$ (just before next cash flow)
- $C_k$ = net external cash flow during sub-period $k$ (positive for inflows)

**Sub-period boundary events:** Every `BUY`, `SELL`, `INFLOW`, `OUTFLOW` transaction creates a boundary. Between boundaries, portfolio value changes due to market movement only (no cash flows).

**Preconditions:**
- `FinancialSnapshot` exists at `start`, `end`, and near every external cash flow date (within ±1 day)
- At least 1 sub-period exists

**Postconditions:**
- `twrr_pct: float | None` — annualised using: $\text{TWRRAnnualised} = (1 + \text{TWRR})^{365/N} - 1$ where $N$ = number of days in period
- `sub_period_count: int` — number of sub-periods computed

**Error Codes:**
- `INSUFFICIENT_SNAPSHOTS` — snapshots missing at key dates; TWRR cannot be computed without them
- `ZERO_BEGINNING_VALUE` — $B_k = 0$ for some sub-period (division by zero); skip that sub-period and flag `is_partial = True`

---

### 4.3 `calculate_max_drawdown(portfolio_id, period)`

$$\text{MaxDrawdown} = \min_{t_{\text{trough}} > t_{\text{peak}}} \frac{V_{t_{\text{trough}}} - V_{t_{\text{peak}}}}{V_{t_{\text{peak}}}} \times 100$$

Where $V_t$ = `net_worth_minor_units` from `FinancialSnapshot` at date $t$.

Algorithm: running-peak method over the sequence of snapshots in chronological order.

```python
peak = snapshots[0].net_worth
max_drawdown = 0.0
peak_date = snapshots[0].snapshot_date
trough_date = None

for snap in snapshots[1:]:
    if snap.net_worth > peak:
        peak = snap.net_worth
        peak_date = snap.snapshot_date
    drawdown = (snap.net_worth - peak) / peak * 100
    if drawdown < max_drawdown:
        max_drawdown = drawdown
        trough_date = snap.snapshot_date
```

**Postconditions:**
- `max_drawdown_pct: float` — always `<= 0.0` (a drawdown is a loss)
- `drawdown_start_date: date` — the peak date
- `drawdown_trough_date: date | None` — the trough date (None if no drawdown occurred)
- `recovery_months: int | None` — months from trough until portfolio regained peak (None if not yet recovered)

**Edge Cases:**
- Monotonically increasing portfolio → `max_drawdown_pct = 0.0`, no trough
- Fewer than 2 snapshots → `max_drawdown_pct = 0.0`, `is_partial = True`

---

### 4.4 `calculate_attribution(portfolio_id, period)`

Return attribution of total portfolio return to each asset class:

$$\text{Contribution}_{\text{class}} = \bar{w}_{\text{class}} \times r_{\text{class}}$$

Where:
- $\bar{w}_{\text{class}}$ = average weight of the class in portfolio over the period (average of begin and end weights)
- $r_{\text{class}}$ = return of the class over the period = $(\text{EndValue}_{\text{class}} - \text{BeginValue}_{\text{class}} - \text{NetFlows}_{\text{class}}) / \text{BeginValue}_{\text{class}}$

**Reconciliation check (mandatory):**
$$\sum_{\text{class}} \text{Contribution}_{\text{class}} \approx \text{TotalPortfolioReturn}$$

If the sum diverges by more than 0.1%, log a warning and set `is_partial = True`.

---

## Engine 5 — PlanningAndScenarioEngine

**Contract ID:** `PSE-v1`  
**Calculation Version:** `v1.0`  
**Module:** `backend/app/services/planning_engine.py`

### 5.1 `calculate_goal_projected_value(goal, assumptions)`

$$\text{ProjectedValue} = \sum_{a \in \text{LinkedAssets}} \text{AttributedValue}(a) \times (1 + g_a)^{Y}$$

Where:
- $Y$ = `goal.target_year - current_year` (years to target)
- $g_a$ = assumed annual growth rate for asset $a$ (from `assumptions.asset_growth_rates`, asset-class default if not specified)
- Default growth assumptions (configurable, not hardcoded):
  - Equity/MF: 12% p.a.
  - Real Estate: 8% p.a.
  - Alternative: 6% p.a.
  - Debt/FD: 7% p.a.

**Postconditions:**
- `projected_value_minor_units: int` — future nominal value of earmarked assets
- `assumptions_used: dict` — full record of growth rates used (for transparency)

---

### 5.2 `calculate_funding_gap(goal, assumptions)`

$$\text{TargetNominal} = \text{goal.target\_amount\_minor\_units} \times (1 + \text{goal.inflation\_assumption\_pct}/100)^Y$$

$$\text{FundingGap} = \text{TargetNominal} - \text{ProjectedValue}$$

$$\text{GoalStatus} = \begin{cases} \text{FUNDED} & \text{if } \text{FundingGap} \leq 0 \\ \text{ON\_TRACK} & \text{if } 0 < \text{FundingGap} \leq 0.10 \times \text{TargetNominal} \\ \text{SHORT} & \text{if } 0.10 < \text{FundingGap} \leq 0.30 \times \text{TargetNominal} \\ \text{AT\_RISK} & \text{if } \text{FundingGap} > 0.30 \times \text{TargetNominal} \end{cases}$$

**Postconditions:**
- `target_nominal_minor_units: int` — what the goal costs in future money
- `funding_gap_minor_units: int` — negative means overfunded
- `goal_status: GoalStatusEnum`
- `years_to_target: int`

---

### 5.3 `model_invest_vs_prepay(params)`

**Invest scenario** — surplus invested at assumed return $r_i$ for $n$ months:

$$\text{FV}_{\text{invest}} = \text{surplus} \times \frac{(1 + r_i/12)^n - 1}{r_i/12} \times (1 + r_i/12)$$

(standard SIP future value formula)

**Prepay scenario** — surplus used to reduce loan principal; interest saved computed on accelerated amortization:

$$\text{InterestSaved} = \text{TotalInterest}_{\text{original}} - \text{TotalInterest}_{\text{accelerated}}$$

**Crossover return** — the $r_c$ where $\text{FV}_{\text{invest}}(r_c) = \text{InterestSaved}$. Solved numerically with Brent's method.

**Postconditions:**
- `invest_terminal_value_minor_units: int`
- `prepay_interest_saved_minor_units: int`
- `crossover_return_pct: float` — annual rate at which both options break even
- `recommended: Literal["INVEST", "PREPAY", "NEUTRAL"]` — based on user's assumed return vs. crossover

**Preconditions:**
- `loan_interest_rate > 0`
- `remaining_tenure_months > 0`
- `monthly_surplus_minor_units > 0`

---

## Engine 6 — ConsentAndMarketplaceEngine

**Contract ID:** `CME-v1`  
**Calculation Version:** `v1.0`  
**Module:** `backend/app/services/consent_engine.py`

### 6.1 `evaluate_data_access(requesting_user_id, data_owner_id, data_field)`

Three-gate sequential evaluation (fail fast):

```
Gate 1: Connection exists and status == ACCEPTED
  → FAIL → AccessDecision(allowed=False, reason="NO_CONNECTION")

Gate 2: consent_expires_at is null OR consent_expires_at > now()
  → FAIL → AccessDecision(allowed=False, reason="CONSENT_EXPIRED")

Gate 3: data_field in connection.permissions
  → FAIL → AccessDecision(allowed=False, reason="FIELD_NOT_PERMITTED")

PASS → AccessDecision(allowed=True, reason="CONSENT_VALID", permitted_fields=[...])
```

**Postconditions:**
- This method is DETERMINISTIC for a given point in time — same inputs always produce same output
- NEVER raises an exception — always returns an `AccessDecision`
- Logging: every access evaluation is logged at DEBUG level; every DENY is logged at INFO level

---

### 6.2 `check_reidentification_risk(borrower_profile)`

Scoring model — sum of specificity weights for each disclosed attribute:

| Attribute Disclosed | Risk Weight |
|---|---|
| Age band (10-year) | +1 |
| City tier (1/2/3) | +1 |
| Income type | +1 |
| Net worth band (₹1Cr wide) | +2 |
| Net worth band (₹25L wide) | +4 |
| Specific asset class disclosed | +1 per class |
| DSR (rounded to nearest 5%) | +1 |
| Exact security assets disclosed | +3 |

$$\text{RiskScore} = \sum \text{weights of disclosed attributes}$$

$$\text{RiskLevel} = \begin{cases} \text{LOW} & \text{if score} \leq 4 \\ \text{MEDIUM} & \text{if } 5 \leq \text{score} \leq 8 \\ \text{HIGH} & \text{if score} \geq 9 \end{cases}$$

**Important:** This is a heuristic model, not a statistical uniqueness test. It errs on the side of privacy protection.

---

### 6.3 `evaluate_advisor_match(user_id, advisors)`

For each advisor, compute a relevance score against the user's portfolio:

```
score = 0
for each specialty in advisor.specialty_areas:
    if specialty matches user's portfolio characteristics:
        score += SPECIALTY_WEIGHT[specialty]

match_reason = top matching specialty + user's relevant holding
```

`SPECIALTY_WEIGHT` is a configurable dict; advisors with zero relevance score are excluded from results.

**Postconditions:**
- Results sorted by score descending
- `match_reason` is always a plain-language string explaining the match (e.g., "Specialises in real estate taxation — you hold 2 properties")

---

## Engine 7 — EstatePlanningControl

**Contract ID:** `EPC-v1`  
**Calculation Version:** `v1.0`  
**Module:** `backend/app/services/estate_engine.py`

### 7.1 `calculate_estate_coverage(user_id)`

$$\text{EstateCoveragePct} = \frac{\sum_{\text{allocations}} (\text{asset.AttributedValue} \times \text{allocation.percentage\_share} / 100)}{\text{TotalAttributedNetWorth}} \times 100$$

**Postconditions:**
- `estate_coverage_pct: float` in `[0.0, 100.0]` (cannot exceed 100% by DB constraint)
- `covered_value_minor_units: int`
- `uncovered_value_minor_units: int`
- `uncovered_value_pct: float` = `100.0 - estate_coverage_pct`

---

### 7.2 `get_default_succession_shares(user_id)`

Returns the HSA Class I default intestacy shares for the user's family structure.

**HSA Class I Heirs (if all alive):**

| Relationship | Share |
|---|---|
| Spouse | Equal share with children + 1 additional share |
| Each child (son or daughter equally since 2005) | 1 share |
| Mother | 1 share |

Formula: `each_share = 1 / (1 + num_children + 1_if_mother_alive)` for spouse, with adjustments per HSA Schedule.

**Simplification for V1:** Returns a human-readable description of default shares, not a legally precise computation. Labelled clearly as "indicative default — consult a legal advisor".

---

### 7.3 `identify_nominee_mismatches(user_id)`

A mismatch exists when a household member designated as a beneficiary in an `InheritanceAllocation` is NOT the registered nominee on the corresponding financial instrument.

**V1 scope:** Mismatches are flagged for **liquid assets only** (where nominee registration is common — MF, insurance, bank). Real estate does not have nominees.

**Postconditions:**
- `List[NomineeMismatch]` — each with `asset_id`, `asset_name`, `intended_beneficiary`, `registered_nominee`, `warning_text`
- Empty list = no mismatches detected (or no nominee information logged)

---

## Engine 8 — PeerBenchmarkingControl

**Contract ID:** `PBC-v1`  
**Calculation Version:** `v1.0`  
**Module:** `backend/app/services/peer_engine.py`

### 8.1 `generate_cohort_benchmark(user_id, metric_type)`

**Cohort definition criteria:**
- `city_tier` (same tier as user)
- `age_band` (10-year band: 25–34, 35–44, 45–54, 55–64, 65+)
- `risk_tolerance` (±1 level from user's tolerance)

**Minimum cohort size:** 10 users. If fewer than 10 qualify, do not generate a benchmark — return `{error: "COHORT_TOO_SMALL"}`.

**Benchmark metrics computed:**

| metric_type | Formula |
|---|---|
| `NET_WORTH` | `median(net_worth_minor_units)` of cohort |
| `EQUITY_ALLOCATION` | `mean(liquid_pct)` of cohort |
| `SAVINGS_RATE` | `mean(savings_rate_pct)` of cohort |
| `DSR` | `mean(dsr_pct)` of cohort |
| `VERIFIED_WEALTH_PCT` | `mean(verified_wealth_pct)` of cohort |

**Why median for net worth?** Net worth distributions are heavily right-skewed (a few very high values pull the mean). Median is more representative of a "typical peer".

**Postconditions:**
- `cohort_size: int` (always `>= 10`)
- `user_metric_value: float`
- `cohort_benchmark_value: float`
- `percentile_rank: int` in `[1, 99]` — user's percentile within cohort (never 0th or 100th to avoid revealing extreme values)
- `generated_at: datetime`

**Error Codes:**
- `COHORT_TOO_SMALL` — fewer than 10 matching users

---

## Appendix: Common Return Types

```python
# Shared across all engines
@dataclass
class ProvenanceMetadata:
    as_of: datetime
    calculation_version: str
    source_ids: list[UUID]
    is_partial: bool
    performance_basis: PerformanceBasisEnum | None = None

@dataclass
class NetWorthResult:
    total_assets_minor_units: int
    total_liabilities_minor_units: int
    net_worth_minor_units: int
    provenance: ProvenanceMetadata

@dataclass
class StalenessResult:
    status: StalenessStatusEnum  # CURRENT | APPROACHING_STALE | STALE
    valuation_age_days: int
    threshold_warning_days: int
    threshold_stale_days: int

@dataclass
class AccessDecision:
    allowed: bool
    reason: str  # "CONSENT_VALID" | "NO_CONNECTION" | "CONSENT_EXPIRED" | "FIELD_NOT_PERMITTED"
    permitted_fields: list[str]

@dataclass
class FundingGapResult:
    target_today_minor_units: int
    target_nominal_minor_units: int
    projected_value_minor_units: int
    funding_gap_minor_units: int
    goal_status: GoalStatusEnum
    years_to_target: int
    assumptions_used: dict
    provenance: ProvenanceMetadata

@dataclass
class XirrResult:
    xirr_pct: float | None
    error_code: str | None
    cashflow_count: int
    provenance: ProvenanceMetadata

@dataclass
class TwrrResult:
    twrr_pct: float | None
    twrr_annualised_pct: float | None
    sub_period_count: int
    error_code: str | None
    provenance: ProvenanceMetadata
```

---

*Next: [02_Design_Patterns.md](./02_Design_Patterns.md)*
