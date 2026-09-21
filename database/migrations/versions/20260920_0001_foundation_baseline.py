"""Establish an empty, verifiable migration baseline.

Revision ID: 20260920_0001
Revises: none
"""

revision: str = "20260920_0001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    """Record the migration head without creating business tables."""


def downgrade() -> None:
    """Remove only the empty foundation revision marker."""
