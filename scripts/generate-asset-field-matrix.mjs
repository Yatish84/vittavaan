import { readFile, writeFile } from "node:fs/promises";

const sourcePath = "docs/v3/02_Analysis/07_India_Subtype_Attribute_Schemas.md";
const outputPath = "docs/v3/02_Analysis/08_Asset_Field_Requirement_Matrix.md";
const source = await readFile(sourcePath, "utf8");
const assetSection = source
  .split("## Asset schemas")[1]
  .split("## Liability schemas")[0];

const rows = [...assetSection.matchAll(/^\| `([^`]+) \/ ([^`]+)` \| (.+) \|$/gm)].map(
  ([, assetClass, assetSubtype, declaration]) => ({ assetClass, assetSubtype, declaration }),
);

const inheritance = new Map([
  ["TRAD_SECURITY/DEBENTURE", "TRAD_SECURITY/CORPORATE_BOND"],
  ["FUND/MONEY_MARKET_FUND", "FUND/MUTUAL_FUND"],
  ["CREDIT_ASSET/MEZZANINE_DEBT", "CREDIT_ASSET/DIRECT_LENDING"],
  ["HEDGE_STRATEGY/LONG_SHORT", "HEDGE_STRATEGY/HEDGE_FUND"],
  ["HEDGE_STRATEGY/GLOBAL_MACRO", "HEDGE_STRATEGY/HEDGE_FUND"],
  ["HEDGE_STRATEGY/ARBITRAGE_STRATEGY", "HEDGE_STRATEGY/HEDGE_FUND"],
  ["REAL_ASSET/COMMERCIAL_PROPERTY", "REAL_ASSET/RESIDENTIAL_PROPERTY"],
  ["REAL_ASSET/AGRICULTURAL_LAND", "REAL_ASSET/LAND"],
]);

const rowByKey = new Map(rows.map((row) => [`${row.assetClass}/${row.assetSubtype}`, row]));
const markerMeaning = {
  R: "Mandatory",
  C: "Conditional",
  O: "Optional",
  D: "System-calculated",
  "R/S": "Mandatory — sensitive",
  "C/S": "Conditional — sensitive",
  "O/S": "Optional — sensitive",
  "D/S": "System-calculated — sensitive",
};

function extractFields(declaration) {
  const matches = [
    ...declaration.matchAll(
      /`([a-z][a-z0-9_]*)`\s+(R\/S|C\/S|O\/S|D\/S|R|C|O|D)\s+(.+?)(?=;\s+`[a-z][a-z0-9_]*`\s+(?:R\/S|C\/S|O\/S|D\/S|R|C|O|D)\s+|\.\s|$)/g,
    ),
  ];
  return matches.map(([, name, marker, type]) => ({
    name,
    marker,
    type: type
      .trim()
      .replace(/\.$/, "")
      .replaceAll("`", "'")
      .replace(/\|/g, "\\|"),
  }));
}

function expandedFields(row, seen = new Set()) {
  const key = `${row.assetClass}/${row.assetSubtype}`;
  if (seen.has(key)) throw new Error(`Circular inheritance at ${key}`);
  const nextSeen = new Set(seen).add(key);
  const baseKey = inheritance.get(key);
  const baseFields = baseKey ? expandedFields(rowByKey.get(baseKey), nextSeen) : [];
  const ownFields = extractFields(row.declaration);
  const merged = new Map(baseFields.map((field) => [field.name, field]));
  for (const field of ownFields) merged.set(field.name, field);
  return [...merged.values()];
}

function title(name) {
  return name
    .split("_")
    .map((word) => word === "id" ? "ID" : word.toUpperCase() === word ? word : word)
    .join(" ")
    .replace(/^./, (character) => character.toUpperCase());
}

