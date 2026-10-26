# Product Requirements Document

## Vision
Self-service Vietnamese wedding invitation website platform with reusable template designs, editing, checkout, and hosted subdomains.

## Roles
- Visitor: browse/search/filter, preview demos, create account.
- Customer: create draft, upload, preview, pay, publish, update, manage guest responses.
- Admin: curate templates/versions, manage orders, moderate assets, investigate incidents.
- Guest: view published invitation, RSVP if enabled.

## MVP scope (P0)
1. Template gallery with category, thumbnail, demo and mobile view.
2. Registration/login and wedding ownership.
3. Schema-driven builder: names, dates, venues, map, gallery, music, theme supported by chosen template.
4. Draft autosave and private preview with actual customer data.
5. Upload images/audio with quotas and validated file types.
6. Order, payment webhook verification and paid entitlement.
7. Publish/republish at unique wildcard subdomain; shareable link/QR.
8. Customer dashboard and admin template management.

## Next phase (P1)
RSVP, personalized guest tokens, analytics, custom domains, billing lifecycle, section reordering, advanced theme controls.

## Out of scope for MVP
Freeform drag/drop canvas, customer-supplied scripts, per-customer deployments, third-party template execution without review.

## Functional acceptance criteria
- Gallery only shows active templates and valid versioned demo links.
- Customer can preview before purchase; preview never publicly indexes or exposes private drafts.
- Same renderer powers preview and published website (different data source).
- Payment provider event is verified, idempotent, reconciled to correct order/amount/currency.
- Publication requires owner authorization, validated draft, available domain and active entitlement.
- After publication, updating draft does not alter public website until explicit republish.
- Unknown/suspended hostname returns controlled 404/410, never another tenant's content.
- Every wedding has a stable URL and share metadata (title, OG image, description).

## Non-functional targets (initial, to validate)
- Availability target: 99.9% monthly after launch.
- p95 public HTML response target: < 800ms at origin under representative load (excluding media).
- Responsive on common mobile widths; accessible form labels and keyboard navigation.
- Document RPO/RTO targets before production; run backup restoration exercises.

## Business rules to decide
Template pricing and license duration; number of weddings per purchase; post-purchase editing rights; domain retention after expiration; cancellation/refund policy; guest data retention; support SLA.
