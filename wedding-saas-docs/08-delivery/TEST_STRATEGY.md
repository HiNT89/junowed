# Test Strategy

## Unit
Pydantic validation; adapter transforms; timezone formatting; slug normalization; reserved hosts; authorization policy; pricing rules.

## Integration
FastAPI service/SQLAlchemy transactions, revision conflict, unique domain constraint, publication ownership, payment webhook dedupe, asset ownership, outbox retry. Run against PostgreSQL (not SQLite) using pytest and an isolated database per test run.

## End-to-end
1. Browse gallery → select → create draft → upload → preview.
2. Pay in sandbox → webhook verified → entitlement → publish → public URL.
3. Edit draft after publish → public stays unchanged → republish → updated content.
4. Unknown/disabled hostname returns safe error.
5. User A cannot access/edit User B wedding.
6. Duplicate webhook/publish requests do not duplicate charge/activation.
7. Rollback restores prior publication.

## Visual regression
Playwright screenshots at 375×812 and 1440×900 for each template and realistic fixtures. Verify font loading, image cropping, motion, countdown, CTA and RSVP. Freeze clock and disable animation for stable screenshots.

## Load
Simulate concurrent guests, bursts from QR shares, high cache miss rates and image downloads. Measure p95 origin latency, DB connections, Redis hit rate and SSR CPU.

## Security
Host header spoofing, XSS, URL injection, cross-tenant cache contamination, webhook replay, SSRF, oversized uploads and preview token expiration.

## Release gate
No critical vulnerabilities, green tests, backup restore verified, rollback documented, template screenshot approval, production secrets reviewed.
