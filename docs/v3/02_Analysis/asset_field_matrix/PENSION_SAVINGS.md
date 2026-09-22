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

| `table_name.column_name` | Description | Note |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_class_code` | Selected top-level asset class. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_subtype_code` | Selected asset subtype. | 🟥 **MANDATORY** — Required. |
| `holdings.name` | User-facing name for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | 🟥 **MANDATORY** — May be empty only when the subtype schema permits it. |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | 🟥 **MANDATORY** — Defaults to ACTIVE. |
| `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | 🟥 **MANDATORY** — Required for each provenance record. |
| `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | 🟥 **MANDATORY** — Required for each provenance record. |
| `ownership_allocations.person_id` | Person receiving an ownership share. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `holdings.subtype_attributes.uan_ref` | Uan ref. Expected value: `ref`. | 🟥 **MANDATORY** — Sensitive. |
| `holdings.subtype_attributes.passbook_as_of` | Passbook as of. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.household_id` | Household in which the holding is shown. | 🟧 **CONDITIONAL** — Mandatory when included in a household portfolio. |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | 🟧 **CONDITIONAL** — Sensitive. |
| `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | 🟧 **CONDITIONAL** — When collection depends on consent. |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | 🟧 **CONDITIONAL** — Required before the asset contributes to net worth. |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `cost_basis_lots.quantity` | Units acquired in the lot. | 🟧 **CONDITIONAL** — When the asset is quantity-based. |
| `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.acquired_on` | Acquisition date for the lot. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `holding_restrictions.restriction_type` | Approved restriction type. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.effective_from` | Date from which the restriction applies. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.status` | Restriction state: active, released or disputed. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `commitments.person_id` | Person responsible for funding the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.committed_minor_units` | Total committed amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.drawn_minor_units` | Amount already drawn. | 🟧 **CONDITIONAL** — Defaults to zero when a commitment exists. |
| `commitments.currency` | ISO 4217 currency of the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `transactions.person_id` | Person who owns the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.source_id` | Provenance source for the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.quantity` | Signed number of units affected. | 🟧 **CONDITIONAL** — When the transaction changes quantity. |
| `transactions.amount_minor_units` | Signed cash amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.currency` | ISO 4217 transaction currency. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `income_streams.person_id` | Person receiving the income. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.name` | Display name of the income stream. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.amount_minor_units` | Expected income amount in minor currency units. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.currency` | ISO 4217 income currency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.frequency` | Expected payment frequency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.starts_on` | Income start date. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.status` | Income-stream state: active, paused or ended. | 🟧 **CONDITIONAL** — Defaults to active when an income stream exists. |
| `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | 🟧 **CONDITIONAL** — Required when the asset is linked to a liability. |
| `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `liability_holding_links.effective_from` | Date from which the liability link applies. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `documents.owner_person_id` | Person who owns the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.document_type` | Approved document type. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.title` | Sanitized document title. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.retention_class` | Retention policy applied to the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `document_versions.original_filename` | Sanitized original filename. | 🟧 **CONDITIONAL** — Required when a document is uploaded. |
| `document_links.document_id` | Document linked to the asset. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `document_links.link_purpose` | Purpose such as evidence, contract or statement. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `verification_evidence.valuation_event_id` | Valuation supported by the evidence. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.document_id` | Supporting document. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.evidence_type` | Approved evidence type. | 🟧 **CONDITIONAL** — Required when verification evidence is recorded. |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.acquired_on` | Known acquisition date. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.provider_code` | Provider or institution code when applicable. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.external_reference_hash` | Non-reversible hash of an external source reference. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.metadata` | Allow-listed, source-specific provenance metadata. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.confidence` | Optional confidence score from 0 to 1. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.metadata` | Bounded, method-specific valuation details. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `cost_basis_lots.source_id` | Source supporting the acquisition lot. | 🟦 **OPTIONAL** — May be supplied. |
| `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.liability_id` | Liability causing or associated with the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.effective_to` | Date on which the restriction stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.source_id` | Evidence source supporting the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.due_on` | Known commitment due date. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_start` | Start of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_end` | End of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.source_id` | Source supporting the commitment. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.trade_date` | Trade or business-effective date. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.settled_at` | Settlement timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.description` | Sanitized transaction description. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.ends_on` | Income end date. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.growth_rate_pct` | Optional expected annual growth rate. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.source_id` | Source supporting the income stream. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.effective_to` | Date on which the liability link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.document_date` | Business-effective date printed on the document. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.expires_on` | Document expiry date. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.source_id` | Source from which the document originated. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.supersedes_version_id` | Prior document version replaced by this version. | 🟦 **OPTIONAL** — May be supplied. |
| `document_links.effective_to` | Timestamp when the document link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.expires_at` | Evidence expiry timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.notes` | Bounded verification notes. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.employer_name` | Employer name. Expected value: `str`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.establishment_ref` | Establishment ref. Expected value: `ref`. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.member_id_ref` | Member ID ref. Expected value: `ref`. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.employee_component` | Employee component. Expected value: `money`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.employer_epf_component` | Employer epf component. Expected value: `money`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.eps_component` | Eps component. Expected value: `money`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum('RECORDED','NOT_RECORDED','UNKNOWN')`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.holding_id` | Unique identifier for the holding. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_by_principal_id` | Application principal that created the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_at` | Creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.updated_at` | Most recent update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | 🟪 **SYSTEM** — System-generated. |
| `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. | 🟪 **SYSTEM** — System-generated. |
| `sources.captured_by_principal_id` | Application principal that captured the information. | 🟪 **SYSTEM** — System-generated when a person or operator captured it. |
| `sources.captured_at` | Timestamp when the information was captured. | 🟪 **SYSTEM** — System-generated. |
| `sources.created_at` | Creation timestamp for the provenance record. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.holding_id` | Holding valued by the observation. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.recorded_at` | Timestamp when the valuation was recorded. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.holding_id` | Holding acquired through the lot. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.holding_id` | Holding affected by the restriction. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `holding_restrictions.created_at` | Creation timestamp for the restriction record. | 🟪 **SYSTEM** — System-generated. |
| `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. | 🟪 **SYSTEM** — System-generated. |
| `commitments.holding_id` | Holding associated with the commitment. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `commitments.version` | Optimistic-lock version for the commitment. | 🟪 **SYSTEM** — System-generated. |
| `transactions.transaction_id` | Unique identifier for an immutable ledger event. | 🟪 **SYSTEM** — System-generated. |
| `transactions.holding_id` | Holding affected by the transaction. | 🟪 **SYSTEM** — System-generated when recorded from the holding. |
| `transactions.recorded_at` | Timestamp when the transaction was recorded. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.income_stream_id` | Unique identifier for recurring or expected income. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.holding_id` | Asset producing the income. | 🟪 **SYSTEM** — System-generated when created from the holding. |
| `income_streams.version` | Optimistic-lock version for the income stream. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.holding_id` | Asset participating in the liability relationship. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `liability_holding_links.created_at` | Creation timestamp for the liability link. | 🟪 **SYSTEM** — System-generated. |
| `documents.document_id` | Unique identifier for supporting document metadata. | 🟪 **SYSTEM** — System-generated. |
| `documents.lifecycle_state` | Document processing and availability state. | 🟪 **SYSTEM** — System-managed. |
| `documents.current_version_id` | Current clean document version. | 🟪 **SYSTEM** — System-managed. |
| `documents.created_by_principal_id` | Application principal that created the document. | 🟪 **SYSTEM** — System-generated. |
| `documents.created_at` | Document creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.updated_at` | Document update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.version` | Optimistic-lock version for document metadata. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_version_id` | Unique identifier for an immutable document version. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_id` | Parent document. | 🟪 **SYSTEM** — System-generated from the parent document. |
| `document_versions.version_number` | Monotonic version number within the document. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.storage_zone` | Quarantine or clean object-storage zone. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.storage_key` | Random non-personal object-storage key. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.checksum_sha256` | SHA-256 integrity digest. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.mime_type` | Server-detected MIME type. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.size_bytes` | Validated object size. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.scan_state` | Malware scanning state. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.scanner_policy_version` | Scanning-policy version used. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.uploaded_at` | Upload timestamp. | 🟪 **SYSTEM** — System-generated. |
| `document_links.document_link_id` | Unique identifier linking a document to the asset. | 🟪 **SYSTEM** — System-generated. |
| `document_links.domain_type` | Approved domain-object type. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.domain_id` | Application-validated target identifier. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.holding_id` | Holding to which the document is linked. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `document_links.effective_from` | Timestamp from which the document link applies. | 🟪 **SYSTEM** — System-generated unless explicitly effective later. |
| `document_links.created_by_principal_id` | Application principal that created the link. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_state` | Pending, verified, rejected or expired state. | 🟪 **SYSTEM** — System-managed. |
| `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.verified_at` | Verification timestamp. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.created_at` | Evidence creation timestamp. | 🟪 **SYSTEM** — System-generated. |

</details>

<a id="asset-subtype-ppf"></a>

<details>
<summary><strong>Asset subtype: <code>PPF</code></strong></summary>

| `table_name.column_name` | Description | Note |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_class_code` | Selected top-level asset class. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_subtype_code` | Selected asset subtype. | 🟥 **MANDATORY** — Required. |
| `holdings.name` | User-facing name for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | 🟥 **MANDATORY** — May be empty only when the subtype schema permits it. |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | 🟥 **MANDATORY** — Defaults to ACTIVE. |
| `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | 🟥 **MANDATORY** — Required for each provenance record. |
| `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | 🟥 **MANDATORY** — Required for each provenance record. |
| `ownership_allocations.person_id` | Person receiving an ownership share. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | 🟥 **MANDATORY** — Sensitive. |
| `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.household_id` | Household in which the holding is shown. | 🟧 **CONDITIONAL** — Mandatory when included in a household portfolio. |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | 🟧 **CONDITIONAL** — Sensitive. |
| `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | 🟧 **CONDITIONAL** — When collection depends on consent. |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | 🟧 **CONDITIONAL** — Required before the asset contributes to net worth. |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `cost_basis_lots.quantity` | Units acquired in the lot. | 🟧 **CONDITIONAL** — When the asset is quantity-based. |
| `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.acquired_on` | Acquisition date for the lot. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `holding_restrictions.restriction_type` | Approved restriction type. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.effective_from` | Date from which the restriction applies. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.status` | Restriction state: active, released or disputed. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `commitments.person_id` | Person responsible for funding the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.committed_minor_units` | Total committed amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.drawn_minor_units` | Amount already drawn. | 🟧 **CONDITIONAL** — Defaults to zero when a commitment exists. |
| `commitments.currency` | ISO 4217 currency of the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `transactions.person_id` | Person who owns the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.source_id` | Provenance source for the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.quantity` | Signed number of units affected. | 🟧 **CONDITIONAL** — When the transaction changes quantity. |
| `transactions.amount_minor_units` | Signed cash amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.currency` | ISO 4217 transaction currency. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `income_streams.person_id` | Person receiving the income. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.name` | Display name of the income stream. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.amount_minor_units` | Expected income amount in minor currency units. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.currency` | ISO 4217 income currency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.frequency` | Expected payment frequency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.starts_on` | Income start date. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.status` | Income-stream state: active, paused or ended. | 🟧 **CONDITIONAL** — Defaults to active when an income stream exists. |
| `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | 🟧 **CONDITIONAL** — Required when the asset is linked to a liability. |
| `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `liability_holding_links.effective_from` | Date from which the liability link applies. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `documents.owner_person_id` | Person who owns the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.document_type` | Approved document type. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.title` | Sanitized document title. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.retention_class` | Retention policy applied to the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `document_versions.original_filename` | Sanitized original filename. | 🟧 **CONDITIONAL** — Required when a document is uploaded. |
| `document_links.document_id` | Document linked to the asset. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `document_links.link_purpose` | Purpose such as evidence, contract or statement. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `verification_evidence.valuation_event_id` | Valuation supported by the evidence. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.document_id` | Supporting document. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.evidence_type` | Approved evidence type. | 🟧 **CONDITIONAL** — Required when verification evidence is recorded. |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.acquired_on` | Known acquisition date. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.provider_code` | Provider or institution code when applicable. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.external_reference_hash` | Non-reversible hash of an external source reference. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.metadata` | Allow-listed, source-specific provenance metadata. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.confidence` | Optional confidence score from 0 to 1. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.metadata` | Bounded, method-specific valuation details. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `cost_basis_lots.source_id` | Source supporting the acquisition lot. | 🟦 **OPTIONAL** — May be supplied. |
| `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.liability_id` | Liability causing or associated with the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.effective_to` | Date on which the restriction stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.source_id` | Evidence source supporting the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.due_on` | Known commitment due date. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_start` | Start of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_end` | End of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.source_id` | Source supporting the commitment. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.trade_date` | Trade or business-effective date. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.settled_at` | Settlement timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.description` | Sanitized transaction description. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.ends_on` | Income end date. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.growth_rate_pct` | Optional expected annual growth rate. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.source_id` | Source supporting the income stream. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.effective_to` | Date on which the liability link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.document_date` | Business-effective date printed on the document. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.expires_on` | Document expiry date. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.source_id` | Source from which the document originated. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.supersedes_version_id` | Prior document version replaced by this version. | 🟦 **OPTIONAL** — May be supplied. |
| `document_links.effective_to` | Timestamp when the document link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.expires_at` | Evidence expiry timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.notes` | Bounded verification notes. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.extension_block_end_date` | Extension block end date. Expected value: `date`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.loan_or_lien_state` | Loan or lien state. Expected value: `enum('NONE','LOAN','LIEN','UNKNOWN')`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.holding_id` | Unique identifier for the holding. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_by_principal_id` | Application principal that created the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_at` | Creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.updated_at` | Most recent update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | 🟪 **SYSTEM** — System-generated. |
| `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. | 🟪 **SYSTEM** — System-generated. |
| `sources.captured_by_principal_id` | Application principal that captured the information. | 🟪 **SYSTEM** — System-generated when a person or operator captured it. |
| `sources.captured_at` | Timestamp when the information was captured. | 🟪 **SYSTEM** — System-generated. |
| `sources.created_at` | Creation timestamp for the provenance record. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.holding_id` | Holding valued by the observation. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.recorded_at` | Timestamp when the valuation was recorded. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.holding_id` | Holding acquired through the lot. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.holding_id` | Holding affected by the restriction. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `holding_restrictions.created_at` | Creation timestamp for the restriction record. | 🟪 **SYSTEM** — System-generated. |
| `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. | 🟪 **SYSTEM** — System-generated. |
| `commitments.holding_id` | Holding associated with the commitment. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `commitments.version` | Optimistic-lock version for the commitment. | 🟪 **SYSTEM** — System-generated. |
| `transactions.transaction_id` | Unique identifier for an immutable ledger event. | 🟪 **SYSTEM** — System-generated. |
| `transactions.holding_id` | Holding affected by the transaction. | 🟪 **SYSTEM** — System-generated when recorded from the holding. |
| `transactions.recorded_at` | Timestamp when the transaction was recorded. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.income_stream_id` | Unique identifier for recurring or expected income. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.holding_id` | Asset producing the income. | 🟪 **SYSTEM** — System-generated when created from the holding. |
| `income_streams.version` | Optimistic-lock version for the income stream. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.holding_id` | Asset participating in the liability relationship. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `liability_holding_links.created_at` | Creation timestamp for the liability link. | 🟪 **SYSTEM** — System-generated. |
| `documents.document_id` | Unique identifier for supporting document metadata. | 🟪 **SYSTEM** — System-generated. |
| `documents.lifecycle_state` | Document processing and availability state. | 🟪 **SYSTEM** — System-managed. |
| `documents.current_version_id` | Current clean document version. | 🟪 **SYSTEM** — System-managed. |
| `documents.created_by_principal_id` | Application principal that created the document. | 🟪 **SYSTEM** — System-generated. |
| `documents.created_at` | Document creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.updated_at` | Document update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.version` | Optimistic-lock version for document metadata. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_version_id` | Unique identifier for an immutable document version. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_id` | Parent document. | 🟪 **SYSTEM** — System-generated from the parent document. |
| `document_versions.version_number` | Monotonic version number within the document. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.storage_zone` | Quarantine or clean object-storage zone. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.storage_key` | Random non-personal object-storage key. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.checksum_sha256` | SHA-256 integrity digest. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.mime_type` | Server-detected MIME type. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.size_bytes` | Validated object size. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.scan_state` | Malware scanning state. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.scanner_policy_version` | Scanning-policy version used. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.uploaded_at` | Upload timestamp. | 🟪 **SYSTEM** — System-generated. |
| `document_links.document_link_id` | Unique identifier linking a document to the asset. | 🟪 **SYSTEM** — System-generated. |
| `document_links.domain_type` | Approved domain-object type. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.domain_id` | Application-validated target identifier. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.holding_id` | Holding to which the document is linked. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `document_links.effective_from` | Timestamp from which the document link applies. | 🟪 **SYSTEM** — System-generated unless explicitly effective later. |
| `document_links.created_by_principal_id` | Application principal that created the link. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_state` | Pending, verified, rejected or expired state. | 🟪 **SYSTEM** — System-managed. |
| `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.verified_at` | Verification timestamp. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.created_at` | Evidence creation timestamp. | 🟪 **SYSTEM** — System-generated. |