const commonRows = [
  ["holdings.holding_id", "Unique identifier for the holding.", "System-generated"],
  ["holdings.owner_person_id", "Person primarily accountable for the holding.", "Mandatory"],
  ["holdings.household_id", "Household in which the holding is shown.", "Conditional — mandatory when included in a household portfolio"],
  ["holdings.asset_class_code", "Selected top-level asset class.", "Mandatory"],
  ["holdings.asset_subtype_code", "Selected asset subtype.", "Mandatory"],
  ["holdings.name", "User-facing name for the holding.", "Mandatory"],
  ["holdings.currency", "Native ISO 4217 currency used for the holding.", "Mandatory"],
  ["holdings.quantity", "Units, shares, weight or other quantity when the asset is quantity-based.", "Conditional"],
  ["holdings.identifier_type", "Kind of primary identifier, such as ISIN, folio or property reference.", "Conditional"],
  ["holdings.identifier_ciphertext", "Encrypted primary identifier value.", "Conditional — sensitive"],
  ["holdings.subtype_schema_version", "Exact subtype field-schema version used to validate the record.", "System-generated"],
  ["holdings.subtype_attributes", "Validated object containing only the subtype fields listed below.", "Mandatory — may be empty only when the subtype schema permits it"],
  ["holdings.status", "Lifecycle state: ACTIVE, CLOSED, DISPOSED or ARCHIVED.", "Mandatory — defaults to ACTIVE"],
  ["holdings.acquired_on", "Known acquisition date.", "Optional"],
  ["holdings.created_by_principal_id", "Application principal that created the record.", "System-generated"],
  ["holdings.created_at", "Creation timestamp.", "System-generated"],
  ["holdings.updated_at", "Most recent update timestamp.", "System-generated"],
  ["holdings.version", "Optimistic-lock version used to prevent conflicting updates.", "System-generated"],
  ["sources.source_id", "Unique identifier for the provenance record referenced by valuations, transactions and evidence.", "System-generated"],
  ["sources.source_type", "How the information was obtained: manual, import, connector, calculated or operator.", "Mandatory for each provenance record"],
  ["sources.provider_code", "Provider or institution code when applicable.", "Optional"],
  ["sources.data_consent_id", "Consent or lawful collection basis used by a connected source.", "Conditional — when collection depends on consent"],
  ["sources.external_reference_hash", "Non-reversible hash of an external source reference.", "Optional"],
  ["sources.trust_tier", "Evidence tier: verified, declared, estimated or unknown.", "Mandatory for each provenance record"],
  ["sources.captured_by_principal_id", "Application principal that captured the information.", "System-generated when a person or operator captured it"],
  ["sources.captured_at", "Timestamp when the information was captured.", "System-generated"],
  ["sources.metadata", "Allow-listed, source-specific provenance metadata.", "Optional — defaults to an empty object"],
  ["sources.created_at", "Creation timestamp for the provenance record.", "System-generated"],
  ["ownership_allocations.ownership_allocation_id", "Unique identifier for an ownership allocation.", "System-generated"],
  ["ownership_allocations.holding_id", "Holding to which the ownership allocation belongs.", "System-generated from the parent holding"],
  ["ownership_allocations.person_id", "Person receiving an ownership share.", "Mandatory for each ownership allocation"],
  ["ownership_allocations.ownership_pct", "Effective ownership percentage for the person.", "Mandatory for each ownership allocation"],
  ["ownership_allocations.effective_from", "Date from which the ownership share applies.", "Mandatory for each ownership allocation"],
  ["ownership_allocations.effective_to", "Date on which the ownership share stopped applying.", "Optional"],
  ["ownership_allocations.source_id", "Evidence source supporting the ownership allocation.", "Optional"],
  ["ownership_allocations.created_at", "Creation timestamp for the ownership allocation.", "System-generated"],
  ["valuation_events.valuation_event_id", "Unique identifier for an immutable valuation observation.", "System-generated"],
  ["valuation_events.holding_id", "Holding valued by the observation.", "System-generated from the parent holding"],
  ["valuation_events.value_minor_units", "Observed or appraised value in the valuation currency.", "Conditional — required before the asset contributes to net worth"],
  ["valuation_events.currency", "ISO 4217 currency of the valuation.", "Conditional — required with a valuation"],
  ["valuation_events.as_of_at", "Date and time to which the valuation applies.", "Conditional — required with a valuation"],
  ["valuation_events.source_id", "Source or manual-entry provenance for the valuation.", "Conditional — required with a valuation"],
  ["valuation_events.valuation_method", "How the value was determined: market, appraisal, declared, modelled or cost.", "Conditional — required with a valuation"],
  ["valuation_events.confidence", "Optional confidence score from 0 to 1.", "Optional"],
  ["valuation_events.supersedes_event_id", "Prior valuation corrected by this event.", "Optional"],
  ["valuation_events.recorded_by_principal_id", "Application principal that recorded the valuation.", "System-generated"],
  ["valuation_events.recorded_at", "Timestamp when the valuation was recorded.", "System-generated"],
  ["valuation_events.metadata", "Bounded, method-specific valuation details.", "Optional — defaults to an empty object"],
  ["cost_basis_lots.cost_basis_lot_id", "Unique identifier for an acquisition-cost lot.", "System-generated"],
  ["cost_basis_lots.holding_id", "Holding acquired through the lot.", "System-generated from the parent holding"],
  ["cost_basis_lots.quantity", "Units acquired in the lot.", "Conditional — when the asset is quantity-based"],
  ["cost_basis_lots.cost_amount_minor_units", "Acquisition cost in minor currency units.", "Conditional — required when recording a cost lot"],
  ["cost_basis_lots.currency", "ISO 4217 currency of the acquisition cost.", "Conditional — required when recording a cost lot"],
  ["cost_basis_lots.acquired_on", "Acquisition date for the lot.", "Conditional — required when recording a cost lot"],
  ["cost_basis_lots.source_id", "Source supporting the acquisition lot.", "Optional"],
  ["cost_basis_lots.supersedes_lot_id", "Prior acquisition lot corrected by this lot.", "Optional"],
  ["cost_basis_lots.recorded_by_principal_id", "Application principal that recorded the lot.", "System-generated"],
  ["cost_basis_lots.recorded_at", "Timestamp when the lot was recorded.", "System-generated"],
  ["holding_restrictions.restriction_id", "Unique identifier for a lien, pledge, lock-in, freeze or legal restriction.", "System-generated"],
  ["holding_restrictions.holding_id", "Holding affected by the restriction.", "System-generated from the parent holding"],
  ["holding_restrictions.liability_id", "Liability causing or associated with the restriction.", "Optional"],
  ["holding_restrictions.restriction_type", "Approved restriction type.", "Conditional — required when a restriction exists"],
  ["holding_restrictions.counterparty_reference", "Bounded reference to the restriction counterparty.", "Optional"],
  ["holding_restrictions.effective_from", "Date from which the restriction applies.", "Conditional — required when a restriction exists"],
  ["holding_restrictions.effective_to", "Date on which the restriction stopped applying.", "Optional"],
  ["holding_restrictions.status", "Restriction state: active, released or disputed.", "Conditional — required when a restriction exists"],
  ["holding_restrictions.source_id", "Evidence source supporting the restriction.", "Optional"],
  ["holding_restrictions.created_at", "Creation timestamp for the restriction record.", "System-generated"],
  ["commitments.commitment_id", "Unique identifier for an undrawn or contingent commitment.", "System-generated"],
  ["commitments.holding_id", "Holding associated with the commitment.", "System-generated from the parent holding"],
  ["commitments.person_id", "Person responsible for funding the commitment.", "Conditional — required when a commitment exists"],
  ["commitments.committed_minor_units", "Total committed amount in minor currency units.", "Conditional — required when a commitment exists"],
  ["commitments.drawn_minor_units", "Amount already drawn.", "Conditional — defaults to zero when a commitment exists"],
  ["commitments.currency", "ISO 4217 currency of the commitment.", "Conditional — required when a commitment exists"],
  ["commitments.due_on", "Known commitment due date.", "Optional"],
  ["commitments.window_start", "Start of the permitted draw window.", "Optional"],
  ["commitments.window_end", "End of the permitted draw window.", "Optional"],
  ["commitments.status", "Commitment state: open, partly drawn, fulfilled or cancelled.", "Conditional — required when a commitment exists"],
  ["commitments.source_id", "Source supporting the commitment.", "Optional"],
  ["commitments.version", "Optimistic-lock version for the commitment.", "System-generated"],
  ["transactions.transaction_id", "Unique identifier for an immutable ledger event.", "System-generated"],
  ["transactions.holding_id", "Holding affected by the transaction.", "System-generated when recorded from the holding"],
  ["transactions.person_id", "Person who owns the transaction.", "Conditional — required when a transaction is recorded"],
  ["transactions.source_id", "Provenance source for the transaction.", "Conditional — required when a transaction is recorded"],
  ["transactions.external_transaction_hash", "Scoped deduplication hash for an imported transaction.", "Optional"],
  ["transactions.transaction_type", "Type such as buy, sell, income, fee, tax or transfer.", "Conditional — required when a transaction is recorded"],
  ["transactions.trade_date", "Trade or business-effective date.", "Optional"],
  ["transactions.settled_at", "Settlement timestamp.", "Optional"],
  ["transactions.quantity", "Signed number of units affected.", "Conditional — when the transaction changes quantity"],
  ["transactions.amount_minor_units", "Signed cash amount in minor currency units.", "Conditional — required when a transaction is recorded"],
  ["transactions.currency", "ISO 4217 transaction currency.", "Conditional — required when a transaction is recorded"],
  ["transactions.description", "Sanitized transaction description.", "Optional"],
  ["transactions.supersedes_transaction_id", "Prior transaction corrected by this event.", "Optional"],
  ["transactions.recorded_at", "Timestamp when the transaction was recorded.", "System-generated"],
  ["income_streams.income_stream_id", "Unique identifier for recurring or expected income.", "System-generated"],
  ["income_streams.person_id", "Person receiving the income.", "Conditional — required when an income stream exists"],
  ["income_streams.holding_id", "Asset producing the income.", "System-generated when created from the holding"],
  ["income_streams.name", "Display name of the income stream.", "Conditional — required when an income stream exists"],
  ["income_streams.income_type", "Income type such as rent, dividend, interest or pension.", "Conditional — required when an income stream exists"],
  ["income_streams.amount_minor_units", "Expected income amount in minor currency units.", "Conditional — required when an income stream exists"],
  ["income_streams.currency", "ISO 4217 income currency.", "Conditional — required when an income stream exists"],
  ["income_streams.frequency", "Expected payment frequency.", "Conditional — required when an income stream exists"],
  ["income_streams.starts_on", "Income start date.", "Conditional — required when an income stream exists"],
  ["income_streams.ends_on", "Income end date.", "Optional"],
  ["income_streams.growth_rate_pct", "Optional expected annual growth rate.", "Optional"],
  ["income_streams.source_id", "Source supporting the income stream.", "Optional"],
  ["income_streams.status", "Income-stream state: active, paused or ended.", "Conditional — defaults to active when an income stream exists"],
  ["income_streams.version", "Optimistic-lock version for the income stream.", "System-generated"],
  ["liability_holding_links.liability_holding_link_id", "Unique identifier linking the asset to a liability.", "System-generated"],
  ["liability_holding_links.liability_id", "Liability secured by, financing or associated with the asset.", "Conditional — required when the asset is linked to a liability"],
  ["liability_holding_links.holding_id", "Asset participating in the liability relationship.", "System-generated from the parent holding"],
  ["liability_holding_links.link_type", "Relationship type: secured by, finances or associated with.", "Conditional — required when linked to a liability"],
  ["liability_holding_links.allocation_pct", "Optional share of the liability attributed to this asset.", "Optional"],
  ["liability_holding_links.effective_from", "Date from which the liability link applies.", "Conditional — required when linked to a liability"],
  ["liability_holding_links.effective_to", "Date on which the liability link stopped applying.", "Optional"],
  ["liability_holding_links.created_at", "Creation timestamp for the liability link.", "System-generated"],
  ["documents.document_id", "Unique identifier for supporting document metadata.", "System-generated"],
  ["documents.owner_person_id", "Person who owns the document.", "Conditional — required when a document is attached"],
  ["documents.document_type", "Approved document type.", "Conditional — required when a document is attached"],
  ["documents.title", "Sanitized document title.", "Conditional — required when a document is attached"],
  ["documents.retention_class", "Retention policy applied to the document.", "Conditional — required when a document is attached"],
  ["documents.lifecycle_state", "Document processing and availability state.", "System-managed"],
  ["documents.current_version_id", "Current clean document version.", "System-managed"],
  ["documents.created_by_principal_id", "Application principal that created the document.", "System-generated"],
  ["documents.created_at", "Document creation timestamp.", "System-generated"],
  ["documents.updated_at", "Document update timestamp.", "System-generated"],
  ["documents.version", "Optimistic-lock version for document metadata.", "System-generated"],
  ["document_versions.document_version_id", "Unique identifier for an immutable document version.", "System-generated"],
  ["document_versions.document_id", "Parent document.", "System-generated from the parent document"],
  ["document_versions.version_number", "Monotonic version number within the document.", "System-generated"],
  ["document_versions.storage_zone", "Quarantine or clean object-storage zone.", "System-managed"],
  ["document_versions.storage_key", "Random non-personal object-storage key.", "System-generated"],
  ["document_versions.checksum_sha256", "SHA-256 integrity digest.", "System-generated"],
  ["document_versions.mime_type", "Server-detected MIME type.", "System-generated"],
  ["document_versions.size_bytes", "Validated object size.", "System-generated"],
  ["document_versions.original_filename", "Sanitized original filename.", "Conditional — required when a document is uploaded"],
  ["document_versions.document_date", "Business-effective date printed on the document.", "Optional"],
  ["document_versions.expires_on", "Document expiry date.", "Optional"],
  ["document_versions.source_id", "Source from which the document originated.", "Optional"],
  ["document_versions.supersedes_version_id", "Prior document version replaced by this version.", "Optional"],
  ["document_versions.scan_state", "Malware scanning state.", "System-managed"],
  ["document_versions.scanner_policy_version", "Scanning-policy version used.", "System-generated"],
  ["document_versions.uploaded_at", "Upload timestamp.", "System-generated"],
  ["document_links.document_link_id", "Unique identifier linking a document to the asset.", "System-generated"],
  ["document_links.document_id", "Document linked to the asset.", "Conditional — required when creating a document link"],
  ["document_links.domain_type", "Approved domain-object type.", "System-generated for an asset link"],
  ["document_links.domain_id", "Application-validated target identifier.", "System-generated for an asset link"],
  ["document_links.holding_id", "Holding to which the document is linked.", "System-generated from the parent holding"],
  ["document_links.link_purpose", "Purpose such as evidence, contract or statement.", "Conditional — required when creating a document link"],
  ["document_links.effective_from", "Timestamp from which the document link applies.", "System-generated unless explicitly effective later"],
  ["document_links.effective_to", "Timestamp when the document link stopped applying.", "Optional"],
  ["document_links.created_by_principal_id", "Application principal that created the link.", "System-generated"],
  ["verification_evidence.verification_evidence_id", "Unique identifier for evidence supporting a valuation or fact.", "System-generated"],
  ["verification_evidence.valuation_event_id", "Valuation supported by the evidence.", "Conditional"],
  ["verification_evidence.document_id", "Supporting document.", "Conditional"],
  ["verification_evidence.evidence_type", "Approved evidence type.", "Conditional — required when verification evidence is recorded"],
  ["verification_evidence.verification_state", "Pending, verified, rejected or expired state.", "System-managed"],
  ["verification_evidence.verified_by_principal_id", "Application principal that performed verification.", "System-generated when verified or rejected"],
  ["verification_evidence.verified_at", "Verification timestamp.", "System-generated when verified or rejected"],
  ["verification_evidence.expires_at", "Evidence expiry timestamp.", "Optional"],
  ["verification_evidence.notes", "Bounded verification notes.", "Optional"],
  ["verification_evidence.created_at", "Evidence creation timestamp.", "System-generated"],
];

