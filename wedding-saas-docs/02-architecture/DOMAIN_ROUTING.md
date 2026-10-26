# Subdomain Routing and Tenant Isolation

## URL plan
- `www.example.com`: marketing and marketplace.
- `app.example.com`: authenticated builder/dashboard.
- `api.example.com`: public/customer API.
- `*.invite.example.com`: customer weddings (recommended separate wildcard zone).
- `assets.example.com`: static/versioned template assets and approved media.

## DNS and TLS
Wildcard DNS `*.invite.example.com` points to ingress; issue wildcard TLS certificate with DNS-01 or use supported managed certificate setup. Reserve internal hostnames; block nested/wildcard abuse. Custom domains require proof of ownership, TLS provisioning and verified routing before activation.

## Resolution algorithm
1. Read Host from trusted ingress, strip port and terminal dot, lowercase, validate IDNA/ASCII hostname, enforce suffix and length.
2. Reject reserved hostnames and unknown hosts.
3. Lookup `WeddingDomain` with unique normalized hostname; require `ACTIVE` domain and wedding.
4. Load `activePublicationId`, verify snapshot belongs to same wedding.
5. Load pinned template version and dispatch to allowlisted runtime ID.
6. Forward internal headers only over private trusted channel; protect renderer against direct public access.

## Security invariants
- Client cannot control `X-Verified-Host`, `X-Wedding-Id` or `X-Template-Runtime`.
- Never proxy to an arbitrary URL stored in database (SSRF risk).
- Cache key includes normalized verified hostname + pathname + publication ID, and guest-specific responses are private/no-store.
- DB uniqueness and transaction prevent slug race; reserve `www`, `api`, `admin`, `app`, `assets`, `support`.
- For preview, use separate authenticated route and expiring scoped token; never serve draft from public wildcard route.

## Operational behavior
Unknown hostname: 404. Suspended wedding: 410 or branded unavailable page. Renderer failure: 503 with no cross-tenant fallback. Re-publication changes active pointer atomically; invalidate relevant HTML cache after commit.
