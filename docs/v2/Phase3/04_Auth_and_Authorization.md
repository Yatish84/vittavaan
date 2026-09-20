# Phase 3 — System Design: Authentication & Authorization

> **OOSE Phase:** System Design
> **Purpose:** Specifies the complete authentication flow and the two-layer authorization system (RBAC + ABAC). This is the security backbone of the platform.
> **Status:** Draft

---

## 1. Authentication Architecture Overview

Vittavaan uses a **delegated authentication model**: user identity and credential management are fully delegated to Supabase Auth. Vittavaan owns the **authorization** layer — what authenticated users are allowed to see and do.

```mermaid
flowchart LR
    U["👤 User"]
    SA["🔑 Supabase Auth\n(External IdP)"]
    VBE["⚙️ Vittavaan Backend\n(FastAPI)"]
    DB["🗄️ PostgreSQL"]

    U -->|1. Credentials| SA
    SA -->|2. Signed JWT| U
    U -->|3. JWT in header| VBE
    VBE -->|4. Verify JWT| SA
    VBE -->|5. User lookup by jwt_sub| DB
    DB -->|6. User record + roles| VBE
    VBE -->|7. Authorised response| U
```

**What Supabase Auth handles:**
- Password hashing and storage
- Email verification
- Phone OTP generation and validation
- JWT issuance (RS256 signed)
- Session revocation

**What Vittavaan handles:**
- JWT verification (signature check against Supabase public key)
- User record creation on first authentication
- Role assignment (`is_investor`, `is_advisor`, `is_admin`)
- RBAC — which features each role can access
- ABAC — which data each user can access from other users

---

## 2. Authentication Flow (Full Detail)

```mermaid
sequenceDiagram
    actor User
    participant ClientApp as Client App\n(React / Mobile)
    participant SupabaseSDK as Supabase JS SDK
    participant SupabaseAuth as Supabase Auth\n(cloud.supabase.com)
    participant FastAPI as Vittavaan API\n(FastAPI)
    participant DB as PostgreSQL

    User->>ClientApp: Open Vittavaan app
    ClientApp->>SupabaseSDK: supabase.auth.getSession()
    SupabaseSDK-->>ClientApp: Existing session OR null

    alt No existing session
        User->>ClientApp: Enter email + password
        ClientApp->>SupabaseAuth: POST /auth/v1/token {email, password}
        SupabaseAuth->>SupabaseAuth: Validate credentials
        SupabaseAuth-->>ClientApp: {access_token (JWT), refresh_token, user}

        ClientApp->>FastAPI: POST /api/v1/auth/session\n{Authorization: Bearer <access_token>}
        FastAPI->>FastAPI: Decode JWT header → get kid (key ID)
        FastAPI->>SupabaseAuth: GET /auth/v1/jwks (public key set)
        SupabaseAuth-->>FastAPI: JWKS (public keys)
        FastAPI->>FastAPI: Verify JWT signature (RS256)
        FastAPI->>FastAPI: Check exp claim > now()
        FastAPI->>DB: SELECT * FROM users WHERE jwt_sub = claims.sub

        alt First login (user not found)
            FastAPI->>DB: INSERT INTO users {jwt_sub, email, is_investor=true}
            FastAPI->>DB: INSERT INTO portfolios {user_id}
            FastAPI->>DB: INSERT INTO settings {user_id, defaults}
            FastAPI-->>ClientApp: {user_id, is_new_user: true, active_role: "INVESTOR"}
        else Returning user
            FastAPI->>DB: UPDATE users SET last_login_at = now()
            FastAPI-->>ClientApp: {user_id, is_new_user: false, active_role: "INVESTOR"}
        end

        ClientApp->>ClientApp: Store access_token in memory\n(NOT localStorage — XSS risk)
        ClientApp->>User: Redirect to dashboard
    else Existing session (auto-login)
        SupabaseSDK->>SupabaseAuth: Refresh token if near expiry
        SupabaseAuth-->>SupabaseSDK: Fresh access_token
        SupabaseSDK-->>ClientApp: Valid session
        ClientApp->>User: Show dashboard
    end
```

