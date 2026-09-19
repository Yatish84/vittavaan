# Tech Stack Recommendation — Vittavaan

> **Status:** Draft — awaiting stakeholder approval before implementation begins.
> **Scope:** V1 (desktop web, manual data entry). Mobile (V2) targets are called out explicitly where they influence current decisions.

---

## 1. Guiding Principles for Stack Selection

Before listing tools, these principles drive every choice:

1. **Solo-developer velocity** — The stack must minimize boilerplate without sacrificing correctness. Tools with strong conventions beat blank-slate frameworks.
2. **Local → Staging → Cloud without re-engineering** — Every service chosen must run identically in Docker locally and on managed cloud. No "works on my machine" surprises.
3. **Financial-grade correctness** — The backend must have first-class support for integer arithmetic, typed decimal handling, and financial math libraries.
4. **API-first** — The backend is a pure JSON API. It has no opinion about whether the consumer is a React app, a React Native app, or a third-party integration. This ensures V2 mobile reuse.
5. **Typed end-to-end** — TypeScript on the frontend, Python type hints + Pydantic on the backend. Types are documentation; documentation is what a solo developer needs most.

---

## 2. Recommended Stack — Overview

```
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND (Desktop Web — V1)                                │
│  React 19 + TypeScript + Vite                               │
│  shadcn/ui + Tailwind CSS + Recharts                        │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS / REST JSON
┌──────────────────────────▼──────────────────────────────────┐
│  BACKEND (API Layer)                                        │
│  Python 3.12 + FastAPI + Pydantic v2                        │
│  SQLAlchemy 2.0 (async) + Alembic                           │
│  Celery + Redis (background jobs)                           │
└──────┬───────────────────────────────┬───────────────────────┘
       │                               │
┌──────▼──────┐               ┌────────▼────────┐
│  PostgreSQL │               │  Supabase       │
│  (RDBMS)    │               │  Storage        │
│             │               │  (Data Room)    │
└─────────────┘               └─────────────────┘
       │
┌──────▼──────────────────────────────────────────────────────┐
│  AUTHENTICATION                                             │
│  Supabase Auth (JWT issuance + email/phone/OTP)             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  INFRASTRUCTURE                                             │
│  Docker + Docker Compose (local)                            │
│  GitHub + GitHub Actions (CI/CD)                            │
│  Railway (Staging) → AWS (Production)                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  MOBILE — V2 (future, same backend API)                     │
│  React Native + Expo                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Backend — Python 3.12 + FastAPI

### Why Python?
- **Financial libraries are best-in-class**: `numpy-financial` for XIRR/NPV, `scipy` for numerical methods, `pandas` for time-series data (FinancialSnapshot trend processing).
- **FastAPI** is the modern Python web framework — async by default, Pydantic-powered request/response validation, auto-generated OpenAPI/Swagger docs with zero extra work.
- **Pydantic v2** enforces data contracts at the boundary (incoming JSON validated against typed models), which catches data integrity errors before they touch the database.
- **Type hints throughout** — Python's modern type system + mypy static analysis gives a solo developer the equivalent of a code reviewer catching type errors before runtime.

### Core Libraries

| Library | Purpose | Version |
|---|---|---|
| `fastapi` | Web framework and API routing | `^0.115` |
| `pydantic[email]` | Request/response models, validation | `^2.9` |
| `sqlalchemy[asyncio]` | ORM for PostgreSQL (async) | `^2.0` |
| `alembic` | Database migration management | `^1.13` |
| `asyncpg` | High-performance async PostgreSQL driver | `^0.29` |
| `celery[redis]` | Background job queue | `^5.4` |
| `redis` | Celery broker + caching | `^5.1` |
| `numpy-financial` | XIRR, NPV, IRR calculations | `^1.0` |
| `scipy` | TWRR and numerical methods | `^1.14` |
| `python-jose[cryptography]` | JWT verification (from Supabase Auth) | `^3.3` |
| `supabase` | Supabase Python client (auth + storage) | `^2.7` |
| `python-multipart` | File upload handling | `^0.0.9` |
| `pytest-asyncio` | Async test support | `^0.24` |
| `httpx` | Test HTTP client for FastAPI | `^0.27` |
| `ruff` | Fast Python linter + formatter | `^0.7` |
| `mypy` | Static type checking | `^1.11` |

### Key Architectural Decisions (Backend)

**Integer-only money storage:** All monetary fields in Pydantic models and SQLAlchemy columns use `int`. A custom `Annotated[int, Field(ge=0)]` type alias `MinorUnits` is defined globally and used everywhere. No `float`, `Decimal`, or `str` for money — ever.

```python
# types.py — used everywhere money appears
from typing import Annotated
from pydantic import Field
MinorUnits = Annotated[int, Field(ge=0, description="Amount in paise (1 INR = 100 paise)")]
```

**Async everywhere:** FastAPI + SQLAlchemy async + asyncpg means all I/O is non-blocking. A single worker process handles many concurrent requests efficiently.

**Strict API versioning from day 1:** All endpoints are prefixed `/api/v1/`. When breaking changes are needed, `/api/v2/` is added without removing v1, giving the mobile app (V2) time to migrate.

---

## 4. Frontend — React 19 + TypeScript + Vite

### Why React + Vite?
- **React** is the dominant choice with the largest component ecosystem. React 19 brings built-in async transitions that work well with financial dashboards (charts that update without full re-renders).
- **Vite** replaces Create React App — near-instant hot module replacement (HMR) for a fast local development experience.
- **Not Next.js** — Vittavaan V1 is a Single Page Application (dashboard). Server-side rendering (SSR) adds complexity with no meaningful SEO benefit for an authenticated financial app. Next.js is the right choice if public marketing pages are added later.

### Core Libraries

| Library | Purpose | Version |
|---|---|---|
| `react` | UI framework | `^19.0` |
| `typescript` | Type system | `^5.6` |
| `vite` | Build tool and dev server | `^5.4` |
| `@tanstack/react-query` | Server state management (data fetching, caching) | `^5.59` |
| `react-router-dom` | Client-side routing | `^6.27` |
| `tailwindcss` | Utility-first CSS | `^3.4` |
| `shadcn/ui` | Accessible component library (built on Radix UI) | latest |
| `recharts` | Composable chart library for financial visualizations | `^2.13` |
| `@supabase/supabase-js` | Supabase Auth client | `^2.45` |
| `react-hook-form` | Form state management | `^7.53` |
| `zod` | Runtime schema validation (mirrors backend Pydantic) | `^3.23` |
| `date-fns` | Date manipulation (India timezone aware) | `^3.6` |
| `vitest` | Unit and component testing | `^2.1` |
| `@testing-library/react` | Component testing utilities | `^16.0` |

### Key Architectural Decisions (Frontend)

**No business logic in the frontend.** React components display data; they never calculate net worth, XIRR, or inheritance allocations. Every derived metric comes pre-calculated from the API. This principle ensures the mobile app (V2) gets identical results.

**India locale formatting:** A single utility module `formatters.ts` handles:
- Currency: `₹ 1,47,32,500` (Indian numbering system — lakh/crore, not million/billion)
- Dates: `DD MMM YYYY` format (e.g., `19 Sep 2026`)
- Percentages: `12.4%` (always two decimal places)
- Minor units conversion: every display always divides by 100 before showing; never stores INR as float

**Shared TypeScript types with future React Native app:** All API response types are defined in a shared `packages/types/` package within the monorepo. Both the web app and the future mobile app import from this package.

---

## 5. Database — PostgreSQL 16

### Why PostgreSQL?
The existing architecture docs correctly identify this. Key reasons:
- **ACID compliance** — essential for the `Transaction` ledger. A partial write that records a debit but not a credit is catastrophic in a financial app.
- **JSONB columns** — used for `Connection.permissions` (the field-level consent dictionary). PostgreSQL JSONB is indexed and queryable; this is better than a separate EAV table.
- **Check constraints** — enforce `ownership_split_pct BETWEEN 0 AND 100` and `amount_minor_units >= 0` at the database level, not just the application layer. Defense-in-depth for financial data.
- **Partial indexes** — e.g., an index on `connections WHERE status = 'ACCEPTED'` for fast consent lookups.
- **Row-level security (RLS)** — Supabase exposes this natively. In future, if any queries go directly to Supabase (e.g., Supabase Realtime), RLS ensures users only see their own rows.

### Local Setup
Run via Docker Compose. No installation required on the host Mac.

```yaml
# docker-compose.yml (excerpt)
postgres:
  image: postgres:16-alpine
  environment:
    POSTGRES_DB: vittavaan_dev
    POSTGRES_USER: vittavaan
    POSTGRES_PASSWORD: localdev_only
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

