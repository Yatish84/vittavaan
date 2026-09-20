# Phase 4 — Object Design: Class Interfaces

> **OOSE Phase:** Object Design
> **Purpose:** Defines the complete Python type-annotated interface for every service, repository, and key Pydantic schema. Developers implement against these contracts. No method may be added, removed, or have its signature changed during implementation without updating this document.
> **Python version:** 3.12 (uses modern union syntax `X | Y`, `list[X]`, etc.)
> **Status:** Draft

---

## 1. Core Types (Shared Across All Interfaces)

```python
# backend/app/core/types.py
"""
All shared types used across the entire codebase.
Import from here — never redefine elsewhere.
"""
from typing import Annotated
from uuid import UUID
from datetime import date, datetime
from pydantic import Field

# === MONEY ===
# All monetary values are integers in paise. Never float.
MinorUnits = Annotated[int, Field(ge=0, description="Amount in paise (1 INR = 100 paise)")]
# Note: net_worth can be negative, so use plain int for net worth fields.

# === PERCENTAGE ===
# Percentages are floats in [0.0, 100.0] inclusive.
Percentage = Annotated[float, Field(ge=0.0, le=100.0)]

# === ENUMS ===
from enum import StrEnum

class AssetTypeEnum(StrEnum):
    LIQUID = "LIQUID"
    REAL_ESTATE = "REAL_ESTATE"
    ALTERNATIVE = "ALTERNATIVE"

class VerificationLevelEnum(StrEnum):
    SELF_DECLARED = "SELF_DECLARED"
    DOCUMENTED = "DOCUMENTED"
    VERIFIED = "VERIFIED"
    ACCEPTED = "ACCEPTED"

    @classmethod
    def ordered_value(cls, level: "VerificationLevelEnum") -> int:
        return {cls.SELF_DECLARED: 0, cls.DOCUMENTED: 1,
                cls.VERIFIED: 2, cls.ACCEPTED: 3}[level]

class StalenessStatusEnum(StrEnum):
    CURRENT = "CURRENT"
    APPROACHING_STALE = "APPROACHING_STALE"
    STALE = "STALE"

class ConnectionStatusEnum(StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REVOKED = "REVOKED"

class GoalStatusEnum(StrEnum):
    ON_TRACK = "ON_TRACK"
    SHORT = "SHORT"
    AT_RISK = "AT_RISK"
    FUNDED = "FUNDED"

class PerformanceBasisEnum(StrEnum):
    VERIFIED = "VERIFIED"
    ESTIMATED = "ESTIMATED"
    MIXED = "MIXED"
    PARTIAL = "PARTIAL"

class RoleEnum(StrEnum):
    INVESTOR = "INVESTOR"
    ADVISOR = "ADVISOR"
    ADMIN = "ADMIN"

class TransactionTypeEnum(StrEnum):
    INFLOW = "INFLOW"
    OUTFLOW = "OUTFLOW"
    BUY = "BUY"
    SELL = "SELL"
    RENT = "RENT"
    DIVIDEND = "DIVIDEND"
    INTEREST = "INTEREST"
    EMI_PAYMENT = "EMI_PAYMENT"
    GIFT_OUT = "GIFT_OUT"
    GIFT_IN = "GIFT_IN"

class LiquidSubTypeEnum(StrEnum):
    BANK_SAVINGS = "BANK_SAVINGS"
    BANK_FD = "BANK_FD"
    EQUITY = "EQUITY"
    MUTUAL_FUND = "MUTUAL_FUND"
    ETF = "ETF"
    PPF = "PPF"
    EPF = "EPF"
    NPS = "NPS"
    CRYPTO = "CRYPTO"
    BONDS = "BONDS"
    UNLISTED_EQUITY = "UNLISTED_EQUITY"

class PropertyTypeEnum(StrEnum):
    LAND = "LAND"
    RESIDENTIAL = "RESIDENTIAL"
    COMMERCIAL = "COMMERCIAL"

class RelationshipEnum(StrEnum):
    SPOUSE = "SPOUSE"
    CHILD = "CHILD"
    PARENT = "PARENT"
    SIBLING = "SIBLING"
    IN_LAW = "IN_LAW"
    GRANDCHILD = "GRANDCHILD"
    GRANDPARENT = "GRANDPARENT"
    OTHER = "OTHER"

class GiftOccasionEnum(StrEnum):
    MARRIAGE = "MARRIAGE"
    INHERITANCE = "INHERITANCE"
    GENERAL = "GENERAL"
    CONTEMPLATION_OF_DEATH = "CONTEMPLATION_OF_DEATH"

class TaxTreatmentEnum(StrEnum):
    EXEMPT_RELATIVE = "EXEMPT_RELATIVE"
    EXEMPT_OCCASION = "EXEMPT_OCCASION"
    TAXABLE_FULL = "TAXABLE_FULL"
    TAXABLE_PARTIAL = "TAXABLE_PARTIAL"
```

