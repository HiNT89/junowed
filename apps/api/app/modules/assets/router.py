import hashlib
import hmac
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, Header, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.auth import current_user_id
from app.core.config import get_settings
from app.core.errors import APIError
from app.db.models import Asset, Wedding
from app.db.session import get_db

router = APIRouter(prefix="/assets", tags=["assets"])
ALLOWED_MEDIA_TYPES = {"image/jpeg", "image/png", "image/webp", "audio/mpeg"}
MAX_UPLOAD_BYTES = 15 * 1024 * 1024


def upload_token(asset_id: str) -> str:
    return hmac.new(
        get_settings().preview_token_secret.encode(), asset_id.encode(), hashlib.sha256
    ).hexdigest()


class UploadIntentRequest(BaseModel):
    wedding_id: str = Field(alias="weddingId")
    filename: str = Field(min_length=1, max_length=255)
    content_type: str = Field(alias="contentType")
    size_bytes: int = Field(alias="sizeBytes", gt=0, le=MAX_UPLOAD_BYTES)


@router.post("/upload-intents", status_code=201)
def create_upload_intent(
    payload: UploadIntentRequest,
    user_id: str = Depends(current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    wedding = db.get(Wedding, payload.wedding_id)
    if not wedding or wedding.owner_id != user_id:
        raise APIError(404, "NOT_FOUND", "Wedding not found")
    if payload.content_type not in ALLOWED_MEDIA_TYPES:
        raise APIError(422, "INVALID_CONFIG", "Unsupported file type")
    asset = Asset(
        wedding_id=wedding.id,
        owner_id=user_id,
        storage_key=f"weddings/{wedding.id}/{uuid4()}",
        media_type=payload.content_type,
        size_bytes=payload.size_bytes,
    )
    db.add(asset)
    db.commit()
    token = upload_token(asset.id)
    # Local development adapter. Production replaces this URL with S3/R2 signed PUT URL.
    return {
        "assetId": asset.id,
        "storageKey": asset.storage_key,
        "status": asset.status,
        "upload": {
            "method": "PUT",
            "contentType": asset.media_type,
            "url": f"/v1/assets/uploads/{asset.id}?token={token}",
        },
    }


@router.put("/uploads/{asset_id}", status_code=204)
async def upload_local_asset(
    asset_id: str,
    request: Request,
    token: str,
    content_type: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> None:
    """Development-only signed-upload adapter with strict size/type verification."""
    if not hmac.compare_digest(token, upload_token(asset_id)):
        raise APIError(401, "UNAUTHORIZED", "Invalid upload token")
    asset = db.get(Asset, asset_id)
    if not asset or asset.status != "PENDING":
        raise APIError(404, "NOT_FOUND", "Upload intent not found")
    if content_type != asset.media_type:
        raise APIError(422, "INVALID_CONFIG", "Upload media type does not match intent")
    content = await request.body()
    if len(content) != asset.size_bytes:
        raise APIError(422, "INVALID_CONFIG", "Upload size does not match intent")
    destination = Path(get_settings().asset_storage_dir) / asset.storage_key
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    asset.status = "READY"
    db.commit()
