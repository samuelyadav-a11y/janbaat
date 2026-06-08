"""create post_authors (anonymous privacy)

Revision ID: 004
Revises: 003
Create Date: 2026-06-08
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "post_authors",
        sa.Column("post_id", UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("post_id"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        # user_id references auth.users(id) — enforced via RLS, not FK (cross-schema)
    )
    op.create_index("idx_post_authors_user", "post_authors", ["user_id"])


def downgrade() -> None:
    op.drop_table("post_authors")
