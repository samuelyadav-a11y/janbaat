"""create ai_clusters

Revision ID: 010
Revises: 009
Create Date: 2026-06-08
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "010"
down_revision = "009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ai_clusters",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("district_id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(30), nullable=True),
        sa.Column("topic", sa.String(200), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("post_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("agree_percentage", sa.Numeric(5, 2), nullable=True),
        sa.Column("sentiment_score", sa.Numeric(3, 2), nullable=True),
        sa.Column("is_highlighted", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["district_id"], ["districts.id"]),
    )
    op.create_index(
        "idx_clusters_district", "ai_clusters",
        ["district_id", sa.text("post_count DESC")]
    )
    op.create_index(
        "idx_clusters_highlighted", "ai_clusters",
        ["district_id"],
        postgresql_where=sa.text("is_highlighted = true")
    )


def downgrade() -> None:
    op.drop_table("ai_clusters")
