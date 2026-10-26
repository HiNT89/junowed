from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import current_user_id
from app.core.errors import APIError
from app.db.models import TemplateVersion, User, Wedding, WeddingDraft
from app.db.session import get_db
from app.modules.weddings.schemas import (
    CreateWeddingRequest,
    DraftResponse,
    PatchDraftRequest,
    default_config,
    validate_config,
)

router = APIRouter(prefix="/weddings", tags=["weddings"])


def owned_wedding(db: Session, wedding_id: str, user_id: str) -> Wedding:
    wedding = db.scalar(
        select(Wedding).where(Wedding.id == wedding_id, Wedding.owner_id == user_id)
    )
    if not wedding:
        raise APIError(404, "NOT_FOUND", "Wedding not found")
    return wedding


@router.post("", status_code=201)
def create_wedding(
    payload: CreateWeddingRequest,
    user_id: str = Depends(current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    version = db.get(TemplateVersion, payload.template_version_id)
    if not version:
        raise APIError(422, "INVALID_CONFIG", "Approved template version not found")
    config = payload.config or default_config()
    try:
        validate_config(config)
    except ValueError as exc:
        raise APIError(422, "INVALID_CONFIG", str(exc)) from exc
    # Identity provisioning belongs to the eventual auth module. This keeps local development usable.
    if not db.get(User, user_id):
        db.add(User(id=user_id, email=f"dev-{user_id}@local.invalid", name="Development user"))
        db.flush()
    wedding = Wedding(owner_id=user_id, template_version_id=version.id, slug=payload.slug)
    db.add(wedding)
    db.flush()
    db.add(WeddingDraft(wedding_id=wedding.id, config=config, revision=1))
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise APIError(409, "SLUG_TAKEN", "This wedding slug is already in use") from exc
    return {"id": wedding.id, "slug": wedding.slug, "revision": 1, "status": wedding.status}


@router.get("/{wedding_id}")
def get_wedding(
    wedding_id: str, user_id: str = Depends(current_user_id), db: Session = Depends(get_db)
) -> dict:
    wedding = owned_wedding(db, wedding_id, user_id)
    draft = db.get(WeddingDraft, wedding.id)
    return {
        "id": wedding.id,
        "slug": wedding.slug,
        "status": wedding.status,
        "templateVersionId": wedding.template_version_id,
        "draft": {"revision": draft.revision, "config": draft.config},
    }


@router.patch("/{wedding_id}/draft", response_model=DraftResponse)
def patch_draft(
    wedding_id: str,
    payload: PatchDraftRequest,
    user_id: str = Depends(current_user_id),
    db: Session = Depends(get_db),
) -> DraftResponse:
    wedding = owned_wedding(db, wedding_id, user_id)
    try:
        validate_config(payload.config)
    except ValueError as exc:
        raise APIError(422, "INVALID_CONFIG", str(exc)) from exc
    now = datetime.now(timezone.utc)
    result = db.execute(
        update(WeddingDraft)
        .where(
            WeddingDraft.wedding_id == wedding.id,
            WeddingDraft.revision == payload.expected_revision,
        )
        .values(config=payload.config, revision=WeddingDraft.revision + 1, updated_at=now)
    )
    if result.rowcount != 1:
        db.rollback()
        current = db.get(WeddingDraft, wedding.id)
        raise APIError(
            409,
            "STALE_REVISION",
            "Draft has been updated by another request",
            {"revision": current.revision},
        )
    wedding.current_revision = payload.expected_revision + 1
    db.commit()
    return DraftResponse(revision=payload.expected_revision + 1, updated_at=now)