---

## 3. JWT Structure & Claims

Supabase Auth issues JWTs with the following structure:

```json
Header:
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "supabase-public-key-id"
}

Payload (claims):
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",  // Supabase user ID (→ jwt_sub in our DB)
  "email": "yatish@example.com",
  "aud": "authenticated",
  "role": "authenticated",
  "exp": 1758345600,                               // Token expiry (Unix timestamp)
  "iat": 1758259200,                               // Issued at
  "iss": "https://yourproject.supabase.co/auth/v1"
}
```

**FastAPI extracts:**
- `sub` → maps to `users.jwt_sub` → used to fetch the `user_id` and role flags
- `exp` → verified to be in the future
- Signature → verified against Supabase's RS256 public key (fetched once at startup, cached with TTL)

**Vittavaan does NOT extend JWT claims.** Role information (`is_investor`, `is_advisor`, `is_admin`) is always read from PostgreSQL, not the JWT. This prevents stale role data from tokens issued before a role change.

---

## 4. Token Storage Security

| Client Type | Storage Method | Rationale |
|---|---|---|
| React web app | **In-memory** (React state / context) | Prevents XSS access to tokens. Token is lost on page refresh — Supabase SDK auto-refreshes silently via secure cookie or refresh token. |
| React Native mobile (V2) | **Secure enclave** via `expo-secure-store` | Hardware-backed secure storage; not accessible to other apps |
| **NEVER** | `localStorage`, `sessionStorage` | Vulnerable to XSS; a single injected script can steal the token |

---

## 5. RBAC — Role-Based Access Control

RBAC determines which **features and endpoints** a user can access.

### 5.1 Role Flags

```python
# backend/app/core/auth.py
class UserContext:
    user_id: UUID
    jwt_sub: str
    is_investor: bool
    is_advisor: bool
    is_admin: bool
    active_role: RoleEnum  # The currently selected role (can switch)
```

### 5.2 Endpoint Role Guards

FastAPI dependency injection applies role checks as decorators:

```python
# Dependency: any authenticated user
async def get_current_user(jwt: str = Depends(verify_jwt)) -> UserContext: ...

# Dependency: must be an investor
async def require_investor(user: UserContext = Depends(get_current_user)) -> UserContext:
    if not user.is_investor:
        raise HTTPException(403, "Investor role required")
    return user

# Dependency: must be an advisor
async def require_advisor(user: UserContext = Depends(get_current_user)) -> UserContext:
    if not user.is_advisor:
        raise HTTPException(403, "Advisor role required")
    return user

# Dependency: must be admin
async def require_admin(user: UserContext = Depends(get_current_user)) -> UserContext:
    if not user.is_admin:
        raise HTTPException(403, "Admin role required")
    return user
```

### 5.3 RBAC Matrix — Endpoint Access

```mermaid
flowchart TD
    AuthUser["✅ Authenticated User\n(all endpoints below require valid JWT)"]

    AuthUser --> INVESTOR_FEAT["Investor Features\nRequires: is_investor=true"]
    AuthUser --> ADVISOR_FEAT["Advisor Features\nRequires: is_advisor=true"]
    AuthUser --> ADMIN_FEAT["Admin Features\nRequires: is_admin=true"]
    AuthUser --> SHARED["Shared Features\nAny authenticated user"]

    INVESTOR_FEAT --> I1["POST /portfolio/assets\nPOST /portfolio/transactions\nGET /dashboard\nGET /estate/*\nPOST /gifts/*\nPOST /credit/*\nGET /profile/investor/resume"]
    ADVISOR_FEAT --> A1["PUT /profile/advisor\nPOST /insights\nPOST /queries/{id}/respond\nGET /queries/{id}/context"]
    ADMIN_FEAT --> ADM1["PATCH /advisors/{id}/verify\nPOST /gifts/rules (admin-only)\nGET /audit-logs/platform"]
    SHARED --> S1["GET /advisors (search)\nGET /connections\nPATCH /connections/{id}/consent\nGET /settings\nPOST /auth/session"]
```

