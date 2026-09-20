# Calculation Contracts

## Common contract

Every engine validates input sufficiency, calculates with `Decimal`/integer arithmetic, reconciles components, applies one documented rounding point, and returns provenance plus named failures. It never substitutes zero for missing data.

## Attributed value and wealth

For valuation `V` in minor units and ownership percentage `p`:

\[
A = \operatorname{round}_{policy}\left(V \times \frac{p}{100}\right)
\]

Allocation rounding uses largest remainder so attributed parts reconcile exactly to `V`:

1. Calculate unrounded shares at high precision.
2. Floor each to minor units.
3. Distribute remaining minor units in descending fractional-remainder order, with stable person-ID tie-break.

\[
\text{NetWorth} = \sum A_{included\ assets} - \sum A_{included\ direct\ liabilities}
\]

Contingent liabilities and undrawn commitments are disclosed separately unless policy marks them crystallized/included.

**Failures:** `NO_APPLICABLE_VALUATION`, `OWNERSHIP_SCHEDULE_INVALID`, `FX_RATE_MISSING`, `VALUATION_POLICY_CONFLICT`. Partial aggregates must name omissions.

## Verified wealth

\[
\text{VerifiedWealthPct} =
\frac{\sum A_{assets\ meeting\ verified\ policy}}
{\sum A_{included\ assets}} \times 100
\]

The denominator is attributed assets, not net worth, avoiding distortion from liabilities. The UI must label the denominator. A separate verified net-worth figure may be shown only with an explicitly defined liability-verification policy.

## Movement reconciliation

\[
\Delta NW = NW_{end} - NW_{start}
\]

Components distinguish external contributions/withdrawals, earned income/expense where used, realized/unrealized valuation change, ownership-scope change, liability drawdown/repayment and FX effect. Internal transfers contribute zero at consolidated scope.

\[
Residual = \Delta NW - \sum Components
\]

Residual must equal zero after minor-unit rounding or appear as `UNRECONCILED` with the exact amount; it is never hidden in “other.”

## Cash flow and debt

\[
Surplus = ExternalInflows + Income - Expenses - DebtPayments - ExternalOutflows
\]

Internal transfers are excluded. Savings-rate denominator policy must be displayed:

\[
SavingsRate = \frac{Surplus}{IncomeBase} \times 100
\]

If `IncomeBase <= 0`, return `INCOME_BASE_NOT_POSITIVE` rather than infinity/zero.

\[
DSR = \frac{MonthlyDebtService}{MonthlyGrossIncome} \times 100
\]

For reducing-balance EMI with principal `P`, monthly rate `r`, periods `n`:

\[
EMI = P \times \frac{r(1+r)^n}{(1+r)^n-1}
\]

For zero rate, `EMI = P/n`. Final payment absorbs rounding so closing principal is exactly zero.

## XIRR

With dated external cash flows `C_i`, dates `d_i`, base date `d_0`:

\[
0 = \sum_i \frac{C_i}{(1+r)^{(d_i-d_0)/365}}
\]

Sign convention is from investor perspective: contributions negative; withdrawals/income received and terminal value positive. Requirements:

- At least one negative and one positive cash flow.
- Complete cash-flow history for requested scope/period.
- Terminal market value represented at period end where method requires it.
- Solve using a bracketed method such as Brent; deterministic search bounds/tolerance/version.
- Multiple roots return `AMBIGUOUS_MULTIPLE_ROOTS` unless approved selection policy exists.

**Failures:** `INSUFFICIENT_CASH_FLOWS`, `INCOMPLETE_HISTORY`, `NO_SIGN_CHANGE`, `CONVERGENCE_FAILED`, `AMBIGUOUS_MULTIPLE_ROOTS`.

## TWRR

For each subperiod bounded by external cash flows:

\[
r_i = \frac{E_i - B_i - CF_i}{B_i}
\]

where cash-flow timing convention is fixed by engine version. Geometric link:

\[
TWRR = \prod_{i=1}^{n}(1+r_i)-1
\]

Missing boundary valuations return `INSUFFICIENT_BOUNDARY_VALUATIONS`; never interpolate silently.

## Attribution

Default Brinson-like class contribution for period `i`:

\[
Contribution_k = AverageWeight_k \times Return_k
\]

All contributions and explicitly defined interaction/residual components reconcile to displayed portfolio TWRR under the method version. The output separately reports class return, weight, contribution percentage and rupee movement to prevent semantic confusion.

## Maximum drawdown

For value series `V_t`, running peak `P_t = max(V_0...V_t)`:

\[
Drawdown_t = \frac{V_t-P_t}{P_t}
\]

Return minimum drawdown, peak date, trough date and recovery date/ongoing state. Non-positive peak yields a named unsupported state.

## Goal projection

Inflation-adjusted target after `Y` years:

\[
TargetNominal = TargetToday \times (1+i)^Y
\]

Each linked holding is projected under its explicit class/holding assumption and contribution schedule. No hidden defaults; configured defaults are copied into the saved scenario.

\[
FundingGap = TargetNominal - ProjectedAvailableValue
\]

`ProjectedAvailableValue` excludes or separately reports value unavailable by the target date. Result includes amount status and liquidity status independently.

## Invest versus prepay

Compare cash flows over the same horizon:

- Prepay path: interest/principal schedule avoided, charges and tax treatment included only when explicitly provided.
- Invest path: projected investment cash flows at visible assumed return, fees/tax only if supplied.
- Crossover rate solves equality of end position/NPV under one versioned timing convention.

The result never labels a recommendation. It reports assumptions, exclusions, both paths, difference and crossover.

## FX conversion

For money `M` and approved rate `R(base→display)`:

\[
ConvertedMinorUnits = round_{currency}\left(M \times R\right)
\]

Rate selection uses nearest policy-permitted rate at or before financial as-of, with source/licence and age. No current rate may rewrite historical calculations. Missing/too-stale rate produces omission/failure.

## Calculation error vocabulary

`INSUFFICIENT_DATA`, `INCOMPLETE_HISTORY`, `NO_APPLICABLE_VALUATION`, `STALE_INPUT_EXCLUDED`, `FX_RATE_MISSING`, `BENCHMARK_UNAVAILABLE`, `LICENSE_RESTRICTED`, `NO_SIGN_CHANGE`, `CONVERGENCE_FAILED`, `AMBIGUOUS_MULTIPLE_ROOTS`, `RECONCILIATION_FAILED`, `POLICY_CONFLICT`, `UNSUPPORTED_NON_POSITIVE_BASE`.

