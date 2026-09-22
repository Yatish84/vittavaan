# Asset Field Requirement Matrix

> **Status:** Draft implementation field checklist derived from `07_India_Subtype_Attribute_Schemas.md`.
>
> **Scope:** Assets only: all 93 planned asset class/subtype combinations. Liabilities remain in the source schema document and should receive a separate matrix.

## Purpose

This document gives product, design, engineering and testing teams a row-by-row checklist of the information captured for each asset type. It complements the database design; it does not create one physical table per subtype.

A path such as `holdings.subtype_attributes.interest_rate_pct` means the `interest_rate_pct` key inside the schema-validated `holdings.subtype_attributes` JSONB column. It is written in dotted form so its exact logical storage location is unambiguous. Normalized facts—ownership, valuation, transactions, income, restrictions and documents—remain in their dedicated tables.

## Requirement meanings

| Requirement | Plain-English meaning |
|---|---|
| Mandatory | Must be present before the holding can become active. |
| Conditional | Must be present only when the stated feature or circumstance applies. |
| Optional | May be supplied; absence means unknown or not applicable. |
| System-generated / System-calculated | Produced by Vittavaan and not accepted as an authoritative manual value. |
| Sensitive | Must be encrypted or represented by a protected reference and masked in normal responses. |

## Fields common to every asset

These fields are not repeated under every subtype. They apply to every asset in addition to that subtype's matrix.

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | Mandatory |
| `holdings.household_id` | Household in which the holding is shown. | Conditional — mandatory when included in a household portfolio |
| `holdings.asset_class_code` | Selected top-level asset class. | Mandatory |
| `holdings.asset_subtype_code` | Selected asset subtype. | Mandatory |
| `holdings.name` | User-facing name for the holding. | Mandatory |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | Mandatory |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Conditional |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | Conditional |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | Conditional — sensitive |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | System-generated |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | Mandatory — may be empty only when the subtype schema permits it |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Mandatory — defaults to ACTIVE |
| `holdings.acquired_on` | Known acquisition date. | Optional |
| `holdings.created_by_principal_id` | Application principal that created the record. | System-generated |
| `holdings.created_at` | Creation timestamp. | System-generated |
| `holdings.updated_at` | Most recent update timestamp. | System-generated |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | System-generated |
| `ownership_allocations.person_id` | Person receiving an ownership share. | Mandatory for each ownership allocation |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Mandatory for each ownership allocation |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | Mandatory for each ownership allocation |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | Optional |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Conditional — required before the asset contributes to net worth |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | Conditional — required with a valuation |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | Conditional — required with a valuation |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Conditional — required with a valuation |

## Fields available to any asset when applicable

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | Optional |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Conditional — mandatory when offshore is true |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Conditional — mandatory when offshore is true |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Conditional — mandatory when offshore is true |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Optional — sensitive |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | Optional |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Optional — sensitive |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | Optional |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | Optional |

## Subtype-by-subtype fields

## Asset class: `TRAD_SECURITY`

### Asset subtype: `PUBLIC_EQUITY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_name` | Issuer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.security_name` | Security name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.symbol` | Symbol. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.exchange_code` | Exchange code. Expected value: `enum('NSE','BSE','OTHER')`. | Conditional |
| `holdings.subtype_attributes.listing_status` | Listing status. Expected value: `enum('LISTED','SUSPENDED','DELISTED','UNLISTED')`. | Mandatory |
| `holdings.subtype_attributes.sector_code` | Sector code. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.demat_account_ref` | Demat account ref. Expected value: `ref`. | Optional — sensitive |

### Asset subtype: `GOVERNMENT_BOND`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_level` | Issuer level. Expected value: `enum('CENTRAL','STATE','SOVEREIGN_OTHER')`. | Mandatory |
| `holdings.subtype_attributes.issuer_name` | Issuer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.security_name` | Security name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.face_value` | Face value. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.coupon_rate_pct` | Coupon rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.coupon_frequency` | Coupon frequency. Expected value: `enum`. | Conditional |
| `holdings.subtype_attributes.issue_date` | Issue date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.redemption_terms` | Redemption terms. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.demat_account_ref` | Demat account ref. Expected value: `ref`. | Optional — sensitive |

### Asset subtype: `MUNICIPAL_BOND`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_name` | Issuer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.security_name` | Security name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.face_value` | Face value. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.coupon_rate_pct` | Coupon rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.coupon_frequency` | Coupon frequency. Expected value: `enum`. | Conditional |
| `holdings.subtype_attributes.issue_date` | Issue date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.credit_rating` | Credit rating. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.rating_agency` | Rating agency. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.rating_as_of` | Rating as of. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.security_or_escrow_summary` | Security or escrow summary. Expected value: `str`. | Optional |

### Asset subtype: `CORPORATE_BOND`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_name` | Issuer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.security_name` | Security name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.face_value` | Face value. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.coupon_rate_pct` | Coupon rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.coupon_frequency` | Coupon frequency. Expected value: `enum`. | Conditional |
| `holdings.subtype_attributes.issue_date` | Issue date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.secured_status` | Secured status. Expected value: `enum('SECURED','UNSECURED','UNKNOWN')`. | Mandatory |
| `holdings.subtype_attributes.seniority` | Seniority. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.credit_rating` | Credit rating. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.rating_agency` | Rating agency. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.rating_as_of` | Rating as of. Expected value: `date`. | Conditional |

### Asset subtype: `DEBENTURE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_name` | Issuer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.security_name` | Security name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.face_value` | Face value. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.coupon_rate_pct` | Coupon rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.coupon_frequency` | Coupon frequency. Expected value: `enum`. | Conditional |
| `holdings.subtype_attributes.issue_date` | Issue date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.secured_status` | Secured status. Expected value: `enum('SECURED','UNSECURED','UNKNOWN')`. | Mandatory |
| `holdings.subtype_attributes.seniority` | Seniority. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.credit_rating` | Credit rating. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.rating_agency` | Rating agency. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.rating_as_of` | Rating as of. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.convertibility` | Convertibility. Expected value: `enum('NCD','FULLY_CONVERTIBLE','PARTLY_CONVERTIBLE','OPTIONALLY_CONVERTIBLE')`. | Mandatory |
| `holdings.subtype_attributes.conversion_terms` | Conversion terms. Expected value: `object`. | Conditional |
| `holdings.subtype_attributes.debenture_trustee` | Debenture trustee. Expected value: `str`. | Optional |

### Asset subtype: `COMMERCIAL_PAPER`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_name` | Issuer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.face_value` | Face value. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.issue_date` | Issue date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.discount_or_yield_pct` | Discount or yield pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.credit_rating` | Credit rating. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.rating_agency` | Rating agency. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.rating_as_of` | Rating as of. Expected value: `date`. | Conditional |

### Asset subtype: `CERTIFICATE_OF_DEPOSIT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuing_bank_or_fi` | Issuing bank or fi. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.face_value` | Face value. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.issue_date` | Issue date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.discount_or_interest_rate_pct` | Discount or interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.demat_account_ref` | Demat account ref. Expected value: `ref`. | Optional — sensitive |

