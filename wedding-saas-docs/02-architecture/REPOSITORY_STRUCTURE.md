# Repository Structure

```text
wedding-platform/
  apps/
    web/                     # Next.js marketplace/editor/dashboard
    api/                     # Python FastAPI modular monolith
      app/
        api/v1/              # routers and Pydantic request/response schemas
        modules/{auth,templates,weddings,assets,orders,payments,domains,publications,rsvp}/
        db/                  # SQLAlchemy models, sessions and repositories
        core/                # settings, auth, logging and error handling
      alembic/               # PostgreSQL migrations
      tests/
      pyproject.toml
    gateway/                 # trusted host resolution / reverse routing
    static-runtime/          # HTML + compatible React template rendering
    next-runtime/            # compatible converted Next templates
    worker/                  # Celery tasks / outbox processor (may live in api/app/worker)
  packages/
    wedding-schema/          # TypeScript canonical contracts for web/template adapters
    template-sdk/            # manifest/adapter interfaces
    template-registry/       # allowlisted templates and versions
    database/                # shared SQL fixtures / migration documentation
    ui/                      # reusable admin/editor components
    config/                  # eslint/tsconfig/build config
  templates/
    html-classic/
    react-romantic/
    next-elegant/
    ...                      # migrate after inventory
  infra/
    docker/
    compose.yaml
    Caddyfile
  docs/                      # copy this documentation directory
  pnpm-workspace.yaml        # web, template SDK and JavaScript runtimes
  turbo.json
```

## Migration strategy
Keep existing 10 repositories intact during audit. Import compatible ones as workspace packages one at a time. For Next apps requiring custom routing/middleware, deploy as isolated runtime with stable internal service ID. Do not allow DB values to become arbitrary import paths or network destinations.

## Suggested package ownership
`wedding-schema` contains the browser/template business contract only; FastAPI Pydantic models define HTTP input/output and translate into the same canonical data shape. `template-sdk` defines adapters and manifests; `template-registry` maps approved IDs to compiled bundles or internal service names; `api/alembic` owns migrations; `api` owns authorization and transactions; renderers own presentation only.

## CI rules
Affected package lint/typecheck/unit tests; schema contract tests; template screenshots; integration migrations on disposable database; image build with digest; staging smoke tests; production release with rollback plan.