---

## 6. Authentication — Supabase Auth

### Why Supabase Auth?
- **Local development parity**: The Supabase CLI runs a full local Supabase stack (Auth, Storage, Studio UI) via Docker. Local and cloud behavior are identical — no "it worked locally" surprises.
- **JWT tokens**: Supabase issues standard JWTs. The FastAPI backend verifies these using the project's public key — no Supabase dependency in the hot path of every API request.
- **Supports Indian phone OTP**: SMS OTP login (via Twilio/MSG91) for Indian mobile numbers is supported out of the box.
- **Seamless cloud move**: Local → Supabase cloud (supabase.com) requires only environment variable changes, no code changes.

### Auth Flow
```
User → Supabase Auth (email/OTP) → JWT issued
JWT → FastAPI (Authorization: Bearer ...) → Verified using Supabase public key
FastAPI → Extracts user_id from JWT → Fetches/creates User record in PostgreSQL
```

The FastAPI backend never stores passwords. It trusts only cryptographically signed JWTs from Supabase.

---

## 7. Object Storage — Supabase Storage

### Why Supabase Storage?
- Supabase Storage is S3-compatible. Files stored locally in Supabase CLI's local stack work identically on Supabase cloud.
- **Signed URLs**: Documents in the Data Room (wills, deeds, valuation reports) are never publicly accessible. Every download generates a time-limited signed URL (default: 60 minutes).
- When the app moves to full AWS production, the storage bucket can be migrated to AWS S3 with no application code changes (same S3-compatible API).

