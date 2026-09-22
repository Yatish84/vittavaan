# Asset Field Requirement Matrix

> **Status:** Draft implementation field checklist derived from `07_India_Subtype_Attribute_Schemas.md`.
>
> **Scope:** Assets only: all 93 planned asset class/subtype combinations. Liabilities remain in the source schema document and should receive a separate matrix.

## Purpose

This document gives product, design, engineering and testing teams a row-by-row checklist of the information captured for each asset type. It complements the database design; it does not create one physical table per subtype.

A path such as `holdings.subtype_attributes.interest_rate_pct` means the `interest_rate_pct` key inside the schema-validated `holdings.subtype_attributes` JSONB column. It is written in dotted form so its exact logical storage location is unambiguous. Normalized facts—ownership, valuation, transactions, income, restrictions and documents—remain in their dedicated tables.

## Status tags

Each field path starts with a small colored tag. Rows inside each subtype are sorted in the order shown here. The Notes column is blank unless a condition or other qualification matters.

| Tag | Plain-English meaning |
|---|---|
| <code>🟥 MANDATORY</code> | Must be present before the holding can become active, or before the named related record can be created. |
| <code>🟧 CONDITIONAL</code> | Must be present only when the stated feature or circumstance applies. |
| <code>🟦 OPTIONAL</code> | May be supplied; absence means unknown or not applicable. |
| <code>🟪 SYSTEM</code> | Generated, calculated or lifecycle-managed by Vittavaan rather than entered freely by a user. |

A note may also identify sensitive information. Sensitive values must be encrypted or represented by a protected reference and masked in normal responses.

## Quantity rule audit

The `holdings.quantity` requirement was reviewed across all 93 asset subtypes. It is mandatory for an active holding in 16 explicitly unit based subtypes (listed below). For other subtypes, it is conditional when the holding is represented in units; it is not needed for assets such as a bank account or a property. The physical database column remains nullable because it serves all asset types.