---

## 2. Service Layer Interfaces (Protocol Classes)

### 2.1 WealthAndOwnershipEngineProtocol

```python
# backend/app/services/protocols.py
from typing import Protocol

class WealthAndOwnershipEngineProtocol(Protocol):
    """
    Contract for WealthAndOwnershipEngine.
    All monetary outputs are in minor units (paise).
    All percentage outputs are floats in [0.0, 100.0].
    """

    async def calculate_net_worth(
        self,
        portfolio_id: UUID,
        *,
        as_of: datetime | None = None,
    ) -> NetWorthResult: ...

    async def calculate_attributed_value(
        self,
        asset: Asset,
    ) -> int:
        """Always returns integer (paise). Floor applied."""
        ...

    async def calculate_asset_class_breakdown(
        self,
        portfolio_id: UUID,
    ) -> AssetClassBreakdown: ...

    async def calculate_net_worth_waterfall(
        self,
        portfolio_id: UUID,
        period: Literal["1M", "3M", "6M", "1Y"],
    ) -> WaterfallResult: ...

    async def calculate_household_net_worth(
        self,
        user_id: UUID,
    ) -> HouseholdNetWorthResult: ...
```

### 2.2 ValuationAndVerificationEngineProtocol

```python
class ValuationAndVerificationEngineProtocol(Protocol):

    async def calculate_verified_wealth_pct(
        self,
        portfolio_id: UUID,
    ) -> float: ...

    async def check_staleness(
        self,
        asset: Asset,
    ) -> StalenessResult: ...

    async def get_stale_assets(
        self,
        portfolio_id: UUID,
    ) -> list[StaleAssetSummary]: ...

    async def evaluate_verification_level(
        self,
        asset: Asset,
        documents: list[Document],
    ) -> VerificationLevelEnum: ...

    async def calculate_valuation_age_days(
        self,
        asset: Asset,
    ) -> int: ...
```

### 2.3 CashFlowAndDebtEngineProtocol

```python
class CashFlowAndDebtEngineProtocol(Protocol):

    async def calculate_monthly_surplus(
        self,
        portfolio_id: UUID,
        month: YearMonth,
    ) -> MonthlySurplusResult: ...

    async def calculate_debt_service_ratio(
        self,
        portfolio_id: UUID,
    ) -> DSRResult: ...

    async def calculate_amortization_schedule(
        self,
        liability: Liability,
    ) -> list[AmortizationRow]: ...

    async def calculate_savings_rate(
        self,
        portfolio_id: UUID,
        period: DateRange,
    ) -> float | None: ...

    async def group_income_by_source(
        self,
        portfolio_id: UUID,
        period: DateRange,
    ) -> list[IncomeGroup]: ...

    async def group_expenses_by_category(
        self,
        portfolio_id: UUID,
        period: DateRange,
    ) -> list[ExpenseGroup]: ...
```

### 2.4 PerformanceAndAttributionEngineProtocol

