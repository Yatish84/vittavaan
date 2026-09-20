# Phase 3 — System Design: Data Room Architecture

> **OOSE Phase:** System Design
> **Purpose:** Specifies how documents are stored, accessed, secured, and managed throughout their lifecycle. The Data Room is critical for legal provenance — title deeds, appraisal reports, consent audit logs, will documents, and data exports.
> **Status:** Draft

---

## 1. What is the Data Room?

The Data Room is the secure document storage subsystem of Vittavaan. It stores:

| Category | Examples | Sensitivity |
|---|---|---|
| **Asset provenance** | Title deeds, purchase agreements, FD receipts, valuation reports, appraisal certificates | HIGH |
| **Estate documents** | Wills, gift deeds, succession certificates | VERY HIGH |
| **Consent audit** | Consent grant records, consent expiry logs | HIGH |
| **Legal compliance** | Gift rule versions, stamp duty receipts, registration records | HIGH |
| **User export** | Complete data export ZIP | HIGH |
| **Platform** | Advisory query attachments | MEDIUM |

All documents are:
- **Encrypted at rest** (AES-256) — provided by Supabase Storage / S3
- **Encrypted in transit** — TLS 1.3 only
- **Access-controlled** — every download requires a fresh time-limited signed URL
- **Never publicly accessible** — no public bucket permissions; no CDN caching of documents
- **Soft-deletable** — deleted documents are marked `is_active = FALSE`; physically removed after 30 days

---

## 2. Storage Architecture

### Local / Staging: Supabase Storage
- S3-compatible object store managed by Supabase
- Integrated with Supabase Auth — storage RLS policies possible
- 1 GB free tier; adequate for local dev and staging
- Storage bucket: `vittavaan-data-room` (private, no public access)

### Production: AWS S3 (`ap-south-1`, Mumbai)
- S3 bucket: `vittavaan-data-room-prod`
- Bucket policy: all public access blocked
- Encryption: SSE-S3 (AES-256) by default; upgrade to SSE-KMS (AWS KMS managed key) for VERY HIGH sensitivity documents
- Access logging: S3 server access logs → CloudWatch Logs
- Lifecycle rule: Objects in `exports/` prefix → delete after 72 hours (user export files)
- Versioning: **Disabled** (we use soft-delete + append-only at application layer; S3 versioning creates legal complexity)

---

## 3. Storage Key Conventions

All objects are stored with a structured key (path) that encodes ownership and type:

```
Pattern:
  users/{user_id}/{category}/{year}/{document_id}.{ext}

Examples:
  users/550e8400-e29b-41d4-a716-446655440000/deeds/2026/abc12345-deed.pdf
  users/550e8400-e29b-41d4-a716-446655440000/wills/2026/def67890-will.pdf
  users/550e8400-e29b-41d4-a716-446655440000/consent-logs/2026/ghi11111-consent.json
  users/550e8400-e29b-41d4-a716-446655440000/exports/2026/jkl22222-export.json
  users/550e8400-e29b-41d4-a716-446655440000/appraisals/2026/mno33333-appraisal.pdf
```

**Category slug → `document_type` mapping:**

| Category Slug | Document Types |
|---|---|
| `deeds` | `TITLE_DEED`, `GIFT_DEED` |
| `valuations` | `VALUATION_REPORT`, `APPRAISAL_REPORT` |
| `agreements` | `PURCHASE_AGREEMENT`, `LOAN_AGREEMENT` |
| `wills` | `WILL` |
| `consent-logs` | `CONSENT_FORM`, `CONSENT_EXPIRY_LOG` |
| `tax` | `TAX_DOCUMENT` |
| `insurance` | `INSURANCE_POLICY` |
| `exports` | `USER_EXPORT` |
| `other` | `OTHER` |

---

## 4. Document Upload Flow

