from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Template, TemplateVersion

ROMANTIC_MANIFEST = {
    "id": "react-romantic",
    "version": "1.0.0",
    "name": "Romantic Wedding",
    "framework": "react",
    "runtime": "react-ssr",
    "runtimeId": "static-runtime-v1",
    "schemaVersion": "1.0.0",
    "capabilities": ["hero", "gallery", "countdown", "music"],
    "assetBase": "/assets/react-romantic/1.0.0/",
}


def seed_templates(db: Session) -> None:
    if db.scalar(select(TemplateVersion.id).limit(1)):
        return
    template = Template(id="react-romantic", name="Romantic Wedding", slug="romantic-wedding")
    db.add(template)
    db.add(
        TemplateVersion(
            template_id=template.id,
            version="1.0.0",
            runtime="react-ssr",
            runtime_id="static-runtime-v1",
            manifest=ROMANTIC_MANIFEST,
        )
    )
    db.commit()