- [`PUBLIC_EQUITY`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-public-equity)
- [`GOVERNMENT_BOND`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-government-bond)
- [`MUNICIPAL_BOND`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-municipal-bond)
- [`CORPORATE_BOND`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-corporate-bond)
- [`DEBENTURE`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-debenture)
- [`COMMERCIAL_PAPER`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-commercial-paper)
- [`CERTIFICATE_OF_DEPOSIT`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-certificate-of-deposit)
- [`MUTUAL_FUND`](asset_field_matrix/FUND.md#asset-subtype-mutual-fund)
- [`MONEY_MARKET_FUND`](asset_field_matrix/FUND.md#asset-subtype-money-market-fund)
- [`REIT`](asset_field_matrix/REAL_ASSET.md#asset-subtype-reit)
- [`CRYPTO_TOKEN`](asset_field_matrix/DIGITAL_ASSET.md#asset-subtype-crypto-token)
- [`NFT`](asset_field_matrix/DIGITAL_ASSET.md#asset-subtype-nft)
- [`TOKENIZED_ASSET`](asset_field_matrix/DIGITAL_ASSET.md#asset-subtype-tokenized-asset)
- [`CAT_BOND`](asset_field_matrix/INSURANCE_SECURITY.md#asset-subtype-cat-bond)
- [`EQUITY_OPTION`](asset_field_matrix/DERIVATIVE.md#asset-subtype-equity-option)
- [`CONVERTIBLE_SECURITY`](asset_field_matrix/DERIVATIVE.md#asset-subtype-convertible-security)

## Asset subtype index

- **`TRAD_SECURITY`**
  - [`PUBLIC_EQUITY`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-public-equity)
  - [`GOVERNMENT_BOND`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-government-bond)
  - [`MUNICIPAL_BOND`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-municipal-bond)
  - [`CORPORATE_BOND`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-corporate-bond)
  - [`DEBENTURE`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-debenture)
  - [`COMMERCIAL_PAPER`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-commercial-paper)
  - [`CERTIFICATE_OF_DEPOSIT`](asset_field_matrix/TRAD_SECURITY.md#asset-subtype-certificate-of-deposit)
- **`CASH`**
  - [`SAVINGS_ACCOUNT`](asset_field_matrix/CASH.md#asset-subtype-savings-account)
  - [`CURRENT_ACCOUNT`](asset_field_matrix/CASH.md#asset-subtype-current-account)
  - [`FIXED_DEPOSIT`](asset_field_matrix/CASH.md#asset-subtype-fixed-deposit)
  - [`RECURRING_DEPOSIT`](asset_field_matrix/CASH.md#asset-subtype-recurring-deposit)
  - [`SWEEP_ACCOUNT`](asset_field_matrix/CASH.md#asset-subtype-sweep-account)
  - [`POSITIVE_CARD_BALANCE`](asset_field_matrix/CASH.md#asset-subtype-positive-card-balance)
  - [`SAFE_DEPOSIT_LOCKER`](asset_field_matrix/CASH.md#asset-subtype-safe-deposit-locker)
- **`FUND`**
  - [`MUTUAL_FUND`](asset_field_matrix/FUND.md#asset-subtype-mutual-fund)
  - [`MONEY_MARKET_FUND`](asset_field_matrix/FUND.md#asset-subtype-money-market-fund)
  - [`PMS`](asset_field_matrix/FUND.md#asset-subtype-pms)
  - [`AIF`](asset_field_matrix/FUND.md#asset-subtype-aif)
- **`CREDIT_ASSET`**
  - [`P2P_LOAN`](asset_field_matrix/CREDIT_ASSET.md#asset-subtype-p2p-loan)
  - [`DIRECT_LENDING`](asset_field_matrix/CREDIT_ASSET.md#asset-subtype-direct-lending)
  - [`MEZZANINE_DEBT`](asset_field_matrix/CREDIT_ASSET.md#asset-subtype-mezzanine-debt)
  - [`MICROFINANCE_INTEREST`](asset_field_matrix/CREDIT_ASSET.md#asset-subtype-microfinance-interest)
  - [`MORTGAGE_CREDIT`](asset_field_matrix/CREDIT_ASSET.md#asset-subtype-mortgage-credit)
  - [`WORKING_CAPITAL_CREDIT`](asset_field_matrix/CREDIT_ASSET.md#asset-subtype-working-capital-credit)
- **`PENSION_SAVINGS`**
  - [`EPF`](asset_field_matrix/PENSION_SAVINGS.md#asset-subtype-epf)
  - [`PPF`](asset_field_matrix/PENSION_SAVINGS.md#asset-subtype-ppf)
  - [`NPS`](asset_field_matrix/PENSION_SAVINGS.md#asset-subtype-nps)
  - [`SSY`](asset_field_matrix/PENSION_SAVINGS.md#asset-subtype-ssy)
  - [`SCSS`](asset_field_matrix/PENSION_SAVINGS.md#asset-subtype-scss)
  - [`POST_OFFICE_SAVINGS`](asset_field_matrix/PENSION_SAVINGS.md#asset-subtype-post-office-savings)
  - [`APY`](asset_field_matrix/PENSION_SAVINGS.md#asset-subtype-apy)
  - [`GRATUITY`](asset_field_matrix/PENSION_SAVINGS.md#asset-subtype-gratuity)
  - [`ANNUITY`](asset_field_matrix/PENSION_SAVINGS.md#asset-subtype-annuity)
- **`PRIVATE_CAPITAL`**
  - [`VENTURE_CAPITAL`](asset_field_matrix/PRIVATE_CAPITAL.md#asset-subtype-venture-capital)
  - [`GROWTH_BUYOUT`](asset_field_matrix/PRIVATE_CAPITAL.md#asset-subtype-growth-buyout)
  - [`DISTRESSED_INVESTMENT`](asset_field_matrix/PRIVATE_CAPITAL.md#asset-subtype-distressed-investment)
  - [`SYNDICATE_INTEREST`](asset_field_matrix/PRIVATE_CAPITAL.md#asset-subtype-syndicate-interest)
  - [`CONVERTIBLE_NOTE`](asset_field_matrix/PRIVATE_CAPITAL.md#asset-subtype-convertible-note)
  - [`ESOP_OPTION`](asset_field_matrix/PRIVATE_CAPITAL.md#asset-subtype-esop-option)
- **`HEDGE_STRATEGY`**
  - [`HEDGE_FUND`](asset_field_matrix/HEDGE_STRATEGY.md#asset-subtype-hedge-fund)
  - [`LONG_SHORT`](asset_field_matrix/HEDGE_STRATEGY.md#asset-subtype-long-short)
  - [`GLOBAL_MACRO`](asset_field_matrix/HEDGE_STRATEGY.md#asset-subtype-global-macro)
  - [`ARBITRAGE_STRATEGY`](asset_field_matrix/HEDGE_STRATEGY.md#asset-subtype-arbitrage-strategy)
- **`REAL_ASSET`**
  - [`RESIDENTIAL_PROPERTY`](asset_field_matrix/REAL_ASSET.md#asset-subtype-residential-property)
  - [`COMMERCIAL_PROPERTY`](asset_field_matrix/REAL_ASSET.md#asset-subtype-commercial-property)
  - [`LAND`](asset_field_matrix/REAL_ASSET.md#asset-subtype-land)
  - [`AGRICULTURAL_LAND`](asset_field_matrix/REAL_ASSET.md#asset-subtype-agricultural-land)
  - [`REIT`](asset_field_matrix/REAL_ASSET.md#asset-subtype-reit)
  - [`FRACTIONAL_PROPERTY`](asset_field_matrix/REAL_ASSET.md#asset-subtype-fractional-property)
  - [`PARKING_STORAGE_UNIT`](asset_field_matrix/REAL_ASSET.md#asset-subtype-parking-storage-unit)
- **`INFRASTRUCTURE`**
  - [`TOLL_ROAD`](asset_field_matrix/INFRASTRUCTURE.md#asset-subtype-toll-road)
  - [`AIRPORT`](asset_field_matrix/INFRASTRUCTURE.md#asset-subtype-airport)
  - [`PIPELINE`](asset_field_matrix/INFRASTRUCTURE.md#asset-subtype-pipeline)
  - [`PPP_PROJECT`](asset_field_matrix/INFRASTRUCTURE.md#asset-subtype-ppp-project)
  - [`ENERGY_PROJECT`](asset_field_matrix/INFRASTRUCTURE.md#asset-subtype-energy-project)
- **`TANGIBLE`**
  - [`PRECIOUS_METAL`](asset_field_matrix/TANGIBLE.md#asset-subtype-precious-metal)
  - [`COMMODITY_INTEREST`](asset_field_matrix/TANGIBLE.md#asset-subtype-commodity-interest)
  - [`ART`](asset_field_matrix/TANGIBLE.md#asset-subtype-art)
  - [`WINE`](asset_field_matrix/TANGIBLE.md#asset-subtype-wine)
  - [`COINS_STAMPS`](asset_field_matrix/TANGIBLE.md#asset-subtype-coins-stamps)
  - [`JEWELLERY`](asset_field_matrix/TANGIBLE.md#asset-subtype-jewellery)
  - [`OTHER_COLLECTIBLE`](asset_field_matrix/TANGIBLE.md#asset-subtype-other-collectible)
- **`DIGITAL_ASSET`**
  - [`CRYPTO_TOKEN`](asset_field_matrix/DIGITAL_ASSET.md#asset-subtype-crypto-token)
  - [`NFT`](asset_field_matrix/DIGITAL_ASSET.md#asset-subtype-nft)
  - [`TOKENIZED_ASSET`](asset_field_matrix/DIGITAL_ASSET.md#asset-subtype-tokenized-asset)
  - [`DOMAIN_NAME`](asset_field_matrix/DIGITAL_ASSET.md#asset-subtype-domain-name)
- **`TRUST_INTEREST`**
  - [`TRUST_BENEFICIAL_INTEREST`](asset_field_matrix/TRUST_INTEREST.md#asset-subtype-trust-beneficial-interest)
- **`CONTRACT_RIGHT`**
  - [`RECEIVABLE`](asset_field_matrix/CONTRACT_RIGHT.md#asset-subtype-receivable)
  - [`EARNOUT`](asset_field_matrix/CONTRACT_RIGHT.md#asset-subtype-earnout)
  - [`PROFIT_SHARE`](asset_field_matrix/CONTRACT_RIGHT.md#asset-subtype-profit-share)
  - [`ROYALTY`](asset_field_matrix/CONTRACT_RIGHT.md#asset-subtype-royalty)
  - [`FRANCHISE`](asset_field_matrix/CONTRACT_RIGHT.md#asset-subtype-franchise)
  - [`LITIGATION_FINANCE`](asset_field_matrix/CONTRACT_RIGHT.md#asset-subtype-litigation-finance)
  - [`SPORTS_INTEREST`](asset_field_matrix/CONTRACT_RIGHT.md#asset-subtype-sports-interest)
  - [`ENTERTAINMENT_RIGHT`](asset_field_matrix/CONTRACT_RIGHT.md#asset-subtype-entertainment-right)
- **`INSURANCE_SECURITY`**
  - [`CAT_BOND`](asset_field_matrix/INSURANCE_SECURITY.md#asset-subtype-cat-bond)
- **`DERIVATIVE`**
  - [`EQUITY_OPTION`](asset_field_matrix/DERIVATIVE.md#asset-subtype-equity-option)
  - [`FUTURE`](asset_field_matrix/DERIVATIVE.md#asset-subtype-future)
  - [`FX_FORWARD_SWAP`](asset_field_matrix/DERIVATIVE.md#asset-subtype-fx-forward-swap)
  - [`COMMODITY_DERIVATIVE`](asset_field_matrix/DERIVATIVE.md#asset-subtype-commodity-derivative)
  - [`CONVERTIBLE_SECURITY`](asset_field_matrix/DERIVATIVE.md#asset-subtype-convertible-security)
- **`SPECIALIZED`**
  - [`AGRI_BUSINESS`](asset_field_matrix/SPECIALIZED.md#asset-subtype-agri-business)
  - [`CARBON_CREDIT`](asset_field_matrix/SPECIALIZED.md#asset-subtype-carbon-credit)
  - [`SHIPPING_INTEREST`](asset_field_matrix/SPECIALIZED.md#asset-subtype-shipping-interest)
  - [`SPACE_INVESTMENT`](asset_field_matrix/SPECIALIZED.md#asset-subtype-space-investment)
  - [`DATA_AI_INTEREST`](asset_field_matrix/SPECIALIZED.md#asset-subtype-data-ai-interest)
  - [`BIOTECH_RIGHT`](asset_field_matrix/SPECIALIZED.md#asset-subtype-biotech-right)
- **`VEHICLE`**
  - [`ROAD_VEHICLE`](asset_field_matrix/VEHICLE.md#asset-subtype-road-vehicle)
  - [`AIRCRAFT`](asset_field_matrix/VEHICLE.md#asset-subtype-aircraft)
  - [`VESSEL`](asset_field_matrix/VEHICLE.md#asset-subtype-vessel)
  - [`FRACTIONAL_VEHICLE`](asset_field_matrix/VEHICLE.md#asset-subtype-fractional-vehicle)
- **`TAX_ASSET`**
  - [`GST_INPUT_CREDIT`](asset_field_matrix/TAX_ASSET.md#asset-subtype-gst-input-credit)
- **`OTHER`**
  - [`CUSTOM_ASSET`](asset_field_matrix/OTHER.md#asset-subtype-custom-asset)

Each linked class page contains the complete field table for every subtype in that class. Open a subtype there to see its fields, including the shared holding, ownership, valuation and related table columns.

## Completeness and maintenance rules

- This version contains **93 asset subtypes** and **888 expanded subtype-field rows**.
- The 93 self-contained subtype tables contain **16786 total field rows**, including repeated normalized and cross-cutting fields.
- Inherited profiles—such as debentures inheriting corporate-bond fields—are expanded here so readers do not have to jump between sections.
- The source of truth for validation details remains `07_India_Subtype_Attribute_Schemas.md`; this matrix must be regenerated whenever that source changes.
- A subtype field cannot be moved into or out of normalized storage without updating the database design, API contract, migration plan and tests.
- Mandatory is a business activation rule. Database `NOT NULL` constraints are documented separately in `03_Database_Design.md`.