const crossCuttingRows = [
  ["offshore", "Whether the holding is outside India.", "Optional"],
  ["jurisdiction", "Country governing the offshore holding.", "Conditional — mandatory when offshore is true"],
  ["tax_residency_relevance", "Whether the offshore holding is relevant to tax-residency reporting.", "Conditional — mandatory when offshore is true"],
  ["reporting_status", "Current foreign-asset reporting state.", "Conditional — mandatory when offshore is true"],
  ["foreign_account_ref", "Protected foreign account reference.", "Optional — sensitive"],
  ["custodian_name", "Name of the custodian.", "Optional"],
  ["custody_account_ref", "Protected custody-account reference.", "Optional — sensitive"],
  ["beneficial_owner_declaration", "Whether beneficial ownership has been declared.", "Optional"],
  ["notes", "Bounded non-secret notes about the asset.", "Optional"],
];

const output = [];
output.push("# Asset Field Requirement Matrix");
output.push("");
output.push("> **Status:** Draft implementation field checklist derived from `07_India_Subtype_Attribute_Schemas.md`.");
output.push(">");
output.push("> **Scope:** Assets only: all 93 planned asset class/subtype combinations. Liabilities remain in the source schema document and should receive a separate matrix.");
output.push("");
output.push("## Purpose");
output.push("");
output.push("This document gives product, design, engineering and testing teams a row-by-row checklist of the information captured for each asset type. It complements the database design; it does not create one physical table per subtype.");
output.push("");
output.push("A path such as `holdings.subtype_attributes.interest_rate_pct` means the `interest_rate_pct` key inside the schema-validated `holdings.subtype_attributes` JSONB column. It is written in dotted form so its exact logical storage location is unambiguous. Normalized facts—ownership, valuation, transactions, income, restrictions and documents—remain in their dedicated tables.");
output.push("");
output.push("## Requirement meanings");
output.push("");
output.push("| Requirement | Plain-English meaning |");
output.push("|---|---|");
output.push("| Mandatory | Must be present before the holding can become active. |");
output.push("| Conditional | Must be present only when the stated feature or circumstance applies. |");
output.push("| Optional | May be supplied; absence means unknown or not applicable. |");
output.push("| System-generated / System-calculated | Produced by Vittavaan and not accepted as an authoritative manual value. |");
output.push("| System-managed | Maintained by Vittavaan as a workflow or lifecycle state rather than entered freely by a user. |");
output.push("| Sensitive | Must be encrypted or represented by a protected reference and masked in normal responses. |");
output.push("");
output.push("## Fields common to every asset");
output.push("");
output.push("These normalized fields apply to every asset. They are also repeated inside every subtype table below so each subtype is a complete, standalone checklist.");
output.push("");
output.push("| `table_name.column_name` | Description | Requirement |");
output.push("|---|---|---|");
for (const [path, description, requirement] of commonRows) {
  output.push(`| \`${path}\` | ${description} | ${requirement} |`);
}
output.push("");
output.push("## Fields available to any asset when applicable");
output.push("");
output.push("| `table_name.column_name` | Description | Requirement |");
output.push("|---|---|---|");
for (const field of crossCuttingRows) {
  output.push(`| \`holdings.subtype_attributes.${field[0]}\` | ${field[1]} | ${field[2]} |`);
}
output.push("");
output.push("## Subtype-by-subtype fields");
output.push("");