---

## 8. Background Jobs — Celery + Redis

### What runs in the background?
| Job | Trigger | Frequency |
|---|---|---|
| `capture_financial_snapshot` | Asset/Liability updated event | On every portfolio change |
| `check_stale_valuations` | Scheduled | Daily at 2:00 AM IST |
| `expire_consents` | Scheduled | Every 15 minutes |
| `send_notification_alerts` | Event-driven | When triggered |
| `generate_peer_benchmarks` | Scheduled | Weekly |

### Why Celery + Redis?
- **Celery** is the de facto standard Python background job library. Works well with FastAPI via async task dispatching.
- **Redis** serves as both the Celery message broker and an application cache (for expensive calculation results like XIRR).
- Redis runs in Docker locally; in staging/production it is replaced by a managed Redis service (Railway provides managed Redis; AWS offers ElastiCache).

---

## 9. Infrastructure & Deployment

### Local Development
**All services run in Docker Compose** — PostgreSQL, Redis, the FastAPI app, and the Supabase local stack. A developer clones the repo and runs `docker compose up` to have a full working environment in minutes.

```
docker compose up
→ FastAPI backend on http://localhost:8000
→ React frontend (Vite dev server) on http://localhost:5173
→ PostgreSQL on localhost:5432
→ Redis on localhost:6379
→ Supabase Studio on http://localhost:54323
→ Supabase API on http://localhost:54321
```

