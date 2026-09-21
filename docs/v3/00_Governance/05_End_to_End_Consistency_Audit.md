# End-to-End Consistency Audit

## Audit scope and result

This audit was refreshed after completing the subtype dictionary and OCI deployment specification. It checks the chain from all 25 wireframe files and the operator PDF through requirements, Cockburn use cases, domain controls, persistence/API/events, sprint assignment, tests and operations.

**Result:** the v3 draft is structurally complete for owner review. Every first-beta surface has a requirements and implementation home. The audit found and corrected one material omission: source/processing consent was described in requirements and UI coverage but lacked its own database aggregate, API lifecycle, event/job behavior and detailed use case. `data_consents`, `FR3-CONSENT-*` and `UC3-CONSENT-001` now close that gap.

The main contradictions identified in v2 are resolved consistently:

| Prior conflict | v3 resolution |
|---|---|
| Old wireframes | All 25 current files categorized; beta tabs/states explicit. |
| Supabase auth duplication | auth-core is sole identity/session authority. |
| User portfolio ownership | People own one canonical shared holding through allocations. |
| Mutable current value | Append-only valuation events plus selection policy. |
| Three generic asset types | Every operator-PDF type recordable; P1 rich, long-tail extensible. |
| Small scale target | 100k users/10k concurrent with measurable SLOs. |
| Unclear regulated features | Disabled gates with evidence requirements. |
| “Nothing deleted” vs privacy | Class-based retention, access revocation, legal hold and anonymization. |
| Raw-request calculations | Versioned projections over authoritative facts. |

## Quantitative coverage snapshot

| Artefact | Coverage at audit |
|---|---:|
| Current wireframe HTML files inventoried | 25 |
| First-beta top-level surfaces | 9 |
| Embedded Assets and liabilities states | 9 |
| Detailed beta use cases | 15 |
| Asset subtype seed codes | 93 |
| Liability subtype contracts | 13 |
| Planned database tables | 50 |
| Legal/external feature gates | 12 |

Counts are navigation aids, not proof by themselves. Traceability and negative/error behavior determine completeness.

## Trace-chain audit

| Chain | Result | Evidence / remaining refinement |
|---|---|---|
| Wireframes → scope | Pass | All 25 files classified; all nine embedded Assets/Liabilities states explicitly scoped. |
| Scope → functional requirements | Pass | IAM, household, holdings, ledger, imports, consent, documents, wealth, analysis, planning, settings and gates have stable families. |
| Requirements → use cases | Pass with sprint refinement | Core user-goal flows have 15 detailed cases; element-level screen interactions can be added during the owning sprint without inventing domain behavior. |
| Requirements/use cases → domain controls | Pass | ECB model covers aggregates, controls, boundaries and consent/access distinction. |
| Domain → database | Pass at logical-design level | 50 table dictionaries; physical DDL awaits listed technology/security/legal decisions. |
| Domain → API/events/jobs | Pass | CRUD/workflow boundaries, consent lifecycle, append/correct behavior, outbox and projections are specified. |
| API/data → security/privacy | Pass at design level | auth-core boundary, non-enumerating authorization, encryption, audit, consent and retention controls specified; threat testing remains implementation evidence. |
| Capabilities → tests/sprints | Pass | Traceability matrix maps each beta capability to evidence and S0-S12. Golden numeric fixtures remain a sprint deliverable. |
| Runtime → deployment/recovery | Pass at design level | Local/OCI portability, Terraform inventory, release, backup, restore, exit and AWS production separation specified. |

## Audit corrections made

1. Added a first-class purpose-bound `SourceConsent` model distinct from household `AccessGrant`.
2. Added five consent requirements and a detailed grant/review/revoke consent use case.
3. Added `data_consents` as the 50th planned table and linked source provenance to the consent/basis used at collection.
4. Added consent/source API routes, change event and expiry/revocation enforcement job.
5. Added detailed liability and preference use cases and linked them into the traceability matrix.
6. Updated stale phase-audit wording that still described the subtype dictionary and infrastructure design as future work.
7. Distinguished OCI staging recovery evidence from the production RPO/RTO commitment.

## Remaining decisions

The authoritative list is [Owner Review and Decision Checklist](./06_Owner_Review_and_Decision_Checklist.md). Items are divided into baseline/S1 blockers, decisions due before their owning sprint, and release/feature-gate approvals. The subtype dictionary and deployment design are no longer listed as missing documents.

## Documentation readiness

The draft is sufficient for owner review and, after approval of the baseline/S1 checklist items, repository/platform scaffolding. This does not authorize product implementation automatically. Before each sprint, its due decisions, exact contracts, fixtures and acceptance evidence must be approved. Legal/vendor-dependent capabilities remain disabled regardless of documentation completeness.

## Final audit disposition

| Disposition | Meaning |
|---|---|
| Ready for owner baseline review | Yes. |
| Ready to create the S1 implementation backlog | Yes. |
| Ready to start S1 | Yes. `DEC3-001`–`DEC3-007` were confirmed by the owner on 20 Sep 2026; foundation-only scope applies. |
| Ready for customer beta | No; implementation, testing, security, recovery, legal and operational evidence do not yet exist. |
| Authorization to enable gated features | No. |
