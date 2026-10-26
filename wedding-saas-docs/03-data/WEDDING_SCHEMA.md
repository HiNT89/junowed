# Canonical Wedding Data Contract

## Principles
- Common data schema is independent of framework and layout.
- Template manifests declare supported fields and capabilities.
- Adapter maps canonical data to existing template-specific props.
- Use explicit schema version and migrations; validate at draft update and publish.

## Example payload
```json
{
  "schemaVersion": "1.0.0",
  "couple": {"groom": {"name": "Minh"}, "bride": {"name": "Anh"}},
  "events": [{"id":"ceremony", "title":"Lễ cưới", "startsAt":"2027-01-20T11:00:00+07:00", "timezone":"Asia/Ho_Chi_Minh", "venue":"Wedding Palace", "address":"Hà Nội"}],
  "gallery": ["https://assets.example.com/weddings/123/photo-1.webp"],
  "music": {"enabled": false},
  "theme": {"primaryColor":"#B48A78", "fontFamily":"Playfair Display"},
  "sections": {"hero":true,"gallery":true,"countdown":true,"rsvp":false}
}
```

## Validation requirements
- Couple names 1–120 characters, no HTML.
- `startsAt`: ISO 8601 offset-aware string; timezone IANA identifier. Always format with specified timezone.
- Gallery max count and total size by plan; URLs only from approved storage/CDN.
- Theme fonts/colors from template-approved whitelist.
- Maps: validated https URL or normalized location fields; no arbitrary script URLs.
- Sections must be subset of template capabilities.
- Public projection excludes owner email, order/payment data, private guest lists, preview tokens and asset storage credentials.

## Schema evolution
Keep `schemaVersion` with each draft and publication. Define migration functions v1→v2; never silently change published snapshots. Template adapters are pinned to compatible schema versions.

## Draft concurrency
Send `revision` with PATCH; reject stale updates with 409 and current revision to prevent autosave overwriting changes from another tab.
