"""create posts

Revision ID: 003
Revises: 002
Create Date: 2026-06-08
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("post_type", sa.String(10), nullable=False),
        sa.Column("post_format", sa.String(10), server_default="text", nullable=False),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("state_id", sa.Integer(), nullable=True),
        sa.Column("district_id", sa.Integer(), nullable=True),
        sa.Column("city_id", sa.Integer(), nullable=True),
        sa.Column("agree_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("disagree_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("metoo_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("comment_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("sentiment", sa.String(10), server_default="neutral", nullable=False),
        sa.Column("status", sa.String(10), server_default="active", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["state_id"], ["states.id"]),
        sa.ForeignKeyConstraint(["district_id"], ["districts.id"]),
        sa.ForeignKeyConstraint(["city_id"], ["cities.id"]),
        sa.CheckConstraint("char_length(content) <= 500", name="ck_posts_content_len"),
        sa.CheckConstraint("post_type IN ('anonymous', 'public')", name="ck_posts_type"),
        sa.CheckConstraint("post_format IN ('text', 'image', 'poll')", name="ck_posts_format"),
        sa.CheckConstraint("status IN ('active', 'removed', 'flagged')", name="ck_posts_status"),
        sa.CheckConstraint("sentiment IN ('positive', 'negative', 'neutral')", name="ck_posts_sentiment"),
    )

    # Critical performance indexes
    op.create_index(
        "idx_posts_district_time", "posts", ["district_id", sa.text("created_at DESC")],
        postgresql_where=sa.text("status = 'active'")
    )
    op.create_index(
        "idx_posts_city_time", "posts", ["city_id", sa.text("created_at DESC")],
        postgresql_where=sa.text("status = 'active'")
    )
    op.create_index(
        "idx_posts_state_time", "posts", ["state_id", sa.text("created_at DESC")],
        postgresql_where=sa.text("status = 'active'")
    )
    op.create_index(
        "idx_posts_trending", "posts", [sa.text("agree_count DESC"), sa.text("created_at DESC")],
        postgresql_where=sa.text("status = 'active'")
    )
    op.create_index(
        "idx_posts_category", "posts", ["district_id", "category", sa.text("created_at DESC")],
        postgresql_where=sa.text("status = 'active'")
    )

    # Full-text search index (pg_trgm) — Phase 5
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute("CREATE INDEX idx_posts_content_trgm ON posts USING gin (content gin_trgm_ops) WHERE status = 'active'")


def downgrade() -> None:
    op.drop_table("posts")
