# Security and Privacy

## Threat model
Multi-tenant isolation failures, untrusted Host headers, SSRF via runtime routing, template XSS, malicious file uploads, unauthorized draft preview, forged payment callbacks, webhook replay, RSVP spam, guest data leaks and CDN cache poisoning.

## Controls
- Authentication with secure HttpOnly SameSite cookies or short-lived access tokens; CSRF protection when using cookie sessions.
- Owner checks on every wedding/draft/order/asset mutation.
- Trusted ingress removes and replaces all internal identity/host headers; internal runtime unreachable from public network or protected by service authentication.
- Approved template registry only; no arbitrary eval, dynamic remote imports or user-defined scripts.
- Escape HTML text, validate URL protocols/hosts, sanitize rich text, CSP adapted to template requirements.
- Upload with MIME sniffing, extension and size quotas, malware scan where practical; transform images and serve via controlled storage paths.
- No secrets, guest list, provider raw payloads or draft tokens in public JSON.
- Payment webhook signature verification, timestamp/replay checks, idempotency and reconciliation.
- Rate limits for login, preview sessions, upload intents, RSVP and webhook endpoints.
- Cache separation by verified hostname, path, publication and personalization status.
- Audit log for publish, rollback, domain and payment/entitlement changes.

## Privacy
Wedding data may include names, photographs, locations, phone numbers and guest lists. Define consent/notice, retention, deletion/export process and least-privilege admin access. Avoid exposing private guest data to crawlers.

## Security release gates
Cross-tenant authorization tests, forged host header tests, XSS fixtures, signed URL expiration, webhook replay tests, database backup restore and dependency vulnerability scan.
