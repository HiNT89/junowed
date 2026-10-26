# Deployment and Operations

## Recommended initial topology
Cloudflare DNS/CDN/WAF + R2 for media; VPS running Caddy/Nginx, `web`, `api`, `gateway`, `static-runtime`, compatible `next-runtime`, `worker`, PostgreSQL and Redis (consider managed DB early if budget allows).

The `api` image runs FastAPI through Gunicorn with Uvicorn workers (or Uvicorn directly for a small deployment). The `worker` image runs Celery against the same versioned application code and Redis. Run Alembic migrations as a one-off release job before new application instances receive traffic.

## Environments
Local `.env` (not committed), staging with separate DB/bucket/payment sandbox, production with isolated credentials and deployment approvals.

## Docker Compose service sketch
```yaml
services:
  web:
    image: registry.example.com/wedding/web:${APP_VERSION}
    restart: unless-stopped
  api:
    image: registry.example.com/wedding/api:${APP_VERSION}
    command: gunicorn app.main:app -k uvicorn.workers.UvicornWorker
    restart: unless-stopped
  gateway:
    image: registry.example.com/wedding/gateway:${APP_VERSION}
    restart: unless-stopped
  static-runtime:
    image: registry.example.com/wedding/static-runtime:${APP_VERSION}
    restart: unless-stopped
  worker:
    image: registry.example.com/wedding/worker:${APP_VERSION}
    command: celery -A app.worker.celery_app worker --loglevel=INFO
    restart: unless-stopped
```
This is a **topology sketch**, not a ready-to-run compose file. Configure networks, secrets, volumes, healthchecks, DB/Redis, resource limits, ingress and TLS before deployment.

## Production runbook
- Build immutable container images and pin digests.
- Run migration as separate controlled release step.
- Deploy to staging and run smoke + cross-tenant tests.
- Deploy production using rolling/blue-green strategy where possible.
- Check readiness, 5xx, latency, queue lag, payment events.
- Roll back app image if error budget breached; avoid destructive DB rollback.

## Backups and recovery
Daily encrypted backup plus WAL/PITR where available, offsite retention, periodic restore drill. Define explicit RPO/RTO and responsible owner.

## Capacity and costs
Track bandwidth/media egress, image processing, DB connections, cache hit ratio, template SSR CPU and traffic bursts. Scale renderers independently from core API.

## Secrets
Use secrets manager or protected runtime env; rotate payment keys; restrict DB credentials; never commit `.env` or service tokens.
