"""create votes

Revision ID: 006
Revises: 005
Create Date: 2026-06-08
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("post_id", UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), nullable=False),
        sa.Column("vote_type", sa.String(10), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("post_id", "user_id", name="uq_votes_post_user"),
        sa.CheckConstraint("vote_type IN ('agree', 'disagree', 'metoo')", name="ck_votes_type"),
    )
    op.create_index("idx_votes_post", "votes", ["post_id"])
    op.create_index("idx_votes_user", "votes", ["user_id"])


def downgrade() -> None:
    op.drop_table("votes")
