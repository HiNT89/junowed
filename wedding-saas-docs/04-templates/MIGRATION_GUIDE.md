# Migrating Existing Templates

## Common audit
Capture framework/version, build scripts, routes, dependency tree, global CSS, DOM manipulation, hardcoded strings, image/audio paths, animation libraries, SSR reliance, forms, external scripts, license and screenshot baseline.

## HTML/CSS/JS
1. Copy into `templates/html-<slug>` and preserve asset paths.
2. Replace text constants with escaped placeholders (e.g. Handlebars `{{couple.groom.name}}`).
3. Build adapter for dates, images, section flags.
4. Compile template on server using approved source file; never compile customer-supplied HTML.
5. Publish CSS/JS as versioned static assets; validate URL contexts separately.
6. Move RSVP POST to central API; prevent scripts from leaking draft tokens.

```ts
import Handlebars from 'handlebars';
const compiled = Handlebars.compile(approvedHtmlSource);
const html = compiled({ couple: { groom: { name: 'Minh' } } });
```

## ReactJS
1. Replace constants with typed `wedding` props or context.
2. Isolate browser-only libraries into effects/dynamic client components.
3. Use SSR only if compatible; `renderToString` alone is insufficient for interactive hydration.
4. Package versioned JS/CSS; hydrate with safe bootstrap data or fetch public config API.
5. Test CSS isolation in iframe and avoid leaking styles to editor.

```tsx
export function Romantic({ wedding }: { wedding: WeddingData }) {
  return <h1>{wedding.couple.groom.name} &amp; {wedding.couple.bride.name}</h1>;
}
```

## Next.js
1. Determine whether project is pure UI or uses App Router/Pages Router, middleware, API routes, Server Actions, `next/image`, server data or cookies.
2. Pure UI: extract components into shared `next-runtime` and inject validated wedding config.
3. Complex app: keep as isolated versioned Next service, use authenticated internal publication resolver.
4. Route by allowlisted runtime service ID; never import arbitrary Next app source at request time.
5. Ensure static assets and `/_next/*` are routed to correct runtime/version; avoid collisions between independently built Next apps.
6. Test metadata/OG, SSR, caching, redirects, headers and image optimization.

## Completion checklist
No hardcoded couple names/dates/URLs; adapter fixture passes; preview/public render same visual output; no secrets/client leakage; mobile screenshot approved; no cross-tenant state.