</details>

<a id="asset-subtype-nps"></a>

<details>
<summary><strong>Asset subtype: <code>NPS</code></strong></summary>

| `table_name.column_name` | Description | Note |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_class_code` | Selected top-level asset class. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_subtype_code` | Selected asset subtype. | 🟥 **MANDATORY** — Required. |
| `holdings.name` | User-facing name for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | 🟥 **MANDATORY** — May be empty only when the subtype schema permits it. |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | 🟥 **MANDATORY** — Defaults to ACTIVE. |
| `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | 🟥 **MANDATORY** — Required for each provenance record. |
| `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | 🟥 **MANDATORY** — Required for each provenance record. |
| `ownership_allocations.person_id` | Person receiving an ownership share. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `holdings.subtype_attributes.pran_ref` | Pran ref. Expected value: `ref`. | 🟥 **MANDATORY** — Sensitive. |
| `holdings.subtype_attributes.tier` | Tier. Expected value: `enum('TIER_I','TIER_II')`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.statement_as_of` | Statement as of. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.household_id` | Household in which the holding is shown. | 🟧 **CONDITIONAL** — Mandatory when included in a household portfolio. |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | 🟧 **CONDITIONAL** — Sensitive. |
| `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | 🟧 **CONDITIONAL** — When collection depends on consent. |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | 🟧 **CONDITIONAL** — Required before the asset contributes to net worth. |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `cost_basis_lots.quantity` | Units acquired in the lot. | 🟧 **CONDITIONAL** — When the asset is quantity-based. |
| `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.acquired_on` | Acquisition date for the lot. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `holding_restrictions.restriction_type` | Approved restriction type. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.effective_from` | Date from which the restriction applies. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.status` | Restriction state: active, released or disputed. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `commitments.person_id` | Person responsible for funding the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.committed_minor_units` | Total committed amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.drawn_minor_units` | Amount already drawn. | 🟧 **CONDITIONAL** — Defaults to zero when a commitment exists. |
| `commitments.currency` | ISO 4217 currency of the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `transactions.person_id` | Person who owns the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.source_id` | Provenance source for the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.quantity` | Signed number of units affected. | 🟧 **CONDITIONAL** — When the transaction changes quantity. |
| `transactions.amount_minor_units` | Signed cash amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.currency` | ISO 4217 transaction currency. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `income_streams.person_id` | Person receiving the income. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.name` | Display name of the income stream. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.amount_minor_units` | Expected income amount in minor currency units. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.currency` | ISO 4217 income currency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.frequency` | Expected payment frequency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.starts_on` | Income start date. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.status` | Income-stream state: active, paused or ended. | 🟧 **CONDITIONAL** — Defaults to active when an income stream exists. |
| `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | 🟧 **CONDITIONAL** — Required when the asset is linked to a liability. |
| `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `liability_holding_links.effective_from` | Date from which the liability link applies. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `documents.owner_person_id` | Person who owns the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.document_type` | Approved document type. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.title` | Sanitized document title. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.retention_class` | Retention policy applied to the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `document_versions.original_filename` | Sanitized original filename. | 🟧 **CONDITIONAL** — Required when a document is uploaded. |
| `document_links.document_id` | Document linked to the asset. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `document_links.link_purpose` | Purpose such as evidence, contract or statement. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `verification_evidence.valuation_event_id` | Valuation supported by the evidence. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.document_id` | Supporting document. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.evidence_type` | Approved evidence type. | 🟧 **CONDITIONAL** — Required when verification evidence is recorded. |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.acquired_on` | Known acquisition date. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.provider_code` | Provider or institution code when applicable. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.external_reference_hash` | Non-reversible hash of an external source reference. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.metadata` | Allow-listed, source-specific provenance metadata. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.confidence` | Optional confidence score from 0 to 1. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.metadata` | Bounded, method-specific valuation details. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `cost_basis_lots.source_id` | Source supporting the acquisition lot. | 🟦 **OPTIONAL** — May be supplied. |
| `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.liability_id` | Liability causing or associated with the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.effective_to` | Date on which the restriction stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.source_id` | Evidence source supporting the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.due_on` | Known commitment due date. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_start` | Start of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_end` | End of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.source_id` | Source supporting the commitment. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.trade_date` | Trade or business-effective date. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.settled_at` | Settlement timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.description` | Sanitized transaction description. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.ends_on` | Income end date. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.growth_rate_pct` | Optional expected annual growth rate. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.source_id` | Source supporting the income stream. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.effective_to` | Date on which the liability link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.document_date` | Business-effective date printed on the document. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.expires_on` | Document expiry date. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.source_id` | Source from which the document originated. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.supersedes_version_id` | Prior document version replaced by this version. | 🟦 **OPTIONAL** — May be supplied. |
| `document_links.effective_to` | Timestamp when the document link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.expires_at` | Evidence expiry timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.notes` | Bounded verification notes. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.cra_name` | Cra name. Expected value: `str`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.pop_name` | Pop name. Expected value: `str`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.pension_fund_manager` | Pension fund manager. Expected value: `str`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.investment_choice` | Investment choice. Expected value: `enum('ACTIVE','AUTO','UNKNOWN')`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.scheme_allocation` | Scheme allocation. Expected value: `object`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.holding_id` | Unique identifier for the holding. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_by_principal_id` | Application principal that created the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_at` | Creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.updated_at` | Most recent update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | 🟪 **SYSTEM** — System-generated. |
| `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. | 🟪 **SYSTEM** — System-generated. |
| `sources.captured_by_principal_id` | Application principal that captured the information. | 🟪 **SYSTEM** — System-generated when a person or operator captured it. |
| `sources.captured_at` | Timestamp when the information was captured. | 🟪 **SYSTEM** — System-generated. |
| `sources.created_at` | Creation timestamp for the provenance record. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.holding_id` | Holding valued by the observation. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.recorded_at` | Timestamp when the valuation was recorded. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.holding_id` | Holding acquired through the lot. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.holding_id` | Holding affected by the restriction. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `holding_restrictions.created_at` | Creation timestamp for the restriction record. | 🟪 **SYSTEM** — System-generated. |
| `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. | 🟪 **SYSTEM** — System-generated. |
| `commitments.holding_id` | Holding associated with the commitment. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `commitments.version` | Optimistic-lock version for the commitment. | 🟪 **SYSTEM** — System-generated. |
| `transactions.transaction_id` | Unique identifier for an immutable ledger event. | 🟪 **SYSTEM** — System-generated. |
| `transactions.holding_id` | Holding affected by the transaction. | 🟪 **SYSTEM** — System-generated when recorded from the holding. |
| `transactions.recorded_at` | Timestamp when the transaction was recorded. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.income_stream_id` | Unique identifier for recurring or expected income. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.holding_id` | Asset producing the income. | 🟪 **SYSTEM** — System-generated when created from the holding. |
| `income_streams.version` | Optimistic-lock version for the income stream. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.holding_id` | Asset participating in the liability relationship. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `liability_holding_links.created_at` | Creation timestamp for the liability link. | 🟪 **SYSTEM** — System-generated. |
| `documents.document_id` | Unique identifier for supporting document metadata. | 🟪 **SYSTEM** — System-generated. |
| `documents.lifecycle_state` | Document processing and availability state. | 🟪 **SYSTEM** — System-managed. |
| `documents.current_version_id` | Current clean document version. | 🟪 **SYSTEM** — System-managed. |
| `documents.created_by_principal_id` | Application principal that created the document. | 🟪 **SYSTEM** — System-generated. |
| `documents.created_at` | Document creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.updated_at` | Document update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.version` | Optimistic-lock version for document metadata. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_version_id` | Unique identifier for an immutable document version. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_id` | Parent document. | 🟪 **SYSTEM** — System-generated from the parent document. |
| `document_versions.version_number` | Monotonic version number within the document. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.storage_zone` | Quarantine or clean object-storage zone. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.storage_key` | Random non-personal object-storage key. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.checksum_sha256` | SHA-256 integrity digest. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.mime_type` | Server-detected MIME type. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.size_bytes` | Validated object size. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.scan_state` | Malware scanning state. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.scanner_policy_version` | Scanning-policy version used. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.uploaded_at` | Upload timestamp. | 🟪 **SYSTEM** — System-generated. |
| `document_links.document_link_id` | Unique identifier linking a document to the asset. | 🟪 **SYSTEM** — System-generated. |
| `document_links.domain_type` | Approved domain-object type. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.domain_id` | Application-validated target identifier. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.holding_id` | Holding to which the document is linked. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `document_links.effective_from` | Timestamp from which the document link applies. | 🟪 **SYSTEM** — System-generated unless explicitly effective later. |
| `document_links.created_by_principal_id` | Application principal that created the link. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_state` | Pending, verified, rejected or expired state. | 🟪 **SYSTEM** — System-managed. |
| `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.verified_at` | Verification timestamp. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.created_at` | Evidence creation timestamp. | 🟪 **SYSTEM** — System-generated. |

