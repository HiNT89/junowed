"""Illustrative SQLAlchemy 2.0 mappings; create production changes with Alembic."""
from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, JSON, String, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def uuid_pk() -> Mapped[str]:
    return mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))


class WeddingStatus(str, enum.Enum): DRAFT = "DRAFT"; ACTIVE = "ACTIVE"; SUSPENDED = "SUSPENDED"; ARCHIVED = "ARCHIVED"
class OrderStatus(str, enum.Enum): PENDING = "PENDING"; PAID = "PAID"; CANCELLED = "CANCELLED"; REFUNDED = "REFUNDED"
class PaymentStatus(str, enum.Enum): PENDING = "PENDING"; SUCCEEDED = "SUCCEEDED"; FAILED = "FAILED"; REFUNDED = "REFUNDED"
class DomainStatus(str, enum.Enum): PENDING = "PENDING"; ACTIVE = "ACTIVE"; DISABLED = "DISABLED"


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = uuid_pk(); email: Mapped[str] = mapped_column(String(320), unique=True); name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Template(Base):
    __tablename__ = "templates"
    id: Mapped[str] = mapped_column(String(100), primary_key=True); name: Mapped[str] = mapped_column(String(255)); slug: Mapped[str] = mapped_column(String(120), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class TemplateVersion(Base):
    __tablename__ = "template_versions"; __table_args__ = (UniqueConstraint("template_id", "version"),)
    id: Mapped[str] = uuid_pk(); template_id: Mapped[str] = mapped_column(ForeignKey("templates.id")); version: Mapped[str] = mapped_column(String(64))
    runtime: Mapped[str] = mapped_column(String(64)); runtime_id: Mapped[str] = mapped_column(String(128)); manifest: Mapped[dict] = mapped_column(JSON); schema_: Mapped[dict] = mapped_column("schema", JSON)


class Wedding(Base):
    __tablename__ = "weddings"
    id: Mapped[str] = uuid_pk(); owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True); template_version_id: Mapped[str] = mapped_column(ForeignKey("template_versions.id"))
    slug: Mapped[str] = mapped_column(String(120), unique=True); status: Mapped[WeddingStatus] = mapped_column(Enum(WeddingStatus), default=WeddingStatus.DRAFT)
    current_revision: Mapped[int] = mapped_column(Integer, default=0); created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WeddingDraft(Base):
    __tablename__ = "wedding_drafts"
    wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id", ondelete="CASCADE"), primary_key=True); config: Mapped[dict] = mapped_column(JSON)
    revision: Mapped[int] = mapped_column(Integer, default=1); updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WeddingPublication(Base):
    __tablename__ = "wedding_publications"; __table_args__ = (UniqueConstraint("wedding_id", "revision"),)
    id: Mapped[str] = uuid_pk(); wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id"), index=True); revision: Mapped[int] = mapped_column(Integer); config: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WeddingDomain(Base):
    __tablename__ = "wedding_domains"
    id: Mapped[str] = uuid_pk(); wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id")); hostname: Mapped[str] = mapped_column(String(253), unique=True)
    status: Mapped[DomainStatus] = mapped_column(Enum(DomainStatus), default=DomainStatus.PENDING); is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    active_publication_id: Mapped[str | None] = mapped_column(ForeignKey("wedding_publications.id")); created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[str] = uuid_pk(); user_id: Mapped[str] = mapped_column(ForeignKey("users.id")); wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id"))
    amount: Mapped[int] = mapped_column(Integer); currency: Mapped[str] = mapped_column(String(3), default="VND"); status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Payment(Base):
    __tablename__ = "payments"; __table_args__ = (UniqueConstraint("provider", "transaction_id"),)
    id: Mapped[str] = uuid_pk(); order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), index=True); provider: Mapped[str] = mapped_column(String(64)); transaction_id: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING); amount: Mapped[int] = mapped_column(Integer); raw_event: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Guest(Base):
    __tablename__ = "guests"
    id: Mapped[str] = uuid_pk(); wedding_id: Mapped[str] = mapped_column(ForeignKey("weddings.id"), index=True); name: Mapped[str] = mapped_column(String(255)); invitation_token: Mapped[str] = mapped_column(String(255), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RSVP(Base):
    __tablename__ = "rsvps"
    id: Mapped[str] = uuid_pk(); guest_id: Mapped[str] = mapped_column(ForeignKey("guests.id")); attending: Mapped[bool] = mapped_column(Boolean); guest_count: Mapped[int] = mapped_column(Integer, default=1)
    message: Mapped[str | None] = mapped_column(String); created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