## Asset class: `CASH`

### Asset subtype: `SAVINGS_ACCOUNT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.branch_ifsc` | Branch ifsc. Expected value: `str(11)`. | Optional |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.deposit_insurance_status` | Deposit insurance status. Expected value: `enum('ELIGIBLE','NOT_ELIGIBLE','UNKNOWN')`. | Optional |
| `holdings.subtype_attributes.lien_state` | Lien state. Expected value: `enum('NONE','LIEN','FROZEN','UNKNOWN')`. | Optional |

### Asset subtype: `CURRENT_ACCOUNT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.branch_ifsc` | Branch ifsc. Expected value: `str(11)`. | Optional |
| `holdings.subtype_attributes.overdraft_enabled` | Overdraft enabled. Expected value: `bool`. | Optional |
| `holdings.subtype_attributes.lien_state` | Lien state. Expected value: `enum`. | Optional |

### Asset subtype: `FIXED_DEPOSIT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.deposit_ref` | Deposit ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.principal_amount` | Principal amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Mandatory |
| `holdings.subtype_attributes.interest_payout_frequency` | Interest payout frequency. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_amount` | Maturity amount. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.auto_renewal` | Auto renewal. Expected value: `bool`. | Optional |
| `holdings.subtype_attributes.premature_break_rule` | Premature break rule. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.deposit_insurance_status` | Deposit insurance status. Expected value: `enum`. | Optional |

### Asset subtype: `RECURRING_DEPOSIT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.deposit_ref` | Deposit ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.instalment_amount` | Instalment amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.instalment_frequency` | Instalment frequency. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Mandatory |
| `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_amount` | Maturity amount. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.missed_instalments` | Missed instalments. Expected value: `int>=0`. | Optional |

### Asset subtype: `SWEEP_ACCOUNT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.linked_account_ref` | Linked account ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.sweep_threshold` | Sweep threshold. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.sweep_direction` | Sweep direction. Expected value: `enum('AUTO_CREATE_DEPOSIT','AUTO_BREAK_DEPOSIT','BOTH')`. | Mandatory |

### Asset subtype: `POSITIVE_CARD_BALANCE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_name` | Issuer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.card_ref` | Card ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.statement_date` | Statement date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.reason` | Reason. Expected value: `enum('REFUND','OVERPAYMENT','CASHBACK','OTHER')`. | Optional |

### Asset subtype: `SAFE_DEPOSIT_LOCKER`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.locker_ref` | Locker ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.branch_ifsc` | Branch ifsc. Expected value: `str(11)`. | Optional |
| `holdings.subtype_attributes.annual_fee` | Annual fee. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.contents_recorded_separately` | Contents recorded separately. Expected value: `bool`. | Mandatory |

## Asset class: `FUND`

### Asset subtype: `MUTUAL_FUND`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.scheme_name` | Scheme name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.amc_name` | Amc name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.scheme_code` | Scheme code. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.folio_ref` | Folio ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.plan_type` | Plan type. Expected value: `enum('DIRECT','REGULAR','INSTITUTIONAL','UNKNOWN')`. | Mandatory |
| `holdings.subtype_attributes.option_type` | Option type. Expected value: `enum('GROWTH','IDCW_PAYOUT','IDCW_REINVESTMENT','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.fund_category` | Fund category. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.expense_ratio_pct` | Expense ratio pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.expense_as_of` | Expense as of. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.lock_in_until` | Lock in until. Expected value: `date`. | Optional |

### Asset subtype: `MONEY_MARKET_FUND`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.scheme_name` | Scheme name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.amc_name` | Amc name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.scheme_code` | Scheme code. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.folio_ref` | Folio ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.plan_type` | Plan type. Expected value: `enum('DIRECT','REGULAR','INSTITUTIONAL','UNKNOWN')`. | Mandatory |
| `holdings.subtype_attributes.option_type` | Option type. Expected value: `enum('GROWTH','IDCW_PAYOUT','IDCW_REINVESTMENT','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.fund_category` | Fund category. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.expense_ratio_pct` | Expense ratio pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.expense_as_of` | Expense as of. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.lock_in_until` | Lock in until. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.money_market_category` | Money market category. Expected value: `enum('LIQUID','OVERNIGHT','MONEY_MARKET','ULTRA_SHORT','OTHER')`. | Optional |
| `holdings.subtype_attributes.weighted_average_maturity_days` | Weighted average maturity days. Expected value: `int>=0`. | Optional |

### Asset subtype: `PMS`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.portfolio_manager_name` | Portfolio manager name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.sebi_registration_ref` | Sebi registration ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.client_account_ref` | Client account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.strategy_name` | Strategy name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.mandate_type` | Mandate type. Expected value: `enum('DISCRETIONARY','NON_DISCRETIONARY','ADVISORY')`. | Mandatory |
| `holdings.subtype_attributes.benchmark_name` | Benchmark name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.fee_terms` | Fee terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.reporting_date` | Reporting date. Expected value: `date`. | Mandatory |

### Asset subtype: `AIF`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.fund_name` | Fund name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.scheme_name` | Scheme name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.sebi_registration_ref` | Sebi registration ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.category` | Category. Expected value: `enum('CATEGORY_I','CATEGORY_II','CATEGORY_III')`. | Mandatory |
| `holdings.subtype_attributes.class_or_series` | Class or series. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.commitment_amount` | Commitment amount. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.drawn_amount` | Drawn amount. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.unfunded_commitment` | Unfunded commitment. Expected value: `money`. | System-calculated |
| `holdings.subtype_attributes.vintage_year` | Vintage year. Expected value: `int`. | Optional |
| `holdings.subtype_attributes.tenure_end_date` | Tenure end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.manager_name` | Manager name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.statement_date` | Statement date. Expected value: `date`. | Mandatory |

## Asset class: `CREDIT_ASSET`

### Asset subtype: `P2P_LOAN`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.platform_name` | Platform name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.loan_ref` | Loan ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.borrower_ref` | Borrower ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.original_principal` | Original principal. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.principal_outstanding` | Principal outstanding. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Mandatory |
| `holdings.subtype_attributes.started_on` | Started on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.due_on` | Due on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.payment_frequency` | Payment frequency. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.credit_state` | Credit state. Expected value: `enum('CURRENT','LATE','DELINQUENT','DEFAULTED','RESTRUCTURED','RECOVERED','DISPUTED')`. | Mandatory |
| `holdings.subtype_attributes.days_past_due` | Days past due. Expected value: `int>=0`. | Conditional |
| `holdings.subtype_attributes.risk_grade` | Risk grade. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.escrow_or_trustee_known` | Escrow or trustee known. Expected value: `bool`. | Optional |

### Asset subtype: `DIRECT_LENDING`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.counterparty_ref` | Counterparty ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.agreement_ref` | Agreement ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.original_principal` | Original principal. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.principal_outstanding` | Principal outstanding. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.rate_type` | Rate type. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.started_on` | Started on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.due_on` | Due on. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.payment_frequency` | Payment frequency. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.security_summary` | Security summary. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.credit_state` | Credit state. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.days_past_due` | Days past due. Expected value: `int>=0`. | Conditional |

