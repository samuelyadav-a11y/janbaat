"""create reports

Revision ID: 008
Revises: 007
Create Date: 2026-06-08
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "008"
down_revision = "007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("post_id", UUID(as_uuid=True), nullable=False),
        sa.Column("reporter_id", UUID(as_uuid=True), nullable=False),
        sa.Column("reason", sa.String(50), nullable=False),
        sa.Column("status", sa.String(10), server_default="pending", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("post_id", "reporter_id", name="uq_reports_post_reporter"),
        sa.CheckConstraint("status IN ('pending', 'reviewed', 'dismissed')", name="ck_reports_status"),
    )
    op.create_index("idx_reports_status", "reports", ["status", sa.text("created_at DESC")])


def downgrade() -> None:
    op.drop_table("reports")
