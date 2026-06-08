"""create profiles

Revision ID: 002
Revises: 001
Create Date: 2026-06-08
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("phone", sa.String(15), nullable=True),
        sa.Column("name", sa.String(100), nullable=True),
        sa.Column("avatar_url", sa.Text(), nullable=True),
        sa.Column("state_id", sa.Integer(), nullable=True),
        sa.Column("district_id", sa.Integer(), nullable=True),
        sa.Column("city_id", sa.Integer(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("device_fingerprint", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone", name="uq_profiles_phone"),
        sa.ForeignKeyConstraint(["state_id"], ["states.id"]),
        sa.ForeignKeyConstraint(["district_id"], ["districts.id"]),
        sa.ForeignKeyConstraint(["city_id"], ["cities.id"]),
    )
    op.create_index("idx_profiles_district", "profiles", ["district_id"])

    # Supabase DB trigger: auto-create profile row when user signs up via Auth
    # Run this in Supabase SQL editor (requires auth schema access):
    # CREATE OR REPLACE FUNCTION public.handle_new_user()
    # RETURNS trigger AS $$
    # BEGIN
    #   INSERT INTO public.profiles (id, phone)
    #   VALUES (new.id, new.phone);
    #   RETURN new;
    # END;
    # $$ LANGUAGE plpgsql SECURITY DEFINER;
    #
    # CREATE TRIGGER on_auth_user_created
    #   AFTER INSERT ON auth.users
    #   FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();


def downgrade() -> None:
    op.drop_table("profiles")
