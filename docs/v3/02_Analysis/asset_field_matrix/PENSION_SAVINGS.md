# Asset class: `PENSION_SAVINGS`

[← All asset subtypes](../08_Asset_Field_Requirement_Matrix.md)

Each subtype below expands into its complete field checklist. The status tags and storage path notation are explained in the [matrix index](../08_Asset_Field_Requirement_Matrix.md#status-tags).

## Subtypes in this class

- [`EPF`](#asset-subtype-epf)
- [`PPF`](#asset-subtype-ppf)
- [`NPS`](#asset-subtype-nps)
- [`SSY`](#asset-subtype-ssy)
- [`SCSS`](#asset-subtype-scss)
- [`POST_OFFICE_SAVINGS`](#asset-subtype-post-office-savings)
- [`APY`](#asset-subtype-apy)
- [`GRATUITY`](#asset-subtype-gratuity)
- [`ANNUITY`](#asset-subtype-annuity)

<a id="asset-subtype-epf"></a>

<details>
<summary><strong>Asset subtype: <code>EPF</code></strong></summary>

| Status and `table_name.column_name` | Description | Notes |
|---|---|---|
| <code>🟥 MANDATORY</code> `holdings.owner_person_id` | Person primarily accountable for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_class_code` | Selected top-level asset class. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_subtype_code` | Selected asset subtype. |  |
| <code>🟥 MANDATORY</code> `holdings.name` | User-facing name for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.currency` | Native ISO 4217 currency used for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | May be empty only when the subtype schema permits it. |
| <code>🟥 MANDATORY</code> `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Defaults to ACTIVE. |
| <code>🟥 MANDATORY</code> `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `ownership_allocations.person_id` | Person receiving an ownership share. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.effective_from` | Date from which the ownership share applies. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.uan_ref` | Uan ref. Expected value: `ref`. | Sensitive. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.passbook_as_of` | Passbook as of. Expected value: `date`. |  |
| <code>🟧 CONDITIONAL</code> `holdings.household_id` | Household in which the holding is shown. | Mandatory when included in a household portfolio. |
| <code>🟧 CONDITIONAL</code> `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Only when measured as units; omit for non-unitized assets. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | When a canonical identifier is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_ciphertext` | Encrypted primary identifier value. | When a canonical identifier is recorded; sensitive. |
| <code>🟧 CONDITIONAL</code> `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | When collection depends on consent. |
| <code>🟧 CONDITIONAL</code> `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Required before the asset contributes to net worth. |
| <code>🟧 CONDITIONAL</code> `valuation_events.currency` | ISO 4217 currency of the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.as_of_at` | Date and time to which the valuation applies. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.quantity` | Units acquired in the lot. | When the asset is quantity-based. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.acquired_on` | Acquisition date for the lot. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.restriction_type` | Approved restriction type. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.effective_from` | Date from which the restriction applies. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.status` | Restriction state: active, released or disputed. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `commitments.person_id` | Person responsible for funding the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.committed_minor_units` | Total committed amount in minor currency units. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.drawn_minor_units` | Amount already drawn. | Defaults to zero when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.currency` | ISO 4217 currency of the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `transactions.person_id` | Person who owns the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.source_id` | Provenance source for the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.quantity` | Signed number of units affected. | When the transaction changes quantity. |
| <code>🟧 CONDITIONAL</code> `transactions.amount_minor_units` | Signed cash amount in minor currency units. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.currency` | ISO 4217 transaction currency. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `income_streams.person_id` | Person receiving the income. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.name` | Display name of the income stream. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.amount_minor_units` | Expected income amount in minor currency units. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.currency` | ISO 4217 income currency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.frequency` | Expected payment frequency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.starts_on` | Income start date. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.status` | Income-stream state: active, paused or ended. | Defaults to active when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | Required when the asset is linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.effective_from` | Date from which the liability link applies. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `documents.owner_person_id` | Person who owns the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.document_type` | Approved document type. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.title` | Sanitized document title. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.retention_class` | Retention policy applied to the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `document_versions.original_filename` | Sanitized original filename. | Required when a document is uploaded. |
| <code>🟧 CONDITIONAL</code> `document_links.document_id` | Document linked to the asset. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `document_links.link_purpose` | Purpose such as evidence, contract or statement. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `verification_evidence.valuation_event_id` | Valuation supported by the evidence. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.document_id` | Supporting document. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.evidence_type` | Approved evidence type. | Required when verification evidence is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Mandatory when offshore is true. |
| <code>🟦 OPTIONAL</code> `holdings.acquired_on` | Known acquisition date. |  |
| <code>🟦 OPTIONAL</code> `sources.provider_code` | Provider or institution code when applicable. |  |
| <code>🟦 OPTIONAL</code> `sources.external_reference_hash` | Non-reversible hash of an external source reference. |  |
| <code>🟦 OPTIONAL</code> `sources.metadata` | Allow-listed, source-specific provenance metadata. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. |  |
| <code>🟦 OPTIONAL</code> `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.confidence` | Optional confidence score from 0 to 1. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.metadata` | Bounded, method-specific valuation details. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.source_id` | Source supporting the acquisition lot. |  |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.liability_id` | Liability causing or associated with the restriction. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.effective_to` | Date on which the restriction stopped applying. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.source_id` | Evidence source supporting the restriction. |  |
| <code>🟦 OPTIONAL</code> `commitments.due_on` | Known commitment due date. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_start` | Start of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_end` | End of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.source_id` | Source supporting the commitment. |  |
| <code>🟦 OPTIONAL</code> `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. |  |
| <code>🟦 OPTIONAL</code> `transactions.trade_date` | Trade or business-effective date. |  |
| <code>🟦 OPTIONAL</code> `transactions.settled_at` | Settlement timestamp. |  |
| <code>🟦 OPTIONAL</code> `transactions.description` | Sanitized transaction description. |  |
| <code>🟦 OPTIONAL</code> `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `income_streams.ends_on` | Income end date. |  |
| <code>🟦 OPTIONAL</code> `income_streams.growth_rate_pct` | Optional expected annual growth rate. |  |
| <code>🟦 OPTIONAL</code> `income_streams.source_id` | Source supporting the income stream. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.effective_to` | Date on which the liability link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `document_versions.document_date` | Business-effective date printed on the document. |  |
| <code>🟦 OPTIONAL</code> `document_versions.expires_on` | Document expiry date. |  |
| <code>🟦 OPTIONAL</code> `document_versions.source_id` | Source from which the document originated. |  |
| <code>🟦 OPTIONAL</code> `document_versions.supersedes_version_id` | Prior document version replaced by this version. |  |
| <code>🟦 OPTIONAL</code> `document_links.effective_to` | Timestamp when the document link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.expires_at` | Evidence expiry timestamp. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.notes` | Bounded verification notes. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.offshore` | Whether the holding is outside India. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custodian_name` | Name of the custodian. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.employer_name` | Employer name. Expected value: `str`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.establishment_ref` | Establishment ref. Expected value: `ref`. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.member_id_ref` | Member ID ref. Expected value: `ref`. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.employee_component` | Employee component. Expected value: `money`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.employer_epf_component` | Employer epf component. Expected value: `money`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.eps_component` | Eps component. Expected value: `money`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum('RECORDED','NOT_RECORDED','UNKNOWN')`. |  |
| <code>🟪 SYSTEM</code> `holdings.holding_id` | Unique identifier for the holding. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_by_principal_id` | Application principal that created the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_at` | Creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.updated_at` | Most recent update timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.version` | Optimistic-lock version used to prevent conflicting updates. |  |
| <code>🟪 SYSTEM</code> `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. |  |
| <code>🟪 SYSTEM</code> `sources.captured_by_principal_id` | Application principal that captured the information. | When a person or operator captured it. |
| <code>🟪 SYSTEM</code> `sources.captured_at` | Timestamp when the information was captured. |  |
| <code>🟪 SYSTEM</code> `sources.created_at` | Creation timestamp for the provenance record. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | From the parent holding. |
| <code>🟪 SYSTEM</code> `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.holding_id` | Holding valued by the observation. | From the parent holding. |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_at` | Timestamp when the valuation was recorded. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.holding_id` | Holding acquired through the lot. | From the parent holding. |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.holding_id` | Holding affected by the restriction. | From the parent holding. |
| <code>🟪 SYSTEM</code> `holding_restrictions.created_at` | Creation timestamp for the restriction record. |  |
| <code>🟪 SYSTEM</code> `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. |  |
| <code>🟪 SYSTEM</code> `commitments.holding_id` | Holding associated with the commitment. | From the parent holding. |
| <code>🟪 SYSTEM</code> `commitments.version` | Optimistic-lock version for the commitment. |  |
| <code>🟪 SYSTEM</code> `transactions.transaction_id` | Unique identifier for an immutable ledger event. |  |
| <code>🟪 SYSTEM</code> `transactions.holding_id` | Holding affected by the transaction. | When recorded from the holding. |
| <code>🟪 SYSTEM</code> `transactions.recorded_at` | Timestamp when the transaction was recorded. |  |
| <code>🟪 SYSTEM</code> `income_streams.income_stream_id` | Unique identifier for recurring or expected income. |  |
| <code>🟪 SYSTEM</code> `income_streams.holding_id` | Asset producing the income. | When created from the holding. |
| <code>🟪 SYSTEM</code> `income_streams.version` | Optimistic-lock version for the income stream. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.holding_id` | Asset participating in the liability relationship. | From the parent holding. |
| <code>🟪 SYSTEM</code> `liability_holding_links.created_at` | Creation timestamp for the liability link. |  |
| <code>🟪 SYSTEM</code> `documents.document_id` | Unique identifier for supporting document metadata. |  |
| <code>🟪 SYSTEM</code> `documents.lifecycle_state` | Document processing and availability state. |  |
| <code>🟪 SYSTEM</code> `documents.current_version_id` | Current clean document version. |  |
| <code>🟪 SYSTEM</code> `documents.created_by_principal_id` | Application principal that created the document. |  |
| <code>🟪 SYSTEM</code> `documents.created_at` | Document creation timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.updated_at` | Document update timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.version` | Optimistic-lock version for document metadata. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_version_id` | Unique identifier for an immutable document version. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_id` | Parent document. | From the parent document. |
| <code>🟪 SYSTEM</code> `document_versions.version_number` | Monotonic version number within the document. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_zone` | Quarantine or clean object-storage zone. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_key` | Random non-personal object-storage key. |  |
| <code>🟪 SYSTEM</code> `document_versions.checksum_sha256` | SHA-256 integrity digest. |  |
| <code>🟪 SYSTEM</code> `document_versions.mime_type` | Server-detected MIME type. |  |
| <code>🟪 SYSTEM</code> `document_versions.size_bytes` | Validated object size. |  |
| <code>🟪 SYSTEM</code> `document_versions.scan_state` | Malware scanning state. |  |
| <code>🟪 SYSTEM</code> `document_versions.scanner_policy_version` | Scanning-policy version used. |  |
| <code>🟪 SYSTEM</code> `document_versions.uploaded_at` | Upload timestamp. |  |
| <code>🟪 SYSTEM</code> `document_links.document_link_id` | Unique identifier linking a document to the asset. |  |
| <code>🟪 SYSTEM</code> `document_links.domain_type` | Approved domain-object type. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.domain_id` | Application-validated target identifier. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.holding_id` | Holding to which the document is linked. | From the parent holding. |
| <code>🟪 SYSTEM</code> `document_links.effective_from` | Timestamp from which the document link applies. | Unless explicitly effective later. |
| <code>🟪 SYSTEM</code> `document_links.created_by_principal_id` | Application principal that created the link. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_state` | Pending, verified, rejected or expired state. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_at` | Verification timestamp. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.created_at` | Evidence creation timestamp. |  |

</details>

<a id="asset-subtype-ppf"></a>

<details>
<summary><strong>Asset subtype: <code>PPF</code></strong></summary>

| Status and `table_name.column_name` | Description | Notes |
|---|---|---|
| <code>🟥 MANDATORY</code> `holdings.owner_person_id` | Person primarily accountable for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_class_code` | Selected top-level asset class. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_subtype_code` | Selected asset subtype. |  |
| <code>🟥 MANDATORY</code> `holdings.name` | User-facing name for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.currency` | Native ISO 4217 currency used for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | May be empty only when the subtype schema permits it. |
| <code>🟥 MANDATORY</code> `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Defaults to ACTIVE. |
| <code>🟥 MANDATORY</code> `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `ownership_allocations.person_id` | Person receiving an ownership share. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.effective_from` | Date from which the ownership share applies. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Sensitive. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. |  |
| <code>🟧 CONDITIONAL</code> `holdings.household_id` | Household in which the holding is shown. | Mandatory when included in a household portfolio. |
| <code>🟧 CONDITIONAL</code> `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Only when measured as units; omit for non-unitized assets. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | When a canonical identifier is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_ciphertext` | Encrypted primary identifier value. | When a canonical identifier is recorded; sensitive. |
| <code>🟧 CONDITIONAL</code> `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | When collection depends on consent. |
| <code>🟧 CONDITIONAL</code> `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Required before the asset contributes to net worth. |
| <code>🟧 CONDITIONAL</code> `valuation_events.currency` | ISO 4217 currency of the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.as_of_at` | Date and time to which the valuation applies. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.quantity` | Units acquired in the lot. | When the asset is quantity-based. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.acquired_on` | Acquisition date for the lot. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.restriction_type` | Approved restriction type. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.effective_from` | Date from which the restriction applies. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.status` | Restriction state: active, released or disputed. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `commitments.person_id` | Person responsible for funding the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.committed_minor_units` | Total committed amount in minor currency units. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.drawn_minor_units` | Amount already drawn. | Defaults to zero when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.currency` | ISO 4217 currency of the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `transactions.person_id` | Person who owns the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.source_id` | Provenance source for the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.quantity` | Signed number of units affected. | When the transaction changes quantity. |
| <code>🟧 CONDITIONAL</code> `transactions.amount_minor_units` | Signed cash amount in minor currency units. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.currency` | ISO 4217 transaction currency. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `income_streams.person_id` | Person receiving the income. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.name` | Display name of the income stream. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.amount_minor_units` | Expected income amount in minor currency units. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.currency` | ISO 4217 income currency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.frequency` | Expected payment frequency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.starts_on` | Income start date. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.status` | Income-stream state: active, paused or ended. | Defaults to active when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | Required when the asset is linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.effective_from` | Date from which the liability link applies. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `documents.owner_person_id` | Person who owns the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.document_type` | Approved document type. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.title` | Sanitized document title. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.retention_class` | Retention policy applied to the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `document_versions.original_filename` | Sanitized original filename. | Required when a document is uploaded. |
| <code>🟧 CONDITIONAL</code> `document_links.document_id` | Document linked to the asset. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `document_links.link_purpose` | Purpose such as evidence, contract or statement. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `verification_evidence.valuation_event_id` | Valuation supported by the evidence. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.document_id` | Supporting document. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.evidence_type` | Approved evidence type. | Required when verification evidence is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Mandatory when offshore is true. |
| <code>🟦 OPTIONAL</code> `holdings.acquired_on` | Known acquisition date. |  |
| <code>🟦 OPTIONAL</code> `sources.provider_code` | Provider or institution code when applicable. |  |
| <code>🟦 OPTIONAL</code> `sources.external_reference_hash` | Non-reversible hash of an external source reference. |  |
| <code>🟦 OPTIONAL</code> `sources.metadata` | Allow-listed, source-specific provenance metadata. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. |  |
| <code>🟦 OPTIONAL</code> `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.confidence` | Optional confidence score from 0 to 1. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.metadata` | Bounded, method-specific valuation details. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.source_id` | Source supporting the acquisition lot. |  |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.liability_id` | Liability causing or associated with the restriction. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.effective_to` | Date on which the restriction stopped applying. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.source_id` | Evidence source supporting the restriction. |  |
| <code>🟦 OPTIONAL</code> `commitments.due_on` | Known commitment due date. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_start` | Start of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_end` | End of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.source_id` | Source supporting the commitment. |  |
| <code>🟦 OPTIONAL</code> `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. |  |
| <code>🟦 OPTIONAL</code> `transactions.trade_date` | Trade or business-effective date. |  |
| <code>🟦 OPTIONAL</code> `transactions.settled_at` | Settlement timestamp. |  |
| <code>🟦 OPTIONAL</code> `transactions.description` | Sanitized transaction description. |  |
| <code>🟦 OPTIONAL</code> `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `income_streams.ends_on` | Income end date. |  |
| <code>🟦 OPTIONAL</code> `income_streams.growth_rate_pct` | Optional expected annual growth rate. |  |
| <code>🟦 OPTIONAL</code> `income_streams.source_id` | Source supporting the income stream. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.effective_to` | Date on which the liability link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `document_versions.document_date` | Business-effective date printed on the document. |  |
| <code>🟦 OPTIONAL</code> `document_versions.expires_on` | Document expiry date. |  |
| <code>🟦 OPTIONAL</code> `document_versions.source_id` | Source from which the document originated. |  |
| <code>🟦 OPTIONAL</code> `document_versions.supersedes_version_id` | Prior document version replaced by this version. |  |
| <code>🟦 OPTIONAL</code> `document_links.effective_to` | Timestamp when the document link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.expires_at` | Evidence expiry timestamp. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.notes` | Bounded verification notes. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.offshore` | Whether the holding is outside India. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custodian_name` | Name of the custodian. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.extension_block_end_date` | Extension block end date. Expected value: `date`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.loan_or_lien_state` | Loan or lien state. Expected value: `enum('NONE','LOAN','LIEN','UNKNOWN')`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. |  |
| <code>🟪 SYSTEM</code> `holdings.holding_id` | Unique identifier for the holding. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_by_principal_id` | Application principal that created the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_at` | Creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.updated_at` | Most recent update timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.version` | Optimistic-lock version used to prevent conflicting updates. |  |
| <code>🟪 SYSTEM</code> `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. |  |
| <code>🟪 SYSTEM</code> `sources.captured_by_principal_id` | Application principal that captured the information. | When a person or operator captured it. |
| <code>🟪 SYSTEM</code> `sources.captured_at` | Timestamp when the information was captured. |  |
| <code>🟪 SYSTEM</code> `sources.created_at` | Creation timestamp for the provenance record. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | From the parent holding. |
| <code>🟪 SYSTEM</code> `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.holding_id` | Holding valued by the observation. | From the parent holding. |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_at` | Timestamp when the valuation was recorded. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.holding_id` | Holding acquired through the lot. | From the parent holding. |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.holding_id` | Holding affected by the restriction. | From the parent holding. |
| <code>🟪 SYSTEM</code> `holding_restrictions.created_at` | Creation timestamp for the restriction record. |  |
| <code>🟪 SYSTEM</code> `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. |  |
| <code>🟪 SYSTEM</code> `commitments.holding_id` | Holding associated with the commitment. | From the parent holding. |
| <code>🟪 SYSTEM</code> `commitments.version` | Optimistic-lock version for the commitment. |  |
| <code>🟪 SYSTEM</code> `transactions.transaction_id` | Unique identifier for an immutable ledger event. |  |
| <code>🟪 SYSTEM</code> `transactions.holding_id` | Holding affected by the transaction. | When recorded from the holding. |
| <code>🟪 SYSTEM</code> `transactions.recorded_at` | Timestamp when the transaction was recorded. |  |
| <code>🟪 SYSTEM</code> `income_streams.income_stream_id` | Unique identifier for recurring or expected income. |  |
| <code>🟪 SYSTEM</code> `income_streams.holding_id` | Asset producing the income. | When created from the holding. |
| <code>🟪 SYSTEM</code> `income_streams.version` | Optimistic-lock version for the income stream. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.holding_id` | Asset participating in the liability relationship. | From the parent holding. |
| <code>🟪 SYSTEM</code> `liability_holding_links.created_at` | Creation timestamp for the liability link. |  |
| <code>🟪 SYSTEM</code> `documents.document_id` | Unique identifier for supporting document metadata. |  |
| <code>🟪 SYSTEM</code> `documents.lifecycle_state` | Document processing and availability state. |  |
| <code>🟪 SYSTEM</code> `documents.current_version_id` | Current clean document version. |  |
| <code>🟪 SYSTEM</code> `documents.created_by_principal_id` | Application principal that created the document. |  |
| <code>🟪 SYSTEM</code> `documents.created_at` | Document creation timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.updated_at` | Document update timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.version` | Optimistic-lock version for document metadata. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_version_id` | Unique identifier for an immutable document version. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_id` | Parent document. | From the parent document. |
| <code>🟪 SYSTEM</code> `document_versions.version_number` | Monotonic version number within the document. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_zone` | Quarantine or clean object-storage zone. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_key` | Random non-personal object-storage key. |  |
| <code>🟪 SYSTEM</code> `document_versions.checksum_sha256` | SHA-256 integrity digest. |  |
| <code>🟪 SYSTEM</code> `document_versions.mime_type` | Server-detected MIME type. |  |
| <code>🟪 SYSTEM</code> `document_versions.size_bytes` | Validated object size. |  |
| <code>🟪 SYSTEM</code> `document_versions.scan_state` | Malware scanning state. |  |
| <code>🟪 SYSTEM</code> `document_versions.scanner_policy_version` | Scanning-policy version used. |  |
| <code>🟪 SYSTEM</code> `document_versions.uploaded_at` | Upload timestamp. |  |
| <code>🟪 SYSTEM</code> `document_links.document_link_id` | Unique identifier linking a document to the asset. |  |
| <code>🟪 SYSTEM</code> `document_links.domain_type` | Approved domain-object type. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.domain_id` | Application-validated target identifier. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.holding_id` | Holding to which the document is linked. | From the parent holding. |
| <code>🟪 SYSTEM</code> `document_links.effective_from` | Timestamp from which the document link applies. | Unless explicitly effective later. |
| <code>🟪 SYSTEM</code> `document_links.created_by_principal_id` | Application principal that created the link. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_state` | Pending, verified, rejected or expired state. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_at` | Verification timestamp. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.created_at` | Evidence creation timestamp. |  |

</details>

<a id="asset-subtype-nps"></a>

<details>
<summary><strong>Asset subtype: <code>NPS</code></strong></summary>

| Status and `table_name.column_name` | Description | Notes |
|---|---|---|
| <code>🟥 MANDATORY</code> `holdings.owner_person_id` | Person primarily accountable for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_class_code` | Selected top-level asset class. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_subtype_code` | Selected asset subtype. |  |
| <code>🟥 MANDATORY</code> `holdings.name` | User-facing name for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.currency` | Native ISO 4217 currency used for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | May be empty only when the subtype schema permits it. |
| <code>🟥 MANDATORY</code> `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Defaults to ACTIVE. |
| <code>🟥 MANDATORY</code> `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `ownership_allocations.person_id` | Person receiving an ownership share. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.effective_from` | Date from which the ownership share applies. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.pran_ref` | Pran ref. Expected value: `ref`. | Sensitive. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.tier` | Tier. Expected value: `enum('TIER_I','TIER_II')`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.statement_as_of` | Statement as of. Expected value: `date`. |  |
| <code>🟧 CONDITIONAL</code> `holdings.household_id` | Household in which the holding is shown. | Mandatory when included in a household portfolio. |
| <code>🟧 CONDITIONAL</code> `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Only when measured as units; omit for non-unitized assets. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | When a canonical identifier is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_ciphertext` | Encrypted primary identifier value. | When a canonical identifier is recorded; sensitive. |
| <code>🟧 CONDITIONAL</code> `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | When collection depends on consent. |
| <code>🟧 CONDITIONAL</code> `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Required before the asset contributes to net worth. |
| <code>🟧 CONDITIONAL</code> `valuation_events.currency` | ISO 4217 currency of the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.as_of_at` | Date and time to which the valuation applies. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.quantity` | Units acquired in the lot. | When the asset is quantity-based. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.acquired_on` | Acquisition date for the lot. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.restriction_type` | Approved restriction type. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.effective_from` | Date from which the restriction applies. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.status` | Restriction state: active, released or disputed. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `commitments.person_id` | Person responsible for funding the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.committed_minor_units` | Total committed amount in minor currency units. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.drawn_minor_units` | Amount already drawn. | Defaults to zero when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.currency` | ISO 4217 currency of the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `transactions.person_id` | Person who owns the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.source_id` | Provenance source for the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.quantity` | Signed number of units affected. | When the transaction changes quantity. |
| <code>🟧 CONDITIONAL</code> `transactions.amount_minor_units` | Signed cash amount in minor currency units. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.currency` | ISO 4217 transaction currency. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `income_streams.person_id` | Person receiving the income. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.name` | Display name of the income stream. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.amount_minor_units` | Expected income amount in minor currency units. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.currency` | ISO 4217 income currency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.frequency` | Expected payment frequency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.starts_on` | Income start date. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.status` | Income-stream state: active, paused or ended. | Defaults to active when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | Required when the asset is linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.effective_from` | Date from which the liability link applies. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `documents.owner_person_id` | Person who owns the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.document_type` | Approved document type. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.title` | Sanitized document title. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.retention_class` | Retention policy applied to the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `document_versions.original_filename` | Sanitized original filename. | Required when a document is uploaded. |
| <code>🟧 CONDITIONAL</code> `document_links.document_id` | Document linked to the asset. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `document_links.link_purpose` | Purpose such as evidence, contract or statement. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `verification_evidence.valuation_event_id` | Valuation supported by the evidence. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.document_id` | Supporting document. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.evidence_type` | Approved evidence type. | Required when verification evidence is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Mandatory when offshore is true. |
| <code>🟦 OPTIONAL</code> `holdings.acquired_on` | Known acquisition date. |  |
| <code>🟦 OPTIONAL</code> `sources.provider_code` | Provider or institution code when applicable. |  |
| <code>🟦 OPTIONAL</code> `sources.external_reference_hash` | Non-reversible hash of an external source reference. |  |
| <code>🟦 OPTIONAL</code> `sources.metadata` | Allow-listed, source-specific provenance metadata. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. |  |
| <code>🟦 OPTIONAL</code> `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.confidence` | Optional confidence score from 0 to 1. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.metadata` | Bounded, method-specific valuation details. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.source_id` | Source supporting the acquisition lot. |  |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.liability_id` | Liability causing or associated with the restriction. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.effective_to` | Date on which the restriction stopped applying. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.source_id` | Evidence source supporting the restriction. |  |
| <code>🟦 OPTIONAL</code> `commitments.due_on` | Known commitment due date. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_start` | Start of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_end` | End of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.source_id` | Source supporting the commitment. |  |
| <code>🟦 OPTIONAL</code> `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. |  |
| <code>🟦 OPTIONAL</code> `transactions.trade_date` | Trade or business-effective date. |  |
| <code>🟦 OPTIONAL</code> `transactions.settled_at` | Settlement timestamp. |  |
| <code>🟦 OPTIONAL</code> `transactions.description` | Sanitized transaction description. |  |
| <code>🟦 OPTIONAL</code> `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `income_streams.ends_on` | Income end date. |  |
| <code>🟦 OPTIONAL</code> `income_streams.growth_rate_pct` | Optional expected annual growth rate. |  |
| <code>🟦 OPTIONAL</code> `income_streams.source_id` | Source supporting the income stream. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.effective_to` | Date on which the liability link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `document_versions.document_date` | Business-effective date printed on the document. |  |
| <code>🟦 OPTIONAL</code> `document_versions.expires_on` | Document expiry date. |  |
| <code>🟦 OPTIONAL</code> `document_versions.source_id` | Source from which the document originated. |  |
| <code>🟦 OPTIONAL</code> `document_versions.supersedes_version_id` | Prior document version replaced by this version. |  |
| <code>🟦 OPTIONAL</code> `document_links.effective_to` | Timestamp when the document link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.expires_at` | Evidence expiry timestamp. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.notes` | Bounded verification notes. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.offshore` | Whether the holding is outside India. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custodian_name` | Name of the custodian. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.cra_name` | Cra name. Expected value: `str`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.pop_name` | Pop name. Expected value: `str`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.pension_fund_manager` | Pension fund manager. Expected value: `str`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.investment_choice` | Investment choice. Expected value: `enum('ACTIVE','AUTO','UNKNOWN')`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.scheme_allocation` | Scheme allocation. Expected value: `object`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. |  |
| <code>🟪 SYSTEM</code> `holdings.holding_id` | Unique identifier for the holding. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_by_principal_id` | Application principal that created the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_at` | Creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.updated_at` | Most recent update timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.version` | Optimistic-lock version used to prevent conflicting updates. |  |
| <code>🟪 SYSTEM</code> `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. |  |
| <code>🟪 SYSTEM</code> `sources.captured_by_principal_id` | Application principal that captured the information. | When a person or operator captured it. |
| <code>🟪 SYSTEM</code> `sources.captured_at` | Timestamp when the information was captured. |  |
| <code>🟪 SYSTEM</code> `sources.created_at` | Creation timestamp for the provenance record. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | From the parent holding. |
| <code>🟪 SYSTEM</code> `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.holding_id` | Holding valued by the observation. | From the parent holding. |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_at` | Timestamp when the valuation was recorded. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.holding_id` | Holding acquired through the lot. | From the parent holding. |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.holding_id` | Holding affected by the restriction. | From the parent holding. |
| <code>🟪 SYSTEM</code> `holding_restrictions.created_at` | Creation timestamp for the restriction record. |  |
| <code>🟪 SYSTEM</code> `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. |  |
| <code>🟪 SYSTEM</code> `commitments.holding_id` | Holding associated with the commitment. | From the parent holding. |
| <code>🟪 SYSTEM</code> `commitments.version` | Optimistic-lock version for the commitment. |  |
| <code>🟪 SYSTEM</code> `transactions.transaction_id` | Unique identifier for an immutable ledger event. |  |
| <code>🟪 SYSTEM</code> `transactions.holding_id` | Holding affected by the transaction. | When recorded from the holding. |
| <code>🟪 SYSTEM</code> `transactions.recorded_at` | Timestamp when the transaction was recorded. |  |
| <code>🟪 SYSTEM</code> `income_streams.income_stream_id` | Unique identifier for recurring or expected income. |  |
| <code>🟪 SYSTEM</code> `income_streams.holding_id` | Asset producing the income. | When created from the holding. |
| <code>🟪 SYSTEM</code> `income_streams.version` | Optimistic-lock version for the income stream. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.holding_id` | Asset participating in the liability relationship. | From the parent holding. |
| <code>🟪 SYSTEM</code> `liability_holding_links.created_at` | Creation timestamp for the liability link. |  |
| <code>🟪 SYSTEM</code> `documents.document_id` | Unique identifier for supporting document metadata. |  |
| <code>🟪 SYSTEM</code> `documents.lifecycle_state` | Document processing and availability state. |  |
| <code>🟪 SYSTEM</code> `documents.current_version_id` | Current clean document version. |  |
| <code>🟪 SYSTEM</code> `documents.created_by_principal_id` | Application principal that created the document. |  |
| <code>🟪 SYSTEM</code> `documents.created_at` | Document creation timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.updated_at` | Document update timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.version` | Optimistic-lock version for document metadata. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_version_id` | Unique identifier for an immutable document version. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_id` | Parent document. | From the parent document. |
| <code>🟪 SYSTEM</code> `document_versions.version_number` | Monotonic version number within the document. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_zone` | Quarantine or clean object-storage zone. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_key` | Random non-personal object-storage key. |  |
| <code>🟪 SYSTEM</code> `document_versions.checksum_sha256` | SHA-256 integrity digest. |  |
| <code>🟪 SYSTEM</code> `document_versions.mime_type` | Server-detected MIME type. |  |
| <code>🟪 SYSTEM</code> `document_versions.size_bytes` | Validated object size. |  |
| <code>🟪 SYSTEM</code> `document_versions.scan_state` | Malware scanning state. |  |
| <code>🟪 SYSTEM</code> `document_versions.scanner_policy_version` | Scanning-policy version used. |  |
| <code>🟪 SYSTEM</code> `document_versions.uploaded_at` | Upload timestamp. |  |
| <code>🟪 SYSTEM</code> `document_links.document_link_id` | Unique identifier linking a document to the asset. |  |
| <code>🟪 SYSTEM</code> `document_links.domain_type` | Approved domain-object type. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.domain_id` | Application-validated target identifier. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.holding_id` | Holding to which the document is linked. | From the parent holding. |
| <code>🟪 SYSTEM</code> `document_links.effective_from` | Timestamp from which the document link applies. | Unless explicitly effective later. |
| <code>🟪 SYSTEM</code> `document_links.created_by_principal_id` | Application principal that created the link. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_state` | Pending, verified, rejected or expired state. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_at` | Verification timestamp. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.created_at` | Evidence creation timestamp. |  |

</details>

<a id="asset-subtype-ssy"></a>

<details>
<summary><strong>Asset subtype: <code>SSY</code></strong></summary>

| Status and `table_name.column_name` | Description | Notes |
|---|---|---|
| <code>🟥 MANDATORY</code> `holdings.owner_person_id` | Person primarily accountable for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_class_code` | Selected top-level asset class. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_subtype_code` | Selected asset subtype. |  |
| <code>🟥 MANDATORY</code> `holdings.name` | User-facing name for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.currency` | Native ISO 4217 currency used for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | May be empty only when the subtype schema permits it. |
| <code>🟥 MANDATORY</code> `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Defaults to ACTIVE. |
| <code>🟥 MANDATORY</code> `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `ownership_allocations.person_id` | Person receiving an ownership share. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.effective_from` | Date from which the ownership share applies. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Sensitive. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.beneficiary_person_id` | Beneficiary person ID. Expected value: `ref`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. |  |
| <code>🟧 CONDITIONAL</code> `holdings.household_id` | Household in which the holding is shown. | Mandatory when included in a household portfolio. |
| <code>🟧 CONDITIONAL</code> `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Only when measured as units; omit for non-unitized assets. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | When a canonical identifier is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_ciphertext` | Encrypted primary identifier value. | When a canonical identifier is recorded; sensitive. |
| <code>🟧 CONDITIONAL</code> `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | When collection depends on consent. |
| <code>🟧 CONDITIONAL</code> `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Required before the asset contributes to net worth. |
| <code>🟧 CONDITIONAL</code> `valuation_events.currency` | ISO 4217 currency of the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.as_of_at` | Date and time to which the valuation applies. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.quantity` | Units acquired in the lot. | When the asset is quantity-based. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.acquired_on` | Acquisition date for the lot. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.restriction_type` | Approved restriction type. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.effective_from` | Date from which the restriction applies. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.status` | Restriction state: active, released or disputed. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `commitments.person_id` | Person responsible for funding the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.committed_minor_units` | Total committed amount in minor currency units. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.drawn_minor_units` | Amount already drawn. | Defaults to zero when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.currency` | ISO 4217 currency of the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `transactions.person_id` | Person who owns the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.source_id` | Provenance source for the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.quantity` | Signed number of units affected. | When the transaction changes quantity. |
| <code>🟧 CONDITIONAL</code> `transactions.amount_minor_units` | Signed cash amount in minor currency units. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.currency` | ISO 4217 transaction currency. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `income_streams.person_id` | Person receiving the income. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.name` | Display name of the income stream. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.amount_minor_units` | Expected income amount in minor currency units. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.currency` | ISO 4217 income currency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.frequency` | Expected payment frequency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.starts_on` | Income start date. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.status` | Income-stream state: active, paused or ended. | Defaults to active when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | Required when the asset is linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.effective_from` | Date from which the liability link applies. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `documents.owner_person_id` | Person who owns the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.document_type` | Approved document type. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.title` | Sanitized document title. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.retention_class` | Retention policy applied to the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `document_versions.original_filename` | Sanitized original filename. | Required when a document is uploaded. |
| <code>🟧 CONDITIONAL</code> `document_links.document_id` | Document linked to the asset. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `document_links.link_purpose` | Purpose such as evidence, contract or statement. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `verification_evidence.valuation_event_id` | Valuation supported by the evidence. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.document_id` | Supporting document. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.evidence_type` | Approved evidence type. | Required when verification evidence is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.guardian_person_id` | Guardian person ID. Expected value: `ref`. |  |
| <code>🟦 OPTIONAL</code> `holdings.acquired_on` | Known acquisition date. |  |
| <code>🟦 OPTIONAL</code> `sources.provider_code` | Provider or institution code when applicable. |  |
| <code>🟦 OPTIONAL</code> `sources.external_reference_hash` | Non-reversible hash of an external source reference. |  |
| <code>🟦 OPTIONAL</code> `sources.metadata` | Allow-listed, source-specific provenance metadata. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. |  |
| <code>🟦 OPTIONAL</code> `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.confidence` | Optional confidence score from 0 to 1. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.metadata` | Bounded, method-specific valuation details. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.source_id` | Source supporting the acquisition lot. |  |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.liability_id` | Liability causing or associated with the restriction. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.effective_to` | Date on which the restriction stopped applying. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.source_id` | Evidence source supporting the restriction. |  |
| <code>🟦 OPTIONAL</code> `commitments.due_on` | Known commitment due date. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_start` | Start of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_end` | End of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.source_id` | Source supporting the commitment. |  |
| <code>🟦 OPTIONAL</code> `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. |  |
| <code>🟦 OPTIONAL</code> `transactions.trade_date` | Trade or business-effective date. |  |
| <code>🟦 OPTIONAL</code> `transactions.settled_at` | Settlement timestamp. |  |
| <code>🟦 OPTIONAL</code> `transactions.description` | Sanitized transaction description. |  |
| <code>🟦 OPTIONAL</code> `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `income_streams.ends_on` | Income end date. |  |
| <code>🟦 OPTIONAL</code> `income_streams.growth_rate_pct` | Optional expected annual growth rate. |  |
| <code>🟦 OPTIONAL</code> `income_streams.source_id` | Source supporting the income stream. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.effective_to` | Date on which the liability link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `document_versions.document_date` | Business-effective date printed on the document. |  |
| <code>🟦 OPTIONAL</code> `document_versions.expires_on` | Document expiry date. |  |
| <code>🟦 OPTIONAL</code> `document_versions.source_id` | Source from which the document originated. |  |
| <code>🟦 OPTIONAL</code> `document_versions.supersedes_version_id` | Prior document version replaced by this version. |  |
| <code>🟦 OPTIONAL</code> `document_links.effective_to` | Timestamp when the document link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.expires_at` | Evidence expiry timestamp. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.notes` | Bounded verification notes. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.offshore` | Whether the holding is outside India. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custodian_name` | Name of the custodian. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.annual_deposit_amount` | Annual deposit amount. Expected value: `money`. |  |
| <code>🟪 SYSTEM</code> `holdings.holding_id` | Unique identifier for the holding. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_by_principal_id` | Application principal that created the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_at` | Creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.updated_at` | Most recent update timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.version` | Optimistic-lock version used to prevent conflicting updates. |  |
| <code>🟪 SYSTEM</code> `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. |  |
| <code>🟪 SYSTEM</code> `sources.captured_by_principal_id` | Application principal that captured the information. | When a person or operator captured it. |
| <code>🟪 SYSTEM</code> `sources.captured_at` | Timestamp when the information was captured. |  |
| <code>🟪 SYSTEM</code> `sources.created_at` | Creation timestamp for the provenance record. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | From the parent holding. |
| <code>🟪 SYSTEM</code> `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.holding_id` | Holding valued by the observation. | From the parent holding. |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_at` | Timestamp when the valuation was recorded. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.holding_id` | Holding acquired through the lot. | From the parent holding. |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.holding_id` | Holding affected by the restriction. | From the parent holding. |
| <code>🟪 SYSTEM</code> `holding_restrictions.created_at` | Creation timestamp for the restriction record. |  |
| <code>🟪 SYSTEM</code> `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. |  |
| <code>🟪 SYSTEM</code> `commitments.holding_id` | Holding associated with the commitment. | From the parent holding. |
| <code>🟪 SYSTEM</code> `commitments.version` | Optimistic-lock version for the commitment. |  |
| <code>🟪 SYSTEM</code> `transactions.transaction_id` | Unique identifier for an immutable ledger event. |  |
| <code>🟪 SYSTEM</code> `transactions.holding_id` | Holding affected by the transaction. | When recorded from the holding. |
| <code>🟪 SYSTEM</code> `transactions.recorded_at` | Timestamp when the transaction was recorded. |  |
| <code>🟪 SYSTEM</code> `income_streams.income_stream_id` | Unique identifier for recurring or expected income. |  |
| <code>🟪 SYSTEM</code> `income_streams.holding_id` | Asset producing the income. | When created from the holding. |
| <code>🟪 SYSTEM</code> `income_streams.version` | Optimistic-lock version for the income stream. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.holding_id` | Asset participating in the liability relationship. | From the parent holding. |
| <code>🟪 SYSTEM</code> `liability_holding_links.created_at` | Creation timestamp for the liability link. |  |
| <code>🟪 SYSTEM</code> `documents.document_id` | Unique identifier for supporting document metadata. |  |
| <code>🟪 SYSTEM</code> `documents.lifecycle_state` | Document processing and availability state. |  |
| <code>🟪 SYSTEM</code> `documents.current_version_id` | Current clean document version. |  |
| <code>🟪 SYSTEM</code> `documents.created_by_principal_id` | Application principal that created the document. |  |
| <code>🟪 SYSTEM</code> `documents.created_at` | Document creation timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.updated_at` | Document update timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.version` | Optimistic-lock version for document metadata. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_version_id` | Unique identifier for an immutable document version. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_id` | Parent document. | From the parent document. |
| <code>🟪 SYSTEM</code> `document_versions.version_number` | Monotonic version number within the document. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_zone` | Quarantine or clean object-storage zone. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_key` | Random non-personal object-storage key. |  |
| <code>🟪 SYSTEM</code> `document_versions.checksum_sha256` | SHA-256 integrity digest. |  |
| <code>🟪 SYSTEM</code> `document_versions.mime_type` | Server-detected MIME type. |  |
| <code>🟪 SYSTEM</code> `document_versions.size_bytes` | Validated object size. |  |
| <code>🟪 SYSTEM</code> `document_versions.scan_state` | Malware scanning state. |  |
| <code>🟪 SYSTEM</code> `document_versions.scanner_policy_version` | Scanning-policy version used. |  |
| <code>🟪 SYSTEM</code> `document_versions.uploaded_at` | Upload timestamp. |  |
| <code>🟪 SYSTEM</code> `document_links.document_link_id` | Unique identifier linking a document to the asset. |  |
| <code>🟪 SYSTEM</code> `document_links.domain_type` | Approved domain-object type. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.domain_id` | Application-validated target identifier. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.holding_id` | Holding to which the document is linked. | From the parent holding. |
| <code>🟪 SYSTEM</code> `document_links.effective_from` | Timestamp from which the document link applies. | Unless explicitly effective later. |
| <code>🟪 SYSTEM</code> `document_links.created_by_principal_id` | Application principal that created the link. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_state` | Pending, verified, rejected or expired state. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_at` | Verification timestamp. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.created_at` | Evidence creation timestamp. |  |

</details>

<a id="asset-subtype-scss"></a>

<details>
<summary><strong>Asset subtype: <code>SCSS</code></strong></summary>

| Status and `table_name.column_name` | Description | Notes |
|---|---|---|
| <code>🟥 MANDATORY</code> `holdings.owner_person_id` | Person primarily accountable for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_class_code` | Selected top-level asset class. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_subtype_code` | Selected asset subtype. |  |
| <code>🟥 MANDATORY</code> `holdings.name` | User-facing name for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.currency` | Native ISO 4217 currency used for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | May be empty only when the subtype schema permits it. |
| <code>🟥 MANDATORY</code> `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Defaults to ACTIVE. |
| <code>🟥 MANDATORY</code> `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `ownership_allocations.person_id` | Person receiving an ownership share. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.effective_from` | Date from which the ownership share applies. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Sensitive. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.deposit_amount` | Deposit amount. Expected value: `money`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.interest_payout_frequency` | Interest payout frequency. Expected value: `enum`. |  |
| <code>🟧 CONDITIONAL</code> `holdings.household_id` | Household in which the holding is shown. | Mandatory when included in a household portfolio. |
| <code>🟧 CONDITIONAL</code> `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Only when measured as units; omit for non-unitized assets. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | When a canonical identifier is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_ciphertext` | Encrypted primary identifier value. | When a canonical identifier is recorded; sensitive. |
| <code>🟧 CONDITIONAL</code> `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | When collection depends on consent. |
| <code>🟧 CONDITIONAL</code> `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Required before the asset contributes to net worth. |
| <code>🟧 CONDITIONAL</code> `valuation_events.currency` | ISO 4217 currency of the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.as_of_at` | Date and time to which the valuation applies. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.quantity` | Units acquired in the lot. | When the asset is quantity-based. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.acquired_on` | Acquisition date for the lot. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.restriction_type` | Approved restriction type. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.effective_from` | Date from which the restriction applies. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.status` | Restriction state: active, released or disputed. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `commitments.person_id` | Person responsible for funding the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.committed_minor_units` | Total committed amount in minor currency units. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.drawn_minor_units` | Amount already drawn. | Defaults to zero when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.currency` | ISO 4217 currency of the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `transactions.person_id` | Person who owns the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.source_id` | Provenance source for the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.quantity` | Signed number of units affected. | When the transaction changes quantity. |
| <code>🟧 CONDITIONAL</code> `transactions.amount_minor_units` | Signed cash amount in minor currency units. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.currency` | ISO 4217 transaction currency. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `income_streams.person_id` | Person receiving the income. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.name` | Display name of the income stream. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.amount_minor_units` | Expected income amount in minor currency units. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.currency` | ISO 4217 income currency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.frequency` | Expected payment frequency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.starts_on` | Income start date. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.status` | Income-stream state: active, paused or ended. | Defaults to active when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | Required when the asset is linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.effective_from` | Date from which the liability link applies. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `documents.owner_person_id` | Person who owns the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.document_type` | Approved document type. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.title` | Sanitized document title. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.retention_class` | Retention policy applied to the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `document_versions.original_filename` | Sanitized original filename. | Required when a document is uploaded. |
| <code>🟧 CONDITIONAL</code> `document_links.document_id` | Document linked to the asset. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `document_links.link_purpose` | Purpose such as evidence, contract or statement. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `verification_evidence.valuation_event_id` | Valuation supported by the evidence. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.document_id` | Supporting document. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.evidence_type` | Approved evidence type. | Required when verification evidence is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Mandatory when offshore is true. |
| <code>🟦 OPTIONAL</code> `holdings.acquired_on` | Known acquisition date. |  |
| <code>🟦 OPTIONAL</code> `sources.provider_code` | Provider or institution code when applicable. |  |
| <code>🟦 OPTIONAL</code> `sources.external_reference_hash` | Non-reversible hash of an external source reference. |  |
| <code>🟦 OPTIONAL</code> `sources.metadata` | Allow-listed, source-specific provenance metadata. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. |  |
| <code>🟦 OPTIONAL</code> `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.confidence` | Optional confidence score from 0 to 1. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.metadata` | Bounded, method-specific valuation details. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.source_id` | Source supporting the acquisition lot. |  |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.liability_id` | Liability causing or associated with the restriction. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.effective_to` | Date on which the restriction stopped applying. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.source_id` | Evidence source supporting the restriction. |  |
| <code>🟦 OPTIONAL</code> `commitments.due_on` | Known commitment due date. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_start` | Start of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_end` | End of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.source_id` | Source supporting the commitment. |  |
| <code>🟦 OPTIONAL</code> `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. |  |
| <code>🟦 OPTIONAL</code> `transactions.trade_date` | Trade or business-effective date. |  |
| <code>🟦 OPTIONAL</code> `transactions.settled_at` | Settlement timestamp. |  |
| <code>🟦 OPTIONAL</code> `transactions.description` | Sanitized transaction description. |  |
| <code>🟦 OPTIONAL</code> `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `income_streams.ends_on` | Income end date. |  |
| <code>🟦 OPTIONAL</code> `income_streams.growth_rate_pct` | Optional expected annual growth rate. |  |
| <code>🟦 OPTIONAL</code> `income_streams.source_id` | Source supporting the income stream. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.effective_to` | Date on which the liability link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `document_versions.document_date` | Business-effective date printed on the document. |  |
| <code>🟦 OPTIONAL</code> `document_versions.expires_on` | Document expiry date. |  |
| <code>🟦 OPTIONAL</code> `document_versions.source_id` | Source from which the document originated. |  |
| <code>🟦 OPTIONAL</code> `document_versions.supersedes_version_id` | Prior document version replaced by this version. |  |
| <code>🟦 OPTIONAL</code> `document_links.effective_to` | Timestamp when the document link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.expires_at` | Evidence expiry timestamp. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.notes` | Bounded verification notes. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.offshore` | Whether the holding is outside India. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custodian_name` | Name of the custodian. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.extension_end_date` | Extension end date. Expected value: `date`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. |  |
| <code>🟪 SYSTEM</code> `holdings.holding_id` | Unique identifier for the holding. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_by_principal_id` | Application principal that created the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_at` | Creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.updated_at` | Most recent update timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.version` | Optimistic-lock version used to prevent conflicting updates. |  |
| <code>🟪 SYSTEM</code> `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. |  |
| <code>🟪 SYSTEM</code> `sources.captured_by_principal_id` | Application principal that captured the information. | When a person or operator captured it. |
| <code>🟪 SYSTEM</code> `sources.captured_at` | Timestamp when the information was captured. |  |
| <code>🟪 SYSTEM</code> `sources.created_at` | Creation timestamp for the provenance record. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | From the parent holding. |
| <code>🟪 SYSTEM</code> `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.holding_id` | Holding valued by the observation. | From the parent holding. |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_at` | Timestamp when the valuation was recorded. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.holding_id` | Holding acquired through the lot. | From the parent holding. |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.holding_id` | Holding affected by the restriction. | From the parent holding. |
| <code>🟪 SYSTEM</code> `holding_restrictions.created_at` | Creation timestamp for the restriction record. |  |
| <code>🟪 SYSTEM</code> `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. |  |
| <code>🟪 SYSTEM</code> `commitments.holding_id` | Holding associated with the commitment. | From the parent holding. |
| <code>🟪 SYSTEM</code> `commitments.version` | Optimistic-lock version for the commitment. |  |
| <code>🟪 SYSTEM</code> `transactions.transaction_id` | Unique identifier for an immutable ledger event. |  |
| <code>🟪 SYSTEM</code> `transactions.holding_id` | Holding affected by the transaction. | When recorded from the holding. |
| <code>🟪 SYSTEM</code> `transactions.recorded_at` | Timestamp when the transaction was recorded. |  |
| <code>🟪 SYSTEM</code> `income_streams.income_stream_id` | Unique identifier for recurring or expected income. |  |
| <code>🟪 SYSTEM</code> `income_streams.holding_id` | Asset producing the income. | When created from the holding. |
| <code>🟪 SYSTEM</code> `income_streams.version` | Optimistic-lock version for the income stream. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.holding_id` | Asset participating in the liability relationship. | From the parent holding. |
| <code>🟪 SYSTEM</code> `liability_holding_links.created_at` | Creation timestamp for the liability link. |  |
| <code>🟪 SYSTEM</code> `documents.document_id` | Unique identifier for supporting document metadata. |  |
| <code>🟪 SYSTEM</code> `documents.lifecycle_state` | Document processing and availability state. |  |
| <code>🟪 SYSTEM</code> `documents.current_version_id` | Current clean document version. |  |
| <code>🟪 SYSTEM</code> `documents.created_by_principal_id` | Application principal that created the document. |  |
| <code>🟪 SYSTEM</code> `documents.created_at` | Document creation timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.updated_at` | Document update timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.version` | Optimistic-lock version for document metadata. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_version_id` | Unique identifier for an immutable document version. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_id` | Parent document. | From the parent document. |
| <code>🟪 SYSTEM</code> `document_versions.version_number` | Monotonic version number within the document. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_zone` | Quarantine or clean object-storage zone. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_key` | Random non-personal object-storage key. |  |
| <code>🟪 SYSTEM</code> `document_versions.checksum_sha256` | SHA-256 integrity digest. |  |
| <code>🟪 SYSTEM</code> `document_versions.mime_type` | Server-detected MIME type. |  |
| <code>🟪 SYSTEM</code> `document_versions.size_bytes` | Validated object size. |  |
| <code>🟪 SYSTEM</code> `document_versions.scan_state` | Malware scanning state. |  |
| <code>🟪 SYSTEM</code> `document_versions.scanner_policy_version` | Scanning-policy version used. |  |
| <code>🟪 SYSTEM</code> `document_versions.uploaded_at` | Upload timestamp. |  |
| <code>🟪 SYSTEM</code> `document_links.document_link_id` | Unique identifier linking a document to the asset. |  |
| <code>🟪 SYSTEM</code> `document_links.domain_type` | Approved domain-object type. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.domain_id` | Application-validated target identifier. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.holding_id` | Holding to which the document is linked. | From the parent holding. |
| <code>🟪 SYSTEM</code> `document_links.effective_from` | Timestamp from which the document link applies. | Unless explicitly effective later. |
| <code>🟪 SYSTEM</code> `document_links.created_by_principal_id` | Application principal that created the link. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_state` | Pending, verified, rejected or expired state. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_at` | Verification timestamp. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.created_at` | Evidence creation timestamp. |  |

</details>

<a id="asset-subtype-post-office-savings"></a>

<details>
<summary><strong>Asset subtype: <code>POST_OFFICE_SAVINGS</code></strong></summary>

| Status and `table_name.column_name` | Description | Notes |
|---|---|---|
| <code>🟥 MANDATORY</code> `holdings.owner_person_id` | Person primarily accountable for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_class_code` | Selected top-level asset class. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_subtype_code` | Selected asset subtype. |  |
| <code>🟥 MANDATORY</code> `holdings.name` | User-facing name for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.currency` | Native ISO 4217 currency used for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | May be empty only when the subtype schema permits it. |
| <code>🟥 MANDATORY</code> `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Defaults to ACTIVE. |
| <code>🟥 MANDATORY</code> `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `ownership_allocations.person_id` | Person receiving an ownership share. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.effective_from` | Date from which the ownership share applies. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | Sensitive. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.scheme_kind` | Scheme kind. Expected value: `enum('SAVINGS','RD','TD','MIS','NSC','KVP','OTHER')`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.opened_or_issue_date` | Opened or issue date. Expected value: `date`. |  |
| <code>🟧 CONDITIONAL</code> `holdings.household_id` | Household in which the holding is shown. | Mandatory when included in a household portfolio. |
| <code>🟧 CONDITIONAL</code> `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Only when measured as units; omit for non-unitized assets. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | When a canonical identifier is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_ciphertext` | Encrypted primary identifier value. | When a canonical identifier is recorded; sensitive. |
| <code>🟧 CONDITIONAL</code> `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | When collection depends on consent. |
| <code>🟧 CONDITIONAL</code> `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Required before the asset contributes to net worth. |
| <code>🟧 CONDITIONAL</code> `valuation_events.currency` | ISO 4217 currency of the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.as_of_at` | Date and time to which the valuation applies. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.quantity` | Units acquired in the lot. | When the asset is quantity-based. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.acquired_on` | Acquisition date for the lot. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.restriction_type` | Approved restriction type. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.effective_from` | Date from which the restriction applies. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.status` | Restriction state: active, released or disputed. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `commitments.person_id` | Person responsible for funding the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.committed_minor_units` | Total committed amount in minor currency units. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.drawn_minor_units` | Amount already drawn. | Defaults to zero when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.currency` | ISO 4217 currency of the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `transactions.person_id` | Person who owns the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.source_id` | Provenance source for the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.quantity` | Signed number of units affected. | When the transaction changes quantity. |
| <code>🟧 CONDITIONAL</code> `transactions.amount_minor_units` | Signed cash amount in minor currency units. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.currency` | ISO 4217 transaction currency. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `income_streams.person_id` | Person receiving the income. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.name` | Display name of the income stream. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.amount_minor_units` | Expected income amount in minor currency units. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.currency` | ISO 4217 income currency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.frequency` | Expected payment frequency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.starts_on` | Income start date. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.status` | Income-stream state: active, paused or ended. | Defaults to active when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | Required when the asset is linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.effective_from` | Date from which the liability link applies. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `documents.owner_person_id` | Person who owns the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.document_type` | Approved document type. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.title` | Sanitized document title. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.retention_class` | Retention policy applied to the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `document_versions.original_filename` | Sanitized original filename. | Required when a document is uploaded. |
| <code>🟧 CONDITIONAL</code> `document_links.document_id` | Document linked to the asset. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `document_links.link_purpose` | Purpose such as evidence, contract or statement. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `verification_evidence.valuation_event_id` | Valuation supported by the evidence. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.document_id` | Supporting document. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.evidence_type` | Approved evidence type. | Required when verification evidence is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.certificate_ref` | Certificate ref. Expected value: `ref`. | Sensitive. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. |  |
| <code>🟦 OPTIONAL</code> `holdings.acquired_on` | Known acquisition date. |  |
| <code>🟦 OPTIONAL</code> `sources.provider_code` | Provider or institution code when applicable. |  |
| <code>🟦 OPTIONAL</code> `sources.external_reference_hash` | Non-reversible hash of an external source reference. |  |
| <code>🟦 OPTIONAL</code> `sources.metadata` | Allow-listed, source-specific provenance metadata. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. |  |
| <code>🟦 OPTIONAL</code> `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.confidence` | Optional confidence score from 0 to 1. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.metadata` | Bounded, method-specific valuation details. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.source_id` | Source supporting the acquisition lot. |  |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.liability_id` | Liability causing or associated with the restriction. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.effective_to` | Date on which the restriction stopped applying. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.source_id` | Evidence source supporting the restriction. |  |
| <code>🟦 OPTIONAL</code> `commitments.due_on` | Known commitment due date. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_start` | Start of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_end` | End of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.source_id` | Source supporting the commitment. |  |
| <code>🟦 OPTIONAL</code> `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. |  |
| <code>🟦 OPTIONAL</code> `transactions.trade_date` | Trade or business-effective date. |  |
| <code>🟦 OPTIONAL</code> `transactions.settled_at` | Settlement timestamp. |  |
| <code>🟦 OPTIONAL</code> `transactions.description` | Sanitized transaction description. |  |
| <code>🟦 OPTIONAL</code> `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `income_streams.ends_on` | Income end date. |  |
| <code>🟦 OPTIONAL</code> `income_streams.growth_rate_pct` | Optional expected annual growth rate. |  |
| <code>🟦 OPTIONAL</code> `income_streams.source_id` | Source supporting the income stream. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.effective_to` | Date on which the liability link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `document_versions.document_date` | Business-effective date printed on the document. |  |
| <code>🟦 OPTIONAL</code> `document_versions.expires_on` | Document expiry date. |  |
| <code>🟦 OPTIONAL</code> `document_versions.source_id` | Source from which the document originated. |  |
| <code>🟦 OPTIONAL</code> `document_versions.supersedes_version_id` | Prior document version replaced by this version. |  |
| <code>🟦 OPTIONAL</code> `document_links.effective_to` | Timestamp when the document link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.expires_at` | Evidence expiry timestamp. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.notes` | Bounded verification notes. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.offshore` | Whether the holding is outside India. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custodian_name` | Name of the custodian. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.principal_amount` | Principal amount. Expected value: `money`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.payout_frequency` | Payout frequency. Expected value: `enum`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. |  |
| <code>🟪 SYSTEM</code> `holdings.holding_id` | Unique identifier for the holding. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_by_principal_id` | Application principal that created the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_at` | Creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.updated_at` | Most recent update timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.version` | Optimistic-lock version used to prevent conflicting updates. |  |
| <code>🟪 SYSTEM</code> `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. |  |
| <code>🟪 SYSTEM</code> `sources.captured_by_principal_id` | Application principal that captured the information. | When a person or operator captured it. |
| <code>🟪 SYSTEM</code> `sources.captured_at` | Timestamp when the information was captured. |  |
| <code>🟪 SYSTEM</code> `sources.created_at` | Creation timestamp for the provenance record. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | From the parent holding. |
| <code>🟪 SYSTEM</code> `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.holding_id` | Holding valued by the observation. | From the parent holding. |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_at` | Timestamp when the valuation was recorded. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.holding_id` | Holding acquired through the lot. | From the parent holding. |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.holding_id` | Holding affected by the restriction. | From the parent holding. |
| <code>🟪 SYSTEM</code> `holding_restrictions.created_at` | Creation timestamp for the restriction record. |  |
| <code>🟪 SYSTEM</code> `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. |  |
| <code>🟪 SYSTEM</code> `commitments.holding_id` | Holding associated with the commitment. | From the parent holding. |
| <code>🟪 SYSTEM</code> `commitments.version` | Optimistic-lock version for the commitment. |  |
| <code>🟪 SYSTEM</code> `transactions.transaction_id` | Unique identifier for an immutable ledger event. |  |
| <code>🟪 SYSTEM</code> `transactions.holding_id` | Holding affected by the transaction. | When recorded from the holding. |
| <code>🟪 SYSTEM</code> `transactions.recorded_at` | Timestamp when the transaction was recorded. |  |
| <code>🟪 SYSTEM</code> `income_streams.income_stream_id` | Unique identifier for recurring or expected income. |  |
| <code>🟪 SYSTEM</code> `income_streams.holding_id` | Asset producing the income. | When created from the holding. |
| <code>🟪 SYSTEM</code> `income_streams.version` | Optimistic-lock version for the income stream. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.holding_id` | Asset participating in the liability relationship. | From the parent holding. |
| <code>🟪 SYSTEM</code> `liability_holding_links.created_at` | Creation timestamp for the liability link. |  |
| <code>🟪 SYSTEM</code> `documents.document_id` | Unique identifier for supporting document metadata. |  |
| <code>🟪 SYSTEM</code> `documents.lifecycle_state` | Document processing and availability state. |  |
| <code>🟪 SYSTEM</code> `documents.current_version_id` | Current clean document version. |  |
| <code>🟪 SYSTEM</code> `documents.created_by_principal_id` | Application principal that created the document. |  |
| <code>🟪 SYSTEM</code> `documents.created_at` | Document creation timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.updated_at` | Document update timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.version` | Optimistic-lock version for document metadata. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_version_id` | Unique identifier for an immutable document version. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_id` | Parent document. | From the parent document. |
| <code>🟪 SYSTEM</code> `document_versions.version_number` | Monotonic version number within the document. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_zone` | Quarantine or clean object-storage zone. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_key` | Random non-personal object-storage key. |  |
| <code>🟪 SYSTEM</code> `document_versions.checksum_sha256` | SHA-256 integrity digest. |  |
| <code>🟪 SYSTEM</code> `document_versions.mime_type` | Server-detected MIME type. |  |
| <code>🟪 SYSTEM</code> `document_versions.size_bytes` | Validated object size. |  |
| <code>🟪 SYSTEM</code> `document_versions.scan_state` | Malware scanning state. |  |
| <code>🟪 SYSTEM</code> `document_versions.scanner_policy_version` | Scanning-policy version used. |  |
| <code>🟪 SYSTEM</code> `document_versions.uploaded_at` | Upload timestamp. |  |
| <code>🟪 SYSTEM</code> `document_links.document_link_id` | Unique identifier linking a document to the asset. |  |
| <code>🟪 SYSTEM</code> `document_links.domain_type` | Approved domain-object type. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.domain_id` | Application-validated target identifier. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.holding_id` | Holding to which the document is linked. | From the parent holding. |
| <code>🟪 SYSTEM</code> `document_links.effective_from` | Timestamp from which the document link applies. | Unless explicitly effective later. |
| <code>🟪 SYSTEM</code> `document_links.created_by_principal_id` | Application principal that created the link. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_state` | Pending, verified, rejected or expired state. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_at` | Verification timestamp. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.created_at` | Evidence creation timestamp. |  |

</details>

<a id="asset-subtype-apy"></a>

<details>
<summary><strong>Asset subtype: <code>APY</code></strong></summary>

| Status and `table_name.column_name` | Description | Notes |
|---|---|---|
| <code>🟥 MANDATORY</code> `holdings.owner_person_id` | Person primarily accountable for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_class_code` | Selected top-level asset class. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_subtype_code` | Selected asset subtype. |  |
| <code>🟥 MANDATORY</code> `holdings.name` | User-facing name for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.currency` | Native ISO 4217 currency used for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | May be empty only when the subtype schema permits it. |
| <code>🟥 MANDATORY</code> `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Defaults to ACTIVE. |
| <code>🟥 MANDATORY</code> `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `ownership_allocations.person_id` | Person receiving an ownership share. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.effective_from` | Date from which the ownership share applies. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.pran_ref` | Pran ref. Expected value: `ref`. | Sensitive. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.contribution_frequency` | Contribution frequency. Expected value: `enum`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.contribution_amount` | Contribution amount. Expected value: `money`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.statement_as_of` | Statement as of. Expected value: `date`. |  |
| <code>🟧 CONDITIONAL</code> `holdings.household_id` | Household in which the holding is shown. | Mandatory when included in a household portfolio. |
| <code>🟧 CONDITIONAL</code> `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Only when measured as units; omit for non-unitized assets. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | When a canonical identifier is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_ciphertext` | Encrypted primary identifier value. | When a canonical identifier is recorded; sensitive. |
| <code>🟧 CONDITIONAL</code> `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | When collection depends on consent. |
| <code>🟧 CONDITIONAL</code> `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Required before the asset contributes to net worth. |
| <code>🟧 CONDITIONAL</code> `valuation_events.currency` | ISO 4217 currency of the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.as_of_at` | Date and time to which the valuation applies. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.quantity` | Units acquired in the lot. | When the asset is quantity-based. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.acquired_on` | Acquisition date for the lot. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.restriction_type` | Approved restriction type. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.effective_from` | Date from which the restriction applies. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.status` | Restriction state: active, released or disputed. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `commitments.person_id` | Person responsible for funding the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.committed_minor_units` | Total committed amount in minor currency units. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.drawn_minor_units` | Amount already drawn. | Defaults to zero when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.currency` | ISO 4217 currency of the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `transactions.person_id` | Person who owns the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.source_id` | Provenance source for the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.quantity` | Signed number of units affected. | When the transaction changes quantity. |
| <code>🟧 CONDITIONAL</code> `transactions.amount_minor_units` | Signed cash amount in minor currency units. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.currency` | ISO 4217 transaction currency. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `income_streams.person_id` | Person receiving the income. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.name` | Display name of the income stream. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.amount_minor_units` | Expected income amount in minor currency units. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.currency` | ISO 4217 income currency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.frequency` | Expected payment frequency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.starts_on` | Income start date. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.status` | Income-stream state: active, paused or ended. | Defaults to active when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | Required when the asset is linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.effective_from` | Date from which the liability link applies. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `documents.owner_person_id` | Person who owns the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.document_type` | Approved document type. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.title` | Sanitized document title. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.retention_class` | Retention policy applied to the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `document_versions.original_filename` | Sanitized original filename. | Required when a document is uploaded. |
| <code>🟧 CONDITIONAL</code> `document_links.document_id` | Document linked to the asset. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `document_links.link_purpose` | Purpose such as evidence, contract or statement. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `verification_evidence.valuation_event_id` | Valuation supported by the evidence. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.document_id` | Supporting document. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.evidence_type` | Approved evidence type. | Required when verification evidence is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Mandatory when offshore is true. |
| <code>🟦 OPTIONAL</code> `holdings.acquired_on` | Known acquisition date. |  |
| <code>🟦 OPTIONAL</code> `sources.provider_code` | Provider or institution code when applicable. |  |
| <code>🟦 OPTIONAL</code> `sources.external_reference_hash` | Non-reversible hash of an external source reference. |  |
| <code>🟦 OPTIONAL</code> `sources.metadata` | Allow-listed, source-specific provenance metadata. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. |  |
| <code>🟦 OPTIONAL</code> `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.confidence` | Optional confidence score from 0 to 1. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.metadata` | Bounded, method-specific valuation details. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.source_id` | Source supporting the acquisition lot. |  |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.liability_id` | Liability causing or associated with the restriction. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.effective_to` | Date on which the restriction stopped applying. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.source_id` | Evidence source supporting the restriction. |  |
| <code>🟦 OPTIONAL</code> `commitments.due_on` | Known commitment due date. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_start` | Start of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_end` | End of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.source_id` | Source supporting the commitment. |  |
| <code>🟦 OPTIONAL</code> `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. |  |
| <code>🟦 OPTIONAL</code> `transactions.trade_date` | Trade or business-effective date. |  |
| <code>🟦 OPTIONAL</code> `transactions.settled_at` | Settlement timestamp. |  |
| <code>🟦 OPTIONAL</code> `transactions.description` | Sanitized transaction description. |  |
| <code>🟦 OPTIONAL</code> `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `income_streams.ends_on` | Income end date. |  |
| <code>🟦 OPTIONAL</code> `income_streams.growth_rate_pct` | Optional expected annual growth rate. |  |
| <code>🟦 OPTIONAL</code> `income_streams.source_id` | Source supporting the income stream. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.effective_to` | Date on which the liability link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `document_versions.document_date` | Business-effective date printed on the document. |  |
| <code>🟦 OPTIONAL</code> `document_versions.expires_on` | Document expiry date. |  |
| <code>🟦 OPTIONAL</code> `document_versions.source_id` | Source from which the document originated. |  |
| <code>🟦 OPTIONAL</code> `document_versions.supersedes_version_id` | Prior document version replaced by this version. |  |
| <code>🟦 OPTIONAL</code> `document_links.effective_to` | Timestamp when the document link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.expires_at` | Evidence expiry timestamp. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.notes` | Bounded verification notes. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.offshore` | Whether the holding is outside India. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custodian_name` | Name of the custodian. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.bank_or_pop_name` | Bank or pop name. Expected value: `str`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.guaranteed_pension_band` | Guaranteed pension band. Expected value: `money`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.pension_start_date` | Pension start date. Expected value: `date`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.spouse_person_id` | Spouse person ID. Expected value: `ref`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. |  |
| <code>🟪 SYSTEM</code> `holdings.holding_id` | Unique identifier for the holding. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_by_principal_id` | Application principal that created the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_at` | Creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.updated_at` | Most recent update timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.version` | Optimistic-lock version used to prevent conflicting updates. |  |
| <code>🟪 SYSTEM</code> `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. |  |
| <code>🟪 SYSTEM</code> `sources.captured_by_principal_id` | Application principal that captured the information. | When a person or operator captured it. |
| <code>🟪 SYSTEM</code> `sources.captured_at` | Timestamp when the information was captured. |  |
| <code>🟪 SYSTEM</code> `sources.created_at` | Creation timestamp for the provenance record. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | From the parent holding. |
| <code>🟪 SYSTEM</code> `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.holding_id` | Holding valued by the observation. | From the parent holding. |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_at` | Timestamp when the valuation was recorded. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.holding_id` | Holding acquired through the lot. | From the parent holding. |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.holding_id` | Holding affected by the restriction. | From the parent holding. |
| <code>🟪 SYSTEM</code> `holding_restrictions.created_at` | Creation timestamp for the restriction record. |  |
| <code>🟪 SYSTEM</code> `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. |  |
| <code>🟪 SYSTEM</code> `commitments.holding_id` | Holding associated with the commitment. | From the parent holding. |
| <code>🟪 SYSTEM</code> `commitments.version` | Optimistic-lock version for the commitment. |  |
| <code>🟪 SYSTEM</code> `transactions.transaction_id` | Unique identifier for an immutable ledger event. |  |
| <code>🟪 SYSTEM</code> `transactions.holding_id` | Holding affected by the transaction. | When recorded from the holding. |
| <code>🟪 SYSTEM</code> `transactions.recorded_at` | Timestamp when the transaction was recorded. |  |
| <code>🟪 SYSTEM</code> `income_streams.income_stream_id` | Unique identifier for recurring or expected income. |  |
| <code>🟪 SYSTEM</code> `income_streams.holding_id` | Asset producing the income. | When created from the holding. |
| <code>🟪 SYSTEM</code> `income_streams.version` | Optimistic-lock version for the income stream. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.holding_id` | Asset participating in the liability relationship. | From the parent holding. |
| <code>🟪 SYSTEM</code> `liability_holding_links.created_at` | Creation timestamp for the liability link. |  |
| <code>🟪 SYSTEM</code> `documents.document_id` | Unique identifier for supporting document metadata. |  |
| <code>🟪 SYSTEM</code> `documents.lifecycle_state` | Document processing and availability state. |  |
| <code>🟪 SYSTEM</code> `documents.current_version_id` | Current clean document version. |  |
| <code>🟪 SYSTEM</code> `documents.created_by_principal_id` | Application principal that created the document. |  |
| <code>🟪 SYSTEM</code> `documents.created_at` | Document creation timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.updated_at` | Document update timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.version` | Optimistic-lock version for document metadata. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_version_id` | Unique identifier for an immutable document version. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_id` | Parent document. | From the parent document. |
| <code>🟪 SYSTEM</code> `document_versions.version_number` | Monotonic version number within the document. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_zone` | Quarantine or clean object-storage zone. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_key` | Random non-personal object-storage key. |  |
| <code>🟪 SYSTEM</code> `document_versions.checksum_sha256` | SHA-256 integrity digest. |  |
| <code>🟪 SYSTEM</code> `document_versions.mime_type` | Server-detected MIME type. |  |
| <code>🟪 SYSTEM</code> `document_versions.size_bytes` | Validated object size. |  |
| <code>🟪 SYSTEM</code> `document_versions.scan_state` | Malware scanning state. |  |
| <code>🟪 SYSTEM</code> `document_versions.scanner_policy_version` | Scanning-policy version used. |  |
| <code>🟪 SYSTEM</code> `document_versions.uploaded_at` | Upload timestamp. |  |
| <code>🟪 SYSTEM</code> `document_links.document_link_id` | Unique identifier linking a document to the asset. |  |
| <code>🟪 SYSTEM</code> `document_links.domain_type` | Approved domain-object type. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.domain_id` | Application-validated target identifier. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.holding_id` | Holding to which the document is linked. | From the parent holding. |
| <code>🟪 SYSTEM</code> `document_links.effective_from` | Timestamp from which the document link applies. | Unless explicitly effective later. |
| <code>🟪 SYSTEM</code> `document_links.created_by_principal_id` | Application principal that created the link. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_state` | Pending, verified, rejected or expired state. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_at` | Verification timestamp. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.created_at` | Evidence creation timestamp. |  |

</details>

<a id="asset-subtype-gratuity"></a>

<details>
<summary><strong>Asset subtype: <code>GRATUITY</code></strong></summary>

| Status and `table_name.column_name` | Description | Notes |
|---|---|---|
| <code>🟥 MANDATORY</code> `holdings.owner_person_id` | Person primarily accountable for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_class_code` | Selected top-level asset class. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_subtype_code` | Selected asset subtype. |  |
| <code>🟥 MANDATORY</code> `holdings.name` | User-facing name for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.currency` | Native ISO 4217 currency used for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | May be empty only when the subtype schema permits it. |
| <code>🟥 MANDATORY</code> `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Defaults to ACTIVE. |
| <code>🟥 MANDATORY</code> `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `ownership_allocations.person_id` | Person receiving an ownership share. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.effective_from` | Date from which the ownership share applies. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.employer_name` | Employer name. Expected value: `str`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.employment_start_date` | Employment start date. Expected value: `date`. |  |
| <code>🟧 CONDITIONAL</code> `holdings.household_id` | Household in which the holding is shown. | Mandatory when included in a household portfolio. |
| <code>🟧 CONDITIONAL</code> `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Only when measured as units; omit for non-unitized assets. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | When a canonical identifier is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_ciphertext` | Encrypted primary identifier value. | When a canonical identifier is recorded; sensitive. |
| <code>🟧 CONDITIONAL</code> `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | When collection depends on consent. |
| <code>🟧 CONDITIONAL</code> `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Required before the asset contributes to net worth. |
| <code>🟧 CONDITIONAL</code> `valuation_events.currency` | ISO 4217 currency of the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.as_of_at` | Date and time to which the valuation applies. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.quantity` | Units acquired in the lot. | When the asset is quantity-based. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.acquired_on` | Acquisition date for the lot. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.restriction_type` | Approved restriction type. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.effective_from` | Date from which the restriction applies. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.status` | Restriction state: active, released or disputed. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `commitments.person_id` | Person responsible for funding the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.committed_minor_units` | Total committed amount in minor currency units. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.drawn_minor_units` | Amount already drawn. | Defaults to zero when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.currency` | ISO 4217 currency of the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `transactions.person_id` | Person who owns the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.source_id` | Provenance source for the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.quantity` | Signed number of units affected. | When the transaction changes quantity. |
| <code>🟧 CONDITIONAL</code> `transactions.amount_minor_units` | Signed cash amount in minor currency units. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.currency` | ISO 4217 transaction currency. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `income_streams.person_id` | Person receiving the income. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.name` | Display name of the income stream. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.amount_minor_units` | Expected income amount in minor currency units. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.currency` | ISO 4217 income currency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.frequency` | Expected payment frequency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.starts_on` | Income start date. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.status` | Income-stream state: active, paused or ended. | Defaults to active when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | Required when the asset is linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.effective_from` | Date from which the liability link applies. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `documents.owner_person_id` | Person who owns the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.document_type` | Approved document type. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.title` | Sanitized document title. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.retention_class` | Retention policy applied to the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `document_versions.original_filename` | Sanitized original filename. | Required when a document is uploaded. |
| <code>🟧 CONDITIONAL</code> `document_links.document_id` | Document linked to the asset. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `document_links.link_purpose` | Purpose such as evidence, contract or statement. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `verification_evidence.valuation_event_id` | Valuation supported by the evidence. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.document_id` | Supporting document. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.evidence_type` | Approved evidence type. | Required when verification evidence is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.statement_as_of` | Statement as of. Expected value: `date`. |  |
| <code>🟦 OPTIONAL</code> `holdings.acquired_on` | Known acquisition date. |  |
| <code>🟦 OPTIONAL</code> `sources.provider_code` | Provider or institution code when applicable. |  |
| <code>🟦 OPTIONAL</code> `sources.external_reference_hash` | Non-reversible hash of an external source reference. |  |
| <code>🟦 OPTIONAL</code> `sources.metadata` | Allow-listed, source-specific provenance metadata. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. |  |
| <code>🟦 OPTIONAL</code> `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.confidence` | Optional confidence score from 0 to 1. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.metadata` | Bounded, method-specific valuation details. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.source_id` | Source supporting the acquisition lot. |  |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.liability_id` | Liability causing or associated with the restriction. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.effective_to` | Date on which the restriction stopped applying. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.source_id` | Evidence source supporting the restriction. |  |
| <code>🟦 OPTIONAL</code> `commitments.due_on` | Known commitment due date. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_start` | Start of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_end` | End of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.source_id` | Source supporting the commitment. |  |
| <code>🟦 OPTIONAL</code> `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. |  |
| <code>🟦 OPTIONAL</code> `transactions.trade_date` | Trade or business-effective date. |  |
| <code>🟦 OPTIONAL</code> `transactions.settled_at` | Settlement timestamp. |  |
| <code>🟦 OPTIONAL</code> `transactions.description` | Sanitized transaction description. |  |
| <code>🟦 OPTIONAL</code> `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `income_streams.ends_on` | Income end date. |  |
| <code>🟦 OPTIONAL</code> `income_streams.growth_rate_pct` | Optional expected annual growth rate. |  |
| <code>🟦 OPTIONAL</code> `income_streams.source_id` | Source supporting the income stream. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.effective_to` | Date on which the liability link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `document_versions.document_date` | Business-effective date printed on the document. |  |
| <code>🟦 OPTIONAL</code> `document_versions.expires_on` | Document expiry date. |  |
| <code>🟦 OPTIONAL</code> `document_versions.source_id` | Source from which the document originated. |  |
| <code>🟦 OPTIONAL</code> `document_versions.supersedes_version_id` | Prior document version replaced by this version. |  |
| <code>🟦 OPTIONAL</code> `document_links.effective_to` | Timestamp when the document link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.expires_at` | Evidence expiry timestamp. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.notes` | Bounded verification notes. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.offshore` | Whether the holding is outside India. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custodian_name` | Name of the custodian. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.employment_end_date` | Employment end date. Expected value: `date`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.covered_under_act` | Covered under act. Expected value: `bool`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.last_drawn_eligible_salary` | Last drawn eligible salary. Expected value: `money`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.employer_statement_amount` | Employer statement amount. Expected value: `money`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. |  |
| <code>🟪 SYSTEM</code> `holdings.holding_id` | Unique identifier for the holding. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_by_principal_id` | Application principal that created the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_at` | Creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.updated_at` | Most recent update timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.version` | Optimistic-lock version used to prevent conflicting updates. |  |
| <code>🟪 SYSTEM</code> `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. |  |
| <code>🟪 SYSTEM</code> `sources.captured_by_principal_id` | Application principal that captured the information. | When a person or operator captured it. |
| <code>🟪 SYSTEM</code> `sources.captured_at` | Timestamp when the information was captured. |  |
| <code>🟪 SYSTEM</code> `sources.created_at` | Creation timestamp for the provenance record. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | From the parent holding. |
| <code>🟪 SYSTEM</code> `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.holding_id` | Holding valued by the observation. | From the parent holding. |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_at` | Timestamp when the valuation was recorded. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.holding_id` | Holding acquired through the lot. | From the parent holding. |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.holding_id` | Holding affected by the restriction. | From the parent holding. |
| <code>🟪 SYSTEM</code> `holding_restrictions.created_at` | Creation timestamp for the restriction record. |  |
| <code>🟪 SYSTEM</code> `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. |  |
| <code>🟪 SYSTEM</code> `commitments.holding_id` | Holding associated with the commitment. | From the parent holding. |
| <code>🟪 SYSTEM</code> `commitments.version` | Optimistic-lock version for the commitment. |  |
| <code>🟪 SYSTEM</code> `transactions.transaction_id` | Unique identifier for an immutable ledger event. |  |
| <code>🟪 SYSTEM</code> `transactions.holding_id` | Holding affected by the transaction. | When recorded from the holding. |
| <code>🟪 SYSTEM</code> `transactions.recorded_at` | Timestamp when the transaction was recorded. |  |
| <code>🟪 SYSTEM</code> `income_streams.income_stream_id` | Unique identifier for recurring or expected income. |  |
| <code>🟪 SYSTEM</code> `income_streams.holding_id` | Asset producing the income. | When created from the holding. |
| <code>🟪 SYSTEM</code> `income_streams.version` | Optimistic-lock version for the income stream. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.holding_id` | Asset participating in the liability relationship. | From the parent holding. |
| <code>🟪 SYSTEM</code> `liability_holding_links.created_at` | Creation timestamp for the liability link. |  |
| <code>🟪 SYSTEM</code> `documents.document_id` | Unique identifier for supporting document metadata. |  |
| <code>🟪 SYSTEM</code> `documents.lifecycle_state` | Document processing and availability state. |  |
| <code>🟪 SYSTEM</code> `documents.current_version_id` | Current clean document version. |  |
| <code>🟪 SYSTEM</code> `documents.created_by_principal_id` | Application principal that created the document. |  |
| <code>🟪 SYSTEM</code> `documents.created_at` | Document creation timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.updated_at` | Document update timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.version` | Optimistic-lock version for document metadata. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_version_id` | Unique identifier for an immutable document version. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_id` | Parent document. | From the parent document. |
| <code>🟪 SYSTEM</code> `document_versions.version_number` | Monotonic version number within the document. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_zone` | Quarantine or clean object-storage zone. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_key` | Random non-personal object-storage key. |  |
| <code>🟪 SYSTEM</code> `document_versions.checksum_sha256` | SHA-256 integrity digest. |  |
| <code>🟪 SYSTEM</code> `document_versions.mime_type` | Server-detected MIME type. |  |
| <code>🟪 SYSTEM</code> `document_versions.size_bytes` | Validated object size. |  |
| <code>🟪 SYSTEM</code> `document_versions.scan_state` | Malware scanning state. |  |
| <code>🟪 SYSTEM</code> `document_versions.scanner_policy_version` | Scanning-policy version used. |  |
| <code>🟪 SYSTEM</code> `document_versions.uploaded_at` | Upload timestamp. |  |
| <code>🟪 SYSTEM</code> `document_links.document_link_id` | Unique identifier linking a document to the asset. |  |
| <code>🟪 SYSTEM</code> `document_links.domain_type` | Approved domain-object type. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.domain_id` | Application-validated target identifier. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.holding_id` | Holding to which the document is linked. | From the parent holding. |
| <code>🟪 SYSTEM</code> `document_links.effective_from` | Timestamp from which the document link applies. | Unless explicitly effective later. |
| <code>🟪 SYSTEM</code> `document_links.created_by_principal_id` | Application principal that created the link. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_state` | Pending, verified, rejected or expired state. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_at` | Verification timestamp. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.created_at` | Evidence creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_attributes.completed_service_years` | Completed service years. Expected value: `dec`. |  |

</details>

<a id="asset-subtype-annuity"></a>

<details>
<summary><strong>Asset subtype: <code>ANNUITY</code></strong></summary>

| Status and `table_name.column_name` | Description | Notes |
|---|---|---|
| <code>🟥 MANDATORY</code> `holdings.owner_person_id` | Person primarily accountable for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_class_code` | Selected top-level asset class. |  |
| <code>🟥 MANDATORY</code> `holdings.asset_subtype_code` | Selected asset subtype. |  |
| <code>🟥 MANDATORY</code> `holdings.name` | User-facing name for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.currency` | Native ISO 4217 currency used for the holding. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | May be empty only when the subtype schema permits it. |
| <code>🟥 MANDATORY</code> `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | Defaults to ACTIVE. |
| <code>🟥 MANDATORY</code> `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | Required for each provenance record. |
| <code>🟥 MANDATORY</code> `ownership_allocations.person_id` | Person receiving an ownership share. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `ownership_allocations.effective_from` | Date from which the ownership share applies. | Required for each ownership allocation. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.insurer_name` | Insurer name. Expected value: `str`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.policy_ref` | Policy ref. Expected value: `ref`. | Sensitive. |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.annuity_type` | Annuity type. Expected value: `enum('IMMEDIATE','DEFERRED')`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.life_basis` | Life basis. Expected value: `enum('SINGLE','JOINT','OTHER')`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.annuity_amount` | Annuity amount. Expected value: `money`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.payment_frequency` | Payment frequency. Expected value: `enum`. |  |
| <code>🟥 MANDATORY</code> `holdings.subtype_attributes.commencement_date` | Commencement date. Expected value: `date`. |  |
| <code>🟧 CONDITIONAL</code> `holdings.household_id` | Household in which the holding is shown. | Mandatory when included in a household portfolio. |
| <code>🟧 CONDITIONAL</code> `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | Only when measured as units; omit for non-unitized assets. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | When a canonical identifier is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.identifier_ciphertext` | Encrypted primary identifier value. | When a canonical identifier is recorded; sensitive. |
| <code>🟧 CONDITIONAL</code> `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | When collection depends on consent. |
| <code>🟧 CONDITIONAL</code> `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | Required before the asset contributes to net worth. |
| <code>🟧 CONDITIONAL</code> `valuation_events.currency` | ISO 4217 currency of the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.as_of_at` | Date and time to which the valuation applies. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | Required with a valuation. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.quantity` | Units acquired in the lot. | When the asset is quantity-based. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `cost_basis_lots.acquired_on` | Acquisition date for the lot. | Required when recording a cost lot. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.restriction_type` | Approved restriction type. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.effective_from` | Date from which the restriction applies. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `holding_restrictions.status` | Restriction state: active, released or disputed. | Required when a restriction exists. |
| <code>🟧 CONDITIONAL</code> `commitments.person_id` | Person responsible for funding the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.committed_minor_units` | Total committed amount in minor currency units. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.drawn_minor_units` | Amount already drawn. | Defaults to zero when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.currency` | ISO 4217 currency of the commitment. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | Required when a commitment exists. |
| <code>🟧 CONDITIONAL</code> `transactions.person_id` | Person who owns the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.source_id` | Provenance source for the transaction. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.quantity` | Signed number of units affected. | When the transaction changes quantity. |
| <code>🟧 CONDITIONAL</code> `transactions.amount_minor_units` | Signed cash amount in minor currency units. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `transactions.currency` | ISO 4217 transaction currency. | Required when a transaction is recorded. |
| <code>🟧 CONDITIONAL</code> `income_streams.person_id` | Person receiving the income. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.name` | Display name of the income stream. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.amount_minor_units` | Expected income amount in minor currency units. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.currency` | ISO 4217 income currency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.frequency` | Expected payment frequency. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.starts_on` | Income start date. | Required when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `income_streams.status` | Income-stream state: active, paused or ended. | Defaults to active when an income stream exists. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | Required when the asset is linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `liability_holding_links.effective_from` | Date from which the liability link applies. | Required when linked to a liability. |
| <code>🟧 CONDITIONAL</code> `documents.owner_person_id` | Person who owns the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.document_type` | Approved document type. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.title` | Sanitized document title. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `documents.retention_class` | Retention policy applied to the document. | Required when a document is attached. |
| <code>🟧 CONDITIONAL</code> `document_versions.original_filename` | Sanitized original filename. | Required when a document is uploaded. |
| <code>🟧 CONDITIONAL</code> `document_links.document_id` | Document linked to the asset. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `document_links.link_purpose` | Purpose such as evidence, contract or statement. | Required when creating a document link. |
| <code>🟧 CONDITIONAL</code> `verification_evidence.valuation_event_id` | Valuation supported by the evidence. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.document_id` | Supporting document. |  |
| <code>🟧 CONDITIONAL</code> `verification_evidence.evidence_type` | Approved evidence type. | Required when verification evidence is recorded. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | Mandatory when offshore is true. |
| <code>🟧 CONDITIONAL</code> `holdings.subtype_attributes.secondary_annuitant_person_id` | Secondary annuitant person ID. Expected value: `ref`. |  |
| <code>🟦 OPTIONAL</code> `holdings.acquired_on` | Known acquisition date. |  |
| <code>🟦 OPTIONAL</code> `sources.provider_code` | Provider or institution code when applicable. |  |
| <code>🟦 OPTIONAL</code> `sources.external_reference_hash` | Non-reversible hash of an external source reference. |  |
| <code>🟦 OPTIONAL</code> `sources.metadata` | Allow-listed, source-specific provenance metadata. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. |  |
| <code>🟦 OPTIONAL</code> `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.confidence` | Optional confidence score from 0 to 1. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `valuation_events.metadata` | Bounded, method-specific valuation details. | Defaults to an empty object. |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.source_id` | Source supporting the acquisition lot. |  |
| <code>🟦 OPTIONAL</code> `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.liability_id` | Liability causing or associated with the restriction. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.effective_to` | Date on which the restriction stopped applying. |  |
| <code>🟦 OPTIONAL</code> `holding_restrictions.source_id` | Evidence source supporting the restriction. |  |
| <code>🟦 OPTIONAL</code> `commitments.due_on` | Known commitment due date. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_start` | Start of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.window_end` | End of the permitted draw window. |  |
| <code>🟦 OPTIONAL</code> `commitments.source_id` | Source supporting the commitment. |  |
| <code>🟦 OPTIONAL</code> `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. |  |
| <code>🟦 OPTIONAL</code> `transactions.trade_date` | Trade or business-effective date. |  |
| <code>🟦 OPTIONAL</code> `transactions.settled_at` | Settlement timestamp. |  |
| <code>🟦 OPTIONAL</code> `transactions.description` | Sanitized transaction description. |  |
| <code>🟦 OPTIONAL</code> `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. |  |
| <code>🟦 OPTIONAL</code> `income_streams.ends_on` | Income end date. |  |
| <code>🟦 OPTIONAL</code> `income_streams.growth_rate_pct` | Optional expected annual growth rate. |  |
| <code>🟦 OPTIONAL</code> `income_streams.source_id` | Source supporting the income stream. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. |  |
| <code>🟦 OPTIONAL</code> `liability_holding_links.effective_to` | Date on which the liability link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `document_versions.document_date` | Business-effective date printed on the document. |  |
| <code>🟦 OPTIONAL</code> `document_versions.expires_on` | Document expiry date. |  |
| <code>🟦 OPTIONAL</code> `document_versions.source_id` | Source from which the document originated. |  |
| <code>🟦 OPTIONAL</code> `document_versions.supersedes_version_id` | Prior document version replaced by this version. |  |
| <code>🟦 OPTIONAL</code> `document_links.effective_to` | Timestamp when the document link stopped applying. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.expires_at` | Evidence expiry timestamp. |  |
| <code>🟦 OPTIONAL</code> `verification_evidence.notes` | Bounded verification notes. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.offshore` | Whether the holding is outside India. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custodian_name` | Name of the custodian. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | Sensitive. |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.purchase_price` | Purchase price. Expected value: `money`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.return_of_purchase_price` | Return of purchase price. Expected value: `bool`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.guarantee_period_end` | Guarantee period end. Expected value: `date`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.surrender_terms` | Surrender terms. Expected value: `object`. |  |
| <code>🟦 OPTIONAL</code> `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. |  |
| <code>🟪 SYSTEM</code> `holdings.holding_id` | Unique identifier for the holding. |  |
| <code>🟪 SYSTEM</code> `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_by_principal_id` | Application principal that created the record. |  |
| <code>🟪 SYSTEM</code> `holdings.created_at` | Creation timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.updated_at` | Most recent update timestamp. |  |
| <code>🟪 SYSTEM</code> `holdings.version` | Optimistic-lock version used to prevent conflicting updates. |  |
| <code>🟪 SYSTEM</code> `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. |  |
| <code>🟪 SYSTEM</code> `sources.captured_by_principal_id` | Application principal that captured the information. | When a person or operator captured it. |
| <code>🟪 SYSTEM</code> `sources.captured_at` | Timestamp when the information was captured. |  |
| <code>🟪 SYSTEM</code> `sources.created_at` | Creation timestamp for the provenance record. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. |  |
| <code>🟪 SYSTEM</code> `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | From the parent holding. |
| <code>🟪 SYSTEM</code> `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.holding_id` | Holding valued by the observation. | From the parent holding. |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. |  |
| <code>🟪 SYSTEM</code> `valuation_events.recorded_at` | Timestamp when the valuation was recorded. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.holding_id` | Holding acquired through the lot. | From the parent holding. |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. |  |
| <code>🟪 SYSTEM</code> `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. |  |
| <code>🟪 SYSTEM</code> `holding_restrictions.holding_id` | Holding affected by the restriction. | From the parent holding. |
| <code>🟪 SYSTEM</code> `holding_restrictions.created_at` | Creation timestamp for the restriction record. |  |
| <code>🟪 SYSTEM</code> `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. |  |
| <code>🟪 SYSTEM</code> `commitments.holding_id` | Holding associated with the commitment. | From the parent holding. |
| <code>🟪 SYSTEM</code> `commitments.version` | Optimistic-lock version for the commitment. |  |
| <code>🟪 SYSTEM</code> `transactions.transaction_id` | Unique identifier for an immutable ledger event. |  |
| <code>🟪 SYSTEM</code> `transactions.holding_id` | Holding affected by the transaction. | When recorded from the holding. |
| <code>🟪 SYSTEM</code> `transactions.recorded_at` | Timestamp when the transaction was recorded. |  |
| <code>🟪 SYSTEM</code> `income_streams.income_stream_id` | Unique identifier for recurring or expected income. |  |
| <code>🟪 SYSTEM</code> `income_streams.holding_id` | Asset producing the income. | When created from the holding. |
| <code>🟪 SYSTEM</code> `income_streams.version` | Optimistic-lock version for the income stream. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. |  |
| <code>🟪 SYSTEM</code> `liability_holding_links.holding_id` | Asset participating in the liability relationship. | From the parent holding. |
| <code>🟪 SYSTEM</code> `liability_holding_links.created_at` | Creation timestamp for the liability link. |  |
| <code>🟪 SYSTEM</code> `documents.document_id` | Unique identifier for supporting document metadata. |  |
| <code>🟪 SYSTEM</code> `documents.lifecycle_state` | Document processing and availability state. |  |
| <code>🟪 SYSTEM</code> `documents.current_version_id` | Current clean document version. |  |
| <code>🟪 SYSTEM</code> `documents.created_by_principal_id` | Application principal that created the document. |  |
| <code>🟪 SYSTEM</code> `documents.created_at` | Document creation timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.updated_at` | Document update timestamp. |  |
| <code>🟪 SYSTEM</code> `documents.version` | Optimistic-lock version for document metadata. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_version_id` | Unique identifier for an immutable document version. |  |
| <code>🟪 SYSTEM</code> `document_versions.document_id` | Parent document. | From the parent document. |
| <code>🟪 SYSTEM</code> `document_versions.version_number` | Monotonic version number within the document. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_zone` | Quarantine or clean object-storage zone. |  |
| <code>🟪 SYSTEM</code> `document_versions.storage_key` | Random non-personal object-storage key. |  |
| <code>🟪 SYSTEM</code> `document_versions.checksum_sha256` | SHA-256 integrity digest. |  |
| <code>🟪 SYSTEM</code> `document_versions.mime_type` | Server-detected MIME type. |  |
| <code>🟪 SYSTEM</code> `document_versions.size_bytes` | Validated object size. |  |
| <code>🟪 SYSTEM</code> `document_versions.scan_state` | Malware scanning state. |  |
| <code>🟪 SYSTEM</code> `document_versions.scanner_policy_version` | Scanning-policy version used. |  |
| <code>🟪 SYSTEM</code> `document_versions.uploaded_at` | Upload timestamp. |  |
| <code>🟪 SYSTEM</code> `document_links.document_link_id` | Unique identifier linking a document to the asset. |  |
| <code>🟪 SYSTEM</code> `document_links.domain_type` | Approved domain-object type. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.domain_id` | Application-validated target identifier. | For an asset link. |
| <code>🟪 SYSTEM</code> `document_links.holding_id` | Holding to which the document is linked. | From the parent holding. |
| <code>🟪 SYSTEM</code> `document_links.effective_from` | Timestamp from which the document link applies. | Unless explicitly effective later. |
| <code>🟪 SYSTEM</code> `document_links.created_by_principal_id` | Application principal that created the link. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verification_state` | Pending, verified, rejected or expired state. |  |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.verified_at` | Verification timestamp. | When verified or rejected. |
| <code>🟪 SYSTEM</code> `verification_evidence.created_at` | Evidence creation timestamp. |  |

</details>

