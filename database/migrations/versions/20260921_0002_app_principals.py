"""Create the minimal Vittavaan application principal projection.

Revision ID: 20260921_0002
Revises: 20260920_0001
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260921_0002"
down_revision: str | None = "20260920_0001"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    """Create the auth-core-subject to local-principal mapping."""

    op.create_table(
        "app_principals",
        sa.Column(
            "principal_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("auth_subject_id", sa.Text(), nullable=False),
        sa.Column("principal_type", sa.Text(), nullable=False, server_default="PERSON"),
        sa.Column("status", sa.Text(), nullable=False, server_default="ACTIVE"),
        sa.Column(
            "first_seen_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "last_seen_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("version", sa.BigInteger(), nullable=False, server_default="1"),
        sa.CheckConstraint(
            "principal_type IN ('PERSON', 'SERVICE', 'SUPPORT')",
            name="ck_app_principals_type",
        ),
        sa.CheckConstraint(
            "status IN ('ACTIVE', 'SUSPENDED', 'CLOSED')",
            name="ck_app_principals_status",
        ),
        sa.CheckConstraint("version >= 1", name="ck_app_principals_version"),
        sa.CheckConstraint(
            "length(btrim(auth_subject_id)) BETWEEN 1 AND 255",
            name="ck_app_principals_auth_subject_length",
        ),
        sa.CheckConstraint(
            "last_seen_at >= first_seen_at",
            name="ck_app_principals_seen_order",
        ),
        sa.PrimaryKeyConstraint("principal_id", name="pk_app_principals"),
        sa.UniqueConstraint("auth_subject_id", name="uq_app_principals_auth_subject"),
    )


def downgrade() -> None:
    """Remove only the S2 local-principal projection."""

    op.drop_table("app_principals")
