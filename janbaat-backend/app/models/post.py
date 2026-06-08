import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint, DateTime, Integer, SmallInteger,
    String, Text, func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.vote import Vote
    from app.models.comment import Comment
    from app.models.report import Report


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        CheckConstraint("char_length(content) <= 500", name="ck_posts_content_len"),
        CheckConstraint("post_type IN ('anonymous', 'public')", name="ck_posts_type"),
        CheckConstraint("post_format IN ('text', 'image', 'poll')", name="ck_posts_format"),
        CheckConstraint("status IN ('active', 'removed', 'flagged')", name="ck_posts_status"),
        CheckConstraint("sentiment IN ('positive', 'negative', 'neutral')", name="ck_posts_sentiment"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    post_type: Mapped[str] = mapped_column(String(10), nullable=False)
    post_format: Mapped[str] = mapped_column(String(10), nullable=False, default="text")
    category: Mapped[str] = mapped_column(String(30), nullable=False)

    state_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    district_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    city_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    agree_count: Mapped[int] = mapped_column(Integer, default=0)
    disagree_count: Mapped[int] = mapped_column(Integer, default=0)
    metoo_count: Mapped[int] = mapped_column(Integer, default=0)
    comment_count: Mapped[int] = mapped_column(Integer, default=0)

    sentiment: Mapped[str] = mapped_column(String(10), default="neutral")
    status: Mapped[str] = mapped_column(String(10), default="active")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    author: Mapped["PostAuthor | None"] = relationship(back_populates="post", uselist=False)
    poll_options: Mapped[list["PollOption"]] = relationship(
        back_populates="post", cascade="all, delete-orphan", order_by="PollOption.order_index"
    )
    votes: Mapped[list["Vote"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    reports: Mapped[list["Report"]] = relationship(back_populates="post", cascade="all, delete-orphan")


class PostAuthor(Base):
    """Moderation-only mapping of post → user. RLS: service_role SELECT only."""
    __tablename__ = "post_authors"

    post_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="author")


class PollOption(Base):
    __tablename__ = "poll_options"
    __table_args__ = (
        CheckConstraint("order_index BETWEEN 0 AND 9", name="ck_poll_options_order"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    option_text: Mapped[str] = mapped_column(String(200), nullable=False)
    vote_count: Mapped[int] = mapped_column(Integer, default=0)
    order_index: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    post: Mapped["Post"] = relationship(back_populates="poll_options")
    poll_votes: Mapped[list["PollVote"]] = relationship(back_populates="option", cascade="all, delete-orphan")


class PollVote(Base):
    __tablename__ = "poll_votes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    option_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    option: Mapped["PollOption"] = relationship(back_populates="poll_votes")
