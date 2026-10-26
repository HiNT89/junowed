import base64
import hashlib
import hmac
import json
import time

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import current_user_id
from app.core.config import get_settings
from app.core.errors import APIError
from app.db.models import Entitlement, Wedding, WeddingDraft, WeddingPublication
from app.db.session import get_db
from app.modules.weddings.schemas import validate_config

router = APIRouter(tags=["publications"])


def owned_wedding(db: Session, wedding_id: str, user_id: str) -> Wedding:
    wedding = db.scalar(
        select(Wedding).where(Wedding.id == wedding_id, Wedding.owner_id == user_id)
    )
    if not wedding:
        raise APIError(404, "NOT_FOUND", "Wedding not found")
    return wedding


def preview_token(wedding_id: str, owner_id: str) -> str:
    payload = {
        "weddingId": wedding_id,
        "ownerId": owner_id,
        "exp": int(time.time()) + get_settings().preview_token_ttl_seconds,
    }
    encoded = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).rstrip(
        b"="
    )
    signature = hmac.new(
        get_settings().preview_token_secret.encode(), encoded, hashlib.sha256
    ).digest()
    return f"{encoded.decode()}.{base64.urlsafe_b64encode(signature).decode().rstrip('=')}"


class RollbackRequest(BaseModel):
    revision: int = Field(ge=1)


@router.post("/weddings/{wedding_id}/preview-sessions", status_code=201)
def create_preview_session(
    wedding_id: str, user_id: str = Depends(current_user_id), db: Session = Depends(get_db)
) -> dict:
    owned_wedding(db, wedding_id, user_id)
    return {
        "token": preview_token(wedding_id, user_id),
        "expiresIn": get_settings().preview_token_ttl_seconds,
    }


@router.post("/weddings/{wedding_id}/publish")
def publish(
    wedding_id: str,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    user_id: str = Depends(current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    if not idempotency_key:
        raise APIError(422, "INVALID_CONFIG", "Idempotency-Key is required")
    wedding = owned_wedding(db, wedding_id, user_id)
    entitlement = db.scalar(
        select(Entitlement).where(
            Entitlement.wedding_id == wedding.id,
            Entitlement.kind == "PUBLISH",
            Entitlement.active.is_(True),
        )
    )
    if not entitlement:
        raise APIError(402, "PAYMENT_REQUIRED", "An active publishing entitlement is required")
    draft = db.get(WeddingDraft, wedding.id)
    try:
        validate_config(draft.config)
    except ValueError as exc:
        raise APIError(422, "INVALID_CONFIG", str(exc)) from exc
    existing = db.scalar(
        select(WeddingPublication).where(
            WeddingPublication.wedding_id == wedding.id,
            WeddingPublication.revision == draft.revision,
        )
    )
    if not existing:
        existing = WeddingPublication(
            wedding_id=wedding.id, revision=draft.revision, config=draft.config
        )
        db.add(existing)
        db.flush()
        wedding.status = "ACTIVE"
        wedding.active_publication_id = existing.id
        db.commit()
    return {
        "publicationId": existing.id,
        "weddingId": wedding.id,
        "revision": existing.revision,
        "status": "ACTIVE",
    }


@router.get("/weddings/{wedding_id}/publications")
def list_publications(
    wedding_id: str, user_id: str = Depends(current_user_id), db: Session = Depends(get_db)
) -> list[dict]:
    owned_wedding(db, wedding_id, user_id)
    rows = db.scalars(
        select(WeddingPublication)
        .where(WeddingPublication.wedding_id == wedding_id)
        .order_by(WeddingPublication.revision.desc())
    ).all()
    return [
        {"id": item.id, "revision": item.revision, "createdAt": item.created_at} for item in rows
    ]


@router.post("/weddings/{wedding_id}/rollback")
def rollback(
    wedding_id: str,
    payload: RollbackRequest,
    user_id: str = Depends(current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    wedding = owned_wedding(db, wedding_id, user_id)
    publication = db.scalar(
        select(WeddingPublication).where(
            WeddingPublication.wedding_id == wedding.id,
            WeddingPublication.revision == payload.revision,
        )
    )
    if not publication:
        raise APIError(404, "NOT_FOUND", "Publication not found")
    wedding.status = "ACTIVE"
    wedding.active_publication_id = publication.id
    db.commit()
    return {"weddingId": wedding.id, "revision": publication.revision, "status": "ACTIVE"}
