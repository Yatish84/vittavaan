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
  ["ownership_allocations.person_id", "Person receiving an ownership share.", "Mandatory for each ownership allocation"],
  ["ownership_allocations.ownership_pct", "Effective ownership percentage for the person.", "Mandatory for each ownership allocation"],
  ["ownership_allocations.effective_from", "Date from which the ownership share applies.", "Mandatory for each ownership allocation"],
  ["ownership_allocations.effective_to", "Date on which the ownership share stopped applying.", "Optional"],
  ["valuation_events.value_minor_units", "Observed or appraised value in the valuation currency.", "Conditional — required before the asset contributes to net worth"],
  ["valuation_events.currency", "ISO 4217 currency of the valuation.", "Conditional — required with a valuation"],
  ["valuation_events.as_of_at", "Date and time to which the valuation applies.", "Conditional — required with a valuation"],
  ["valuation_events.source_id", "Source or manual-entry provenance for the valuation.", "Conditional — required with a valuation"],
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
output.push("| Sensitive | Must be encrypted or represented by a protected reference and masked in normal responses. |");
output.push("");
output.push("## Fields common to every asset");
output.push("");
output.push("These fields are not repeated under every subtype. They apply to every asset in addition to that subtype's matrix.");
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
for (const field of [
  ["offshore", "Whether the holding is outside India.", "Optional"],
  ["jurisdiction", "Country governing the offshore holding.", "Conditional — mandatory when offshore is true"],
  ["tax_residency_relevance", "Whether the offshore holding is relevant to tax-residency reporting.", "Conditional — mandatory when offshore is true"],
  ["reporting_status", "Current foreign-asset reporting state.", "Conditional — mandatory when offshore is true"],
  ["foreign_account_ref", "Protected foreign account reference.", "Optional — sensitive"],
  ["custodian_name", "Name of the custodian.", "Optional"],
  ["custody_account_ref", "Protected custody-account reference.", "Optional — sensitive"],
  ["beneficial_owner_declaration", "Whether beneficial ownership has been declared.", "Optional"],
  ["notes", "Bounded non-secret notes about the asset.", "Optional"],
]) {
  output.push(`| \`holdings.subtype_attributes.${field[0]}\` | ${field[1]} | ${field[2]} |`);
}
output.push("");
output.push("## Subtype-by-subtype fields");
output.push("");

let currentClass = "";
let totalFields = 0;
for (const row of rows.slice(0, 93)) {
  if (row.assetClass !== currentClass) {
    currentClass = row.assetClass;
    output.push(`## Asset class: \`${currentClass}\``);
    output.push("");
  }
  const fields = expandedFields(row);
  totalFields += fields.length;
  output.push(`### Asset subtype: \`${row.assetSubtype}\``);
  output.push("");
  output.push("| `table_name.column_name` | Description | Requirement |");
  output.push("|---|---|---|");
  for (const field of fields) {
    const requirement = markerMeaning[field.marker];
    output.push(
      `| \`holdings.subtype_attributes.${field.name}\` | ${title(field.name)}. Expected value: \`${field.type}\`. | ${requirement} |`,
    );
  }
  output.push("");
}

output.push("## Completeness and maintenance rules");
output.push("");
output.push(`- This version contains **${rows.slice(0, 93).length} asset subtypes** and **${totalFields} expanded subtype-field rows**.`);
output.push("- Inherited profiles—such as debentures inheriting corporate-bond fields—are expanded here so readers do not have to jump between sections.");
output.push("- The source of truth for validation details remains `07_India_Subtype_Attribute_Schemas.md`; this matrix must be regenerated whenever that source changes.");
output.push("- A subtype field cannot be moved into or out of normalized storage without updating the database design, API contract, migration plan and tests.");
output.push("- Mandatory is a business activation rule. Database `NOT NULL` constraints are documented separately in `03_Database_Design.md`.");
output.push("");

await writeFile(outputPath, `${output.join("\n")}\n`, "utf8");
console.log(`Generated ${outputPath}: 93 subtypes, ${totalFields} expanded subtype fields.`);