</details>

<a id="asset-subtype-ssy"></a>

<details>
<summary><strong>Asset subtype: <code>SSY</code></strong></summary>

| `table_name.column_name` | Description | Note |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_class_code` | Selected top-level asset class. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_subtype_code` | Selected asset subtype. | 🟥 **MANDATORY** — Required. |
| `holdings.name` | User-facing name for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | 🟥 **MANDATORY** — May be empty only when the subtype schema permits it. |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | 🟥 **MANDATORY** — Defaults to ACTIVE. |
| `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | 🟥 **MANDATORY** — Required for each provenance record. |
| `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | 🟥 **MANDATORY** — Required for each provenance record. |
| `ownership_allocations.person_id` | Person receiving an ownership share. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | 🟥 **MANDATORY** — Sensitive. |
| `holdings.subtype_attributes.beneficiary_person_id` | Beneficiary person ID. Expected value: `ref`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.household_id` | Household in which the holding is shown. | 🟧 **CONDITIONAL** — Mandatory when included in a household portfolio. |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | 🟧 **CONDITIONAL** — Sensitive. |
| `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | 🟧 **CONDITIONAL** — When collection depends on consent. |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | 🟧 **CONDITIONAL** — Required before the asset contributes to net worth. |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `cost_basis_lots.quantity` | Units acquired in the lot. | 🟧 **CONDITIONAL** — When the asset is quantity-based. |
| `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.acquired_on` | Acquisition date for the lot. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `holding_restrictions.restriction_type` | Approved restriction type. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.effective_from` | Date from which the restriction applies. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.status` | Restriction state: active, released or disputed. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `commitments.person_id` | Person responsible for funding the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.committed_minor_units` | Total committed amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.drawn_minor_units` | Amount already drawn. | 🟧 **CONDITIONAL** — Defaults to zero when a commitment exists. |
| `commitments.currency` | ISO 4217 currency of the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `transactions.person_id` | Person who owns the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.source_id` | Provenance source for the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.quantity` | Signed number of units affected. | 🟧 **CONDITIONAL** — When the transaction changes quantity. |
| `transactions.amount_minor_units` | Signed cash amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.currency` | ISO 4217 transaction currency. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `income_streams.person_id` | Person receiving the income. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.name` | Display name of the income stream. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.amount_minor_units` | Expected income amount in minor currency units. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.currency` | ISO 4217 income currency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.frequency` | Expected payment frequency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.starts_on` | Income start date. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.status` | Income-stream state: active, paused or ended. | 🟧 **CONDITIONAL** — Defaults to active when an income stream exists. |
| `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | 🟧 **CONDITIONAL** — Required when the asset is linked to a liability. |
| `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `liability_holding_links.effective_from` | Date from which the liability link applies. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `documents.owner_person_id` | Person who owns the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.document_type` | Approved document type. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.title` | Sanitized document title. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.retention_class` | Retention policy applied to the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `document_versions.original_filename` | Sanitized original filename. | 🟧 **CONDITIONAL** — Required when a document is uploaded. |
| `document_links.document_id` | Document linked to the asset. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `document_links.link_purpose` | Purpose such as evidence, contract or statement. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `verification_evidence.valuation_event_id` | Valuation supported by the evidence. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.document_id` | Supporting document. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.evidence_type` | Approved evidence type. | 🟧 **CONDITIONAL** — Required when verification evidence is recorded. |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.guardian_person_id` | Guardian person ID. Expected value: `ref`. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.acquired_on` | Known acquisition date. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.provider_code` | Provider or institution code when applicable. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.external_reference_hash` | Non-reversible hash of an external source reference. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.metadata` | Allow-listed, source-specific provenance metadata. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.confidence` | Optional confidence score from 0 to 1. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.metadata` | Bounded, method-specific valuation details. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `cost_basis_lots.source_id` | Source supporting the acquisition lot. | 🟦 **OPTIONAL** — May be supplied. |
| `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.liability_id` | Liability causing or associated with the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.effective_to` | Date on which the restriction stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.source_id` | Evidence source supporting the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.due_on` | Known commitment due date. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_start` | Start of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_end` | End of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.source_id` | Source supporting the commitment. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.trade_date` | Trade or business-effective date. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.settled_at` | Settlement timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.description` | Sanitized transaction description. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.ends_on` | Income end date. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.growth_rate_pct` | Optional expected annual growth rate. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.source_id` | Source supporting the income stream. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.effective_to` | Date on which the liability link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.document_date` | Business-effective date printed on the document. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.expires_on` | Document expiry date. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.source_id` | Source from which the document originated. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.supersedes_version_id` | Prior document version replaced by this version. | 🟦 **OPTIONAL** — May be supplied. |
| `document_links.effective_to` | Timestamp when the document link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.expires_at` | Evidence expiry timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.notes` | Bounded verification notes. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.annual_deposit_amount` | Annual deposit amount. Expected value: `money`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.holding_id` | Unique identifier for the holding. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_by_principal_id` | Application principal that created the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_at` | Creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.updated_at` | Most recent update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | 🟪 **SYSTEM** — System-generated. |
| `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. | 🟪 **SYSTEM** — System-generated. |
| `sources.captured_by_principal_id` | Application principal that captured the information. | 🟪 **SYSTEM** — System-generated when a person or operator captured it. |
| `sources.captured_at` | Timestamp when the information was captured. | 🟪 **SYSTEM** — System-generated. |
| `sources.created_at` | Creation timestamp for the provenance record. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.holding_id` | Holding valued by the observation. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.recorded_at` | Timestamp when the valuation was recorded. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.holding_id` | Holding acquired through the lot. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.holding_id` | Holding affected by the restriction. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `holding_restrictions.created_at` | Creation timestamp for the restriction record. | 🟪 **SYSTEM** — System-generated. |
| `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. | 🟪 **SYSTEM** — System-generated. |
| `commitments.holding_id` | Holding associated with the commitment. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `commitments.version` | Optimistic-lock version for the commitment. | 🟪 **SYSTEM** — System-generated. |
| `transactions.transaction_id` | Unique identifier for an immutable ledger event. | 🟪 **SYSTEM** — System-generated. |
| `transactions.holding_id` | Holding affected by the transaction. | 🟪 **SYSTEM** — System-generated when recorded from the holding. |
| `transactions.recorded_at` | Timestamp when the transaction was recorded. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.income_stream_id` | Unique identifier for recurring or expected income. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.holding_id` | Asset producing the income. | 🟪 **SYSTEM** — System-generated when created from the holding. |
| `income_streams.version` | Optimistic-lock version for the income stream. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.holding_id` | Asset participating in the liability relationship. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `liability_holding_links.created_at` | Creation timestamp for the liability link. | 🟪 **SYSTEM** — System-generated. |
| `documents.document_id` | Unique identifier for supporting document metadata. | 🟪 **SYSTEM** — System-generated. |
| `documents.lifecycle_state` | Document processing and availability state. | 🟪 **SYSTEM** — System-managed. |
| `documents.current_version_id` | Current clean document version. | 🟪 **SYSTEM** — System-managed. |
| `documents.created_by_principal_id` | Application principal that created the document. | 🟪 **SYSTEM** — System-generated. |
| `documents.created_at` | Document creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.updated_at` | Document update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.version` | Optimistic-lock version for document metadata. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_version_id` | Unique identifier for an immutable document version. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_id` | Parent document. | 🟪 **SYSTEM** — System-generated from the parent document. |
| `document_versions.version_number` | Monotonic version number within the document. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.storage_zone` | Quarantine or clean object-storage zone. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.storage_key` | Random non-personal object-storage key. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.checksum_sha256` | SHA-256 integrity digest. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.mime_type` | Server-detected MIME type. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.size_bytes` | Validated object size. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.scan_state` | Malware scanning state. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.scanner_policy_version` | Scanning-policy version used. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.uploaded_at` | Upload timestamp. | 🟪 **SYSTEM** — System-generated. |
| `document_links.document_link_id` | Unique identifier linking a document to the asset. | 🟪 **SYSTEM** — System-generated. |
| `document_links.domain_type` | Approved domain-object type. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.domain_id` | Application-validated target identifier. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.holding_id` | Holding to which the document is linked. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `document_links.effective_from` | Timestamp from which the document link applies. | 🟪 **SYSTEM** — System-generated unless explicitly effective later. |
| `document_links.created_by_principal_id` | Application principal that created the link. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_state` | Pending, verified, rejected or expired state. | 🟪 **SYSTEM** — System-managed. |
| `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.verified_at` | Verification timestamp. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.created_at` | Evidence creation timestamp. | 🟪 **SYSTEM** — System-generated. |

