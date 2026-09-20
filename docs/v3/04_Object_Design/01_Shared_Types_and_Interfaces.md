# Shared Types and Interfaces

## Type rules

These signatures are language-neutral contracts illustrated with Python typing. Implementations may add internal types but must preserve the semantics.

```python
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import NewType, Protocol, Sequence
from uuid import UUID

MinorUnits = NewType("MinorUnits", int)
CurrencyCode = NewType("CurrencyCode", str)
Percentage = NewType("Percentage", Decimal)
Quantity = NewType("Quantity", Decimal)
CorrelationId = NewType("CorrelationId", UUID)
Version = NewType("Version", int)

@dataclass(frozen=True)
class Money:
    amount_minor_units: MinorUnits
    currency: CurrencyCode

@dataclass(frozen=True)
class EffectiveRange:
    starts_on: date
    ends_before: date | None

@dataclass(frozen=True)
class AuthorityContext:
    principal_id: UUID
    acting_person_id: UUID
    authority_kind: str
    grant_id: UUID | None
    purpose: str
    correlation_id: CorrelationId
```

`float` is prohibited for money, rates, percentages, ownership, quantities and exchange rates. Domain types validate ISO currency, bounded scale and range at construction.

## Provenance and result contracts

```python
@dataclass(frozen=True)
class Omission:
    code: str
    subject_type: str
    subject_id: UUID | None
    message_key: str

@dataclass(frozen=True)
class Provenance:
    as_of: datetime
    calculated_at: datetime
    calculation_version: str
    policy_version: str
    source_checkpoint: str
    source_ids: tuple[UUID, ...]
    verification_basis: str
    completeness: str
    omissions: tuple[Omission, ...]

@dataclass(frozen=True)
class DomainFailure:
    code: str
    message_key: str
    retryable: bool
    field: str | None = None

@dataclass(frozen=True)
class CalculationResult[T]:
    value: T | None
    provenance: Provenance
    failures: tuple[DomainFailure, ...]
```

Expected financial insufficiency returns named failures, not exceptions. Exceptions represent programming/infrastructure failure and are translated at boundaries.

## Command interfaces

```python
class ApplicationBootstrapControl(Protocol):
    async def bootstrap(self, identity: "VerifiedIdentity") -> "BootstrapView": ...

class HouseholdControl(Protocol):
    async def add_person(self, command: "AddPersonCommand", authority: AuthorityContext) -> "PersonView": ...
    async def change_membership(self, command: "ChangeMembershipCommand", authority: AuthorityContext) -> "MembershipView": ...

class AccessGrantControl(Protocol):
    async def create_grant(self, command: "CreateGrantCommand", authority: AuthorityContext) -> "GrantView": ...
    async def revoke_grant(self, grant_id: UUID, version: Version, authority: AuthorityContext) -> "GrantView": ...
    async def evaluate(self, request: "AccessRequest", identity: "VerifiedIdentity") -> "AccessDecision": ...

class HoldingCommandControl(Protocol):
    async def create(self, command: "CreateHoldingCommand", authority: AuthorityContext, idempotency_key: str) -> "HoldingView": ...
    async def update_metadata(self, holding_id: UUID, command: "UpdateHoldingCommand", expected_version: Version, authority: AuthorityContext) -> "HoldingView": ...
    async def replace_ownership_schedule(self, holding_id: UUID, command: "OwnershipScheduleCommand", expected_version: Version, authority: AuthorityContext) -> "OwnershipScheduleView": ...
    async def archive(self, holding_id: UUID, expected_version: Version, authority: AuthorityContext) -> "HoldingView": ...

class ValuationControl(Protocol):
    async def append(self, command: "AppendValuationCommand", authority: AuthorityContext, idempotency_key: str) -> "ValuationView": ...
    async def correct(self, valuation_id: UUID, command: "CorrectValuationCommand", authority: AuthorityContext, idempotency_key: str) -> "ValuationView": ...

class LedgerControl(Protocol):
    async def append_transaction(self, command: "AppendTransactionCommand", authority: AuthorityContext, idempotency_key: str) -> "TransactionView": ...
    async def correct_transaction(self, transaction_id: UUID, command: "CorrectTransactionCommand", authority: AuthorityContext, idempotency_key: str) -> "TransactionView": ...

class LiabilityControl(Protocol):
    async def create(self, command: "CreateLiabilityCommand", authority: AuthorityContext, idempotency_key: str) -> "LiabilityView": ...
    async def update_terms(self, liability_id: UUID, command: "UpdateLiabilityCommand", expected_version: Version, authority: AuthorityContext) -> "LiabilityView": ...

class ImportControl(Protocol):
    async def initialize(self, command: "InitializeImportCommand", authority: AuthorityContext, idempotency_key: str) -> "ImportJobView": ...
    async def submit_mapping(self, job_id: UUID, command: "MappingCommand", expected_version: Version, authority: AuthorityContext) -> "ImportJobView": ...
    async def commit(self, job_id: UUID, command: "CommitImportCommand", expected_version: Version, authority: AuthorityContext) -> "ImportCommitView": ...

class DocumentControl(Protocol):
    async def initialize_upload(self, command: "InitializeDocumentCommand", authority: AuthorityContext, idempotency_key: str) -> "UploadView": ...
    async def record_scan_result(self, result: "AuthenticatedScanResult") -> "DocumentVersionView": ...
    async def issue_access_url(self, document_id: UUID, command: "DocumentAccessCommand", authority: AuthorityContext) -> "SignedAccessView": ...

class GoalControl(Protocol):
    async def create(self, command: "CreateGoalCommand", authority: AuthorityContext, idempotency_key: str) -> "GoalView": ...
    async def save_scenario(self, goal_id: UUID, command: "ScenarioCommand", expected_version: Version, authority: AuthorityContext) -> "ScenarioView": ...
```

