# Preview, Payment and Publication Workflow

## Draft lifecycle
Create wedding with pinned template version → save draft JSONB with revision → autosave using optimistic concurrency → upload assets via signed URLs → asset validation/processing → preview via scoped token.

## Preview isolation
Preview token is short-lived, audience-bound and wedding-scoped; ideally use a separate preview hostname/path with authenticated session. Response `Cache-Control: private, no-store`, `X-Robots-Tag: noindex`. Do not expose draft through wildcard public route. Renderer receives validated draft via trusted internal endpoint.

## Payment lifecycle
1. API creates order with server-side price and currency.
2. Payment provider creates checkout session/QR.
3. Browser return displays pending/paid based on API state, never assumes success.
4. Provider webhook verified by signature and provider-specific replay protections.
5. Deduplicate provider event ID, validate amount/currency/reference, atomically update order and entitlement.
6. Reconcile ambiguous payments via provider query/job.

## Publish algorithm
1. Authenticate owner and enforce entitlement.
2. Validate schema, template compatibility, media readiness, domain status.
3. Serialize concurrent publish operations (row lock or revision compare-and-swap).
4. Create immutable `WeddingPublication` revision; atomically update active publication pointer and outbox event.
5. Commit, then asynchronously purge CDN/notify/index; retries safe.
6. If renderer preflight fails, do not activate revision.

## Republish and rollback
Customer edits draft without changing active publication. Republish produces new snapshot. Rollback points domain to a previous valid snapshot and retains audit log; never delete history required for live rollback.

## Cache
Versioned asset paths; cache public HTML keyed by verified host + path + publication ID. Avoid public caching of RSVP, preview and guest-personalized pages. TTL alone is not a replacement for revision-aware invalidation.