```python
class PerformanceAndAttributionEngineProtocol(Protocol):

    async def calculate_xirr(
        self,
        portfolio_id: UUID,
        start: date,
        end: date,
    ) -> XirrResult: ...

    async def calculate_twrr(
        self,
        portfolio_id: UUID,
        start: date,
        end: date,
    ) -> TwrrResult: ...

    async def calculate_max_drawdown(
        self,
        portfolio_id: UUID,
        period: DateRange,
    ) -> DrawdownResult: ...

    async def calculate_attribution(
        self,
        portfolio_id: UUID,
        period: DateRange,
    ) -> AttributionResult: ...

    async def calculate_benchmark_return(
        self,
        benchmark_id: str,
        period: DateRange,
    ) -> float: ...

    async def calculate_excess_return(
        self,
        portfolio_id: UUID,
        benchmark_id: str,
        period: DateRange,
    ) -> float: ...
```

### 2.5 PlanningAndScenarioEngineProtocol

```python
class PlanningAndScenarioEngineProtocol(Protocol):

    async def calculate_goal_projected_value(
        self,
        goal: FinancialGoal,
        assumptions: PlanAssumptions,
    ) -> int:  # paise
        ...

    async def calculate_funding_gap(
        self,
        goal: FinancialGoal,
        assumptions: PlanAssumptions,
    ) -> FundingGapResult: ...

    async def model_invest_vs_prepay(
        self,
        params: PrepayScenarioParams,
    ) -> PrepayScenarioResult: ...

    async def get_upcoming_events(
        self,
        user_id: UUID,
        days_ahead: int = 90,
    ) -> list[FinancialEvent]: ...
```

### 2.6 ConsentAndMarketplaceEngineProtocol

```python
class ConsentAndMarketplaceEngineProtocol(Protocol):

    async def get_peer_portfolio(
        self,
        requesting_user_id: UUID,
        data_owner_id: UUID,
        db: AsyncSession,
    ) -> dict: ...

    async def evaluate_data_access(
        self,
        requesting_user_id: UUID,
        data_owner_id: UUID,
        db: AsyncSession,
    ) -> AccessDecision: ...

    def filter_payload(
        self,
        payload: dict,
        permitted_fields: list[str],
    ) -> dict: ...

    async def check_expiring_consents(
        self,
        user_id: UUID,
        days_ahead: int = 7,
    ) -> list[ExpiringConsentAlert]: ...

    async def expire_stale_consents(
        self,
        db: AsyncSession,
    ) -> list[UUID]:  # list of expired connection_ids
        ...

    async def evaluate_advisor_match(
        self,
        user_id: UUID,
        advisors: list[AdvisorProfile],
    ) -> list[AdvisorMatch]: ...

    async def check_reidentification_risk(
        self,
        profile: BorrowerProfile,
    ) -> ReidentificationRisk: ...
```

### 2.7 EstatePlanningControlProtocol

```python
class EstatePlanningControlProtocol(Protocol):

    async def allocate_inheritance(
        self,
        asset_id: UUID,
        beneficiary_id: UUID,
        percentage_share: float,
        distribution_conditions: str | None,
        db: AsyncSession,
    ) -> InheritanceAllocation: ...

    async def validate_total_allocation(
        self,
        asset_id: UUID,
        proposed_addition: float,
        db: AsyncSession,
    ) -> AllocationValidation: ...

    async def calculate_estate_coverage(
        self,
        user_id: UUID,
        db: AsyncSession,
    ) -> EstateCoverageResult: ...

    async def analyse_will_coverage(
        self,
        user_id: UUID,
        db: AsyncSession,
    ) -> WillCoverageResult: ...

    async def get_default_succession_shares(
        self,
        user_id: UUID,
        db: AsyncSession,
    ) -> list[SuccessionShare]: ...

    async def identify_nominee_mismatches(
        self,
        user_id: UUID,
        db: AsyncSession,
    ) -> list[NomineeMismatch]: ...
```

### 2.8 GiftRuleEngineProtocol