</details>

<a id="asset-subtype-scss"></a>

<details>
<summary><strong>Asset subtype: <code>SCSS</code></strong></summary>

| `table_name.column_name` | Description | Note |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_class_code` | Selected top-level asset class. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_subtype_code` | Selected asset subtype. | 🟥 **MANDATORY** — Required. |
| `holdings.name` | User-facing name for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | 🟥 **MANDATORY** — May be empty only when the subtype schema permits it. |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | 🟥 **MANDATORY** — Defaults to ACTIVE. |
| `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | 🟥 **MANDATORY** — Required for each provenance record. |
| `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | 🟥 **MANDATORY** — Required for each provenance record. |
| `ownership_allocations.person_id` | Person receiving an ownership share. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | 🟥 **MANDATORY** — Sensitive. |
| `holdings.subtype_attributes.opened_on` | Opened on. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.deposit_amount` | Deposit amount. Expected value: `money`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.interest_payout_frequency` | Interest payout frequency. Expected value: `enum`. | 🟥 **MANDATORY** — Required. |
| `holdings.household_id` | Household in which the holding is shown. | 🟧 **CONDITIONAL** — Mandatory when included in a household portfolio. |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | 🟧 **CONDITIONAL** — Sensitive. |
| `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | 🟧 **CONDITIONAL** — When collection depends on consent. |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | 🟧 **CONDITIONAL** — Required before the asset contributes to net worth. |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `cost_basis_lots.quantity` | Units acquired in the lot. | 🟧 **CONDITIONAL** — When the asset is quantity-based. |
| `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.acquired_on` | Acquisition date for the lot. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `holding_restrictions.restriction_type` | Approved restriction type. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.effective_from` | Date from which the restriction applies. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.status` | Restriction state: active, released or disputed. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `commitments.person_id` | Person responsible for funding the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.committed_minor_units` | Total committed amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.drawn_minor_units` | Amount already drawn. | 🟧 **CONDITIONAL** — Defaults to zero when a commitment exists. |
| `commitments.currency` | ISO 4217 currency of the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `transactions.person_id` | Person who owns the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.source_id` | Provenance source for the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.quantity` | Signed number of units affected. | 🟧 **CONDITIONAL** — When the transaction changes quantity. |
| `transactions.amount_minor_units` | Signed cash amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.currency` | ISO 4217 transaction currency. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `income_streams.person_id` | Person receiving the income. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.name` | Display name of the income stream. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.amount_minor_units` | Expected income amount in minor currency units. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.currency` | ISO 4217 income currency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.frequency` | Expected payment frequency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.starts_on` | Income start date. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.status` | Income-stream state: active, paused or ended. | 🟧 **CONDITIONAL** — Defaults to active when an income stream exists. |
| `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | 🟧 **CONDITIONAL** — Required when the asset is linked to a liability. |
| `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `liability_holding_links.effective_from` | Date from which the liability link applies. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `documents.owner_person_id` | Person who owns the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.document_type` | Approved document type. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.title` | Sanitized document title. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.retention_class` | Retention policy applied to the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `document_versions.original_filename` | Sanitized original filename. | 🟧 **CONDITIONAL** — Required when a document is uploaded. |
| `document_links.document_id` | Document linked to the asset. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `document_links.link_purpose` | Purpose such as evidence, contract or statement. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `verification_evidence.valuation_event_id` | Valuation supported by the evidence. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.document_id` | Supporting document. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.evidence_type` | Approved evidence type. | 🟧 **CONDITIONAL** — Required when verification evidence is recorded. |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.acquired_on` | Known acquisition date. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.provider_code` | Provider or institution code when applicable. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.external_reference_hash` | Non-reversible hash of an external source reference. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.metadata` | Allow-listed, source-specific provenance metadata. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.confidence` | Optional confidence score from 0 to 1. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.metadata` | Bounded, method-specific valuation details. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `cost_basis_lots.source_id` | Source supporting the acquisition lot. | 🟦 **OPTIONAL** — May be supplied. |
| `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.liability_id` | Liability causing or associated with the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.effective_to` | Date on which the restriction stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.source_id` | Evidence source supporting the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.due_on` | Known commitment due date. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_start` | Start of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_end` | End of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.source_id` | Source supporting the commitment. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.trade_date` | Trade or business-effective date. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.settled_at` | Settlement timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.description` | Sanitized transaction description. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.ends_on` | Income end date. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.growth_rate_pct` | Optional expected annual growth rate. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.source_id` | Source supporting the income stream. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.effective_to` | Date on which the liability link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.document_date` | Business-effective date printed on the document. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.expires_on` | Document expiry date. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.source_id` | Source from which the document originated. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.supersedes_version_id` | Prior document version replaced by this version. | 🟦 **OPTIONAL** — May be supplied. |
| `document_links.effective_to` | Timestamp when the document link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.expires_at` | Evidence expiry timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.notes` | Bounded verification notes. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.extension_end_date` | Extension end date. Expected value: `date`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.holding_id` | Unique identifier for the holding. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_by_principal_id` | Application principal that created the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_at` | Creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.updated_at` | Most recent update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | 🟪 **SYSTEM** — System-generated. |
| `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. | 🟪 **SYSTEM** — System-generated. |
| `sources.captured_by_principal_id` | Application principal that captured the information. | 🟪 **SYSTEM** — System-generated when a person or operator captured it. |
| `sources.captured_at` | Timestamp when the information was captured. | 🟪 **SYSTEM** — System-generated. |
| `sources.created_at` | Creation timestamp for the provenance record. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.holding_id` | Holding valued by the observation. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.recorded_at` | Timestamp when the valuation was recorded. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.holding_id` | Holding acquired through the lot. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.holding_id` | Holding affected by the restriction. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `holding_restrictions.created_at` | Creation timestamp for the restriction record. | 🟪 **SYSTEM** — System-generated. |
| `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. | 🟪 **SYSTEM** — System-generated. |
| `commitments.holding_id` | Holding associated with the commitment. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `commitments.version` | Optimistic-lock version for the commitment. | 🟪 **SYSTEM** — System-generated. |
| `transactions.transaction_id` | Unique identifier for an immutable ledger event. | 🟪 **SYSTEM** — System-generated. |
| `transactions.holding_id` | Holding affected by the transaction. | 🟪 **SYSTEM** — System-generated when recorded from the holding. |
| `transactions.recorded_at` | Timestamp when the transaction was recorded. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.income_stream_id` | Unique identifier for recurring or expected income. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.holding_id` | Asset producing the income. | 🟪 **SYSTEM** — System-generated when created from the holding. |
| `income_streams.version` | Optimistic-lock version for the income stream. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.holding_id` | Asset participating in the liability relationship. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `liability_holding_links.created_at` | Creation timestamp for the liability link. | 🟪 **SYSTEM** — System-generated. |
| `documents.document_id` | Unique identifier for supporting document metadata. | 🟪 **SYSTEM** — System-generated. |
| `documents.lifecycle_state` | Document processing and availability state. | 🟪 **SYSTEM** — System-managed. |
| `documents.current_version_id` | Current clean document version. | 🟪 **SYSTEM** — System-managed. |
| `documents.created_by_principal_id` | Application principal that created the document. | 🟪 **SYSTEM** — System-generated. |
| `documents.created_at` | Document creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.updated_at` | Document update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.version` | Optimistic-lock version for document metadata. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_version_id` | Unique identifier for an immutable document version. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_id` | Parent document. | 🟪 **SYSTEM** — System-generated from the parent document. |
| `document_versions.version_number` | Monotonic version number within the document. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.storage_zone` | Quarantine or clean object-storage zone. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.storage_key` | Random non-personal object-storage key. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.checksum_sha256` | SHA-256 integrity digest. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.mime_type` | Server-detected MIME type. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.size_bytes` | Validated object size. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.scan_state` | Malware scanning state. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.scanner_policy_version` | Scanning-policy version used. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.uploaded_at` | Upload timestamp. | 🟪 **SYSTEM** — System-generated. |
| `document_links.document_link_id` | Unique identifier linking a document to the asset. | 🟪 **SYSTEM** — System-generated. |
| `document_links.domain_type` | Approved domain-object type. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.domain_id` | Application-validated target identifier. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.holding_id` | Holding to which the document is linked. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `document_links.effective_from` | Timestamp from which the document link applies. | 🟪 **SYSTEM** — System-generated unless explicitly effective later. |
| `document_links.created_by_principal_id` | Application principal that created the link. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_state` | Pending, verified, rejected or expired state. | 🟪 **SYSTEM** — System-managed. |
| `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.verified_at` | Verification timestamp. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.created_at` | Evidence creation timestamp. | 🟪 **SYSTEM** — System-generated. |