## Calculation engine interfaces

```python
class WealthEngine(Protocol):
    def calculate_overview(self, facts: "WealthFacts", request: "ScopeAsOfRequest") -> CalculationResult["WealthOverview"]: ...
    def calculate_movements(self, facts: "MovementFacts", request: "PeriodRequest") -> CalculationResult["MovementResult"]: ...

class CashFlowEngine(Protocol):
    def calculate_summary(self, facts: "CashFlowFacts", request: "PeriodRequest") -> CalculationResult["CashFlowSummary"]: ...
    def amortize(self, terms: "LiabilityTerms") -> CalculationResult["AmortizationSchedule"]: ...

class PerformanceEngine(Protocol):
    def calculate_xirr(self, facts: "PerformanceFacts", request: "PeriodRequest") -> CalculationResult["ReturnResult"]: ...
    def calculate_twrr(self, facts: "PerformanceFacts", request: "PeriodRequest") -> CalculationResult["ReturnResult"]: ...
    def calculate_attribution(self, facts: "AttributionFacts", request: "PeriodRequest") -> CalculationResult["AttributionResult"]: ...

class PlanningEngine(Protocol):
    def calculate_goal(self, facts: "GoalFacts", assumptions: "PlanningAssumptions") -> CalculationResult["GoalProjection"]: ...
    def compare_prepay_invest(self, facts: "PrepayFacts", assumptions: "PrepayAssumptions") -> CalculationResult["PrepayComparison"]: ...
```

Engines are pure: no repositories, current clock, network, authorization or mutable cache. Callers pass an explicit clock/as-of and fully authorized facts.

## Repository interfaces

```python
class UnitOfWork(Protocol):
    holdings: "HoldingRepository"
    valuations: "ValuationRepository"
    ledger: "TransactionRepository"
    audit: "AuditEvidenceRepository"
    outbox: "OutboxRepository"
    async def __aenter__(self) -> "UnitOfWork": ...
    async def __aexit__(self, exc_type, exc, tb) -> None: ...
    async def commit(self) -> None: ...

class HoldingRepository(Protocol):
    async def get_for_update(self, holding_id: UUID) -> "Holding": ...
    async def add(self, holding: "Holding") -> None: ...
    async def save(self, holding: "Holding", expected_version: Version) -> None: ...

class ValuationRepository(Protocol):
    async def append(self, event: "ValuationEvent") -> None: ...
    async def list_for_holding(self, holding_id: UUID, through: datetime) -> Sequence["ValuationEvent"]: ...

class TransactionRepository(Protocol):
    async def append(self, transaction: "Transaction") -> None: ...
    async def list_for_scope(self, query: "AuthorizedLedgerQuery") -> Sequence["Transaction"]: ...

class ProjectionRepository(Protocol):
    async def load_checkpoint(self, projection_type: str, scope: "Scope") -> "ProjectionCheckpoint | None": ...
    async def save_if_newer(self, projection: "Projection") -> bool: ...
```

Repositories accept only authorized/scoped query objects for sensitive reads. Generic unrestricted `find_all()` methods are prohibited.

## Adapter interfaces

```python
class IdentityVerifier(Protocol):
    async def verify(self, bearer_token: str) -> "VerifiedIdentity": ...

class ObjectStore(Protocol):
    async def create_upload(self, key: str, constraints: "UploadConstraints") -> "UploadTarget": ...
    async def create_download(self, key: str, expires_in_seconds: int) -> "SignedUrl": ...

class MalwareScanner(Protocol):
    async def submit(self, object_ref: "ObjectRef", correlation_id: CorrelationId) -> "ScanSubmission": ...

class SourceAdapter(Protocol):
    async def fetch(self, consent: "SourceConsent", cursor: str | None) -> "SourceFactBatch": ...

class BenchmarkAdapter(Protocol):
    async def get_series(self, benchmark_id: str, period: "DateRange") -> "LicensedSeries": ...

class NotificationAdapter(Protocol):
    async def send(self, notification: "MinimalNotification") -> "DeliveryReceipt": ...
```

## Exception hierarchy

| Exception | Boundary mapping |
|---|---|
| `AuthenticationRequired` | 401 |
| `PermissionDenied` | 403 or non-enumerating 404 by policy |
| `NotFound` | 404 |
| `DomainValidationError` | 422 problem details |
| `VersionConflict` / `StateConflict` | 409 |
| `IdempotencyConflict` | 409 |
| `RateLimited` | 429 |
| `DependencyUnavailable` | 503 |
| `InvariantViolation` | Internal fault, alert; never expose internals |