### Asset subtype: `MEZZANINE_DEBT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.counterparty_ref` | Counterparty ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.agreement_ref` | Agreement ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.original_principal` | Original principal. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.principal_outstanding` | Principal outstanding. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.rate_type` | Rate type. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.started_on` | Started on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.due_on` | Due on. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.payment_frequency` | Payment frequency. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.security_summary` | Security summary. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.credit_state` | Credit state. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.days_past_due` | Days past due. Expected value: `int>=0`. | Conditional |
| `holdings.subtype_attributes.seniority` | Seniority. Expected value: `enum('SUBORDINATED','JUNIOR','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.equity_kicker` | Equity kicker. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.conversion_or_warrant_terms` | Conversion or warrant terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.cash_pay_rate_pct` | Cash pay rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.pik_rate_pct` | Pik rate pct. Expected value: `pct`. | Optional |

### Asset subtype: `MICROFINANCE_INTEREST`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_or_platform` | Institution or platform. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.facility_ref` | Facility ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.portfolio_or_borrower_group` | Portfolio or borrower group. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.principal_outstanding` | Principal outstanding. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.repayment_frequency` | Repayment frequency. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.delinquency_or_npa_state` | Delinquency or npa state. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.social_or_program_tag` | Social or program tag. Expected value: `str`. | Optional |

### Asset subtype: `MORTGAGE_CREDIT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.borrower_ref` | Borrower ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.agreement_ref` | Agreement ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.principal_outstanding` | Principal outstanding. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.property_security_summary` | Property security summary. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.security_rank` | Security rank. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.credit_state` | Credit state. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.days_past_due` | Days past due. Expected value: `int>=0`. | Conditional |

### Asset subtype: `WORKING_CAPITAL_CREDIT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.counterparty_ref` | Counterparty ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.facility_or_invoice_ref` | Facility or invoice ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.credit_kind` | Credit kind. Expected value: `enum('WORKING_CAPITAL','TRADE_FINANCE','INVOICE','SUPPLY_CHAIN','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.principal_outstanding` | Principal outstanding. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.due_on` | Due on. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.interest_or_discount_rate_pct` | Interest or discount rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.recourse_type` | Recourse type. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.credit_state` | Credit state. Expected value: `enum`. | Mandatory |

## Asset class: `PENSION_SAVINGS`

### Asset subtype: `EPF`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.uan_ref` | Uan ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.employer_name` | Employer name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.establishment_ref` | Establishment ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.member_id_ref` | Member ID ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.employee_component` | Employee component. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.employer_epf_component` | Employer epf component. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.eps_component` | Eps component. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.passbook_as_of` | Passbook as of. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum('RECORDED','NOT_RECORDED','UNKNOWN')`. | Optional |

### Asset subtype: `PPF`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.extension_block_end_date` | Extension block end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.loan_or_lien_state` | Loan or lien state. Expected value: `enum('NONE','LOAN','LIEN','UNKNOWN')`. | Optional |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | Optional |

### Asset subtype: `NPS`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.pran_ref` | Pran ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.tier` | Tier. Expected value: `enum('TIER_I','TIER_II')`. | Mandatory |
| `holdings.subtype_attributes.cra_name` | Cra name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.pop_name` | Pop name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.pension_fund_manager` | Pension fund manager. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.investment_choice` | Investment choice. Expected value: `enum('ACTIVE','AUTO','UNKNOWN')`. | Optional |
| `holdings.subtype_attributes.scheme_allocation` | Scheme allocation. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.statement_as_of` | Statement as of. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | Optional |

### Asset subtype: `SSY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.beneficiary_person_id` | Beneficiary person ID. Expected value: `ref`. | Mandatory |
| `holdings.subtype_attributes.guardian_person_id` | Guardian person ID. Expected value: `ref`. | Conditional |
| `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.annual_deposit_amount` | Annual deposit amount. Expected value: `money`. | Optional |

### Asset subtype: `SCSS`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.deposit_amount` | Deposit amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.interest_payout_frequency` | Interest payout frequency. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.extension_end_date` | Extension end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | Optional |

### Asset subtype: `POST_OFFICE_SAVINGS`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.scheme_kind` | Scheme kind. Expected value: `enum('SAVINGS','RD','TD','MIS','NSC','KVP','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.certificate_ref` | Certificate ref. Expected value: `ref`. | Conditional — sensitive |
| `holdings.subtype_attributes.opened_or_issue_date` | Opened or issue date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.principal_amount` | Principal amount. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.payout_frequency` | Payout frequency. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | Optional |

### Asset subtype: `APY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.pran_ref` | Pran ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.bank_or_pop_name` | Bank or pop name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.contribution_frequency` | Contribution frequency. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.contribution_amount` | Contribution amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.guaranteed_pension_band` | Guaranteed pension band. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.pension_start_date` | Pension start date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.spouse_person_id` | Spouse person ID. Expected value: `ref`. | Optional |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.statement_as_of` | Statement as of. Expected value: `date`. | Mandatory |

### Asset subtype: `GRATUITY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.employer_name` | Employer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.employment_start_date` | Employment start date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.employment_end_date` | Employment end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.covered_under_act` | Covered under act. Expected value: `bool`. | Optional |
| `holdings.subtype_attributes.last_drawn_eligible_salary` | Last drawn eligible salary. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.completed_service_years` | Completed service years. Expected value: `dec`. | System-calculated |
| `holdings.subtype_attributes.employer_statement_amount` | Employer statement amount. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.statement_as_of` | Statement as of. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | Optional |

### Asset subtype: `ANNUITY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.insurer_name` | Insurer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.policy_ref` | Policy ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.annuity_type` | Annuity type. Expected value: `enum('IMMEDIATE','DEFERRED')`. | Mandatory |
| `holdings.subtype_attributes.life_basis` | Life basis. Expected value: `enum('SINGLE','JOINT','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.purchase_price` | Purchase price. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.annuity_amount` | Annuity amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.payment_frequency` | Payment frequency. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.commencement_date` | Commencement date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.return_of_purchase_price` | Return of purchase price. Expected value: `bool`. | Optional |
| `holdings.subtype_attributes.secondary_annuitant_person_id` | Secondary annuitant person ID. Expected value: `ref`. | Conditional |
| `holdings.subtype_attributes.guarantee_period_end` | Guarantee period end. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.surrender_terms` | Surrender terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | Optional |

## Asset class: `PRIVATE_CAPITAL`

### Asset subtype: `VENTURE_CAPITAL`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.company_or_fund_name` | Company or fund name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.instrument_kind` | Instrument kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.share_class` | Share class. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.ownership_pct` | Ownership pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.committed_capital` | Committed capital. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.drawn_capital` | Drawn capital. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.last_round_name` | Last round name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.last_round_date` | Last round date. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.last_round_price` | Last round price. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.dilution_terms` | Dilution terms. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.exit_rights` | Exit rights. Expected value: `str`. | Optional |

