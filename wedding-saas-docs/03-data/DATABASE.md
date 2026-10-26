# Database Design (PostgreSQL + SQLAlchemy)

## Entity map
`User 1:N Wedding`, `Template 1:N TemplateVersion`, `Wedding 1:1 WeddingDraft`, `Wedding 1:N WeddingPublication`, `Wedding 1:N WeddingDomain`, `Wedding 1:N Order`, `Order 1:N Payment`, `Wedding 1:N Guest`, `Guest 1:N RSVP`.

## Key invariants
- `Wedding.ownerId` must match authenticated user on mutation.
- `Wedding.templateVersionId` pins immutable version.
- `WeddingDraft` is mutable JSONB + optimistic revision.
- `WeddingPublication` is immutable JSONB + unique `(weddingId, revision)`.
- `WeddingDomain.hostname` is normalized and globally unique.
- Active publication must belong to domain's wedding; enforce composite FK or transactional guard plus migration-level constraint.
- `Order.amount` integer smallest currency unit; `currency` explicit.
- Payment webhook event IDs unique per provider; repeated events idempotent.
- Use `Asset` table to track ownership, status, media type, size and storage key.

## Models and migrations
See [`../09-examples/models.py`](../09-examples/models.py) for illustrative SQLAlchemy 2.0 models. It is a **starting point**, not an audited production migration. Additional tables: `PaymentWebhookEvent`, `Entitlement`, `Asset`, `OutboxEvent`, `AuditLog`, auth sessions.

Alembic is the only mechanism for schema changes. Generate a candidate revision from model metadata, inspect the generated SQL, add indexes/constraints explicitly, and run it against a disposable PostgreSQL database before merge. Do not rely on `create_all()` outside local experiments.

## Transaction boundaries
- Draft PATCH: owner check + revision compare-and-swap.
- Order creation: server-side pricing, single authoritative amount.
- Payment confirmation: verify provider signature and event ID, update payment/order/entitlement atomically.
- Publish: owner + entitlement + schema + asset readiness; lock wedding row; insert immutable publication; atomically update active pointer; write outbox event.

## Indexes
Unique normalized hostname; unique template `(templateId,version)`; unique publication `(weddingId,revision)`; unique provider webhook event `(provider,eventId)`; indexes on wedding owner, payment order, guest wedding and publication wedding.

## Backup and migrations
Automated encrypted backups + PITR where supported; scheduled restore drills. Expand/contract migrations for zero/low-downtime deploys. Never remove a template version referenced by live weddings.
