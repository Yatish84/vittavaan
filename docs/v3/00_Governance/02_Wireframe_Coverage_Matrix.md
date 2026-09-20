# Wireframe Coverage Matrix

## Interpretation

The directory contains 25 HTML files. Twenty-two represent application surfaces or detailed flows; three are product/design references. Tabs and explicit states inside one HTML file are independently implementable requirements even when they are not separate files.

## First-beta surfaces

| Wireframe | Beta treatment | Required coverage |
|---|---|---|
| `Net worth.dc.html` | Full | Overview, period selection, assets/liabilities/net-worth movement, verified share, non-interpolated trend gaps, movers, ownership-aware composition, income/outflow and “worth a look” signals. |
| `Assets and liabilities.dc.html` | Full | All embedded tabs/states: Net worth, Assets, Liabilities, Cash flow, Data room, Consents, Holding, First run and Account setup. |
| `Household.dc.html` | Full | Scope selection, member ownership, attributed wealth, liquidity, income/dependants, permissions, joint holdings and minor/guardian states. |
| `Analysis.dc.html` | Full | XIRR, TWRR, benchmark comparison, performance basis, verified/self-declared contrast, holding period and cost disclosures. |
| `Attribution.dc.html` | Full | Reconciled attribution, sector/look-through exposure, holding contribution and ledger drill-through. |
| `Planning.dc.html` | Full | Goals, earmarked holdings, liquidity mismatch, deterministic assumptions, saved calculators and factual life-event timeline. |
| `Settings.dc.html` | Full, except gated modules | Display preferences, household/access visibility, privacy choices, notification preferences, security links to auth-core, revenue transparency and data rights. |
| `Investor profile.dc.html` | Partial | Facts and preferences required by wealth/planning; regulated suitability or recommendation behavior is excluded. |
| `Connections.dc.html` | Partial | Manual/import source setup, source status, failed/stale state, consent records and future connector placeholders. No claim of live feeds. |

### Assets and liabilities embedded-state checklist

| Tab/state | Beta | Notes |
|---|---|---|
| Net worth | Yes | Must remain consistent with the dedicated Net worth page. |
| Assets | Yes | Full asset catalogue is selectable; modelling depth varies by subtype. |
| Liabilities | Yes | Direct and contingent liabilities are distinguished. |
| Cash flow | Yes | Append-only transactions, categories, income streams and reconciliation. |
| Data room | Yes | Domain-linked documents, quarantine, provenance, supersession and access history. |
| Consents | Yes | Records source/access consents and expiry; live connector activation remains gated. |
| Holding | Yes | Reusable detail route/state with ownership, value history, documents, goals, pledge and source. |
| First run | Yes | True empty state, guided manual/import entry and no fabricated totals. |
| Account setup | Yes | Manual/import source selection, ownership mapping, validation and reconciliation. |

## Deferred, feature-gated surfaces

| Wireframe | Gate before real-user activation |
|---|---|
| `Financial resume.dc.html` | Consent/privacy threat model, claim-band policy, recipient binding and revocation design. |
| `Peers.dc.html` | Field-level sharing, grant UX, anonymity and anti-ranking acceptance. |
| `Ask.dc.html` | Retrieval authorization, citation quality, model evaluation, document access and advice-boundary approval. |
| `Trends and news.dc.html` | Licensed/approved sources, traceable holding relevance and editorial policy. |
| `Advisors.dc.html` | SEBI/legal review, credential verification, engagement/payment and rating policy. |
| `Credit.dc.html` | Lending/intermediation opinion, regulated lender contracts, k-anonymity data and PII release controls. |
| `All listings.dc.html` | Marketplace classification, seller workflow, diligence standard, disputes and fee approval. |
| `Stamp collection.dc.html` | Marketplace and escrow provider approval; verification/checklist and handover dispute model. |
| `Karjat plot.dc.html` | Marketplace gate plus title, public notice, registration, authorization and mutation operations. |
| `Gift rules.dc.html` | Advocate/CA-approved rule catalogue and jurisdiction/version process. |
| `Gift transfer.dc.html` | Gift rule gate, ownership authorization, registration evidence and dual-ledger reconciliation. |
| `Will.dc.html` | Succession counsel, strict confidentiality model and professional handoff. |
| `Inheritance.dc.html` | Death verification, executor authority, personal-law rules, immutable death snapshot and claims process. |

## Reference artifacts

| File | Use in v3 |
|---|---|
| `Schema.dc.html` | Domain requirements and model alternatives; not accepted blindly where it conflicts with confirmed person-only ownership. |
| `User Flow.dc.html` | Cross-screen invariants, navigation intent, commercial separation and lifecycle continuity. |
| `User Story.dc.html` | Acceptance states, actor narratives, capability gates and “do not invent” boundaries. |

## Global state families to trace

Every applicable surface must specify and test:

- Empty/first-run.
- Loading and resumable long-running operation.
- Complete and verified.
- Partial/incomplete with named omissions.
- Stale with last-known value and age.
- Import/feed failure without loss of prior facts.
- Unauthorized and insufficient grant.
- Revoked or expired consent.
- Negative/zero value where financially possible.
- Unsupported calculation with required remedial input.
- Concurrent edit/version conflict.
- Archived/superseded historical record.

