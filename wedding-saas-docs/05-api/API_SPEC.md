# API Contract — v1

Base URL: `https://api.example.com/v1`. Auth: secure session or bearer token; server-side ownership enforcement. All JSON errors use `{ "error": { "code": "...", "message": "...", "requestId": "..." } }`.

The FastAPI application publishes the matching OpenAPI document at `/openapi.json` and interactive documentation at `/docs` outside production public access where appropriate. This file remains the product-level contract; keep Pydantic route models and generated OpenAPI synchronized with it in CI.

| Method | Path | Auth | Behavior |
|---|---|---|---|
| GET | `/templates` | Public | List active templates |
| GET | `/templates/:id` | Public | Manifest, schema, demo URL |
| POST | `/weddings` | Customer | Create draft from approved template version |
| GET | `/weddings/:id` | Owner | Wedding metadata + draft revision |
| PATCH | `/weddings/:id/draft` | Owner | Update validated draft with expected revision |
| POST | `/weddings/:id/preview-sessions` | Owner | Short-lived scoped preview token |
| POST | `/assets/upload-intents` | Owner | Signed upload URL, quota checks |
| POST | `/orders` | Customer | Server-priced order and payment intent |
| GET | `/orders/:id` | Owner | Authoritative payment/order state |
| POST | `/payments/webhooks/:provider` | Provider | Verified webhook, idempotent processing |
| POST | `/weddings/:id/publish` | Owner | Publish after entitlement/validation |
| GET | `/weddings/:id/publications` | Owner | Revision history |
| POST | `/weddings/:id/rollback` | Owner | Activate eligible earlier publication |
| GET | `/public/weddings/:slug` | Public | Sanitized published projection only |
| POST | `/public/rsvp` | Guest | Token validation, spam protection |

## Example draft PATCH
```json
{
  "expectedRevision": 4,
  "config": {"schemaVersion":"1.0.0","couple":{"groom":{"name":"Minh"},"bride":{"name":"Anh"}},"events":[],"gallery":[],"theme":{},"sections":{}}
}
```
Response: `200 {"revision":5,"updatedAt":"..."}`. Conflict: `409 STALE_REVISION`.

## Publish response
`202 Accepted {"jobId":"...","weddingId":"...","status":"PUBLISHING"}` if async, or `200` after atomic activation if synchronous. Pick one semantics in implementation and document it consistently.

## Error codes
`UNAUTHORIZED` 401, `FORBIDDEN` 403, `NOT_FOUND` 404, `STALE_REVISION` 409, `SLUG_TAKEN` 409, `INVALID_CONFIG` 422, `PAYMENT_REQUIRED` 402, `RATE_LIMITED` 429, `RENDER_FAILED` 503.

## Idempotency
Use `Idempotency-Key` for create order and publish requests. Provider event uniqueness for webhooks. Validate amount/currency/order mapping from provider server-to-server; browser redirect is not proof of payment.