```python
class GiftRuleEngineProtocol(Protocol):

    async def evaluate_gift_eligibility(
        self,
        asset: Asset,
    ) -> GiftEligibility: ...

    async def evaluate_gift_tax_status(
        self,
        donor_id: UUID,
        recipient: HouseholdMember,
        asset: Asset,
        occasion: GiftOccasionEnum,
        transfer_date: date,
    ) -> GiftTaxResult: ...

    async def calculate_stamp_duty(
        self,
        asset: RealEstateAsset,
        jurisdiction: str,
        relationship: RelationshipEnum,
        transfer_date: date,
    ) -> StampDutyResult: ...

    async def calculate_total_transfer_cost(
        self,
        transfer: GiftTransfer,
    ) -> int:  # paise
        ...

    async def evaluate_recipient_cost_basis(
        self,
        transfer: GiftTransfer,
    ) -> CostBasisResult: ...

    async def check_annual_gift_cumulative(
        self,
        donor_id: UUID,
        recipient_member_id: UUID,
        new_amount_minor_units: int,
        financial_year: IndianFinancialYear,
        db: AsyncSession,
    ) -> CumulativeGiftCheck: ...
```

### 2.9 DashboardFacadeProtocol

```python
class DashboardFacadeProtocol(Protocol):

    async def get_dashboard_metrics(
        self,
        user_id: UUID,
        db: AsyncSession,
        as_of: datetime | None = None,
    ) -> DashboardPayload: ...

    async def get_net_worth_trend(
        self,
        user_id: UUID,
        months: int = 13,
    ) -> list[NetWorthTrendPoint]: ...

    async def get_alerts(
        self,
        user_id: UUID,
    ) -> list[DashboardAlert]: ...
```

### 2.10 AuthGatewayControlProtocol

```python
class AuthGatewayControlProtocol(Protocol):

    async def verify_handshake(
        self,
        jwt_token: str,
    ) -> JWTClaims: ...

    async def initialize_user(
        self,
        jwt_claims: JWTClaims,
        db: AsyncSession,
    ) -> tuple[User, bool]:  # (user, is_new_user)
        ...

    async def create_session(
        self,
        user_id: UUID,
        jwt_claims: JWTClaims,
        db: AsyncSession,
    ) -> LocalSession: ...

    async def terminate_all_sessions(
        self,
        user_id: UUID,
        db: AsyncSession,
    ) -> int:  # number of sessions terminated
        ...
```

---

## 3. Repository Interfaces (Protocol Classes)

