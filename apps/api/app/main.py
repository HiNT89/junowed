from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.errors import APIError, api_error_handler, validation_error_handler
from app.db.session import SessionLocal
from app.modules.assets.router import router as assets_router
from app.modules.orders.router import router as orders_router
from app.modules.payments.router import router as payments_router
from app.modules.public.router import router as public_router
from app.modules.publications.router import router as publications_router
from app.modules.templates.router import router as templates_router
from app.modules.weddings.router import router as weddings_router
from app.seed import seed_templates


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Migrations must run before startup. Development data is safe and idempotent.
    with SessionLocal() as db:
        seed_templates(db)
    yield


settings = get_settings()
app = FastAPI(title="Wedding Platform API", version="0.1.0", lifespan=lifespan)
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(templates_router, prefix="/v1")
app.include_router(weddings_router, prefix="/v1")
app.include_router(assets_router, prefix="/v1")
app.include_router(orders_router, prefix="/v1")
app.include_router(payments_router, prefix="/v1")
app.include_router(publications_router, prefix="/v1")
app.include_router(public_router, prefix="/v1")