### Asset subtype: `GROWTH_BUYOUT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.company_or_fund_name` | Company or fund name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.instrument_kind` | Instrument kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.ownership_pct` | Ownership pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.committed_capital` | Committed capital. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.drawn_capital` | Drawn capital. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.distribution_total` | Distribution total. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.vintage_year` | Vintage year. Expected value: `int`. | Optional |
| `holdings.subtype_attributes.manager_name` | Manager name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.liquidity_window` | Liquidity window. Expected value: `object`. | Optional |

### Asset subtype: `DISTRESSED_INVESTMENT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_or_asset_name` | Issuer or asset name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.instrument_kind` | Instrument kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.claim_or_security_ref` | Claim or security ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.seniority` | Seniority. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.restructuring_state` | Restructuring state. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.expected_recovery` | Expected recovery. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.expected_recovery_date` | Expected recovery date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.legal_or_insolvency_reference` | Legal or insolvency reference. Expected value: `ref`. | Optional — sensitive |

### Asset subtype: `SYNDICATE_INTEREST`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.syndicate_or_lead_name` | Syndicate or lead name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.investee_name` | Investee name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.instrument_kind` | Instrument kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.spv_name` | Spv name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.commitment_amount` | Commitment amount. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.drawn_amount` | Drawn amount. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.ownership_or_units` | Ownership or units. Expected value: `dec`. | Optional |
| `holdings.subtype_attributes.carry_or_fee_terms` | Carry or fee terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.exit_rights` | Exit rights. Expected value: `str`. | Optional |

### Asset subtype: `CONVERTIBLE_NOTE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_name` | Issuer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.agreement_ref` | Agreement ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.principal_amount` | Principal amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.issue_date` | Issue date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.valuation_cap` | Valuation cap. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.discount_pct` | Discount pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.conversion_trigger` | Conversion trigger. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.conversion_status` | Conversion status. Expected value: `enum`. | Mandatory |

### Asset subtype: `ESOP_OPTION`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.employer_or_issuer` | Employer or issuer. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.grant_ref` | Grant ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.grant_date` | Grant date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.granted_units` | Granted units. Expected value: `dec`. | Mandatory |
| `holdings.subtype_attributes.vested_units` | Vested units. Expected value: `dec`. | Mandatory |
| `holdings.subtype_attributes.exercised_units` | Exercised units. Expected value: `dec`. | Optional |
| `holdings.subtype_attributes.strike_price` | Strike price. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.vesting_schedule_summary` | Vesting schedule summary. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.next_vesting_date` | Next vesting date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.expiry_date` | Expiry date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.exercise_status` | Exercise status. Expected value: `enum`. | Mandatory |

## Asset class: `HEDGE_STRATEGY`

### Asset subtype: `HEDGE_FUND`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.fund_name` | Fund name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.manager_name` | Manager name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.domicile_country` | Domicile country. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.fund_or_account_ref` | Fund or account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.strategy_name` | Strategy name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.share_class` | Share class. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.redemption_terms` | Redemption terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.lock_up_until` | Lock up until. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.statement_date` | Statement date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.leverage_disclosed` | Leverage disclosed. Expected value: `dec`. | Optional |

### Asset subtype: `LONG_SHORT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.fund_name` | Fund name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.manager_name` | Manager name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.domicile_country` | Domicile country. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.fund_or_account_ref` | Fund or account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.strategy_name` | Strategy name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.share_class` | Share class. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.redemption_terms` | Redemption terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.lock_up_until` | Lock up until. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.statement_date` | Statement date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.leverage_disclosed` | Leverage disclosed. Expected value: `dec`. | Optional |
| `holdings.subtype_attributes.gross_exposure_pct` | Gross exposure pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.net_exposure_pct` | Net exposure pct. Expected value: `dec(-100..100)`. | Optional |
| `holdings.subtype_attributes.shorting_permitted` | Shorting permitted. Expected value: `bool`. | Mandatory |

### Asset subtype: `GLOBAL_MACRO`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.fund_name` | Fund name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.manager_name` | Manager name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.domicile_country` | Domicile country. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.fund_or_account_ref` | Fund or account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.strategy_name` | Strategy name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.share_class` | Share class. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.redemption_terms` | Redemption terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.lock_up_until` | Lock up until. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.statement_date` | Statement date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.leverage_disclosed` | Leverage disclosed. Expected value: `dec`. | Optional |
| `holdings.subtype_attributes.primary_markets` | Primary markets. Expected value: `list<str>`. | Optional |
| `holdings.subtype_attributes.base_currency` | Base currency. Expected value: `ISO4217`. | Mandatory |
| `holdings.subtype_attributes.derivative_usage` | Derivative usage. Expected value: `bool`. | Optional |

### Asset subtype: `ARBITRAGE_STRATEGY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.fund_name` | Fund name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.manager_name` | Manager name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.domicile_country` | Domicile country. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.fund_or_account_ref` | Fund or account ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.strategy_name` | Strategy name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.share_class` | Share class. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.redemption_terms` | Redemption terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.lock_up_until` | Lock up until. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.statement_date` | Statement date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.leverage_disclosed` | Leverage disclosed. Expected value: `dec`. | Optional |
| `holdings.subtype_attributes.arbitrage_kind` | Arbitrage kind. Expected value: `enum('CASH_FUTURES','MERGER','CONVERTIBLE','STATISTICAL','OTHER')`. | Optional |

## Asset class: `REAL_ASSET`

### Asset subtype: `RESIDENTIAL_PROPERTY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.property_kind` | Property kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.address_ref` | Address ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.state_code` | State code. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.district` | District. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.pin_code` | Pin code. Expected value: `str(6)`. | Optional |
| `holdings.subtype_attributes.title_or_registration_ref` | Title or registration ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.rera_project_ref` | Rera project ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.carpet_area` | Carpet area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.built_up_area` | Built up area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.land_share` | Land share. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.possession_status` | Possession status. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.occupancy_status` | Occupancy status. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.completion_or_possession_date` | Completion or possession date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.property_tax_ref` | Property tax ref. Expected value: `ref`. | Optional — sensitive |

