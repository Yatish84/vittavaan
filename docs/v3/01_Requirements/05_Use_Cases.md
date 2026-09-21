# Detailed Beta Use Cases

## UC3-IAM-001 — Enter Vittavaan through Auth-Core

**Primary actor:** Authenticated principal  
**Scope:** Vittavaan and auth-core  
**Level:** User goal  
**Requirements:** FR3-IAM-001–007  
**Wireframes:** All protected pages; First run

**Preconditions:** Vittavaan and auth-core origins are approved; the requested return target is allow-listed.

**Trigger:** A person opens a protected Vittavaan route.

**Main success flow:**

1. Vittavaan detects no usable access context and redirects to auth-core with integrity-bound state and return target.
2. Auth-core completes its applicable login, risk and MFA workflow.
3. Auth-core establishes its secure web session and completes the reviewed handoff without putting tokens in a URL.
4. Vittavaan sends its bootstrap request with the short-lived access token.
5. The API verifies signature, claims, audience and revocation.
6. The API idempotently loads or creates the local principal mapped by `sub`.
7. The API resolves permitted people, households, grants, preferences and feature flags.
8. The web app opens the requested permitted route or the first-run flow.
9. The system records safe authentication/bootstrap evidence without tokens.

**Extensions:**

- 2a. Authentication fails: auth-core owns the retry/recovery experience.
- 3a. Handoff state/return target is invalid: reject and restart from an approved origin.
- 5a. Token expired: return stable `401`; invoke the approved refresh/reauthentication path.
- 5b. JWKS/revocation unavailable: fail closed and show temporary unavailability.
- 7a. Local principal is suspended/closed: return `403` even if auth-core identity is valid.
- 8a. Requested resource is outside scope: use a non-enumerating denial/default route.

**Postconditions:** No authentication secret is stored by Vittavaan; an authorized application context exists or access is safely denied.

## UC3-HH-001 — Create Household and Add a Person

**Primary actor:** Self-service owner  
**Requirements:** FR3-HH-001, 004–009  
**Wireframe:** `Household.dc.html`, Account setup

**Preconditions:** The actor has a valid local principal.

**Main success flow:**

1. The actor creates or opens their household.
2. The actor adds a person with display identity, relationship, date of birth and login state.
3. The system determines whether guardian/minor controls apply.
4. The actor selects a household role and initial access scope.
5. The API validates that the actor may grant the requested authority.
6. The person and membership are committed atomically.
7. The household view recalculates without assuming any ungranted asset visibility.
8. Audit evidence records actor, authority, subject and outcome.

**Extensions:** Duplicate probable person requires explicit reconciliation; invalid/future birth date is rejected; invitation failure retains the non-login person; a minor cannot receive unsupported owner authority; a rejected invitation grants no visibility.

**Postconditions:** The person exists once and has only the explicitly granted household authority.

## UC3-HOLD-001 — Add a Holding Manually

**Primary actor:** Owner or granted administrator  
**Requirements:** FR3-HOLD-001–011, FR3-HH-002–007  
**Wireframes:** Assets, Holding, First run

**Main success flow:**

1. The actor selects any catalogue class/subtype.
2. The form loads universal and versioned subtype fields.
3. The actor enters acquisition, quantity, currency, liquidity and source facts.
4. The actor assigns person ownership allocations.
5. The system requires allocations to total exactly 100% and verifies authority over affected scopes.
6. The actor records an initial valuation with method, value, as-of and verification basis.
7. The API commits the holding, allocations and valuation atomically.
8. An outbox event schedules projections and records audit/provenance.
9. The UI displays the holding as pending/current projection with its verification level.

**Extensions:** Unsupported subtype data is preserved only through its validated extension schema; non-INR value requires currency and later FX provenance; self-declared estimate remains Level 1; pledged/restricted status is required when relevant; probable duplicate prompts review; zero value is allowed only where subtype policy permits; unauthorized administrator draft cannot commit an owner action.

**Postconditions:** One canonical holding exists with valid ownership and at least one traceable valuation or an explicit unvalued state.

## UC3-IMPORT-001 — Import Holdings and Transactions from CSV

**Primary actor:** Owner or granted administrator  
**Requirements:** FR3-IMPORT-001–007  
**Wireframes:** Account setup, First run, Assets, Cash flow, Connections

**Main success flow:**

1. The actor uploads an allowed file and supplies an idempotency key.
2. The service scans the file and creates an isolated import job.
3. The parser identifies format/columns and stages rows without changing the ledger.
4. The actor maps columns and resolves class, subtype, person ownership, currency and source.
5. Validation reports errors, warnings and probable duplicates per row.
6. The actor confirms selected valid rows and duplicate decisions.
7. The service commits the selected batch atomically or in documented resumable chunks.
8. Rejected rows remain downloadable with safe error reasons.
9. Projection events and audit evidence are emitted once.

**Extensions:** Malware or unsupported format quarantines/rejects the file; replay returns the existing job; mixed currencies require row-level currency; partial parse failure retains valid staged rows; authority expiring before commit requires reauthorization; projection failure does not roll back committed facts and is retried idempotently.

