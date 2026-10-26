from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Template, TemplateVersion
from app.db.session import get_db

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("")
def list_templates(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.execute(
        select(Template, TemplateVersion)
        .join(TemplateVersion, Template.id == TemplateVersion.template_id)
        .where(Template.active.is_(True))
        .order_by(Template.name)
    ).all()
    return [
        {
            "id": template.id,
            "name": template.name,
            "slug": template.slug,
            "version": version.version,
            "manifest": version.manifest,
        }
        for template, version in rows
    ]


@router.get("/{template_id}")
def get_template(template_id: str, db: Session = Depends(get_db)) -> dict:
    row = db.execute(
        select(Template, TemplateVersion)
        .join(TemplateVersion, Template.id == TemplateVersion.template_id)
        .where(Template.id == template_id, Template.active.is_(True))
    ).first()
    if not row:
        from app.core.errors import APIError

        raise APIError(404, "NOT_FOUND", "Template not found")
    template, version = row
    return {
        "id": template.id,
        "name": template.name,
        "slug": template.slug,
        "version": version.version,
        "manifest": version.manifest,
        "schemaVersion": version.schema_version,
    }
