import re
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CreateWeddingRequest(BaseModel):
    template_version_id: str = Field(min_length=1, alias="templateVersionId")
    slug: str = Field(min_length=3, max_length=120)
    config: dict[str, Any] | None = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str) -> str:
        value = value.lower()
        if not SLUG_PATTERN.fullmatch(value):
            raise ValueError("Slug must use lowercase letters, digits, and hyphens")
        return value


class PatchDraftRequest(BaseModel):
    expected_revision: int = Field(ge=1, alias="expectedRevision")
    config: dict[str, Any]


class DraftResponse(BaseModel):
    revision: int
    updated_at: datetime | None = Field(serialization_alias="updatedAt")


def validate_config(config: dict[str, Any]) -> None:
    if config.get("schemaVersion") != "1.0.0":
        raise ValueError("schemaVersion must be 1.0.0")
    couple = config.get("couple")
    if not isinstance(couple, dict):
        raise ValueError("couple is required")
    for role in ("groom", "bride"):
        person = couple.get(role)
        name = person.get("name") if isinstance(person, dict) else None
        if (
            not isinstance(name, str)
            or not 1 <= len(name.strip()) <= 120
            or "<" in name
            or ">" in name
        ):
            raise ValueError(f"couple.{role}.name must be 1-120 characters without HTML")
    if not isinstance(config.get("events", []), list) or not isinstance(
        config.get("gallery", []), list
    ):
        raise ValueError("events and gallery must be arrays")
    for event in config.get("events", []):
        if not isinstance(event, dict) or not isinstance(event.get("startsAt"), str):
            raise ValueError("every event requires startsAt")
        try:
            if datetime.fromisoformat(event["startsAt"].replace("Z", "+00:00")).tzinfo is None:
                raise ValueError
        except ValueError as exc:
            raise ValueError("event startsAt must be an offset-aware ISO 8601 timestamp") from exc


def default_config() -> dict[str, Any]:
    return {
        "schemaVersion": "1.0.0",
        "couple": {"groom": {"name": ""}, "bride": {"name": ""}},
        "events": [],
        "gallery": [],
        "theme": {},
        "sections": {},
    }