</details>

<a id="asset-subtype-post-office-savings"></a>

<details>
<summary><strong>Asset subtype: <code>POST_OFFICE_SAVINGS</code></strong></summary>

| `table_name.column_name` | Description | Note |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_class_code` | Selected top-level asset class. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_subtype_code` | Selected asset subtype. | 🟥 **MANDATORY** — Required. |
| `holdings.name` | User-facing name for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | 🟥 **MANDATORY** — May be empty only when the subtype schema permits it. |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | 🟥 **MANDATORY** — Defaults to ACTIVE. |
| `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | 🟥 **MANDATORY** — Required for each provenance record. |
| `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | 🟥 **MANDATORY** — Required for each provenance record. |
| `ownership_allocations.person_id` | Person receiving an ownership share. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `holdings.subtype_attributes.institution_name` | Institution name. Expected value: `str`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.account_ref` | Account ref. Expected value: `ref`. | 🟥 **MANDATORY** — Sensitive. |
| `holdings.subtype_attributes.scheme_kind` | Scheme kind. Expected value: `enum('SAVINGS','RD','TD','MIS','NSC','KVP','OTHER')`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.opened_or_issue_date` | Opened or issue date. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.household_id` | Household in which the holding is shown. | 🟧 **CONDITIONAL** — Mandatory when included in a household portfolio. |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | 🟧 **CONDITIONAL** — Sensitive. |
| `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | 🟧 **CONDITIONAL** — When collection depends on consent. |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | 🟧 **CONDITIONAL** — Required before the asset contributes to net worth. |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `cost_basis_lots.quantity` | Units acquired in the lot. | 🟧 **CONDITIONAL** — When the asset is quantity-based. |
| `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.acquired_on` | Acquisition date for the lot. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `holding_restrictions.restriction_type` | Approved restriction type. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.effective_from` | Date from which the restriction applies. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.status` | Restriction state: active, released or disputed. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `commitments.person_id` | Person responsible for funding the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.committed_minor_units` | Total committed amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.drawn_minor_units` | Amount already drawn. | 🟧 **CONDITIONAL** — Defaults to zero when a commitment exists. |
| `commitments.currency` | ISO 4217 currency of the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `transactions.person_id` | Person who owns the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.source_id` | Provenance source for the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.quantity` | Signed number of units affected. | 🟧 **CONDITIONAL** — When the transaction changes quantity. |
| `transactions.amount_minor_units` | Signed cash amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.currency` | ISO 4217 transaction currency. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `income_streams.person_id` | Person receiving the income. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.name` | Display name of the income stream. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.amount_minor_units` | Expected income amount in minor currency units. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.currency` | ISO 4217 income currency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.frequency` | Expected payment frequency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.starts_on` | Income start date. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.status` | Income-stream state: active, paused or ended. | 🟧 **CONDITIONAL** — Defaults to active when an income stream exists. |
| `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | 🟧 **CONDITIONAL** — Required when the asset is linked to a liability. |
| `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `liability_holding_links.effective_from` | Date from which the liability link applies. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `documents.owner_person_id` | Person who owns the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.document_type` | Approved document type. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.title` | Sanitized document title. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.retention_class` | Retention policy applied to the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `document_versions.original_filename` | Sanitized original filename. | 🟧 **CONDITIONAL** — Required when a document is uploaded. |
| `document_links.document_id` | Document linked to the asset. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `document_links.link_purpose` | Purpose such as evidence, contract or statement. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `verification_evidence.valuation_event_id` | Valuation supported by the evidence. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.document_id` | Supporting document. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.evidence_type` | Approved evidence type. | 🟧 **CONDITIONAL** — Required when verification evidence is recorded. |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.certificate_ref` | Certificate ref. Expected value: `ref`. | 🟧 **CONDITIONAL** — Sensitive. |
| `holdings.subtype_attributes.maturity_date` | Maturity date. Expected value: `date`. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.acquired_on` | Known acquisition date. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.provider_code` | Provider or institution code when applicable. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.external_reference_hash` | Non-reversible hash of an external source reference. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.metadata` | Allow-listed, source-specific provenance metadata. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.confidence` | Optional confidence score from 0 to 1. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.metadata` | Bounded, method-specific valuation details. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `cost_basis_lots.source_id` | Source supporting the acquisition lot. | 🟦 **OPTIONAL** — May be supplied. |
| `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.liability_id` | Liability causing or associated with the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.effective_to` | Date on which the restriction stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.source_id` | Evidence source supporting the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.due_on` | Known commitment due date. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_start` | Start of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_end` | End of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.source_id` | Source supporting the commitment. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.trade_date` | Trade or business-effective date. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.settled_at` | Settlement timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.description` | Sanitized transaction description. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.ends_on` | Income end date. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.growth_rate_pct` | Optional expected annual growth rate. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.source_id` | Source supporting the income stream. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.effective_to` | Date on which the liability link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.document_date` | Business-effective date printed on the document. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.expires_on` | Document expiry date. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.source_id` | Source from which the document originated. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.supersedes_version_id` | Prior document version replaced by this version. | 🟦 **OPTIONAL** — May be supplied. |
| `document_links.effective_to` | Timestamp when the document link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.expires_at` | Evidence expiry timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.notes` | Bounded verification notes. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.principal_amount` | Principal amount. Expected value: `money`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.interest_rate_pct` | Interest rate pct. Expected value: `pct`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.payout_frequency` | Payout frequency. Expected value: `enum`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.holding_id` | Unique identifier for the holding. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_by_principal_id` | Application principal that created the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_at` | Creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.updated_at` | Most recent update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | 🟪 **SYSTEM** — System-generated. |
| `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. | 🟪 **SYSTEM** — System-generated. |
| `sources.captured_by_principal_id` | Application principal that captured the information. | 🟪 **SYSTEM** — System-generated when a person or operator captured it. |
| `sources.captured_at` | Timestamp when the information was captured. | 🟪 **SYSTEM** — System-generated. |
| `sources.created_at` | Creation timestamp for the provenance record. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.holding_id` | Holding valued by the observation. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.recorded_at` | Timestamp when the valuation was recorded. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.holding_id` | Holding acquired through the lot. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.holding_id` | Holding affected by the restriction. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `holding_restrictions.created_at` | Creation timestamp for the restriction record. | 🟪 **SYSTEM** — System-generated. |
| `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. | 🟪 **SYSTEM** — System-generated. |
| `commitments.holding_id` | Holding associated with the commitment. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `commitments.version` | Optimistic-lock version for the commitment. | 🟪 **SYSTEM** — System-generated. |
| `transactions.transaction_id` | Unique identifier for an immutable ledger event. | 🟪 **SYSTEM** — System-generated. |
| `transactions.holding_id` | Holding affected by the transaction. | 🟪 **SYSTEM** — System-generated when recorded from the holding. |
| `transactions.recorded_at` | Timestamp when the transaction was recorded. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.income_stream_id` | Unique identifier for recurring or expected income. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.holding_id` | Asset producing the income. | 🟪 **SYSTEM** — System-generated when created from the holding. |
| `income_streams.version` | Optimistic-lock version for the income stream. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.holding_id` | Asset participating in the liability relationship. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `liability_holding_links.created_at` | Creation timestamp for the liability link. | 🟪 **SYSTEM** — System-generated. |
| `documents.document_id` | Unique identifier for supporting document metadata. | 🟪 **SYSTEM** — System-generated. |
| `documents.lifecycle_state` | Document processing and availability state. | 🟪 **SYSTEM** — System-managed. |
| `documents.current_version_id` | Current clean document version. | 🟪 **SYSTEM** — System-managed. |
| `documents.created_by_principal_id` | Application principal that created the document. | 🟪 **SYSTEM** — System-generated. |
| `documents.created_at` | Document creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.updated_at` | Document update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.version` | Optimistic-lock version for document metadata. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_version_id` | Unique identifier for an immutable document version. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_id` | Parent document. | 🟪 **SYSTEM** — System-generated from the parent document. |
| `document_versions.version_number` | Monotonic version number within the document. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.storage_zone` | Quarantine or clean object-storage zone. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.storage_key` | Random non-personal object-storage key. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.checksum_sha256` | SHA-256 integrity digest. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.mime_type` | Server-detected MIME type. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.size_bytes` | Validated object size. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.scan_state` | Malware scanning state. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.scanner_policy_version` | Scanning-policy version used. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.uploaded_at` | Upload timestamp. | 🟪 **SYSTEM** — System-generated. |
| `document_links.document_link_id` | Unique identifier linking a document to the asset. | 🟪 **SYSTEM** — System-generated. |
| `document_links.domain_type` | Approved domain-object type. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.domain_id` | Application-validated target identifier. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.holding_id` | Holding to which the document is linked. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `document_links.effective_from` | Timestamp from which the document link applies. | 🟪 **SYSTEM** — System-generated unless explicitly effective later. |
| `document_links.created_by_principal_id` | Application principal that created the link. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_state` | Pending, verified, rejected or expired state. | 🟪 **SYSTEM** — System-managed. |
| `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.verified_at` | Verification timestamp. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.created_at` | Evidence creation timestamp. | 🟪 **SYSTEM** — System-generated. |

</details>

<a id="asset-subtype-apy"></a>

<details>
<summary><strong>Asset subtype: <code>APY</code></strong></summary>

