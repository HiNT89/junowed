# Roadmap and Milestones

Estimates are indicative for an experienced full-stack developer, **not commitments**; refine after template audit.

## Phase 0 — Audit (3–5 days)
Inventory 10 repositories, licensing, dependencies, hardcoded data and Next.js server features. Select pilot HTML, React, Next templates. Deliverable: filled template audit.

## Phase 1 — Foundation (1–2 weeks)
Workspace, DB, auth, canonical schema, template registry/SDK, basic observability. DoD: schema contract tests and migration CI pass.

## Phase 2 — First vertical slice (1–2 weeks)
Migrate one HTML template, builder, autosave, private preview, published snapshot and wildcard subdomain. DoD: real data renders and republish works without redeploy.

## Phase 3 — Commerce (1–2 weeks)
Orders, payment sandbox, verified webhook, entitlement, publish gating, idempotency. DoD: duplicate/forged callbacks cannot publish unpaid wedding.

## Phase 4 — Multi-runtime (2–3 weeks)
React adapter/hydration and Next runtime isolation; migrate remaining templates incrementally. DoD: visual baselines pass across representative devices.

## Phase 5 — Production hardening (1–2 weeks)
Monitoring, backups, restore drill, security review, performance test, incident runbook, staged release. DoD: security and reliability checklist passes.

## Risks
- Next apps rely on incompatible routing/server features.
- Hardcoded content scattered across animation scripts.
- Asset licensing or external scripts block commercial use.
- Wildcard TLS/hosting restrictions vary by provider.
- Payment provider settlement and refund semantics require provider-specific integration.

## Backlog priorities
P0: template registry, schema, draft, preview, publish, payment, domain, upload. P1: RSVP, analytics, custom domain. P2: visual editor, multi-language, invitation guest personalization, advanced marketing automation.