```python
# backend/app/repositories/protocols.py

class AssetRepositoryProtocol(Protocol):
    async def get(self, asset_id: UUID) -> Asset | None: ...
    async def list_active(self, portfolio_id: UUID) -> list[Asset]: ...
    async def list_by_type(self, portfolio_id: UUID, asset_type: AssetTypeEnum) -> list[Asset]: ...
    async def create(self, data: AssetCreateData, portfolio_id: UUID) -> Asset: ...
    async def update(self, asset_id: UUID, data: AssetUpdateData) -> Asset: ...
    async def soft_delete(self, asset_id: UUID) -> None: ...


class TransactionRepositoryProtocol(Protocol):
    """Append-only — no update or delete methods exposed."""
    async def get(self, transaction_id: UUID) -> Transaction | None: ...
    async def list_for_portfolio(
        self,
        portfolio_id: UUID,
        *,
        start_date: date | None = None,
        end_date: date | None = None,
        transaction_type: TransactionTypeEnum | None = None,
        asset_id: UUID | None = None,
    ) -> list[Transaction]: ...
    async def insert(self, data: TransactionCreateData) -> Transaction: ...
    # NO update(), NO delete() — append-only by design


class FinancialSnapshotRepositoryProtocol(Protocol):
    """Append-only — no update or delete methods exposed."""
    async def get_latest(self, portfolio_id: UUID) -> FinancialSnapshot | None: ...
    async def get_at_date(self, portfolio_id: UUID, target_date: date) -> FinancialSnapshot | None: ...
    async def list_range(
        self,
        portfolio_id: UUID,
        start_date: date,
        end_date: date,
    ) -> list[FinancialSnapshot]: ...
    async def insert(self, snapshot: FinancialSnapshotCreateData) -> FinancialSnapshot: ...
    # NO update(), NO delete()


class ConnectionRepositoryProtocol(Protocol):
    async def get(self, connection_id: UUID) -> Connection | None: ...
    async def find(
        self,
        requester_id: UUID,
        recipient_id: UUID,
    ) -> Connection | None: ...
    async def list_for_user(
        self,
        user_id: UUID,
        status: ConnectionStatusEnum | None = None,
    ) -> list[Connection]: ...
    async def create(self, data: ConnectionCreateData) -> Connection: ...
    async def update_status(self, connection_id: UUID, status: ConnectionStatusEnum) -> Connection: ...
    async def update_consent(self, connection_id: UUID, consent_data: ConsentUpdateData) -> Connection: ...
    async def list_expiring(
        self,
        before: datetime,
    ) -> list[Connection]:
        """List connections where consent_expires_at <= before and permissions != '[]'."""
        ...


class GiftRuleRepositoryProtocol(Protocol):
    async def get_applicable_rule(
        self,
        jurisdiction: str,
        rule_type: str,
        relationship_category: str | None,
        as_of_date: date,
    ) -> GiftRule | None: ...
    async def list_all_active(self) -> list[GiftRule]: ...
    async def create(self, data: GiftRuleCreateData) -> GiftRule: ...
    # Update is NOT exposed — rules are immutable; new rules are new records


class DocumentRepositoryProtocol(Protocol):
    async def get(self, document_id: UUID) -> Document | None: ...
    async def list_for_owner(self, owner_id: UUID) -> list[Document]: ...
    async def list_for_asset(self, asset_id: UUID) -> list[Document]: ...
    async def create(self, data: DocumentCreateData) -> Document: ...
    async def update_scan_status(self, document_id: UUID, status: str) -> Document: ...
    async def soft_delete(self, document_id: UUID) -> None: ...
```

---

## 4. Key Pydantic Schemas

