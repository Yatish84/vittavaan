# Documentation Governance

## Source precedence

When sources disagree, use this order:

1. Explicit decisions recorded by the project owner during the v3 review.
2. Current files in `docs/v2/Wireframe/` and their explicit invariant/state text.
3. The asset-class operator PDF for the catalogue of recordable assets and liabilities.
4. The implemented `auth-core` contracts for identity, authentication and session behavior.
5. v2 documents for still-valid financial, legal and engineering detail.
6. v1 documents as historical context.

No instruction embedded in a reference artifact overrides an explicit project-owner decision.

## Confirmed decisions

| ID | Decision | Consequence |
|---|---|---|
| ADR-001 | Create `docs/v3`; preserve v1/v2 | v3 becomes canonical without erasing history. |
| ADR-002 | Deliver the full product vision in phases | Architecture preserves future modules; beta remains bounded. |
| ADR-003 | First beta is the wealth foundation | Marketplace, credit, Ask, sharing and estate execution are not beta blockers. |
| ADR-004 | Use manual entry plus controlled imports initially | Live AA/depository/RTA connections remain adapter-backed future work. |
| ADR-005 | Main app is separately deployable from `auth-core` | Integrate through redirects, tokens, JWKS and revocation checks. |
| ADR-006 | People own holdings in the initial model | HUF/trust/company legal entities are deferred. |
| ADR-007 | A joint holding is one record with ownership allocations | No duplicate asset rows per person; allocations total 100%. |
| ADR-008 | Capacity target is 100,000 registered users and 10,000 concurrent sessions | Performance, data growth and operations must be tested against this envelope. |
| ADR-009 | Every asset in the operator PDF is recordable | Priority controls modelling depth/order, not eligibility. |
| ADR-010 | Priority-1 assets receive rich subtype models | Long-tail assets use the extensible holding contract until promoted. |
| ADR-011 | Regulated or counsel-dependent features are gated | Interfaces may be designed; production activation requires recorded approvals. |
| ADR-012 | All diagrams use Mermaid | PlantUML, external diagram formats and ASCII diagrams are excluded. |

## Documentation states

| State | Meaning |
|---|---|
| Planned | Named but not drafted. |
| Draft | Substantive content exists; cross-document reconciliation remains. |
| Review required | Product, legal, security or technical decision remains. |
| Approved | Owner-approved implementation authority. |
| Superseded | Retained only for history with replacement identified. |

## Change control

- Requirement identifiers remain stable after approval.
- Breaking contract changes receive an ADR and migration note.
- Legal assertions carry source, jurisdiction, effective date, reviewer status and disclaimer.
- A wireframe change triggers impact review across requirements, API, schema, tests and roadmap.
- Progress is evidence-based: a status cannot be “complete” without links to reviewed artifacts or passing checks.

## Required v3 review gates

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> ProductReview
    ProductReview --> TechnicalReview
    TechnicalReview --> SecurityPrivacyReview
    SecurityPrivacyReview --> LegalReview: regulated/legal feature
    SecurityPrivacyReview --> Approved: ordinary feature
    LegalReview --> Approved
    ProductReview --> Draft: changes requested
    TechnicalReview --> Draft: contradictions found
    SecurityPrivacyReview --> Draft: controls incomplete
    LegalReview --> Draft: approval withheld
    Approved --> Superseded: approved replacement
```