```mermaid
sequenceDiagram
    actor User
    participant Client as React App
    participant API as FastAPI
    participant DocSvc as DocumentService
    participant Scanner as ClamAV Scanner\n(async job)
    participant Storage as Supabase Storage\n/ S3
    participant DB as PostgreSQL

    User->>Client: Select file + document type + metadata
    Client->>Client: Client-side validation:\n- Max file size: 25 MB\n- Allowed MIME types check\n- File name sanitisation

    alt File too large or wrong type
        Client->>User: Show error before upload
    else Valid file
        Client->>API: POST /api/v1/documents\n(multipart/form-data)

        API->>API: Validate metadata (document_type, etc.)
        API->>API: Generate document_id (UUID)
        API->>API: Build storage_key:\nusers/{user_id}/{category}/{year}/{doc_id}.{ext}

        API->>Storage: Upload file bytes to storage_key
        Storage-->>API: Upload confirmation

        API->>DB: INSERT documents {\n  storage_key,\n  scan_status: "PENDING",\n  is_active: true,\n  owner_id: user_id\n}
        DB-->>API: document_id

        API->>Scanner: Queue scan_document(document_id)\n[async — non-blocking]

        API-->>Client: 201 Created {\n  document_id,\n  scan_status: "PENDING",\n  message: "File uploaded — scanning in progress"\n}
        Client->>User: Show "Uploaded — verification pending"

        Note over Scanner: Async antivirus scan (ClamAV)
        Scanner->>Storage: Fetch file bytes
        Scanner->>Scanner: ClamAV scan
        alt Virus found
            Scanner->>Storage: DELETE file (quarantine)
            Scanner->>DB: UPDATE documents SET\n  scan_status = "QUARANTINED"\n  is_active = FALSE
            Scanner->>User: Send notification:\n"Uploaded file failed security scan and was removed."
        else File clean
            Scanner->>DB: UPDATE documents SET\n  scan_status = "CLEAN"
            Scanner->>User: Send notification:\n"Document verified and saved to Data Room."
        end
    end
```

---

## 5. Document Download Flow (Signed URL)

Documents are **never served directly** from storage. Every download requires:
1. An authenticated API call
2. Ownership verification (the requestor must be the document owner)
3. A freshly generated, time-limited signed URL

```mermaid
sequenceDiagram
    actor User
    participant Client as React App
    participant API as FastAPI
    participant DocSvc as DocumentService
    participant DB as PostgreSQL
    participant Storage as Supabase Storage / S3

    User->>Client: Click "Download [Document Name]"
    Client->>API: GET /api/v1/documents/{document_id}/download\n[Authorization: Bearer JWT]

    API->>DB: SELECT document WHERE\ndocument_id = ? AND owner_id = user_id AND is_active = TRUE

    alt Document not found or not owner
        DB-->>API: No result
        API-->>Client: 404 Not Found
    else scan_status = "QUARANTINED"
        DB-->>API: Document (quarantined)
        API-->>Client: 403 Forbidden\n{error: "Document is quarantined"}
    else scan_status = "PENDING"
        DB-->>API: Document (pending)
        API-->>Client: 409 Conflict\n{error: "Document is still being verified. Try in a moment."}
    else scan_status = "CLEAN"
        DB-->>API: Document record {storage_key, mime_type}
        API->>Storage: Generate signed URL\n(storage_key, expires_in: 900s)
        Storage-->>API: signed_url
        API-->>Client: 200 OK {\n  download_url: signed_url,\n  expires_in_seconds: 900,\n  file_name: "karjat-title-deed.pdf",\n  mime_type: "application/pdf"\n}
        Client->>User: Trigger file download using signed_url
        Note over Client: Client downloads directly from Storage\n(FastAPI is NOT in the download path)
    end
```

**Why the client downloads directly from storage (not via API)?**
- Avoids streaming large files through FastAPI → lower server memory, better performance
- Signed URL has 15-minute TTL — adequate time to download
- If URL expires, user clicks download again (no cost beyond a new URL generation)

---

## 6. Allowed MIME Types

The API rejects uploads with any MIME type not in this allowlist:

| MIME Type | File Extension | Documents Allowed |
|---|---|---|
| `application/pdf` | `.pdf` | All |
| `image/jpeg` | `.jpg`, `.jpeg` | Appraisals, valuations, deeds |
| `image/png` | `.png` | Appraisals, valuations |
| `image/webp` | `.webp` | Appraisals |
| `application/json` | `.json` | Consent logs, exports (system-generated only) |
| `application/zip` | `.zip` | User export only (system-generated) |

Rejected MIME types (any other type including `.exe`, `.docx`, `.xlsx`, `.ppt`) return `400 Bad Request`.

---

## 7. Consent Audit Log — Immutable Design

Consent audit logs deserve special treatment — they are legal records under DPDP Act and must be immutable.

