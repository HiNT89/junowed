import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def uuid_pk() -> Mapped[str]:
    return mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = uuid_pk()
    email: Mapped[str] = mapped_column(String(320), unique=True)
    name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Template(Base):
    __tablename__ = "templates"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class TemplateVersion(Base):
    __tablename__ = "template_versions"
    __table_args__ = (UniqueConstraint("template_id", "version"),)
    id: Mapped[str] = uuid_pk()
    template_id: Mapped[str] = mapped_column(ForeignKey("templates.id"), index=True)
    version: Mapped[str] = mapped_column(String(64))
    runtime: Mapped[str] = mapped_column(String(64))
    runtime_id: Mapped[str] = mapped_column(String(128))
    manifest: Mapped[dict] = mapped_column(JSON)
    schema_version: Mapped[str] = mapped_column(String(32), default="1.0.0")


class Wedding(Base):
    __tablename__ = "weddings"
    id: Mapped[str] = uuid_pk()
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    template_version_id: Mapped[str] = mapped_column(ForeignKey("template_versions.id"))
    slug: Mapped[str] = mapped_column(String(120), unique=True)
    status: Mapped[str] = mapped_column(String(32), default="DRAFT")
    current_revision: Mapped[int] = mapped_column(Integer, default=1)
    active_publication_id: Mapped[str | None] = mapped_column(
        ForeignKey("wedding_publications.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class WeddingDraft(Base):
    __tablename__ = "wedding_drafts"
    wedding_id: Mapped[str] = mapped_column(
        ForeignKey("weddings.id", ondelete="CASCADE"), primary_key=True
    )
    config: Mapped[dict] = mapped_column(JSON)
    revision: Mapped[int] = mapped_column(Integer, default=1)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class WeddingPublication(Base):
    __tablename__ = "wedding_publications"
    __table_args__ = (UniqueConstraint("wedding_id", "revision"),)
    id: Mapped[str] = uuid_pk()
    wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id"), index=True)
    revision: Mapped[int] = mapped_column(Integer)
    config: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[str] = uuid_pk()
    wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id"), index=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    storage_key: Mapped[str] = mapped_column(String(500), unique=True)
    media_type: Mapped[str] = mapped_column(String(100))
    size_bytes: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("user_id", "idempotency_key"),)
    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id"), index=True)
    amount: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(3), default="VND")
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    idempotency_key: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (UniqueConstraint("provider", "transaction_id"),)
    id: Mapped[str] = uuid_pk()
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), index=True)
    provider: Mapped[str] = mapped_column(String(64))
    transaction_id: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    amount: Mapped[int] = mapped_column(Integer)
    raw_event: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PaymentWebhookEvent(Base):
    __tablename__ = "payment_webhook_events"
    __table_args__ = (UniqueConstraint("provider", "event_id"),)
    id: Mapped[str] = uuid_pk()
    provider: Mapped[str] = mapped_column(String(64))
    event_id: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Entitlement(Base):
    __tablename__ = "entitlements"
    __table_args__ = (UniqueConstraint("wedding_id", "kind"),)
    id: Mapped[str] = uuid_pk()
    wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id"), index=True)
    kind: Mapped[str] = mapped_column(String(64), default="PUBLISH")
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Guest(Base):
    __tablename__ = "guests"
    id: Mapped[str] = uuid_pk()
    wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    invitation_token: Mapped[str] = mapped_column(String(255), unique=True)


class RSVP(Base):
    __tablename__ = "rsvps"
    id: Mapped[str] = uuid_pk()
    guest_id: Mapped[str] = mapped_column(ForeignKey("guests.id"), index=True)
    attending: Mapped[bool] = mapped_column(Boolean)
    guest_count: Mapped[int] = mapped_column(Integer, default=1)
    message: Mapped[str | None] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