```python
# backend/app/schemas/

# --- Dashboard ---
class DashboardPayload(BaseModel):
    net_worth_minor_units: int              # can be negative
    total_assets_minor_units: MinorUnits
    total_liabilities_minor_units: MinorUnits
    mom_change_minor_units: int             # can be negative
    mom_change_pct: float
    ytd_change_pct: float
    verified_wealth_pct: Percentage
    income_this_month_minor_units: MinorUnits
    expenses_this_month_minor_units: MinorUnits
    surplus_this_month_minor_units: int     # can be negative
    asset_allocation: AssetClassBreakdown
    waterfall: list[WaterfallBar]
    alerts: list[DashboardAlert]
    provenance: ProvenanceMetadata


class AssetClassBreakdown(BaseModel):
    liquid_pct: Percentage
    real_estate_pct: Percentage
    alternative_pct: Percentage

    @model_validator(mode="after")
    def percentages_sum_to_100(self) -> "AssetClassBreakdown":
        total = self.liquid_pct + self.real_estate_pct + self.alternative_pct
        assert abs(total - 100.0) < 1e-4 or total == 0.0, \
            f"Asset class percentages must sum to 100, got {total}"
        return self


class WaterfallBar(BaseModel):
    label: str
    value_minor_units: int   # can be negative (decline)
    category: AssetTypeEnum


class DashboardAlert(BaseModel):
    alert_type: str  # "STALE_VALUATION" | "CONSENT_EXPIRY" | "UNALLOCATED_ASSET" | etc.
    severity: Literal["INFO", "WARNING", "CRITICAL"]
    title: str
    message: str
    action_url: str | None = None
    asset_id: UUID | None = None
    connection_id: UUID | None = None


# --- Provenance (used in all calculated responses) ---
class ProvenanceMetadata(BaseModel):
    as_of: datetime
    calculation_version: str
    source_ids: list[UUID] = Field(default_factory=list)
    is_partial: bool
    performance_basis: PerformanceBasisEnum | None = None


# --- Net Worth ---
class NetWorthResult(BaseModel):
    total_assets_minor_units: MinorUnits
    total_liabilities_minor_units: MinorUnits
    net_worth_minor_units: int
    provenance: ProvenanceMetadata

    @property
    def net_worth_is_negative(self) -> bool:
        return self.net_worth_minor_units < 0


# --- Performance ---
class XirrResult(BaseModel):
    xirr_pct: float | None = None
    error_code: str | None = None   # None if xirr_pct is present
    cashflow_count: int
    provenance: ProvenanceMetadata

    @model_validator(mode="after")
    def exactly_one_of_xirr_or_error(self) -> "XirrResult":
        has_value = self.xirr_pct is not None
        has_error = self.error_code is not None
        assert has_value ^ has_error, "Exactly one of xirr_pct or error_code must be set"
        return self


class TwrrResult(BaseModel):
    twrr_pct: float | None = None
    twrr_annualised_pct: float | None = None
    sub_period_count: int
    error_code: str | None = None
    provenance: ProvenanceMetadata


class DrawdownResult(BaseModel):
    max_drawdown_pct: float  # always <= 0.0
    drawdown_start_date: date | None = None
    drawdown_trough_date: date | None = None
    recovery_months: int | None = None
    provenance: ProvenanceMetadata


class AttributionResult(BaseModel):
    liquid_contribution_pct: float
    real_estate_contribution_pct: float
    alternative_contribution_pct: float
    total_return_pct: float
    reconciliation_error_pct: float  # Should be near 0
    provenance: ProvenanceMetadata


# --- Planning ---
class FundingGapResult(BaseModel):
    goal_id: UUID
    target_today_minor_units: MinorUnits
    target_nominal_minor_units: MinorUnits
    projected_value_minor_units: MinorUnits
    funding_gap_minor_units: int          # negative = overfunded (good)
    goal_status: GoalStatusEnum
    years_to_target: int
    assumptions_used: dict[str, float]    # {"equity_growth_pct": 12.0, ...}
    provenance: ProvenanceMetadata


class PrepayScenarioParams(BaseModel):
    liability_id: UUID
    monthly_surplus_minor_units: MinorUnits
    assumed_investment_return_pct: float
    months_to_compare: int = Field(ge=1, le=360)


class PrepayScenarioResult(BaseModel):
    invest_terminal_value_minor_units: int
    prepay_interest_saved_minor_units: MinorUnits
    crossover_return_pct: float
    recommended: Literal["INVEST", "PREPAY", "NEUTRAL"]
    explanation: str  # Plain-language: "At your assumed 12% return, investing beats prepayment."


# --- Gift Evaluation ---
class GiftEvaluationResult(BaseModel):
    eligibility: Literal["ELIGIBLE", "BLOCKED"]
    block_reason: str | None = None   # Set if eligibility == "BLOCKED"
    tax_status: TaxTreatmentEnum | None = None
    applicable_rule_reference: str | None = None
    rule_version: str | None = None
    stamp_duty_minor_units: MinorUnits | None = None
    registration_fee_minor_units: MinorUnits | None = None
    total_transfer_cost_minor_units: int | None = None
    recipient_cost_basis_minor_units: MinorUnits | None = None
    recipient_holding_period_start: date | None = None
    warnings: list[str] = Field(default_factory=list)


# --- Consent ---
class AccessDecision(BaseModel):
    allowed: bool
    reason: Literal[
        "CONSENT_VALID",
        "NO_CONNECTION",
        "CONSENT_EXPIRED",
        "FIELD_NOT_PERMITTED",
    ]
    permitted_fields: list[str] = Field(default_factory=list)


class ConsentUpdateRequest(BaseModel):
    permitted_fields: list[str] = Field(min_length=1)
    consent_purpose: str = Field(min_length=5)
    consent_expires_at: datetime

    @field_validator("consent_expires_at")
    @classmethod
    def expiry_must_be_future(cls, v: datetime) -> datetime:
        if v <= datetime.now(UTC):
            raise ValueError("consent_expires_at must be in the future")
        return v


# --- Asset Creation ---
class AssetCreateRequest(BaseModel):
    asset_type: AssetTypeEnum
    name: str = Field(min_length=1, max_length=200)
    ownership_split_pct: Percentage
    purchase_price_minor_units: MinorUnits = 0
    current_value_minor_units: MinorUnits
    purchase_date: date
    currency: str = "INR"
    verification_level: VerificationLevelEnum = VerificationLevelEnum.SELF_DECLARED
    valuation_method: str = "USER_ESTIMATE"
    valuation_as_of: datetime | None = None
    notes: str | None = None

    # Subtype fields (only required when asset_type matches)
    institution_name: str | None = None
    liquid_sub_type: LiquidSubTypeEnum | None = None
    ticker_symbol: str | None = None
    scheme_code: str | None = None
    quantity_held: float | None = None

    property_type: PropertyTypeEnum | None = None
    location_address: str | None = None
    area_sqft: float | None = None
    price_per_sqft_minor_units: MinorUnits | None = None
    title_verification_status: str = "UNCHECKED"
    encumbrance_status: str = "CLEAR"
    mutation_status: str = "PENDING"

    collection_type: str | None = None
    last_appraisal_date: date | None = None
    appraiser_name: str | None = None

    @model_validator(mode="after")
    def validate_subtype_fields(self) -> "AssetCreateRequest":
        if self.asset_type == AssetTypeEnum.LIQUID:
            if self.liquid_sub_type is None:
                raise ValueError("liquid_sub_type is required for LIQUID assets")
        if self.asset_type == AssetTypeEnum.REAL_ESTATE:
            if self.property_type is None or self.location_address is None:
                raise ValueError("property_type and location_address required for REAL_ESTATE")
        if self.asset_type == AssetTypeEnum.ALTERNATIVE:
            if self.collection_type is None:
                raise ValueError("collection_type is required for ALTERNATIVE assets")
        return self


# --- Transaction ---
class TransactionCreateRequest(BaseModel):
    transaction_date: date
    amount_minor_units: MinorUnits
    transaction_type: TransactionTypeEnum
    category: str = Field(min_length=1)
    asset_id: UUID | None = None
    liability_id: UUID | None = None
    notes: str | None = None
    is_correction_for: UUID | None = None

    @field_validator("transaction_date")
    @classmethod
    def date_not_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Transaction date cannot be in the future")
        return v


# --- Inheritance Allocation ---
class AllocationCreateRequest(BaseModel):
    asset_id: UUID
    beneficiary_id: UUID
    percentage_share: float = Field(gt=0.0, le=100.0)
    distribution_conditions: str | None = None


class AllocationValidation(BaseModel):
    is_valid: bool
    currently_allocated_pct: float
    proposed_addition_pct: float
    resulting_total_pct: float
    remaining_after_pct: float
    error_message: str | None = None


# --- Credit ---
class BorrowerProfile(BaseModel):
    """Anonymous credit profile — NO PII. All fields are bands, not exact values."""
    age_band: str            # "35-44"
    city_tier: str           # "TIER_1"
    income_type: str         # "SALARIED" | "SELF_EMPLOYED" | "BUSINESS_OWNER"
    net_worth_band: str      # "₹1Cr-₹5Cr"
    security_coverage_multiple: float
    dsr_pct: float           # rounded to nearest 5%
    asset_classes_offered: list[str]  # ["REAL_ESTATE", "LIQUID"]
    on_time_payment_record: bool
```

