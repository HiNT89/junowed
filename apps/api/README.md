# Wedding Platform API

FastAPI modular-monolith foundation for the wedding SaaS.

## Run locally

```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
alembic upgrade head
uvicorn app.main:app --reload
```

Open `/docs`. Authenticated development routes require an `X-User-Id` header containing a UUID. This is deliberately a temporary boundary; replace it with verified session/JWT authentication before production.

The startup seed registers the documented `react-romantic@1.0.0` template. Run migrations; the application does not call `create_all()`.

## Current backend capabilities

- Drafts use revision-based optimistic locking.
- Upload intents have a local signed-PUT adapter for development; replace it with an object-storage signer in production.
- Orders use a server-side VND price (`WEDDING_PUBLISH_PRICE_VND`). Provider webhooks use HMAC during integration testing, are idempotent by provider event ID, and activate publishing entitlement only after a matching payment succeeds.
- Publishing is synchronous: it snapshots an immutable revision and updates the active public publication atomically.