| `table_name.column_name` | Description | Note |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_class_code` | Selected top-level asset class. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_subtype_code` | Selected asset subtype. | 🟥 **MANDATORY** — Required. |
| `holdings.name` | User-facing name for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | 🟥 **MANDATORY** — May be empty only when the subtype schema permits it. |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | 🟥 **MANDATORY** — Defaults to ACTIVE. |
| `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | 🟥 **MANDATORY** — Required for each provenance record. |
| `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | 🟥 **MANDATORY** — Required for each provenance record. |
| `ownership_allocations.person_id` | Person receiving an ownership share. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `holdings.subtype_attributes.pran_ref` | Pran ref. Expected value: `ref`. | 🟥 **MANDATORY** — Sensitive. |
| `holdings.subtype_attributes.contribution_frequency` | Contribution frequency. Expected value: `enum`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.contribution_amount` | Contribution amount. Expected value: `money`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.statement_as_of` | Statement as of. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.household_id` | Household in which the holding is shown. | 🟧 **CONDITIONAL** — Mandatory when included in a household portfolio. |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | 🟧 **CONDITIONAL** — Sensitive. |
| `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | 🟧 **CONDITIONAL** — When collection depends on consent. |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | 🟧 **CONDITIONAL** — Required before the asset contributes to net worth. |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `cost_basis_lots.quantity` | Units acquired in the lot. | 🟧 **CONDITIONAL** — When the asset is quantity-based. |
| `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.acquired_on` | Acquisition date for the lot. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `holding_restrictions.restriction_type` | Approved restriction type. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.effective_from` | Date from which the restriction applies. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.status` | Restriction state: active, released or disputed. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `commitments.person_id` | Person responsible for funding the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.committed_minor_units` | Total committed amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.drawn_minor_units` | Amount already drawn. | 🟧 **CONDITIONAL** — Defaults to zero when a commitment exists. |
| `commitments.currency` | ISO 4217 currency of the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `transactions.person_id` | Person who owns the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.source_id` | Provenance source for the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.quantity` | Signed number of units affected. | 🟧 **CONDITIONAL** — When the transaction changes quantity. |
| `transactions.amount_minor_units` | Signed cash amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.currency` | ISO 4217 transaction currency. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `income_streams.person_id` | Person receiving the income. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.name` | Display name of the income stream. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.amount_minor_units` | Expected income amount in minor currency units. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.currency` | ISO 4217 income currency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.frequency` | Expected payment frequency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.starts_on` | Income start date. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.status` | Income-stream state: active, paused or ended. | 🟧 **CONDITIONAL** — Defaults to active when an income stream exists. |
| `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | 🟧 **CONDITIONAL** — Required when the asset is linked to a liability. |
| `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `liability_holding_links.effective_from` | Date from which the liability link applies. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `documents.owner_person_id` | Person who owns the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.document_type` | Approved document type. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.title` | Sanitized document title. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.retention_class` | Retention policy applied to the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `document_versions.original_filename` | Sanitized original filename. | 🟧 **CONDITIONAL** — Required when a document is uploaded. |
| `document_links.document_id` | Document linked to the asset. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `document_links.link_purpose` | Purpose such as evidence, contract or statement. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `verification_evidence.valuation_event_id` | Valuation supported by the evidence. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.document_id` | Supporting document. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.evidence_type` | Approved evidence type. | 🟧 **CONDITIONAL** — Required when verification evidence is recorded. |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.acquired_on` | Known acquisition date. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.provider_code` | Provider or institution code when applicable. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.external_reference_hash` | Non-reversible hash of an external source reference. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.metadata` | Allow-listed, source-specific provenance metadata. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.confidence` | Optional confidence score from 0 to 1. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.metadata` | Bounded, method-specific valuation details. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `cost_basis_lots.source_id` | Source supporting the acquisition lot. | 🟦 **OPTIONAL** — May be supplied. |
| `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.liability_id` | Liability causing or associated with the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.effective_to` | Date on which the restriction stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.source_id` | Evidence source supporting the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.due_on` | Known commitment due date. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_start` | Start of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_end` | End of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.source_id` | Source supporting the commitment. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.trade_date` | Trade or business-effective date. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.settled_at` | Settlement timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.description` | Sanitized transaction description. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.ends_on` | Income end date. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.growth_rate_pct` | Optional expected annual growth rate. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.source_id` | Source supporting the income stream. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.effective_to` | Date on which the liability link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.document_date` | Business-effective date printed on the document. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.expires_on` | Document expiry date. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.source_id` | Source from which the document originated. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.supersedes_version_id` | Prior document version replaced by this version. | 🟦 **OPTIONAL** — May be supplied. |
| `document_links.effective_to` | Timestamp when the document link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.expires_at` | Evidence expiry timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.notes` | Bounded verification notes. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.bank_or_pop_name` | Bank or pop name. Expected value: `str`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.guaranteed_pension_band` | Guaranteed pension band. Expected value: `money`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.pension_start_date` | Pension start date. Expected value: `date`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.spouse_person_id` | Spouse person ID. Expected value: `ref`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.holding_id` | Unique identifier for the holding. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_by_principal_id` | Application principal that created the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_at` | Creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.updated_at` | Most recent update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | 🟪 **SYSTEM** — System-generated. |
| `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. | 🟪 **SYSTEM** — System-generated. |
| `sources.captured_by_principal_id` | Application principal that captured the information. | 🟪 **SYSTEM** — System-generated when a person or operator captured it. |
| `sources.captured_at` | Timestamp when the information was captured. | 🟪 **SYSTEM** — System-generated. |
| `sources.created_at` | Creation timestamp for the provenance record. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.holding_id` | Holding valued by the observation. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.recorded_at` | Timestamp when the valuation was recorded. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.holding_id` | Holding acquired through the lot. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.holding_id` | Holding affected by the restriction. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `holding_restrictions.created_at` | Creation timestamp for the restriction record. | 🟪 **SYSTEM** — System-generated. |
| `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. | 🟪 **SYSTEM** — System-generated. |
| `commitments.holding_id` | Holding associated with the commitment. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `commitments.version` | Optimistic-lock version for the commitment. | 🟪 **SYSTEM** — System-generated. |
| `transactions.transaction_id` | Unique identifier for an immutable ledger event. | 🟪 **SYSTEM** — System-generated. |
| `transactions.holding_id` | Holding affected by the transaction. | 🟪 **SYSTEM** — System-generated when recorded from the holding. |
| `transactions.recorded_at` | Timestamp when the transaction was recorded. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.income_stream_id` | Unique identifier for recurring or expected income. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.holding_id` | Asset producing the income. | 🟪 **SYSTEM** — System-generated when created from the holding. |
| `income_streams.version` | Optimistic-lock version for the income stream. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.holding_id` | Asset participating in the liability relationship. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `liability_holding_links.created_at` | Creation timestamp for the liability link. | 🟪 **SYSTEM** — System-generated. |
| `documents.document_id` | Unique identifier for supporting document metadata. | 🟪 **SYSTEM** — System-generated. |
| `documents.lifecycle_state` | Document processing and availability state. | 🟪 **SYSTEM** — System-managed. |
| `documents.current_version_id` | Current clean document version. | 🟪 **SYSTEM** — System-managed. |
| `documents.created_by_principal_id` | Application principal that created the document. | 🟪 **SYSTEM** — System-generated. |
| `documents.created_at` | Document creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.updated_at` | Document update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.version` | Optimistic-lock version for document metadata. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_version_id` | Unique identifier for an immutable document version. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_id` | Parent document. | 🟪 **SYSTEM** — System-generated from the parent document. |
| `document_versions.version_number` | Monotonic version number within the document. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.storage_zone` | Quarantine or clean object-storage zone. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.storage_key` | Random non-personal object-storage key. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.checksum_sha256` | SHA-256 integrity digest. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.mime_type` | Server-detected MIME type. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.size_bytes` | Validated object size. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.scan_state` | Malware scanning state. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.scanner_policy_version` | Scanning-policy version used. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.uploaded_at` | Upload timestamp. | 🟪 **SYSTEM** — System-generated. |
| `document_links.document_link_id` | Unique identifier linking a document to the asset. | 🟪 **SYSTEM** — System-generated. |
| `document_links.domain_type` | Approved domain-object type. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.domain_id` | Application-validated target identifier. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.holding_id` | Holding to which the document is linked. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `document_links.effective_from` | Timestamp from which the document link applies. | 🟪 **SYSTEM** — System-generated unless explicitly effective later. |
| `document_links.created_by_principal_id` | Application principal that created the link. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_state` | Pending, verified, rejected or expired state. | 🟪 **SYSTEM** — System-managed. |
| `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.verified_at` | Verification timestamp. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.created_at` | Evidence creation timestamp. | 🟪 **SYSTEM** — System-generated. |

</details>

<a id="asset-subtype-gratuity"></a>

<details>
<summary><strong>Asset subtype: <code>GRATUITY</code></strong></summary>

