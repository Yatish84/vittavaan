# Test Personas and Golden Scenarios

All names/data are synthetic.

## P1 — New individual investor

One owner, INR cash/FD/equity/mutual fund, one home loan, short history and manual/CSV data. Exercises first run, imports, duplicates, cash flow, insufficient XIRR and basic goal planning.

## P2 — Joint complex household

Two adults, two minors and one dependant parent; jointly owned property, individual securities, ESOPs, NPS/SSY, AIF commitment, gold/collectible, mortgage/LAS and internal transfers. Exercises shared holding attribution, guardian/admin limits, liquidity, look-through, partial verification and goal mismatch.

## P3 — Data-quality stress household

Stale property appraisal, missing transaction month, conflicting imported valuation, foreign holding missing FX, contingent guarantee, malformed document and revoked grant. Exercises partial results, gaps, correction/reconciliation and denial behavior.

## Golden financial vectors

| Vector | Required assertion |
|---|---|
| Ownership rounding | ₹1.00 split 33.33/33.33/33.34 reconciles to exactly 100 paise with deterministic recipient. |
| Joint roll-up | One ₹1 Cr property at 60/40 appears once household, ₹60L/₹40L person views. |
| Transfer neutrality | Internal ₹1L transfer changes neither household income nor net worth. |
| Correction chain | Original + reversal + corrected event produces exact intended net effect while all remain. |
| Zero-rate EMI | Principal divides across periods and final payment absorbs minor-unit remainder. |
| XIRR | Known dated cash-flow vector matches independently calculated tolerance; missing flow returns failure. |
| TWRR | Cash-flow boundary subperiods geometrically link and differ appropriately from XIRR. |
| Attribution | Contributions plus explicit residual reconcile exactly to headline. |
| Drawdown | Known series returns peak, trough, percentage and recovery/ongoing state. |
| FX history | Historical INR result uses historical approved rate, unaffected by current rate change. |
| Goal liquidity | Sufficient projected value maturing after target reports amount-funded but liquidity-short. |

Exact input/output fixture files will be created during implementation planning and reviewed against independent calculations before engine code.