---

## 6. ABAC — Attribute-Based Access Control (Consent Proxy)

ABAC determines which **data fields** from another user's profile a requesting user can read. This is the Protection Proxy pattern.

### 6.1 Access Decision Logic

```mermaid
flowchart TD
    REQ["API Request:\nGET /peers/{investor_id}/portfolio\nRequester: advisor_user_id"]
    REQ --> FETCH_CONN["Fetch Connection WHERE\nrequester=advisor_id\nrecipient=investor_id"]
    FETCH_CONN --> CHECK_EXISTS{"Connection exists\nand status=ACCEPTED?"}
    CHECK_EXISTS -->|No| DENY403["Return 403\n'No connection to this user'"]
    CHECK_EXISTS -->|Yes| CHECK_EXPIRY{"consent_expires_at\n> NOW()?"}
    CHECK_EXPIRY -->|No| DENY403B["Return 403\n'Consent has expired'"]
    CHECK_EXPIRY -->|Yes| FETCH_PERMS["Read permissions JSONB array\nfrom Connection record"]
    FETCH_PERMS --> GET_DATA["Fetch full portfolio data\nfrom WealthAndOwnershipEngine"]
    GET_DATA --> FILTER["Filter response payload:\nRemove all fields NOT\nin permissions array"]
    FILTER --> RETURN200["Return 200 OK\nwith filtered payload only"]

    style DENY403 fill:#fee2e2,stroke:#ef4444
    style DENY403B fill:#fee2e2,stroke:#ef4444
    style RETURN200 fill:#dcfce7,stroke:#22c55e
```

### 6.2 Permitted Field Registry

The `permissions` JSONB field stores an array of field identifiers from this registry:

| Field Identifier | Data Disclosed | Notes |
|---|---|---|
| `total_net_worth` | Net worth in ₹ band (e.g., "₹1–5 Cr") | Never exact figure unless `exact_net_worth` is granted |
| `exact_net_worth` | Exact net worth in minor units | Requires explicit selection — not included in defaults |
| `asset_allocation` | % split across Liquid / RE / Alternative | No individual asset details |
| `liquid_assets` | Total liquid assets value + sub-type breakdown | No institution names |
| `real_estate_assets` | RE asset list with location (city only), value | No exact addresses |
| `alternative_assets` | Alternative asset list with values | |
| `liabilities` | Total liabilities, DSR | No lender names |
| `cash_flow_summary` | Monthly income, expenses, surplus | No transaction details |
| `financial_goals` | Goal names, target, status | No asset linkage details |
| `credit_profile` | Credit score band, DSR, security coverage | Anonymous |
| `verification_status` | `verified_wealth_pct` | |

**Security rule:** If `exact_net_worth` is not in the permissions list but `total_net_worth` is, the response contains `net_worth_band: "₹1–5 Cr"` instead of `net_worth_minor_units: 24500000`.

### 6.3 Implementation: FastAPI Dependency

