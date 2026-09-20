# Sequence and State Diagrams

## Create a jointly owned holding

```mermaid
sequenceDiagram
    actor Actor
    participant UI as Holding Boundary
    participant Authz as Authorization Control
    participant HC as Holding Command Control
    participant Cat as Catalogue Policy
    participant Repo as Holding Repository
    participant Outbox as Outbox/Audit

    Actor->>UI: Submit holding, allocations, valuation
    UI->>Authz: Resolve authority for affected people
    Authz-->>UI: Allowed authority context
    UI->>HC: Create command + context
    HC->>Cat: Validate subtype/attributes/method
    Cat-->>HC: Validated normalized facts
    HC->>HC: Validate active allocations total 100%
    HC->>Repo: Atomic insert holding + allocations + valuation
    Repo->>Outbox: Record projection and audit events
    Repo-->>HC: Canonical IDs/version
    HC-->>UI: Created; projections pending
    UI-->>Actor: Holding with provenance/status
```

## Import and reconcile a CSV

```mermaid
sequenceDiagram
    actor Actor
    participant UI as Import Boundary
    participant IC as Import Control
    participant Store as Quarantine Storage
    participant Parser
    participant RC as Reconciliation Control
    participant Ledger as Ledger Controls
    participant Outbox

    Actor->>UI: Upload file + idempotency key
    UI->>IC: Create/reuse import job
    IC->>Store: Store and checksum
    IC->>Parser: Parse into staged rows
    Parser-->>IC: Rows + structural errors
    IC-->>UI: Mapping/validation view
    Actor->>UI: Map columns and owners
    UI->>RC: Validate and find duplicates
    RC-->>UI: Errors, warnings, candidates
    Actor->>UI: Confirm selected rows/decisions
    UI->>IC: Commit confirmed job version
    IC->>Ledger: Atomic/resumable canonical commands
    Ledger->>Outbox: Projection and audit events
    IC-->>UI: Committed/rejected row report
```

## Append and correct a valuation

```mermaid
sequenceDiagram
    actor Actor
    participant UI as Holding Boundary
    participant VC as Valuation Control
    participant Policy as Valuation Policy
    participant Repo as Valuation Repository
    participant Proj as Projection Control

    Actor->>UI: Add valuation assertion
    UI->>VC: Append with authority/provenance
    VC->>Policy: Validate method, date, subtype
    VC->>Repo: Insert immutable event
    VC->>Policy: Select applicable current event
    VC->>Proj: Emit invalidation event
    VC-->>UI: New event and current/stale state
    alt correction required
      Actor->>UI: Correct prior valuation
      UI->>VC: Append superseding event
      VC->>Repo: Insert link to prior event
      VC->>Proj: Emit new invalidation event
    end
```

## Build and serve a wealth projection

```mermaid
sequenceDiagram
    participant Outbox
    participant Worker
    participant Facts as Authorized Fact Reader
    participant Engine as Wealth Engine
    participant ReadDB as Projection Store
    actor Viewer
    participant API as Dashboard Boundary

    Outbox->>Worker: Holding/valuation/ledger changed
    Worker->>Worker: Claim idempotency key
    Worker->>Facts: Load versioned facts and policies
    Facts-->>Worker: Facts + lineage
    Worker->>Engine: Calculate scope projections
    Engine-->>Worker: Values + provenance/failures
    Worker->>ReadDB: Upsert versioned projection
    Viewer->>API: Request dashboard/scope
    API->>ReadDB: Read authorized current projection
    ReadDB-->>API: Projection + freshness
    API-->>Viewer: Values, gaps and provenance
```

## Upload and scan a document