**Postconditions:** Ledger facts are traceable to file/checksum/row and no duplicate commit occurs from replay.

## UC3-VAL-001 — Add or Correct a Valuation

**Primary actor:** Owner or granted administrator  
**Requirements:** FR3-HOLD-004–010, NFR3-FIN-001–006  
**Wireframes:** Holding, Assets, Net worth

**Main success flow:**

1. The actor selects a holding and enters value, currency, method, source and as-of time.
2. The API validates subtype-compatible method and actor scope.
3. A new immutable valuation event is appended.
4. Selection policy identifies the applicable current event.
5. Staleness and verification are derived.
6. Projections refresh and the UI shows changed totals with provenance.

**Extensions:** A correction appends a superseding event linked to the erroneous one; future as-of dates are rejected; document upload cannot auto-promote to independent verification; conflicting same-time sources remain visible and require an explicit selection/reconciliation policy.

## UC3-LEDGER-001 — Record and Correct a Transaction

**Primary actor:** Owner or granted administrator  
**Requirements:** FR3-LEDGER-004–007  
**Wireframes:** Cash flow, Holding

**Main success flow:** The actor records date, amount/currency, type, category, owner/scope, source and optional holding/liability links; the system distinguishes external flow from internal transfer; the immutable entry commits; affected projections recalculate; provenance and audit evidence appear in the ledger.

**Extensions:** A mistake is corrected through a linked reversing/correcting entry; transfer sides must reconcile; future dates require an explicitly supported scheduled state; uncategorized entries remain visible as data-quality work rather than disappearing.

## UC3-DOC-001 — Upload and Access a Document

**Primary actor:** Owner or granted administrator  
**Requirements:** FR3-DOC-001–006  
**Wireframes:** Data room, Holding

**Main success flow:**

1. The actor selects document type and linked domain record.
2. The API authorizes the link target and issues a bounded upload process.
3. Bytes enter quarantine with checksum and metadata.
4. The malware scanner returns a correlated result.
5. A clean document becomes available; OCR proposals remain uncommitted suggestions.
6. An authorized reader requests access.
7. The API rechecks scope and creates a short-lived signed download URL.
8. Upload and access are audited.

**Extensions:** Malware causes quarantine and notification; scanner outage leaves the file pending; checksum duplicate offers linking rather than duplicate upload; revoked grant invalidates future signed-URL issuance; supersession preserves the old version under retention policy.

## UC3-WEALTH-001 — View Net Worth and Drill into a Holding

**Primary actor:** Authorized viewer  
**Requirements:** FR3-WEALTH-001–008  
**Wireframes:** `Net worth.dc.html`, all relevant Assets and liabilities tabs

**Main success flow:**

1. The actor selects a permitted person/household scope and period.
2. The API resolves the current projection and underlying provenance.
3. The page shows assets, liabilities, net worth, verified share, movements and trend.
4. Missing/stale facts are named and gaps remain visible.
5. The actor opens a class and then one holding.
6. The API returns only authorized holding, ownership, valuation, restriction and document metadata.
7. Values reconcile to the selected scope and as-of policy.

**Extensions:** First run shows guided entry/import; negative net worth remains correctly represented; stale values remain last-known and labelled; projection lag shows last-calculated time; no authority returns non-enumerating denial; partial data marks aggregate completeness rather than fabricating a full total.

## UC3-AN-001 — Review Performance and Attribution

**Primary actor:** Authorized owner/viewer  
**Requirements:** FR3-AN-001–007  
**Wireframes:** `Analysis.dc.html`, `Attribution.dc.html`

**Main success flow:** The actor selects scope/period; the engine verifies cash-flow and valuation sufficiency; computes XIRR, TWRR, benchmark and attribution separately; reconciles contribution; calculates verified/self-declared comparisons where required; returns versioned provenance; UI explains basis and permits ledger drill-down.

**Extensions:** Insufficient cash flows withhold XIRR; missing valuation boundaries withhold TWRR; unlicensed benchmark is unavailable; partial-period holding uses documented weighting; negative return displays normally; attribution mismatch fails calculation rather than hiding a residual.

## UC3-PLAN-001 — Create a Goal and Detect a Liquidity Mismatch

**Primary actor:** Owner  
**Requirements:** FR3-PLAN-001–006  
**Wireframe:** `Planning.dc.html`

**Main success flow:** The owner defines target/date and assumptions; links permitted holdings; the engine projects versioned contributions and growth; compares availability/exit windows with target date; returns amount and liquidity funding gaps; user saves the scenario with immutable assumptions; later holding changes identify affected goals.

**Extensions:** No funding holdings produces an explicit unfunded state; the same holding funding multiple goals is disclosed; a sold/pledged holding triggers recalculation; changed assumptions create a new scenario version; past target requires close/revise workflow.

## UC3-SET-001 — Export or Close an Account

