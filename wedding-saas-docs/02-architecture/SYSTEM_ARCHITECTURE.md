# System Architecture

## Logical topology
```mermaid
flowchart TB
 U[Browser / Guest] --> CF[Cloudflare DNS/CDN/WAF]
 CF --> GW[Trusted ingress + Wedding Gateway]
 CF --> WEB[Next.js SaaS Web]
 WEB --> API[FastAPI Core API]
 GW --> RES[Domain resolver / publication cache]
 RES --> S[Static HTML/React renderer]
 RES --> N[Next.js runtime(s)]
 S --> PUB[Published snapshot read API]
 N --> PUB
 API --> PG[(PostgreSQL)]
 API --> R[(Redis)]
 API --> OBJ[(R2 object storage)]
 API --> Q[Celery workers]
 PUB --> PG
```

## Services
- `web`: marketplace, builder, checkout, dashboard.
- `api`: authentication/authorization, template registry metadata, drafts, orders, entitlement, publications, domains, assets, RSVP.
- `gateway`: trusted hostname routing, safe path forwarding, runtime dispatch.
- `static-runtime`: static HTML template compilation and compatible React SSR/CSR bundles.
- `next-runtime`: converted Next templates; incompatible apps run as separately deployed versioned services.
- `worker`: outbox, cache invalidation, media processing, email/notifications.

## Backend technology baseline
- **API:** Python 3.12+, FastAPI and Uvicorn (Gunicorn/Uvicorn workers in production).
- **Validation and contracts:** Pydantic v2 request/response models; OpenAPI is generated from FastAPI and is the implementation-facing API contract.
- **Persistence:** SQLAlchemy 2.0 async ORM with `asyncpg`; Alembic owns reviewed PostgreSQL migrations.
- **Background work:** Celery with Redis broker/result backend. API requests enqueue only durable, idempotent jobs; workers do not expose public HTTP endpoints.
- **Configuration:** `pydantic-settings`; secrets are injected by the runtime, never committed.

Use one `AsyncSession` per request or job. Service-layer transaction boundaries enforce authorization and invariants; route handlers remain thin. The worker uses its own session lifecycle and must never reuse a request session.

## Request path
1. Ingress validates public Host and strips client-provided internal headers.
2. Gateway normalizes hostname and queries cached domain mapping.
3. Resolve active publication ID and pinned template version.
4. Fetch public snapshot via authenticated internal service or read replica.
5. Dispatch to matching versioned renderer; return HTML/assets.
6. Cache only safe, public responses keyed by verified host + path + publication revision.

## Architecture decisions
**ADR-001 Dynamic multi-tenant:** no per-customer build; enables republish and lower operational overhead.

**ADR-002 Version pinning:** each wedding references a template version; upgrades are explicit and testable.

**ADR-003 Snapshot publishing:** draft writes cannot accidentally leak to guests; atomic active-publication pointer.

**ADR-004 Modular monolith API:** transactions and ownership checks are simpler than early microservices.

**ADR-005 Mixed runtime:** keep original technology where feasible, convert Next apps only if dependency/routing audit permits.

## Scaling
Scale gateway and renderers horizontally; offload immutable assets to CDN; cache public snapshots by ID; keep DB as source of truth; introduce managed DB and separate workers as load grows. Cache purge is advisory; revisioned cache keys prevent cross-revision confusion.

## Observability
Structured logs with request ID, wedding ID (internal only), template ID/version, publication ID, runtime, latency and error code; traces across gateway/API/renderer; alerts for payment webhook failures, 5xx, queue lag and storage errors.