```mermaid
sequenceDiagram
    actor Actor
    participant API as Document Boundary
    participant DC as Document Control
    participant Q as Quarantine Store
    participant Scan as Malware Scanner
    participant Clean as Clean Store
    participant Audit

    Actor->>API: Create metadata/link and upload
    API->>DC: Authorize target and initialize version
    DC->>Q: Store bytes/checksum
    DC-->>Actor: Pending scan
    Q->>Scan: Authenticated scan request
    Scan-->>DC: Correlated clean/infected/error result
    alt clean
      DC->>Clean: Promote/copy approved object
      DC->>Audit: Record availability
    else infected
      DC->>Audit: Record quarantine outcome
    else scanner error
      DC->>DC: Keep pending; bounded retry
    end
```

## Grant and revoke access

```mermaid
sequenceDiagram
    actor Grantor
    actor Grantee
    participant UI
    participant GC as Access Grant Control
    participant Authz as Authorization Policy
    participant Repo as Grant Repository
    participant Audit

    Grantor->>UI: Choose grantee, scope, level, purpose, expiry
    UI->>GC: Create grant command
    GC->>Authz: Verify grantor may delegate requested scope
    Authz-->>GC: Allowed
    GC->>Repo: Insert active grant
    GC->>Audit: Record grant evidence
    Grantee->>UI: Request scoped data
    UI->>GC: Evaluate active grant
    GC-->>UI: Server-filtered permitted response
    Grantor->>UI: Revoke grant
    UI->>GC: Revoke
    GC->>Repo: Append revocation state/time
    GC->>Audit: Record revocation
```

## Import job state

```mermaid
stateDiagram-v2
    [*] --> Uploaded
    Uploaded --> Quarantined
    Quarantined --> Parsing: scan clean
    Quarantined --> Rejected: infected/invalid
    Parsing --> MappingRequired
    Parsing --> Failed: unrecoverable parser error
    MappingRequired --> Validating: mapping submitted
    Validating --> ReviewRequired
    ReviewRequired --> Committing: confirmed version
    ReviewRequired --> Cancelled
    Committing --> Completed
    Committing --> PartiallyCompleted: resumable chunks
    Committing --> Failed: safe failure
    PartiallyCompleted --> Committing: resume
    Failed --> Parsing: retryable/restart
    Completed --> [*]
    Rejected --> [*]
    Cancelled --> [*]
```

## Document version state

```mermaid
stateDiagram-v2
    [*] --> PendingUpload
    PendingUpload --> Quarantined
    Quarantined --> ScanPending
    ScanPending --> Available: clean
    ScanPending --> QuarantinedInfected: infected
    ScanPending --> ScanPending: bounded retry
    Available --> Superseded: replacement accepted
    Available --> RetainedInactive: owner removal under policy
    Superseded --> RetainedInactive: retention transition
    RetainedInactive --> AnonymizedOrPurged: policy permits
```

## Access grant state

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Active: validated grant
    Active --> Expired: expiry reached
    Active --> Revoked: grantor/system revokes
    Active --> Suspended: security/legal hold
    Suspended --> Active: reviewed and restored
    Suspended --> Revoked
    Expired --> [*]
    Revoked --> [*]
```

## Holding lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> ActiveUnvalued: valid ownership, no applicable valuation
    Draft --> ActiveValued: valid ownership and valuation
    ActiveUnvalued --> ActiveValued: valuation appended
    ActiveValued --> ActiveStale: tolerance exceeded
    ActiveStale --> ActiveValued: new valuation
    ActiveValued --> Restricted: pledge/lien/hold
    Restricted --> ActiveValued: restriction released
    ActiveUnvalued --> Archived: no longer owned/recorded
    ActiveValued --> Archived: sold/transferred/closed
    Restricted --> Archived: authorized resolution
    Archived --> [*]
```

## Projection state

```mermaid
stateDiagram-v2
    [*] --> Missing
    Missing --> Queued: relevant fact committed
    Current --> Stale: newer fact/policy/version
    Stale --> Queued
    Queued --> Building
    Building --> Current: successful reproducible result
    Building --> Partial: supported result with named omissions
    Building --> Failed: engine/infrastructure failure
    Partial --> Queued: missing fact supplied
    Failed --> Queued: bounded retry or corrective input
```