### Asset subtype: `COMMERCIAL_PROPERTY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.property_kind` | Property kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.address_ref` | Address ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.state_code` | State code. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.district` | District. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.pin_code` | Pin code. Expected value: `str(6)`. | Optional |
| `holdings.subtype_attributes.title_or_registration_ref` | Title or registration ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.rera_project_ref` | Rera project ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.carpet_area` | Carpet area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.built_up_area` | Built up area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.land_share` | Land share. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.possession_status` | Possession status. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.occupancy_status` | Occupancy status. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.completion_or_possession_date` | Completion or possession date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.property_tax_ref` | Property tax ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.commercial_kind` | Commercial kind. Expected value: `enum('OFFICE','RETAIL','WAREHOUSE','INDUSTRIAL','HOSPITALITY','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.lease_status` | Lease status. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.tenant_count` | Tenant count. Expected value: `int`. | Optional |
| `holdings.subtype_attributes.lease_expiry_date` | Lease expiry date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.occupancy_area_pct` | Occupancy area pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.noi_basis_available` | Noi basis available. Expected value: `bool`. | Optional |

### Asset subtype: `LAND`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.land_kind` | Land kind. Expected value: `enum('RESIDENTIAL','COMMERCIAL','INDUSTRIAL','DEVELOPMENT','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.address_ref` | Address ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.state_code` | State code. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.district` | District. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.survey_or_khasra_ref` | Survey or khasra ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.title_or_registration_ref` | Title or registration ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.area` | Area. Expected value: `object`. | Mandatory |
| `holdings.subtype_attributes.usable_area` | Usable area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.saleable_area` | Saleable area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.waste_area` | Waste area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.land_use_or_zoning` | Land use or zoning. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.conversion_status` | Conversion status. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.development_status` | Development status. Expected value: `enum`. | Optional |

### Asset subtype: `AGRICULTURAL_LAND`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.land_kind` | Land kind. Expected value: `enum('RESIDENTIAL','COMMERCIAL','INDUSTRIAL','DEVELOPMENT','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.address_ref` | Address ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.state_code` | State code. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.district` | District. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.survey_or_khasra_ref` | Survey or khasra ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.title_or_registration_ref` | Title or registration ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.area` | Area. Expected value: `object`. | Mandatory |
| `holdings.subtype_attributes.usable_area` | Usable area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.saleable_area` | Saleable area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.waste_area` | Waste area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.land_use_or_zoning` | Land use or zoning. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.conversion_status` | Conversion status. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.development_status` | Development status. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.agricultural_land_class` | Agricultural land class. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.crop_or_use` | Crop or use. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.irrigation_status` | Irrigation status. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.tenancy_or_cultivation_status` | Tenancy or cultivation status. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.state_eligibility_confirmed` | State eligibility confirmed. Expected value: `bool`. | Optional |

### Asset subtype: `REIT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.trust_name` | Trust name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.symbol` | Symbol. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.exchange_code` | Exchange code. Expected value: `enum`. | Conditional |
| `holdings.subtype_attributes.manager_name` | Manager name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.reit_kind` | Reit kind. Expected value: `enum('REIT','SM_REIT')`. | Optional |
| `holdings.subtype_attributes.distribution_frequency` | Distribution frequency. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.demat_account_ref` | Demat account ref. Expected value: `ref`. | Optional — sensitive |

### Asset subtype: `FRACTIONAL_PROPERTY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.platform_or_manager_name` | Platform or manager name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.spv_or_scheme_name` | Spv or scheme name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_ref` | Interest ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.underlying_property_summary` | Underlying property summary. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum('SPV_SECURITY','SM_REIT_UNIT','CO_OWNERSHIP','CONTRACTUAL','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.ownership_or_units` | Ownership or units. Expected value: `dec`. | Optional |
| `holdings.subtype_attributes.rera_project_ref` | Rera project ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.lock_in_until` | Lock in until. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.exit_terms` | Exit terms. Expected value: `object`. | Optional |

### Asset subtype: `PARKING_STORAGE_UNIT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.unit_kind` | Unit kind. Expected value: `enum('PARKING','SELF_STORAGE','WAREHOUSE_UNIT')`. | Mandatory |
| `holdings.subtype_attributes.address_ref` | Address ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.unit_or_registration_ref` | Unit or registration ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.area` | Area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.title_kind` | Title kind. Expected value: `enum('SEPARATE_TITLE','APPURTENANT','LEASE','CONTRACTUAL','UNKNOWN')`. | Mandatory |
| `holdings.subtype_attributes.occupancy_status` | Occupancy status. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.lease_expiry_date` | Lease expiry date. Expected value: `date`. | Optional |

## Asset class: `INFRASTRUCTURE`

### Asset subtype: `TOLL_ROAD`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.project_or_spv_name` | Project or spv name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.concession_authority` | Concession authority. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.concession_ref` | Concession ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.concession_end_date` | Concession end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.operational_status` | Operational status. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.route_or_location` | Route or location. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.traffic_or_revenue_source_date` | Traffic or revenue source date. Expected value: `date`. | Optional |

### Asset subtype: `AIRPORT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.project_or_spv_name` | Project or spv name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.airport_name_or_code` | Airport name or code. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.concession_authority` | Concession authority. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.concession_end_date` | Concession end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.operational_status` | Operational status. Expected value: `enum`. | Mandatory |

### Asset subtype: `PIPELINE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.project_or_spv_name` | Project or spv name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.commodity_or_service` | Commodity or service. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.route_or_region` | Route or region. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.capacity` | Capacity. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.concession_or_contract_end` | Concession or contract end. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.operational_status` | Operational status. Expected value: `enum`. | Mandatory |

### Asset subtype: `PPP_PROJECT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.project_or_spv_name` | Project or spv name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.sector` | Sector. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.government_counterparty` | Government counterparty. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.concession_or_agreement_ref` | Concession or agreement ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.concession_end_date` | Concession end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.project_stage` | Project stage. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.revenue_model` | Revenue model. Expected value: `enum`. | Optional |

### Asset subtype: `ENERGY_PROJECT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.project_or_spv_name` | Project or spv name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.energy_kind` | Energy kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.installed_capacity` | Installed capacity. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.location` | Location. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.offtake_counterparty` | Offtake counterparty. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.ppa_end_date` | Ppa end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.project_stage` | Project stage. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.operational_since` | Operational since. Expected value: `date`. | Optional |

## Asset class: `TANGIBLE`

### Asset subtype: `PRECIOUS_METAL`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.metal_type` | Metal type. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.form` | Form. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.weight` | Weight. Expected value: `object`. | Mandatory |
| `holdings.subtype_attributes.purity` | Purity. Expected value: `dec`. | Optional |
| `holdings.subtype_attributes.hallmark_or_serial_ref` | Hallmark or serial ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.custody_location_class` | Custody location class. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.appraiser_name` | Appraiser name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.appraisal_date` | Appraisal date. Expected value: `date`. | Conditional |

### Asset subtype: `COMMODITY_INTEREST`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.commodity_type` | Commodity type. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.form_or_grade` | Form or grade. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.quantity_and_unit` | Quantity and unit. Expected value: `object`. | Mandatory |
| `holdings.subtype_attributes.warehouse_or_custodian` | Warehouse or custodian. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.warehouse_receipt_ref` | Warehouse receipt ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.delivery_location` | Delivery location. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.expiry_or_storage_end` | Expiry or storage end. Expected value: `date`. | Optional |

### Asset subtype: `ART`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.artist_or_maker` | Artist or maker. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.work_title` | Work title. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.medium` | Medium. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.creation_year` | Creation year. Expected value: `int`. | Optional |
| `holdings.subtype_attributes.dimensions` | Dimensions. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.provenance_summary` | Provenance summary. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.authenticity_state` | Authenticity state. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.catalogue_or_serial_ref` | Catalogue or serial ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.storage_location_class` | Storage location class. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.insured_value` | Insured value. Expected value: `money`. | Optional |

### Asset subtype: `WINE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.producer` | Producer. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.label_or_cuvee` | Label or cuvee. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.vintage_year` | Vintage year. Expected value: `int`. | Optional |
| `holdings.subtype_attributes.region_country` | Region country. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.bottle_count` | Bottle count. Expected value: `int>0`. | Mandatory |
| `holdings.subtype_attributes.bottle_size_ml` | Bottle size ml. Expected value: `int`. | Optional |
| `holdings.subtype_attributes.storage_location_class` | Storage location class. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.provenance_summary` | Provenance summary. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.condition_grade` | Condition grade. Expected value: `str`. | Optional |

### Asset subtype: `COINS_STAMPS`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.collection_kind` | Collection kind. Expected value: `enum('COIN','STAMP','MIXED')`. | Mandatory |
| `holdings.subtype_attributes.description` | Description. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.item_count` | Item count. Expected value: `int`. | Optional |
| `holdings.subtype_attributes.country_or_issue` | Country or issue. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.year_or_period` | Year or period. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.grade_or_condition` | Grade or condition. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.certification_ref` | Certification ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.provenance_summary` | Provenance summary. Expected value: `str`. | Optional |

### Asset subtype: `JEWELLERY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.item_type` | Item type. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.metal_type` | Metal type. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.gross_weight` | Gross weight. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.net_metal_weight` | Net metal weight. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.purity` | Purity. Expected value: `dec`. | Optional |
| `holdings.subtype_attributes.gemstone_summary` | Gemstone summary. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.hallmark_or_certificate_ref` | Hallmark or certificate ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.appraiser_name` | Appraiser name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.appraisal_date` | Appraisal date. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.insured_value` | Insured value. Expected value: `money`. | Optional |

### Asset subtype: `OTHER_COLLECTIBLE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.item_type` | Item type. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.description` | Description. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.maker_or_brand` | Maker or brand. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.serial_ref` | Serial ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.year_or_period` | Year or period. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.provenance_summary` | Provenance summary. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.authenticity_state` | Authenticity state. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.condition_grade` | Condition grade. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.appraiser_name` | Appraiser name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.appraisal_date` | Appraisal date. Expected value: `date`. | Conditional |

## Asset class: `DIGITAL_ASSET`

### Asset subtype: `CRYPTO_TOKEN`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.asset_symbol` | Asset symbol. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.asset_name` | Asset name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.network` | Network. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.contract_address` | Contract address. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.custody_type` | Custody type. Expected value: `enum('SELF_CUSTODY','EXCHANGE','INSTITUTIONAL','SMART_CONTRACT','UNKNOWN')`. | Mandatory |
| `holdings.subtype_attributes.wallet_or_account_hash` | Wallet or account hash. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.venue_name` | Venue name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.fiu_registration_status` | Fiu registration status. Expected value: `enum('REGISTERED','NOT_REGISTERED','UNKNOWN','NOT_APPLICABLE')`. | Optional |
| `holdings.subtype_attributes.tax_lot_method` | Tax lot method. Expected value: `enum`. | Optional |

### Asset subtype: `NFT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.collection_name` | Collection name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.token_id` | Token ID. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.network` | Network. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.contract_address` | Contract address. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.token_standard` | Token standard. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.custody_type` | Custody type. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.wallet_or_account_hash` | Wallet or account hash. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.creator_or_issuer` | Creator or issuer. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.rights_summary` | Rights summary. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.metadata_uri_hash` | Metadata uri hash. Expected value: `str`. | Optional |

### Asset subtype: `TOKENIZED_ASSET`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.token_name` | Token name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.token_id_or_symbol` | Token ID or symbol. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.network_or_registry` | Network or registry. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.contract_address` | Contract address. Expected value: `str`. | Conditional |
| `holdings.subtype_attributes.underlying_asset_type` | Underlying asset type. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.issuer_or_spv` | Issuer or spv. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.legal_claim_type` | Legal claim type. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.custodian_or_trustee` | Custodian or trustee. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.redemption_terms` | Redemption terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.regulatory_classification` | Regulatory classification. Expected value: `str`. | Optional |

### Asset subtype: `DOMAIN_NAME`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.domain_name` | Domain name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.registrar_name` | Registrar name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.registrar_account_ref` | Registrar account ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.registration_date` | Registration date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.expiry_date` | Expiry date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.auto_renewal` | Auto renewal. Expected value: `bool`. | Optional |
| `holdings.subtype_attributes.registry_lock` | Registry lock. Expected value: `bool`. | Optional |
| `holdings.subtype_attributes.monetization_status` | Monetization status. Expected value: `enum`. | Optional |

## Asset class: `TRUST_INTEREST`

### Asset subtype: `TRUST_BENEFICIAL_INTEREST`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.trust_name` | Trust name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.trust_jurisdiction` | Trust jurisdiction. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.trust_deed_ref` | Trust deed ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.trustee_name` | Trustee name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_type` | Interest type. Expected value: `enum('FIXED','DISCRETIONARY','CONTINGENT','LIFE_INTEREST','REMAINDER','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.beneficial_share_pct` | Beneficial share pct. Expected value: `pct`. | Conditional |
| `holdings.subtype_attributes.distribution_terms` | Distribution terms. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.vesting_or_end_date` | Vesting or end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.revocability` | Revocability. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.statement_date` | Statement date. Expected value: `date`. | Mandatory |

## Asset class: `CONTRACT_RIGHT`

### Asset subtype: `RECEIVABLE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.counterparty_ref` | Counterparty ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.contract_or_invoice_ref` | Contract or invoice ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.original_amount` | Original amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.amount_outstanding` | Amount outstanding. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.due_date` | Due date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.interest_or_penalty_terms` | Interest or penalty terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.credit_state` | Credit state. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.assignability` | Assignability. Expected value: `enum`. | Optional |

### Asset subtype: `EARNOUT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.counterparty_ref` | Counterparty ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.agreement_ref` | Agreement ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.measurement_period` | Measurement period. Expected value: `object`. | Mandatory |
| `holdings.subtype_attributes.trigger_or_formula` | Trigger or formula. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.maximum_entitlement` | Maximum entitlement. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.amount_received` | Amount received. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.next_assessment_date` | Next assessment date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.contingency_state` | Contingency state. Expected value: `enum`. | Mandatory |

### Asset subtype: `PROFIT_SHARE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.counterparty_ref` | Counterparty ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.agreement_ref` | Agreement ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.profit_base` | Profit base. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.share_pct` | Share pct. Expected value: `pct`. | Mandatory |
| `holdings.subtype_attributes.effective_from` | Effective from. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.expires_on` | Expires on. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.payment_frequency` | Payment frequency. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.audit_rights` | Audit rights. Expected value: `bool`. | Optional |

### Asset subtype: `ROYALTY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.right_type` | Right type. Expected value: `enum('MUSIC','PATENT','TRADEMARK','BOOK','SOFTWARE','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.work_or_ip_name` | Work or ip name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.registration_or_contract_ref` | Registration or contract ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.payer_or_licensee` | Payer or licensee. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.territory` | Territory. Expected value: `list<country>`. | Optional |
| `holdings.subtype_attributes.payment_basis` | Payment basis. Expected value: `object`. | Mandatory |
| `holdings.subtype_attributes.effective_from` | Effective from. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.expires_on` | Expires on. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.assignability` | Assignability. Expected value: `enum`. | Optional |

### Asset subtype: `FRANCHISE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.franchisor_name` | Franchisor name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.brand_name` | Brand name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.agreement_ref` | Agreement ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.territory` | Territory. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.effective_from` | Effective from. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.expires_on` | Expires on. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.initial_fee` | Initial fee. Expected value: `money`. | Optional |
| `holdings.subtype_attributes.ongoing_fee_basis` | Ongoing fee basis. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.renewal_terms` | Renewal terms. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.transferability` | Transferability. Expected value: `enum`. | Optional |

### Asset subtype: `LITIGATION_FINANCE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.case_ref` | Case ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.court_or_forum` | Court or forum. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.funded_party_ref` | Funded party ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.agreement_ref` | Agreement ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.funded_amount` | Funded amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.return_waterfall` | Return waterfall. Expected value: `object`. | Mandatory |
| `holdings.subtype_attributes.case_stage` | Case stage. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.expected_resolution_date` | Expected resolution date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.adverse_cost_exposure` | Adverse cost exposure. Expected value: `money`. | Optional |

### Asset subtype: `SPORTS_INTEREST`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.team_or_athlete_ref` | Team or athlete ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.contract_ref` | Contract ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.effective_from` | Effective from. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.expires_on` | Expires on. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.payment_or_revenue_basis` | Payment or revenue basis. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.territory_or_league` | Territory or league. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.assignability` | Assignability. Expected value: `enum`. | Optional |

### Asset subtype: `ENTERTAINMENT_RIGHT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.project_or_work_name` | Project or work name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.media_kind` | Media kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.contract_ref` | Contract ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.right_kind` | Right kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.territory` | Territory. Expected value: `list<country>`. | Optional |
| `holdings.subtype_attributes.effective_from` | Effective from. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.expires_on` | Expires on. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.revenue_share_basis` | Revenue share basis. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.recoupment_waterfall` | Recoupment waterfall. Expected value: `object`. | Optional |

## Asset class: `INSURANCE_SECURITY`

### Asset subtype: `CAT_BOND`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_or_spv` | Issuer or spv. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.security_name` | Security name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Conditional |
| `holdings.subtype_attributes.peril_or_trigger` | Peril or trigger. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.trigger_type` | Trigger type. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.face_value` | Face value. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.coupon_rate_pct` | Coupon rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.issue_date` | Issue date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.loss_attachment_terms` | Loss attachment terms. Expected value: `str`. | Optional |

## Asset class: `DERIVATIVE`

### Asset subtype: `EQUITY_OPTION`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.underlying_ref` | Underlying ref. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.option_type` | Option type. Expected value: `enum('CALL','PUT')`. | Mandatory |
| `holdings.subtype_attributes.position_side` | Position side. Expected value: `enum('LONG','SHORT')`. | Mandatory |
| `holdings.subtype_attributes.exercise_style` | Exercise style. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.strike_price` | Strike price. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.expiry_date` | Expiry date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.contract_multiplier` | Contract multiplier. Expected value: `dec>0`. | Mandatory |
| `holdings.subtype_attributes.settlement_type` | Settlement type. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.exchange_code` | Exchange code. Expected value: `str`. | Optional |

### Asset subtype: `FUTURE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.underlying_ref` | Underlying ref. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.position_side` | Position side. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.expiry_date` | Expiry date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.contract_quantity` | Contract quantity. Expected value: `dec>0`. | Mandatory |
| `holdings.subtype_attributes.contract_multiplier` | Contract multiplier. Expected value: `dec>0`. | Mandatory |
| `holdings.subtype_attributes.settlement_type` | Settlement type. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.exchange_code` | Exchange code. Expected value: `str`. | Optional |

### Asset subtype: `FX_FORWARD_SWAP`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.instrument_kind` | Instrument kind. Expected value: `enum('FORWARD','SWAP')`. | Mandatory |
| `holdings.subtype_attributes.buy_currency` | Buy currency. Expected value: `ISO4217`. | Mandatory |
| `holdings.subtype_attributes.sell_currency` | Sell currency. Expected value: `ISO4217`. | Mandatory |
| `holdings.subtype_attributes.buy_amount` | Buy amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.sell_amount` | Sell amount. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.contract_rate` | Contract rate. Expected value: `dec`. | Mandatory |
| `holdings.subtype_attributes.settlement_date` | Settlement date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.counterparty_ref` | Counterparty ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.deliverability` | Deliverability. Expected value: `enum`. | Optional |

### Asset subtype: `COMMODITY_DERIVATIVE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.underlying_commodity` | Underlying commodity. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.instrument_kind` | Instrument kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.position_side` | Position side. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.quantity_and_unit` | Quantity and unit. Expected value: `object`. | Mandatory |
| `holdings.subtype_attributes.strike_price` | Strike price. Expected value: `money`. | Conditional |
| `holdings.subtype_attributes.expiry_date` | Expiry date. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.settlement_type` | Settlement type. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.exchange_code` | Exchange code. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.delivery_location` | Delivery location. Expected value: `str`. | Optional |

### Asset subtype: `CONVERTIBLE_SECURITY`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.issuer_name` | Issuer name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.security_name` | Security name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.isin` | Isin. Expected value: `str(12)`. | Optional |
| `holdings.subtype_attributes.principal_or_face_value` | Principal or face value. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.coupon_rate_pct` | Coupon rate pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.conversion_ratio_or_formula` | Conversion ratio or formula. Expected value: `object`. | Mandatory |
| `holdings.subtype_attributes.conversion_start_date` | Conversion start date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.conversion_end_date` | Conversion end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.conversion_status` | Conversion status. Expected value: `enum`. | Mandatory |

## Asset class: `SPECIALIZED`

### Asset subtype: `AGRI_BUSINESS`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum('FARMLAND','TIMBER','LIVESTOCK','AGRIBUSINESS_EQUITY','REVENUE_SHARE','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.project_or_business_name` | Project or business name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.location` | Location. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.units_or_area` | Units or area. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.crop_species_or_activity` | Crop species or activity. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.harvest_or_cycle_date` | Harvest or cycle date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.operator_name` | Operator name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.biological_asset_count` | Biological asset count. Expected value: `int`. | Optional |

### Asset subtype: `CARBON_CREDIT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.project_name` | Project name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.credit_standard` | Credit standard. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.registry_name` | Registry name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.registry_ref` | Registry ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.project_country` | Project country. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.vintage_year` | Vintage year. Expected value: `int`. | Mandatory |
| `holdings.subtype_attributes.credit_type` | Credit type. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.units_tco2e` | Units tco2e. Expected value: `dec>=0`. | Mandatory |
| `holdings.subtype_attributes.retirement_status` | Retirement status. Expected value: `enum('ACTIVE','RETIRED','CANCELLED','UNKNOWN')`. | Mandatory |
| `holdings.subtype_attributes.retirement_date` | Retirement date. Expected value: `date`. | Conditional |
| `holdings.subtype_attributes.verification_body` | Verification body. Expected value: `str`. | Optional |

### Asset subtype: `SHIPPING_INTEREST`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum('CONTAINER','VESSEL','CARGO','LEASE','EQUITY','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.asset_or_project_name` | Asset or project name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.imo_or_container_ref` | Imo or container ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.operator_name` | Operator name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.flag_country` | Flag country. Expected value: `country`. | Optional |
| `holdings.subtype_attributes.capacity_or_units` | Capacity or units. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.lease_or_charter_end` | Lease or charter end. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.operational_status` | Operational status. Expected value: `enum`. | Mandatory |

### Asset subtype: `SPACE_INVESTMENT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.company_or_project_name` | Company or project name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.jurisdiction` | Jurisdiction. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.development_stage` | Development stage. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.mission_or_asset_summary` | Mission or asset summary. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.launch_or_milestone_date` | Launch or milestone date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.commercialization_stage` | Commercialization stage. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.material_risk_note` | Material risk note. Expected value: `str`. | Mandatory |

### Asset subtype: `DATA_AI_INTEREST`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.company_or_asset_name` | Company or asset name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum('EQUITY','DATA_RIGHT','MODEL_RIGHT','COMPUTE_CAPACITY','DATA_CENTRE','OTHER')`. | Mandatory |
| `holdings.subtype_attributes.jurisdiction` | Jurisdiction. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.rights_or_capacity_summary` | Rights or capacity summary. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.contract_ref` | Contract ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.term_end_date` | Term end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.commercialization_stage` | Commercialization stage. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.data_rights_basis` | Data rights basis. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.material_risk_note` | Material risk note. Expected value: `str`. | Mandatory |

### Asset subtype: `BIOTECH_RIGHT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.company_or_program_name` | Company or program name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_kind` | Interest kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.jurisdiction` | Jurisdiction. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.therapy_or_program` | Therapy or program. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.development_phase` | Development phase. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.milestone_terms` | Milestone terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.royalty_terms` | Royalty terms. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.patent_or_contract_ref` | Patent or contract ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.exclusivity_end_date` | Exclusivity end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.material_risk_note` | Material risk note. Expected value: `str`. | Mandatory |

## Asset class: `VEHICLE`

### Asset subtype: `ROAD_VEHICLE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.vehicle_kind` | Vehicle kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.make` | Make. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.model` | Model. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.variant` | Variant. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.manufacture_year` | Manufacture year. Expected value: `int`. | Mandatory |
| `holdings.subtype_attributes.registration_ref` | Registration ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.registration_state` | Registration state. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.vin_or_chassis_ref` | Vin or chassis ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.engine_or_motor_ref` | Engine or motor ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.fuel_type` | Fuel type. Expected value: `enum`. | Optional |
| `holdings.subtype_attributes.odometer_km` | Odometer km. Expected value: `int>=0`. | Optional |
| `holdings.subtype_attributes.insurance_expiry` | Insurance expiry. Expected value: `date`. | Optional |

### Asset subtype: `AIRCRAFT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.make` | Make. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.model` | Model. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.manufacture_year` | Manufacture year. Expected value: `int`. | Optional |
| `holdings.subtype_attributes.registration_ref` | Registration ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.serial_ref` | Serial ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.jurisdiction` | Jurisdiction. Expected value: `country`. | Mandatory |
| `holdings.subtype_attributes.ownership_interest_pct` | Ownership interest pct. Expected value: `pct`. | Optional |
| `holdings.subtype_attributes.operator_name` | Operator name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.airworthiness_expiry` | Airworthiness expiry. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.hours_or_cycles` | Hours or cycles. Expected value: `object`. | Optional |

### Asset subtype: `VESSEL`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.vessel_kind` | Vessel kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.make_or_builder` | Make or builder. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.model_or_name` | Model or name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.manufacture_year` | Manufacture year. Expected value: `int`. | Optional |
| `holdings.subtype_attributes.registration_or_imo_ref` | Registration or imo ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.flag_country` | Flag country. Expected value: `country`. | Optional |
| `holdings.subtype_attributes.length_or_tonnage` | Length or tonnage. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.berth_or_location_class` | Berth or location class. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.insurance_expiry` | Insurance expiry. Expected value: `date`. | Optional |

### Asset subtype: `FRACTIONAL_VEHICLE`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.underlying_vehicle_kind` | Underlying vehicle kind. Expected value: `enum`. | Mandatory |
| `holdings.subtype_attributes.platform_or_spv_name` | Platform or spv name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.interest_ref` | Interest ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.ownership_pct_or_units` | Ownership pct or units. Expected value: `dec`. | Mandatory |
| `holdings.subtype_attributes.usage_rights` | Usage rights. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.operator_name` | Operator name. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.term_end_date` | Term end date. Expected value: `date`. | Optional |
| `holdings.subtype_attributes.exit_terms` | Exit terms. Expected value: `object`. | Optional |

## Asset class: `TAX_ASSET`

### Asset subtype: `GST_INPUT_CREDIT`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.gstin_ref` | Gstin ref. Expected value: `ref`. | Mandatory — sensitive |
| `holdings.subtype_attributes.tax_period` | Tax period. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.credit_component` | Credit component. Expected value: `enum('IGST','CGST','SGST','UTGST','CESS','MIXED')`. | Mandatory |
| `holdings.subtype_attributes.ledger_balance` | Ledger balance. Expected value: `money`. | Mandatory |
| `holdings.subtype_attributes.ledger_as_of` | Ledger as of. Expected value: `date`. | Mandatory |
| `holdings.subtype_attributes.eligibility_state` | Eligibility state. Expected value: `enum('ELIGIBLE','BLOCKED','DISPUTED','REVERSAL_PENDING','UNKNOWN')`. | Mandatory |
| `holdings.subtype_attributes.return_or_ledger_ref` | Return or ledger ref. Expected value: `ref`. | Optional — sensitive |

## Asset class: `OTHER`

### Asset subtype: `CUSTOM_ASSET`

| `table_name.column_name` | Description | Requirement |
|---|---|---|
| `holdings.subtype_attributes.custom_type_name` | Custom type name. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.description` | Description. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.legal_or_contract_basis` | Legal or contract basis. Expected value: `str`. | Optional |
| `holdings.subtype_attributes.identifier_ref` | Identifier ref. Expected value: `ref`. | Optional — sensitive |
| `holdings.subtype_attributes.jurisdiction` | Jurisdiction. Expected value: `country`. | Optional |
| `holdings.subtype_attributes.units_or_interest` | Units or interest. Expected value: `object`. | Optional |
| `holdings.subtype_attributes.valuation_basis_note` | Valuation basis note. Expected value: `str`. | Mandatory |
| `holdings.subtype_attributes.material_risk_note` | Material risk note. Expected value: `str`. | Mandatory |

## Completeness and maintenance rules

- This version contains **93 asset subtypes** and **888 expanded subtype-field rows**.
- Inherited profiles—such as debentures inheriting corporate-bond fields—are expanded here so readers do not have to jump between sections.
- The source of truth for validation details remains `07_India_Subtype_Attribute_Schemas.md`; this matrix must be regenerated whenever that source changes.
- A subtype field cannot be moved into or out of normalized storage without updating the database design, API contract, migration plan and tests.
- Mandatory is a business activation rule. Database `NOT NULL` constraints are documented separately in `03_Database_Design.md`.

