"""initial foundation tables

Revision ID: 0001_initial
Revises:
"""

import sqlalchemy as sa

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False, unique=True),
        sa.Column("name", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "templates",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "template_versions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("template_id", sa.String(100), sa.ForeignKey("templates.id"), nullable=False),
        sa.Column("version", sa.String(64), nullable=False),
        sa.Column("runtime", sa.String(64), nullable=False),
        sa.Column("runtime_id", sa.String(128), nullable=False),
        sa.Column("manifest", sa.JSON(), nullable=False),
        sa.Column("schema_version", sa.String(32), nullable=False, server_default="1.0.0"),
        sa.UniqueConstraint("template_id", "version"),
    )
    op.create_index("ix_template_versions_template_id", "template_versions", ["template_id"])
    op.create_table(
        "weddings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "template_version_id",
            sa.String(36),
            sa.ForeignKey("template_versions.id"),
            nullable=False,
        ),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="DRAFT"),
        sa.Column("current_revision", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_weddings_owner_id", "weddings", ["owner_id"])
    op.create_table(
        "wedding_drafts",
        sa.Column(
            "wedding_id",
            sa.String(36),
            sa.ForeignKey("weddings.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("config", sa.JSON(), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("wedding_drafts")
    op.drop_index("ix_weddings_owner_id", table_name="weddings")
    op.drop_table("weddings")
    op.drop_index("ix_template_versions_template_id", table_name="template_versions")
    op.drop_table("template_versions")
    op.drop_table("templates")
    op.drop_table("users")