let currentClass = "";
let totalFields = 0;
let totalMatrixRows = 0;
for (const row of rows.slice(0, 93)) {
  if (row.assetClass !== currentClass) {
    currentClass = row.assetClass;
    output.push(`## Asset class: \`${currentClass}\``);
    output.push("");
  }
  const fields = expandedFields(row);
  totalFields += fields.length;
  const subtypeRows = fields.map((field) => [
    `holdings.subtype_attributes.${field.name}`,
    `${title(field.name)}. Expected value: \`${field.type}\`.`,
    markerMeaning[field.marker],
  ]);
  const completeRows = new Map();
  for (const field of commonRows) completeRows.set(field[0], field);
  for (const field of crossCuttingRows) {
    const expanded = [`holdings.subtype_attributes.${field[0]}`, field[1], field[2]];
    completeRows.set(expanded[0], expanded);
  }
  for (const field of subtypeRows) completeRows.set(field[0], field);
  totalMatrixRows += completeRows.size;
  output.push(`### Asset subtype: \`${row.assetSubtype}\``);
  output.push("");
  output.push("| `table_name.column_name` | Description | Requirement |");
  output.push("|---|---|---|");
  for (const [path, description, requirement] of completeRows.values()) {
    output.push(`| \`${path}\` | ${description} | ${requirement} |`);
  }
  output.push("");
}

output.push("## Completeness and maintenance rules");
output.push("");
output.push(`- This version contains **${rows.slice(0, 93).length} asset subtypes** and **${totalFields} expanded subtype-field rows**.`);
output.push(`- The 93 self-contained subtype tables contain **${totalMatrixRows} total field rows**, including repeated normalized and cross-cutting fields.`);
output.push("- Inherited profiles—such as debentures inheriting corporate-bond fields—are expanded here so readers do not have to jump between sections.");
output.push("- The source of truth for validation details remains `07_India_Subtype_Attribute_Schemas.md`; this matrix must be regenerated whenever that source changes.");
output.push("- A subtype field cannot be moved into or out of normalized storage without updating the database design, API contract, migration plan and tests.");
output.push("- Mandatory is a business activation rule. Database `NOT NULL` constraints are documented separately in `03_Database_Design.md`.");
output.push("");

await writeFile(outputPath, `${output.join("\n")}\n`, "utf8");
console.log(`Generated ${outputPath}: 93 subtypes, ${totalFields} subtype fields, ${totalMatrixRows} complete matrix rows.`);