```python
# backend/app/core/consent.py

class ConsentGate:
    """Protection Proxy — wraps all cross-user data access."""

    async def evaluate(
        self,
        requesting_user_id: UUID,
        data_owner_id: UUID,
        db: AsyncSession
    ) -> ConsentDecision:
        connection = await db.execute(
            select(Connection)
            .where(
                Connection.requester_id == requesting_user_id,
                Connection.recipient_id == data_owner_id,
                Connection.status == "ACCEPTED"
            )
        )
        conn = connection.scalar_one_or_none()

        if conn is None:
            return ConsentDecision(allowed=False, reason="NO_CONNECTION", permitted_fields=[])

        if conn.consent_expires_at and conn.consent_expires_at < datetime.now(UTC):
            return ConsentDecision(allowed=False, reason="CONSENT_EXPIRED", permitted_fields=[])

        return ConsentDecision(
            allowed=True,
            reason="CONSENT_VALID",
            permitted_fields=conn.permissions or []
        )

    def filter_payload(self, payload: dict, permitted_fields: list[str]) -> dict:
        """Strip all keys not explicitly listed in permitted_fields."""
        if not permitted_fields:
            return {}
        return {k: v for k, v in payload.items() if k in permitted_fields}
```

---

## 7. Two-Factor Authentication (2FA)

2FA is delegated to Supabase Auth and is configured by the user in Settings.

### Supported 2FA Methods
1. **TOTP (Time-based One-Time Password)** — via authenticator apps (Google Authenticator, Authy)
2. **SMS OTP** — via Indian phone number (Twilio/MSG91 integration in Supabase)

### 2FA Flow

```mermaid
stateDiagram-v2
    [*] --> EmailPassword : User submits email+password
    EmailPassword --> MFARequired : Supabase detects 2FA enrolled
    EmailPassword --> JWTIssued : No 2FA enrolled
    MFARequired --> TOTPPrompt : TOTP method
    MFARequired --> SMSPrompt : SMS OTP method
    TOTPPrompt --> TOTPVerify : User enters 6-digit code
    SMSPrompt --> SMSVerify : User enters SMS code
    TOTPVerify --> JWTIssued : Valid TOTP code
    TOTPVerify --> MFAFailed : Invalid code
    SMSVerify --> JWTIssued : Valid SMS code
    SMSVerify --> MFAFailed : Invalid code
    MFAFailed --> MFARequired : Retry (max 5 attempts)
    JWTIssued --> [*] : Session established
```

---

## 8. Session Management

### Session Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Active : POST /auth/session (valid JWT)
    Active --> Expired : exp claim reached
    Active --> Revoked : User logs out\nor admin terminates
    Expired --> Active : Supabase refresh token\n(auto-refresh in SDK)
    Revoked --> [*] : Session terminated
```

### Session Table
The `local_sessions` table records every session with:
- `session_id` — UUID
- `user_id` — who is authenticated
- `jwt_sub` — the Supabase user ID (for cross-reference)
- `active_role` — current role context (INVESTOR or ADVISOR)
- `expires_at` — matches the JWT `exp` claim
- `is_active` — set to `false` on explicit logout
- `device_info` — user-agent string (for "view active sessions" feature)
- `ip_address` — for audit purposes (not displayed to user by default)

### Logout Everywhere
`DELETE /auth/sessions` sets `is_active = FALSE` for all sessions for the current `user_id`. The user must re-authenticate on all devices.

---

## 9. Admin Access Control

Admin-only endpoints are guarded by the `require_admin` dependency. Admins have:
- Read access to all advisor profiles for credential verification
- Write access to `advisor_profiles.credential_verification_status`
- Write access to `gift_rules` table (adding new rules on Finance Act updates)
- Read access to platform-level audit logs

**Admins do NOT have:** Access to any individual Investor's financial data (portfolio, transactions, estate plan). This is enforced at the service layer — admin role does not bypass the ABAC consent gate.

---

## 10. Security Headers

All API responses include:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'none'
Cache-Control: no-store  (for all authenticated endpoints)
```

CORS is configured to allow only known origins:
```python
# backend/app/core/config.py
ALLOWED_ORIGINS = [
    "http://localhost:5173",               # local Vite dev server
    "https://staging.vittavaan.in",        # staging frontend
    "https://vittavaan.in",                # production frontend
    "https://www.vittavaan.in",
]
```

---

*Next document: [05_Event_and_Background_Jobs.md](./05_Event_and_Background_Jobs.md)*
