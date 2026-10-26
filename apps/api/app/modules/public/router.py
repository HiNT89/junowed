from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import APIError
from app.db.models import RSVP, Guest, Wedding, WeddingPublication
from app.db.session import get_db

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/weddings/{slug}")
def get_public_wedding(slug: str, db: Session = Depends(get_db)) -> dict:
    wedding = db.scalar(select(Wedding).where(Wedding.slug == slug, Wedding.status == "ACTIVE"))
    if not wedding:
        raise APIError(404, "NOT_FOUND", "Wedding not found")
    publication = db.get(WeddingPublication, wedding.active_publication_id)
    if not publication:
        raise APIError(404, "NOT_FOUND", "Published wedding not found")
    return {"slug": wedding.slug, "revision": publication.revision, "config": publication.config}


class RSVPRequest(BaseModel):
    token: str = Field(min_length=16, max_length=255)
    attending: bool
    guest_count: int = Field(default=1, alias="guestCount", ge=0, le=10)
    message: str | None = Field(default=None, max_length=1000)


@router.post("/rsvp", status_code=201)
def create_rsvp(payload: RSVPRequest, db: Session = Depends(get_db)) -> dict:
    guest = db.scalar(select(Guest).where(Guest.invitation_token == payload.token))
    if not guest:
        raise APIError(404, "NOT_FOUND", "Invitation not found")
    rsvp = RSVP(
        guest_id=guest.id,
        attending=payload.attending,
        guest_count=payload.guest_count,
        message=payload.message,
    )
    db.add(rsvp)
    db.commit()
    return {"id": rsvp.id, "status": "received"}