---

## 5. Domain Model Classes (Dataclasses — Internal Use)

```python
# backend/app/models/domain.py
"""
Pure domain objects — no SQLAlchemy, no Pydantic validators.
Used internally within service/engine layers.
"""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Asset:
    asset_id: UUID
    portfolio_id: UUID
    asset_type: AssetTypeEnum
    name: str
    ownership_split_pct: float
    purchase_price_minor_units: int
    current_value_minor_units: int
    purchase_date: date
    verification_level: VerificationLevelEnum
    valuation_method: str
    valuation_as_of: datetime | None
    is_active: bool

    @property
    def attributed_value(self) -> int:
        """Convenience — integer floor of ownership-adjusted value."""
        return int(self.current_value_minor_units * self.ownership_split_pct / 100)

    @property
    def unrealised_gain(self) -> int:
        """Attributed value minus attributed cost basis."""
        attributed_cost = int(self.purchase_price_minor_units * self.ownership_split_pct / 100)
        return self.attributed_value - attributed_cost


@dataclass(frozen=True)
class HouseholdMember:
    member_id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    relationship: RelationshipEnum
    date_of_birth: date | None

    @property
    def is_relative_for_gift_tax(self) -> bool:
        """
        Section 56(2)(x) relative definition.
        See Phase4/04_Legal_Rules_Engine_Design.md for the complete list.
        """
        return self.relationship in {
            RelationshipEnum.SPOUSE,
            RelationshipEnum.CHILD,
            RelationshipEnum.PARENT,
            RelationshipEnum.SIBLING,
            RelationshipEnum.IN_LAW,
            RelationshipEnum.GRANDCHILD,
            RelationshipEnum.GRANDPARENT,
        }


@dataclass
class IndianFinancialYear:
    """Represents an Indian financial year (Apr–Mar)."""
    year: int  # The starting year, e.g., 2024 for FY 2024-25

    @property
    def start(self) -> date:
        return date(self.year, 4, 1)

    @property
    def end(self) -> date:
        return date(self.year + 1, 3, 31)

    @classmethod
    def from_date(cls, d: date) -> "IndianFinancialYear":
        return cls(year=d.year if d.month >= 4 else d.year - 1)

    def __contains__(self, d: date) -> bool:
        return self.start <= d <= self.end


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self) -> None:
        assert self.start <= self.end, "DateRange start must be <= end"

    @property
    def days(self) -> int:
        return (self.end - self.start).days


@dataclass
class YearMonth:
    year: int
    month: int  # 1–12

    @property
    def first_day(self) -> date:
        return date(self.year, self.month, 1)

    @property
    def last_day(self) -> date:
        import calendar
        return date(self.year, self.month, calendar.monthrange(self.year, self.month)[1])

    @classmethod
    def current(cls) -> "YearMonth":
        today = date.today()
        return cls(year=today.year, month=today.month)
```