**Primary actor:** Authenticated person acting for self  
**Requirements:** FR3-SET-003–006, NFR3-PRIV-004–008  
**Wireframe:** `Settings.dc.html`

**Main success flow (export):** Verify recent authentication as required; create an idempotent export job; compile Vittavaan-owned data and manifest; store encrypted artifact; notify without exposing content; issue expiring authenticated access; audit generation/download/expiry.

**Main success flow (closure):** Reconfirm intent and consequences; coordinate auth-core identity/session action through the approved workflow; immediately block ordinary access; classify data for deletion, retention or legal hold; anonymize when due; preserve pseudonymous required evidence; report completion state.

**Extensions:** Repeated request returns current job; job failure is retryable; unresolved ownership/estate obligations may require a governed pause; closure never silently deletes another person’s shared holding facts.

## UC3-GRANT-001 — Grant and Revoke Household Access

**Primary actor:** Owner/grantor  
**Requirements:** FR3-HH-004–008, NFR3-PRIV-003  
**Wireframes:** Household, Consents, Settings

**Main success flow:** Grantor selects grantee, exact scope, access level, purpose and expiry; server verifies grantor authority; grant commits and is audited; grantee bootstrap reflects only allowed scope; grantor later revokes; subsequent reads fail immediately and the historical evidence remains.

**Extensions:** Expiry auto-revokes effective access; no grant may exceed grantor authority; document permission is independent where required; client-side hiding never substitutes for response filtering.

## UC3-CONSENT-001 — Grant, Review and Revoke Source Consent

**Primary actor:** Person providing consent
**Requirements:** FR3-CONSENT-001–005, FR3-IMPORT-007–008
**Wireframes:** Consents, Connections, Account setup

**Preconditions:** The actor is authenticated, represents the consent subject, and the provider/purpose/data-category contract is approved for the environment. A placeholder connector cannot request operational consent.

**Main success flow:**

1. The actor opens Consents and selects a supported source/provider.
2. The system displays the exact purposes, data categories, duration, withdrawal effect and retention treatment.
3. The actor confirms through the required auth-core reauthentication/consent ceremony.
4. The API validates subject authority and records an immutable consent artefact/reference plus effective consent state.
5. The connector receives only the allowed provider, person, purposes and categories.
6. Collection/imported facts retain the consent and source provenance used at collection time.
7. The Consents surface shows grant time, expiry, current state and available actions.
8. On revocation, future collection stops promptly and the action is audited; retained prior facts follow their documented legal/retention basis.

**Extensions:** An expired consent cannot start a fetch; provider callback state mismatch is rejected; a provider outage does not silently revoke consent; revoked consent does not erase shared or legally retained facts; a changed purpose/category set requires a new consent rather than broadening the old one; an inactive connector is labelled unavailable and cannot create a misleading active record.

**Postconditions:** Future processing is limited to an effective compatible consent or another explicitly recorded basis, and grant/revocation evidence remains auditable.

## UC3-LIAB-001 — Add and Maintain a Liability

**Primary actor:** Borrower/owner or granted administrator
**Requirements:** FR3-LEDGER-001–003, FR3-LEDGER-008
**Wireframes:** Liabilities, Holding, Account setup

**Main success flow:**

1. The actor selects one of the liability catalogue subtypes and identifies direct, contingent, tax or court-ordered nature.
2. The form loads universal and versioned subtype fields.
3. The actor enters borrower, lender/authority, currency, terms, dates, rate/reset facts and source.
4. The actor records a dated direct balance or contingent exposure and, where applicable, a versioned repayment schedule.
5. The actor links financed/pledged holdings without duplicating them.
6. The API validates authority, subtype schema, balance nature, collateral and schedule consistency.
7. Liability terms, balance event, links and outbox/audit evidence commit atomically.
8. Projections display direct debt in net worth and contingent exposure separately with provenance/as-of state.

**Extensions:** A balance correction appends a superseding event; incomplete schedules remain partial rather than invented; floating debt without required benchmark/reset is rejected; guarantee crystallization creates a new direct-balance fact and preserves contingent history; paid-off status requires an accepted zero balance or explained residual; unauthorized collateral linkage is rejected without exposing the holding.

**Postconditions:** The obligation is represented once with reproducible terms, dated balance and correct direct/contingent treatment.

## UC3-PREF-001 — Change Application Preferences

**Primary actor:** Authenticated principal
**Requirements:** FR3-SET-001–002
**Wireframe:** Settings

**Main success flow:** The actor opens Settings; reviews display currency, locale/time zone, accessibility and notification choices plus current access visibility; changes permitted preferences; the API validates values and expected version; preferences commit; subsequent presentation changes without altering stored financial facts; the action is audited where material.

**Extensions:** A concurrent update returns a version conflict; unsupported locale/time zone/channel is rejected; mandatory security/legal notifications cannot be disabled; display-currency change recalculates presentation through dated FX facts and never rewrites native amounts; reduced-motion/text-scale settings apply accessibly on the next render.

**Postconditions:** Principal preferences are updated independently of financial facts and access authority.