### Version Control
- **GitHub** — private repository
- **Branch strategy**: `main` (protected, production-ready) + `develop` (integration) + `feature/xxx` branches
- **Conventional Commits**: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:` prefixes enforced via `commitlint`
- **Pre-commit hooks** (via `pre-commit`): ruff, mypy, prettier, vitest on changed files

### CI/CD — GitHub Actions
Every push to `develop` or `main` triggers:
1. Backend lint (ruff) + type check (mypy)
2. Backend unit + integration tests (pytest)
3. Frontend lint (ESLint + Prettier check)
4. Frontend unit tests (Vitest)
5. Docker image build (fails if build breaks)
6. On merge to `develop` → auto-deploy to **Railway staging**
7. On merge to `main` → manual approval required → deploy to **AWS production**

### Staging Environment — Railway
[Railway](https://railway.app) is a developer-friendly cloud platform that connects directly to GitHub and auto-deploys Docker containers.

Why Railway for staging (not AWS directly):
- Zero infrastructure management for a solo developer
- Auto-deploys from GitHub on push
- Managed PostgreSQL + Redis included
- Generous free tier for low-traffic staging
- When the app graduates to production scale, it moves to AWS — Railway is never the production platform

### Production Environment — AWS (when ready)
When a staging-tested module is ready for production:

| AWS Service | Purpose |
|---|---|
| ECS Fargate | Containerized FastAPI + Celery workers |
| RDS PostgreSQL | Managed database with daily automated backups |
| ElastiCache Redis | Managed Redis for Celery |
| S3 | Document storage (migrated from Supabase Storage) |
| CloudFront | CDN for the React static bundle |
| ACM | SSL certificates |
| Route 53 | DNS |
| Secrets Manager | Environment variables and secrets |

This AWS setup is provisioned using **Terraform** (Infrastructure as Code). The Terraform files live in the repo at `infrastructure/terraform/`.

---

## 10. Mobile — V2 Forward Planning

**React Native + Expo** is the planned mobile framework.

Why this works well with the current stack:
- Shares the same TypeScript type package (`packages/types/`) with the web frontend.
- Calls the exact same FastAPI backend — no mobile-specific backend needed.
- Expo simplifies the Mac → iOS Simulator → Android Emulator workflow without ejecting.
- Expo Go app allows live testing on a physical device during development.

**What we do NOW to prepare for mobile:**
1. All API responses are designed with mobile consumption in mind (no server-rendered HTML, no web-only assumptions).
2. The shared `packages/types/` package is set up from day one.
3. No web-only libraries (e.g., no `window`, no DOM-specific APIs) in business logic — only in UI components.

---

## 11. Monorepo Structure (Top Level)

```
vittavaan/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/              # Route handlers (thin — no business logic)
│   │   ├── services/         # Calculation engines, business logic
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── db/               # Alembic migrations, DB session
│   │   ├── core/             # Config, auth, middleware
│   │   └── tests/            # pytest test suite
│   ├── pyproject.toml        # Python dependencies (uv or Poetry)
│   └── Dockerfile
│
├── frontend/                 # React application
│   ├── src/
│   │   ├── pages/            # Route-level components (one per wireframe)
│   │   ├── components/       # Reusable UI components
│   │   ├── hooks/            # Custom React Query hooks
│   │   ├── lib/              # Formatters, utils, API client
│   │   └── types/            # Type imports from packages/types
│   ├── package.json
│   └── Dockerfile
│
├── packages/
│   └── types/                # Shared TypeScript types (used by frontend + future mobile)
│       ├── src/
│       │   ├── api.ts         # API request/response types
│       │   ├── domain.ts      # Core domain types (Asset, Portfolio, etc.)
│       │   └── index.ts
│       └── package.json
│
├── infrastructure/
│   └── terraform/            # AWS IaC (used when moving to production)
│
├── docs/
│   └── v2/                   # This documentation folder
│
├── docker-compose.yml        # Full local dev stack
├── docker-compose.test.yml   # CI test stack (no Supabase)
├── Makefile                  # Common commands: make dev, make test, make migrate
└── README.md                 # Quick-start guide for the project
```

---

## 12. Summary — Decision Matrix

| Category | Choice | Primary Reason |
|---|---|---|
| Backend Language | Python 3.12 | Financial math libraries + type safety |
| Backend Framework | FastAPI | Async, Pydantic, auto-docs |
| ORM | SQLAlchemy 2.0 (async) | Mature, typed, async support |
| Migrations | Alembic | Standard SQLAlchemy companion |
| Background Jobs | Celery + Redis | Industry standard for Python |
| Frontend Framework | React 19 | Largest ecosystem; React Native reuse in V2 |
| Build Tool | Vite | Fast HMR, modern ESM |
| Styling | Tailwind CSS + shadcn/ui | Utility-first; accessible components |
| Charts | Recharts | Composable, lightweight, React-native |
| Database | PostgreSQL 16 | ACID, JSONB, constraints, RLS |
| Auth | Supabase Auth | Local-cloud parity, JWT, Indian phone OTP |
| Object Storage | Supabase Storage | S3-compatible, local-cloud parity |
| Containerization | Docker + Compose | Local-cloud parity |
| CI/CD | GitHub Actions | Free for solo developer |
| Staging | Railway | Zero-ops, auto-deploy from GitHub |
| Production | AWS (ECS + RDS + S3) | Reliable, India region (ap-south-1) |
| Mobile (V2) | React Native + Expo | Shares types and API with web |
| IaC | Terraform | Standard, repeatable cloud provisioning |

---

*Approved by: [Yatish Karkera — pending]*
*Last updated: September 2026*