| `table_name.column_name` | Description | Note |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_class_code` | Selected top-level asset class. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_subtype_code` | Selected asset subtype. | 🟥 **MANDATORY** — Required. |
| `holdings.name` | User-facing name for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | 🟥 **MANDATORY** — May be empty only when the subtype schema permits it. |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | 🟥 **MANDATORY** — Defaults to ACTIVE. |
| `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | 🟥 **MANDATORY** — Required for each provenance record. |
| `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | 🟥 **MANDATORY** — Required for each provenance record. |
| `ownership_allocations.person_id` | Person receiving an ownership share. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `holdings.subtype_attributes.employer_name` | Employer name. Expected value: `str`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.employment_start_date` | Employment start date. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.household_id` | Household in which the holding is shown. | 🟧 **CONDITIONAL** — Mandatory when included in a household portfolio. |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | 🟧 **CONDITIONAL** — Sensitive. |
| `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | 🟧 **CONDITIONAL** — When collection depends on consent. |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | 🟧 **CONDITIONAL** — Required before the asset contributes to net worth. |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `cost_basis_lots.quantity` | Units acquired in the lot. | 🟧 **CONDITIONAL** — When the asset is quantity-based. |
| `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.acquired_on` | Acquisition date for the lot. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `holding_restrictions.restriction_type` | Approved restriction type. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.effective_from` | Date from which the restriction applies. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.status` | Restriction state: active, released or disputed. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `commitments.person_id` | Person responsible for funding the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.committed_minor_units` | Total committed amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.drawn_minor_units` | Amount already drawn. | 🟧 **CONDITIONAL** — Defaults to zero when a commitment exists. |
| `commitments.currency` | ISO 4217 currency of the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `transactions.person_id` | Person who owns the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.source_id` | Provenance source for the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.quantity` | Signed number of units affected. | 🟧 **CONDITIONAL** — When the transaction changes quantity. |
| `transactions.amount_minor_units` | Signed cash amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.currency` | ISO 4217 transaction currency. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `income_streams.person_id` | Person receiving the income. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.name` | Display name of the income stream. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.amount_minor_units` | Expected income amount in minor currency units. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.currency` | ISO 4217 income currency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.frequency` | Expected payment frequency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.starts_on` | Income start date. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.status` | Income-stream state: active, paused or ended. | 🟧 **CONDITIONAL** — Defaults to active when an income stream exists. |
| `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | 🟧 **CONDITIONAL** — Required when the asset is linked to a liability. |
| `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `liability_holding_links.effective_from` | Date from which the liability link applies. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `documents.owner_person_id` | Person who owns the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.document_type` | Approved document type. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.title` | Sanitized document title. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.retention_class` | Retention policy applied to the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `document_versions.original_filename` | Sanitized original filename. | 🟧 **CONDITIONAL** — Required when a document is uploaded. |
| `document_links.document_id` | Document linked to the asset. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `document_links.link_purpose` | Purpose such as evidence, contract or statement. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `verification_evidence.valuation_event_id` | Valuation supported by the evidence. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.document_id` | Supporting document. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.evidence_type` | Approved evidence type. | 🟧 **CONDITIONAL** — Required when verification evidence is recorded. |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.statement_as_of` | Statement as of. Expected value: `date`. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.acquired_on` | Known acquisition date. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.provider_code` | Provider or institution code when applicable. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.external_reference_hash` | Non-reversible hash of an external source reference. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.metadata` | Allow-listed, source-specific provenance metadata. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.confidence` | Optional confidence score from 0 to 1. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.metadata` | Bounded, method-specific valuation details. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `cost_basis_lots.source_id` | Source supporting the acquisition lot. | 🟦 **OPTIONAL** — May be supplied. |
| `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.liability_id` | Liability causing or associated with the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.effective_to` | Date on which the restriction stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.source_id` | Evidence source supporting the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.due_on` | Known commitment due date. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_start` | Start of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_end` | End of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.source_id` | Source supporting the commitment. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.trade_date` | Trade or business-effective date. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.settled_at` | Settlement timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.description` | Sanitized transaction description. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.ends_on` | Income end date. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.growth_rate_pct` | Optional expected annual growth rate. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.source_id` | Source supporting the income stream. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.effective_to` | Date on which the liability link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.document_date` | Business-effective date printed on the document. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.expires_on` | Document expiry date. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.source_id` | Source from which the document originated. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.supersedes_version_id` | Prior document version replaced by this version. | 🟦 **OPTIONAL** — May be supplied. |
| `document_links.effective_to` | Timestamp when the document link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.expires_at` | Evidence expiry timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.notes` | Bounded verification notes. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.employment_end_date` | Employment end date. Expected value: `date`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.covered_under_act` | Covered under act. Expected value: `bool`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.last_drawn_eligible_salary` | Last drawn eligible salary. Expected value: `money`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.employer_statement_amount` | Employer statement amount. Expected value: `money`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.holding_id` | Unique identifier for the holding. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_by_principal_id` | Application principal that created the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_at` | Creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.updated_at` | Most recent update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | 🟪 **SYSTEM** — System-generated. |
| `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. | 🟪 **SYSTEM** — System-generated. |
| `sources.captured_by_principal_id` | Application principal that captured the information. | 🟪 **SYSTEM** — System-generated when a person or operator captured it. |
| `sources.captured_at` | Timestamp when the information was captured. | 🟪 **SYSTEM** — System-generated. |
| `sources.created_at` | Creation timestamp for the provenance record. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.holding_id` | Holding valued by the observation. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.recorded_at` | Timestamp when the valuation was recorded. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.holding_id` | Holding acquired through the lot. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.holding_id` | Holding affected by the restriction. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `holding_restrictions.created_at` | Creation timestamp for the restriction record. | 🟪 **SYSTEM** — System-generated. |
| `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. | 🟪 **SYSTEM** — System-generated. |
| `commitments.holding_id` | Holding associated with the commitment. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `commitments.version` | Optimistic-lock version for the commitment. | 🟪 **SYSTEM** — System-generated. |
| `transactions.transaction_id` | Unique identifier for an immutable ledger event. | 🟪 **SYSTEM** — System-generated. |
| `transactions.holding_id` | Holding affected by the transaction. | 🟪 **SYSTEM** — System-generated when recorded from the holding. |
| `transactions.recorded_at` | Timestamp when the transaction was recorded. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.income_stream_id` | Unique identifier for recurring or expected income. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.holding_id` | Asset producing the income. | 🟪 **SYSTEM** — System-generated when created from the holding. |
| `income_streams.version` | Optimistic-lock version for the income stream. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.holding_id` | Asset participating in the liability relationship. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `liability_holding_links.created_at` | Creation timestamp for the liability link. | 🟪 **SYSTEM** — System-generated. |
| `documents.document_id` | Unique identifier for supporting document metadata. | 🟪 **SYSTEM** — System-generated. |
| `documents.lifecycle_state` | Document processing and availability state. | 🟪 **SYSTEM** — System-managed. |
| `documents.current_version_id` | Current clean document version. | 🟪 **SYSTEM** — System-managed. |
| `documents.created_by_principal_id` | Application principal that created the document. | 🟪 **SYSTEM** — System-generated. |
| `documents.created_at` | Document creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.updated_at` | Document update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.version` | Optimistic-lock version for document metadata. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_version_id` | Unique identifier for an immutable document version. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_id` | Parent document. | 🟪 **SYSTEM** — System-generated from the parent document. |
| `document_versions.version_number` | Monotonic version number within the document. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.storage_zone` | Quarantine or clean object-storage zone. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.storage_key` | Random non-personal object-storage key. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.checksum_sha256` | SHA-256 integrity digest. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.mime_type` | Server-detected MIME type. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.size_bytes` | Validated object size. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.scan_state` | Malware scanning state. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.scanner_policy_version` | Scanning-policy version used. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.uploaded_at` | Upload timestamp. | 🟪 **SYSTEM** — System-generated. |
| `document_links.document_link_id` | Unique identifier linking a document to the asset. | 🟪 **SYSTEM** — System-generated. |
| `document_links.domain_type` | Approved domain-object type. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.domain_id` | Application-validated target identifier. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.holding_id` | Holding to which the document is linked. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `document_links.effective_from` | Timestamp from which the document link applies. | 🟪 **SYSTEM** — System-generated unless explicitly effective later. |
| `document_links.created_by_principal_id` | Application principal that created the link. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_state` | Pending, verified, rejected or expired state. | 🟪 **SYSTEM** — System-managed. |
| `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.verified_at` | Verification timestamp. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.created_at` | Evidence creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_attributes.completed_service_years` | Completed service years. Expected value: `dec`. | 🟪 **SYSTEM** — System-calculated. |

</details>

<a id="asset-subtype-annuity"></a>

<details>
<summary><strong>Asset subtype: <code>ANNUITY</code></strong></summary>

| `table_name.column_name` | Description | Note |
|---|---|---|
| `holdings.owner_person_id` | Person primarily accountable for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_class_code` | Selected top-level asset class. | 🟥 **MANDATORY** — Required. |
| `holdings.asset_subtype_code` | Selected asset subtype. | 🟥 **MANDATORY** — Required. |
| `holdings.name` | User-facing name for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.currency` | Native ISO 4217 currency used for the holding. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes` | Validated object containing only the subtype fields listed below. | 🟥 **MANDATORY** — May be empty only when the subtype schema permits it. |
| `holdings.status` | Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED. | 🟥 **MANDATORY** — Defaults to ACTIVE. |
| `sources.source_type` | How the information was obtained: manual, import, connector, calculated or operator. | 🟥 **MANDATORY** — Required for each provenance record. |
| `sources.trust_tier` | Evidence tier: verified, declared, estimated or unknown. | 🟥 **MANDATORY** — Required for each provenance record. |
| `ownership_allocations.person_id` | Person receiving an ownership share. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.ownership_pct` | Effective ownership percentage for the person. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `ownership_allocations.effective_from` | Date from which the ownership share applies. | 🟥 **MANDATORY** — Required for each ownership allocation. |
| `holdings.subtype_attributes.insurer_name` | Insurer name. Expected value: `str`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.policy_ref` | Policy ref. Expected value: `ref`. | 🟥 **MANDATORY** — Sensitive. |
| `holdings.subtype_attributes.annuity_type` | Annuity type. Expected value: `enum('IMMEDIATE','DEFERRED')`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.life_basis` | Life basis. Expected value: `enum('SINGLE','JOINT','OTHER')`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.annuity_amount` | Annuity amount. Expected value: `money`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.payment_frequency` | Payment frequency. Expected value: `enum`. | 🟥 **MANDATORY** — Required. |
| `holdings.subtype_attributes.commencement_date` | Commencement date. Expected value: `date`. | 🟥 **MANDATORY** — Required. |
| `holdings.household_id` | Household in which the holding is shown. | 🟧 **CONDITIONAL** — Mandatory when included in a household portfolio. |
| `holdings.quantity` | Units, shares, weight or other quantity when the asset is quantity-based. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_type` | Kind of primary identifier, such as ISIN, folio or property reference. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.identifier_ciphertext` | Encrypted primary identifier value. | 🟧 **CONDITIONAL** — Sensitive. |
| `sources.data_consent_id` | Consent or lawful collection basis used by a connected source. | 🟧 **CONDITIONAL** — When collection depends on consent. |
| `valuation_events.value_minor_units` | Observed or appraised value in the valuation currency. | 🟧 **CONDITIONAL** — Required before the asset contributes to net worth. |
| `valuation_events.currency` | ISO 4217 currency of the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.as_of_at` | Date and time to which the valuation applies. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.source_id` | Source or manual-entry provenance for the valuation. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `valuation_events.valuation_method` | How the value was determined: market, appraisal, declared, modelled or cost. | 🟧 **CONDITIONAL** — Required with a valuation. |
| `cost_basis_lots.quantity` | Units acquired in the lot. | 🟧 **CONDITIONAL** — When the asset is quantity-based. |
| `cost_basis_lots.cost_amount_minor_units` | Acquisition cost in minor currency units. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.currency` | ISO 4217 currency of the acquisition cost. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `cost_basis_lots.acquired_on` | Acquisition date for the lot. | 🟧 **CONDITIONAL** — Required when recording a cost lot. |
| `holding_restrictions.restriction_type` | Approved restriction type. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.effective_from` | Date from which the restriction applies. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `holding_restrictions.status` | Restriction state: active, released or disputed. | 🟧 **CONDITIONAL** — Required when a restriction exists. |
| `commitments.person_id` | Person responsible for funding the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.committed_minor_units` | Total committed amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.drawn_minor_units` | Amount already drawn. | 🟧 **CONDITIONAL** — Defaults to zero when a commitment exists. |
| `commitments.currency` | ISO 4217 currency of the commitment. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `commitments.status` | Commitment state: open, partly drawn, fulfilled or cancelled. | 🟧 **CONDITIONAL** — Required when a commitment exists. |
| `transactions.person_id` | Person who owns the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.source_id` | Provenance source for the transaction. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.transaction_type` | Type such as buy, sell, income, fee, tax or transfer. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.quantity` | Signed number of units affected. | 🟧 **CONDITIONAL** — When the transaction changes quantity. |
| `transactions.amount_minor_units` | Signed cash amount in minor currency units. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `transactions.currency` | ISO 4217 transaction currency. | 🟧 **CONDITIONAL** — Required when a transaction is recorded. |
| `income_streams.person_id` | Person receiving the income. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.name` | Display name of the income stream. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.income_type` | Income type such as rent, dividend, interest or pension. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.amount_minor_units` | Expected income amount in minor currency units. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.currency` | ISO 4217 income currency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.frequency` | Expected payment frequency. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.starts_on` | Income start date. | 🟧 **CONDITIONAL** — Required when an income stream exists. |
| `income_streams.status` | Income-stream state: active, paused or ended. | 🟧 **CONDITIONAL** — Defaults to active when an income stream exists. |
| `liability_holding_links.liability_id` | Liability secured by, financing or associated with the asset. | 🟧 **CONDITIONAL** — Required when the asset is linked to a liability. |
| `liability_holding_links.link_type` | Relationship type: secured by, finances or associated with. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `liability_holding_links.effective_from` | Date from which the liability link applies. | 🟧 **CONDITIONAL** — Required when linked to a liability. |
| `documents.owner_person_id` | Person who owns the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.document_type` | Approved document type. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.title` | Sanitized document title. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `documents.retention_class` | Retention policy applied to the document. | 🟧 **CONDITIONAL** — Required when a document is attached. |
| `document_versions.original_filename` | Sanitized original filename. | 🟧 **CONDITIONAL** — Required when a document is uploaded. |
| `document_links.document_id` | Document linked to the asset. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `document_links.link_purpose` | Purpose such as evidence, contract or statement. | 🟧 **CONDITIONAL** — Required when creating a document link. |
| `verification_evidence.valuation_event_id` | Valuation supported by the evidence. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.document_id` | Supporting document. | 🟧 **CONDITIONAL** — Required when applicable. |
| `verification_evidence.evidence_type` | Approved evidence type. | 🟧 **CONDITIONAL** — Required when verification evidence is recorded. |
| `holdings.subtype_attributes.jurisdiction` | Country governing the offshore holding. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.tax_residency_relevance` | Whether the offshore holding is relevant to tax-residency reporting. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.reporting_status` | Current foreign-asset reporting state. | 🟧 **CONDITIONAL** — Mandatory when offshore is true. |
| `holdings.subtype_attributes.secondary_annuitant_person_id` | Secondary annuitant person ID. Expected value: `ref`. | 🟧 **CONDITIONAL** — Required when applicable. |
| `holdings.acquired_on` | Known acquisition date. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.provider_code` | Provider or institution code when applicable. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.external_reference_hash` | Non-reversible hash of an external source reference. | 🟦 **OPTIONAL** — May be supplied. |
| `sources.metadata` | Allow-listed, source-specific provenance metadata. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `ownership_allocations.effective_to` | Date on which the ownership share stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `ownership_allocations.source_id` | Evidence source supporting the ownership allocation. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.confidence` | Optional confidence score from 0 to 1. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.supersedes_event_id` | Prior valuation corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `valuation_events.metadata` | Bounded, method-specific valuation details. | 🟦 **OPTIONAL** — Defaults to an empty object. |
| `cost_basis_lots.source_id` | Source supporting the acquisition lot. | 🟦 **OPTIONAL** — May be supplied. |
| `cost_basis_lots.supersedes_lot_id` | Prior acquisition lot corrected by this lot. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.liability_id` | Liability causing or associated with the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.counterparty_reference` | Bounded reference to the restriction counterparty. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.effective_to` | Date on which the restriction stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `holding_restrictions.source_id` | Evidence source supporting the restriction. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.due_on` | Known commitment due date. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_start` | Start of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.window_end` | End of the permitted draw window. | 🟦 **OPTIONAL** — May be supplied. |
| `commitments.source_id` | Source supporting the commitment. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.external_transaction_hash` | Scoped deduplication hash for an imported transaction. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.trade_date` | Trade or business-effective date. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.settled_at` | Settlement timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.description` | Sanitized transaction description. | 🟦 **OPTIONAL** — May be supplied. |
| `transactions.supersedes_transaction_id` | Prior transaction corrected by this event. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.ends_on` | Income end date. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.growth_rate_pct` | Optional expected annual growth rate. | 🟦 **OPTIONAL** — May be supplied. |
| `income_streams.source_id` | Source supporting the income stream. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.allocation_pct` | Optional share of the liability attributed to this asset. | 🟦 **OPTIONAL** — May be supplied. |
| `liability_holding_links.effective_to` | Date on which the liability link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.document_date` | Business-effective date printed on the document. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.expires_on` | Document expiry date. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.source_id` | Source from which the document originated. | 🟦 **OPTIONAL** — May be supplied. |
| `document_versions.supersedes_version_id` | Prior document version replaced by this version. | 🟦 **OPTIONAL** — May be supplied. |
| `document_links.effective_to` | Timestamp when the document link stopped applying. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.expires_at` | Evidence expiry timestamp. | 🟦 **OPTIONAL** — May be supplied. |
| `verification_evidence.notes` | Bounded verification notes. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.offshore` | Whether the holding is outside India. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.foreign_account_ref` | Protected foreign account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.custodian_name` | Name of the custodian. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.custody_account_ref` | Protected custody-account reference. | 🟦 **OPTIONAL** — Sensitive. |
| `holdings.subtype_attributes.beneficial_owner_declaration` | Whether beneficial ownership has been declared. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.notes` | Bounded non-secret notes about the asset. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.purchase_price` | Purchase price. Expected value: `money`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.return_of_purchase_price` | Return of purchase price. Expected value: `bool`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.guarantee_period_end` | Guarantee period end. Expected value: `date`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.surrender_terms` | Surrender terms. Expected value: `object`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.subtype_attributes.nomination_status` | Nomination status. Expected value: `enum`. | 🟦 **OPTIONAL** — May be supplied. |
| `holdings.holding_id` | Unique identifier for the holding. | 🟪 **SYSTEM** — System-generated. |
| `holdings.subtype_schema_version` | Exact subtype field-schema version used to validate the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_by_principal_id` | Application principal that created the record. | 🟪 **SYSTEM** — System-generated. |
| `holdings.created_at` | Creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.updated_at` | Most recent update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `holdings.version` | Optimistic-lock version used to prevent conflicting updates. | 🟪 **SYSTEM** — System-generated. |
| `sources.source_id` | Unique identifier for the provenance record referenced by valuations, transactions and evidence. | 🟪 **SYSTEM** — System-generated. |
| `sources.captured_by_principal_id` | Application principal that captured the information. | 🟪 **SYSTEM** — System-generated when a person or operator captured it. |
| `sources.captured_at` | Timestamp when the information was captured. | 🟪 **SYSTEM** — System-generated. |
| `sources.created_at` | Creation timestamp for the provenance record. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.ownership_allocation_id` | Unique identifier for an ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `ownership_allocations.holding_id` | Holding to which the ownership allocation belongs. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `ownership_allocations.created_at` | Creation timestamp for the ownership allocation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.valuation_event_id` | Unique identifier for an immutable valuation observation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.holding_id` | Holding valued by the observation. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `valuation_events.recorded_by_principal_id` | Application principal that recorded the valuation. | 🟪 **SYSTEM** — System-generated. |
| `valuation_events.recorded_at` | Timestamp when the valuation was recorded. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.cost_basis_lot_id` | Unique identifier for an acquisition-cost lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.holding_id` | Holding acquired through the lot. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `cost_basis_lots.recorded_by_principal_id` | Application principal that recorded the lot. | 🟪 **SYSTEM** — System-generated. |
| `cost_basis_lots.recorded_at` | Timestamp when the lot was recorded. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.restriction_id` | Unique identifier for a lien, pledge, lock-in, freeze or legal restriction. | 🟪 **SYSTEM** — System-generated. |
| `holding_restrictions.holding_id` | Holding affected by the restriction. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `holding_restrictions.created_at` | Creation timestamp for the restriction record. | 🟪 **SYSTEM** — System-generated. |
| `commitments.commitment_id` | Unique identifier for an undrawn or contingent commitment. | 🟪 **SYSTEM** — System-generated. |
| `commitments.holding_id` | Holding associated with the commitment. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `commitments.version` | Optimistic-lock version for the commitment. | 🟪 **SYSTEM** — System-generated. |
| `transactions.transaction_id` | Unique identifier for an immutable ledger event. | 🟪 **SYSTEM** — System-generated. |
| `transactions.holding_id` | Holding affected by the transaction. | 🟪 **SYSTEM** — System-generated when recorded from the holding. |
| `transactions.recorded_at` | Timestamp when the transaction was recorded. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.income_stream_id` | Unique identifier for recurring or expected income. | 🟪 **SYSTEM** — System-generated. |
| `income_streams.holding_id` | Asset producing the income. | 🟪 **SYSTEM** — System-generated when created from the holding. |
| `income_streams.version` | Optimistic-lock version for the income stream. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.liability_holding_link_id` | Unique identifier linking the asset to a liability. | 🟪 **SYSTEM** — System-generated. |
| `liability_holding_links.holding_id` | Asset participating in the liability relationship. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `liability_holding_links.created_at` | Creation timestamp for the liability link. | 🟪 **SYSTEM** — System-generated. |
| `documents.document_id` | Unique identifier for supporting document metadata. | 🟪 **SYSTEM** — System-generated. |
| `documents.lifecycle_state` | Document processing and availability state. | 🟪 **SYSTEM** — System-managed. |
| `documents.current_version_id` | Current clean document version. | 🟪 **SYSTEM** — System-managed. |
| `documents.created_by_principal_id` | Application principal that created the document. | 🟪 **SYSTEM** — System-generated. |
| `documents.created_at` | Document creation timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.updated_at` | Document update timestamp. | 🟪 **SYSTEM** — System-generated. |
| `documents.version` | Optimistic-lock version for document metadata. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_version_id` | Unique identifier for an immutable document version. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.document_id` | Parent document. | 🟪 **SYSTEM** — System-generated from the parent document. |
| `document_versions.version_number` | Monotonic version number within the document. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.storage_zone` | Quarantine or clean object-storage zone. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.storage_key` | Random non-personal object-storage key. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.checksum_sha256` | SHA-256 integrity digest. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.mime_type` | Server-detected MIME type. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.size_bytes` | Validated object size. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.scan_state` | Malware scanning state. | 🟪 **SYSTEM** — System-managed. |
| `document_versions.scanner_policy_version` | Scanning-policy version used. | 🟪 **SYSTEM** — System-generated. |
| `document_versions.uploaded_at` | Upload timestamp. | 🟪 **SYSTEM** — System-generated. |
| `document_links.document_link_id` | Unique identifier linking a document to the asset. | 🟪 **SYSTEM** — System-generated. |
| `document_links.domain_type` | Approved domain-object type. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.domain_id` | Application-validated target identifier. | 🟪 **SYSTEM** — System-generated for an asset link. |
| `document_links.holding_id` | Holding to which the document is linked. | 🟪 **SYSTEM** — System-generated from the parent holding. |
| `document_links.effective_from` | Timestamp from which the document link applies. | 🟪 **SYSTEM** — System-generated unless explicitly effective later. |
| `document_links.created_by_principal_id` | Application principal that created the link. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_evidence_id` | Unique identifier for evidence supporting a valuation or fact. | 🟪 **SYSTEM** — System-generated. |
| `verification_evidence.verification_state` | Pending, verified, rejected or expired state. | 🟪 **SYSTEM** — System-managed. |
| `verification_evidence.verified_by_principal_id` | Application principal that performed verification. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.verified_at` | Verification timestamp. | 🟪 **SYSTEM** — System-generated when verified or rejected. |
| `verification_evidence.created_at` | Evidence creation timestamp. | 🟪 **SYSTEM** — System-generated. |

</details>