---

## 6. Error Types

```python
# backend/app/core/exceptions.py

class VittavaanError(Exception):
    """Base exception for all application errors."""
    def __init__(self, code: str, message: str, **details) -> None:
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class CalculationError(VittavaanError):
    """Raised by engines when computation is impossible."""
    # Common codes: INSUFFICIENT_DATA, CONVERGENCE_FAILED,
    #               NO_SNAPSHOT_AT_PERIOD_END, PORTFOLIO_NOT_FOUND,
    #               COHORT_TOO_SMALL, NO_INCOME_DATA, ZERO_BEGINNING_VALUE


class PermissionDenied(VittavaanError):
    """Raised by ConsentAndMarketplaceEngine (Protection Proxy)."""
    # Common codes: NO_CONNECTION, CONSENT_EXPIRED, FIELD_NOT_PERMITTED


class ValidationError(VittavaanError):
    """Raised by service layer for business rule violations."""
    # Common codes: ALLOCATION_EXCEEDS_100, ASSET_PLEDGED,
    #               ASSET_TYPE_RESTRICTED, DATE_IN_FUTURE


class NotFoundError(VittavaanError):
    """Raised when a requested resource does not exist."""
    pass


# FastAPI exception handler converts these to HTTP responses:
# CalculationError → 200 OK with {data: null, error: {code, message}}
# PermissionDenied → 403 Forbidden
# ValidationError → 422 Unprocessable Entity
# NotFoundError → 404 Not Found
```

---

*Next: [04_Legal_Rules_Engine_Design.md](./04_Legal_Rules_Engine_Design.md)*