```mermaid
flowchart LR
    EVENT["Consent Event\n(grant or expiry)"]
    BUILD["ConsentAndMarketplaceEngine\nbuilds ConsentAuditRecord:\n{grantor_id, grantee_id,\ngranted_fields, purpose,\naction, timestamp, ip_hash}"]
    SIGN["Add integrity hash:\nSHA-256 of record JSON"]
    STORE["Upload to Storage\nas immutable JSON object\n(no overwrite possible)"]
    DOCDB["INSERT Document record\n{type: CONSENT_FORM,\nstorage_key, owner_id}"]

    EVENT --> BUILD --> SIGN --> STORE --> DOCDB

    style STORE fill:#fef9c3,stroke:#eab308
```

**Immutability enforcement:**
- The S3 bucket has **Object Lock** enabled for the `consent-logs/` prefix in production
- Logs are written with a `COMPLIANCE` mode retention of 7 years (matching data retention rules)
- The application never issues a `DELETE` for consent log objects — any such call would be rejected by S3

---

## 8. Document Soft Delete

When a user requests deletion of a document:
1. The `Document.is_active` flag is set to `FALSE`
2. The object in storage is **not immediately deleted**
3. A scheduled job (`purge_deleted_documents`) runs weekly and hard-deletes storage objects for documents where `is_active = FALSE AND (NOW() - created_at) > 30 days`

**Exception:** Consent audit logs and `USER_EXPORT` documents are **never hard-deleted before their retention expiry** (7 years and 72 hours respectively).

```mermaid
stateDiagram-v2
    [*] --> Active : Document uploaded (scan_status=CLEAN)
    Active --> Quarantined : ClamAV detected threat
    Active --> SoftDeleted : User requests deletion
    SoftDeleted --> HardDeleted : 30 days after soft delete\n(weekly purge job)
    Quarantined --> HardDeleted : Immediately purged
    HardDeleted --> [*]
```

---

## 9. File Size Limits

| Limit | Value | Applies To |
|---|---|---|
| Maximum file size per upload | 25 MB | All user uploads |
| Maximum total Data Room storage per user | 2 GB | Soft limit (configurable) |
| Maximum user export file size | 200 MB | System-generated export |
| Maximum consent log size | 50 KB | System-generated JSON |

Users approaching 80% of their storage quota receive an email notification.

---

## 10. Data Room + Estate Plan Integration

When an `EstatePlan` or `Will` is created, the Data Room provides a structured document checklist:

```mermaid
flowchart TD
    ESTATE["Estate Plan Created"]
    ESTATE --> CHECK["Document Checklist\nfor Estate Planning"]
    CHECK --> W["☐ Upload executed Will document\nType: WILL"]
    CHECK --> TD["☐ Upload title deeds for all\nReal Estate assets\nType: TITLE_DEED"]
    CHECK --> VA["☐ Upload appraisal certificates for\nAlternative assets\nType: APPRAISAL_REPORT"]
    CHECK --> GD["☐ Upload gift deeds for\ncompleted Gift Transfers\nType: TITLE_DEED (gift category)"]
    CHECK --> NOM["☐ Upload nominee confirmation\nletters from financial institutions\nType: OTHER"]

    style W fill:#fef9c3
    style TD fill:#fef9c3
    style VA fill:#fef9c3
    style GD fill:#fef9c3
    style NOM fill:#fef9c3
```

The `EstateCoveragePct` metric includes a **document completeness component**: an estate plan with all documents uploaded scores higher than one with missing provenance.

---

## 11. Local Development Setup

In local development, Supabase Storage runs inside Docker (part of the `supabase/*` docker-compose services):

```yaml
# docker-compose.yml (relevant excerpt)
services:
  supabase-storage:
    image: supabase/storage-api:v0.43.11
    environment:
      ANON_KEY: ${SUPABASE_ANON_KEY}
      SERVICE_KEY: ${SUPABASE_SERVICE_KEY}
      STORAGE_BACKEND: file     # local filesystem in dev (not S3)
      FILE_STORAGE_BACKEND_PATH: /var/lib/storage
    volumes:
      - supabase_storage_data:/var/lib/storage
    ports:
      - "5000:5000"
```

In production, the `STORAGE_BACKEND=s3` environment variable switches Supabase Storage to use the real S3 bucket — no code changes needed.

---

*← Previous: [05_Event_and_Background_Jobs.md](./05_Event_and_Background_Jobs.md)*

*Phase 3 complete. Next: Phase 4 — Object Design (class-level interfaces, design patterns, final API contracts)*
