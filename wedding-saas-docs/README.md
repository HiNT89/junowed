# Wedding Invitation SaaS — Project Documentation

**Status:** Architecture proposal / implementation blueprint (not deployed).  
**Language:** Vietnamese.  
**Context:** 10 independent templates built using HTML/CSS/JS, React, Next.js; currently hardcoded; hosting undecided; dynamic multi-tenant rendering chosen.

## Product goal
Marketplace → select template → live demo → create wedding draft → enter content/upload assets → personalized preview → checkout → verified payment → publish wildcard subdomain → manage, update and share; optional RSVP.

## Documentation map
| File | Purpose |
|---|---|
| `01-product/PRD.md` | Scope, personas, acceptance criteria |
| `01-product/USER_FLOWS.md` | Customer, admin and publication flows |
| `02-architecture/SYSTEM_ARCHITECTURE.md` | System design and ADRs |
| `02-architecture/REPOSITORY_STRUCTURE.md` | Monorepo layout and ownership |
| `02-architecture/DOMAIN_ROUTING.md` | Hostname resolution and isolation |
| `03-data/WEDDING_SCHEMA.md` | Canonical data, validation and evolution |
| `03-data/DATABASE.md` | SQLAlchemy models, constraints, Alembic migrations |
| `04-templates/TEMPLATE_SDK.md` | Adapter and manifest contracts |
| `04-templates/MIGRATION_GUIDE.md` | HTML, React, Next migration playbooks |
| `04-templates/TEMPLATE_AUDIT.md` | Inventory worksheet for 10 templates |
| `05-api/API_SPEC.md` | API endpoints and errors |
| `06-workflows/PREVIEW_PUBLISH.md` | Draft, payments, publishing and rollback |
| `07-operations/DEPLOYMENT.md` | Infrastructure, CI/CD and operations |
| `07-operations/SECURITY.md` | Threat model and security checklist |
| `08-delivery/ROADMAP.md` | Milestones, priorities, definition of done |
| `08-delivery/TEST_STRATEGY.md` | Unit, integration, E2E and visual tests |
| `09-examples/` | Illustrative contracts and adapter code |

## Key decisions
1. **One deployed runtime per compatible template group**, never per customer.
2. **Canonical WeddingData**, template-specific adapters and versioned manifests.
3. **Immutable published snapshots**, editable draft isolated from public traffic.
4. **Verified hostname routing** using wildcard DNS and trusted gateway.
5. **Core API modular monolith** (Python FastAPI + SQLAlchemy); separate runtimes only when required.
6. **Initial deployment recommendation:** VPS + Docker Compose, Cloudflare DNS/CDN/R2; reassess after audit.

## Suggested implementation order
Audit templates → canonical schema → migrate one HTML template → draft builder + preview → publish via wildcard domain → payment entitlement → React migration → Next migration → remaining templates → hardening.

## Important caveats
The example code is **reference material**, not a complete runnable application. No source repositories, credentials, template inventory, payment provider or domain have been supplied. Security-critical logic must be implemented and tested before production.
