"""add publication, asset, commerce, and rsvp tables

Revision ID: 0002_commerce_publication
Revises: 0001_initial
"""

import sqlalchemy as sa

from alembic import op

revision = "0002_commerce_publication"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "wedding_publications",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("wedding_id", sa.String(36), sa.ForeignKey("weddings.id"), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("wedding_id", "revision"),
    )
    op.create_index("ix_wedding_publications_wedding_id", "wedding_publications", ["wedding_id"])
    op.add_column("weddings", sa.Column("active_publication_id", sa.String(36), nullable=True))
    op.create_table(
        "assets",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("wedding_id", sa.String(36), sa.ForeignKey("weddings.id"), nullable=False),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("storage_key", sa.String(500), nullable=False, unique=True),
        sa.Column("media_type", sa.String(100), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="PENDING"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_assets_wedding_id", "assets", ["wedding_id"])
    op.create_index("ix_assets_owner_id", "assets", ["owner_id"])
    op.create_table(
        "orders",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("wedding_id", sa.String(36), sa.ForeignKey("weddings.id"), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="PENDING"),
        sa.Column("idempotency_key", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "idempotency_key"),
    )
    op.create_index("ix_orders_user_id", "orders", ["user_id"])
    op.create_index("ix_orders_wedding_id", "orders", ["wedding_id"])
    op.create_table(
        "payments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("order_id", sa.String(36), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("provider", sa.String(64), nullable=False),
        sa.Column("transaction_id", sa.String(255)),
        sa.Column("status", sa.String(32), nullable=False, server_default="PENDING"),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("raw_event", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("provider", "transaction_id"),
    )
    op.create_index("ix_payments_order_id", "payments", ["order_id"])
    op.create_table(
        "payment_webhook_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("provider", sa.String(64), nullable=False),
        sa.Column("event_id", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("provider", "event_id"),
    )
    op.create_table(
        "entitlements",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("wedding_id", sa.String(36), sa.ForeignKey("weddings.id"), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("wedding_id", "kind"),
    )
    op.create_index("ix_entitlements_wedding_id", "entitlements", ["wedding_id"])
    op.create_table(
        "guests",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("wedding_id", sa.String(36), sa.ForeignKey("weddings.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("invitation_token", sa.String(255), nullable=False, unique=True),
    )
    op.create_index("ix_guests_wedding_id", "guests", ["wedding_id"])
    op.create_table(
        "rsvps",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("guest_id", sa.String(36), sa.ForeignKey("guests.id"), nullable=False),
        sa.Column("attending", sa.Boolean(), nullable=False),
        sa.Column("guest_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("message", sa.String(1000)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_rsvps_guest_id", "rsvps", ["guest_id"])


def downgrade() -> None:
    for table in (
        "rsvps",
        "guests",
        "entitlements",
        "payment_webhook_events",
        "payments",
        "orders",
        "assets",
        "wedding_publications",
    ):
        op.drop_table(table)
