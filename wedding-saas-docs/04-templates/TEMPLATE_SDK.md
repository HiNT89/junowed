# Template SDK Contract

## Manifest
```json
{
  "id": "react-romantic",
  "version": "1.0.0",
  "name": "Romantic",
  "framework": "react",
  "runtime": "react-ssr",
  "runtimeId": "static-runtime-v1",
  "schemaVersion": "1.0.0",
  "capabilities": ["hero","gallery","countdown","music"],
  "assetBase": "/assets/react-romantic/1.0.0/"
}
```

## TypeScript contract
```ts
export type RenderMode = 'preview' | 'published';
export interface TemplateContext {
  weddingId: string;
  publicationId?: string;
  mode: RenderMode;
}
export interface TemplateAdapter<TConfig> {
  id: string;
  version: string;
  validate(input: unknown): WeddingData;
  transform(data: WeddingData, context: TemplateContext): TConfig;
}
```

## Responsibilities
Adapter: deterministic data transformation, localization, defaults and supported fields. Renderer: HTML/React/Next presentation. Registry: approved mapping of `(id, version)` to adapter and deployed runtime. Backend: security, payments, ownership and publication.

## Rules
- Never evaluate customer JavaScript or arbitrary templates from DB.
- Template manifest is deployed/approved by admin; runtime ID is allowlisted.
- Pin template versions; preserve old assets for active weddings.
- Preview and publication use identical renderer and version, different authorized data sources.
- Do not perform DB access in adapters; provide data through context/services.

## SDK testing
Contract test each adapter with canonical fixture; screenshot tests at 375px and 1440px; verify optional fields, broken images, locale/timezone, animations, SEO and keyboard accessibility.
