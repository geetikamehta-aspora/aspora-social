"""The canonical contract every ingestion source must satisfy.

Whether data came from the YouTube Data API, the (future, contingent)
Instagram Graph API, or a manually uploaded CSV/XLSX/PDF/screenshot, it ends
up as one of these two models before it's written to Supabase. This is what
lets `storage/supabase_client.py` and the review-queue UI stay ignorant of
where a number originally came from.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

Platform = Literal["instagram", "linkedin", "x", "youtube"]
PostType = Literal[
    "image", "video", "reel", "carousel", "text", "article", "short", "livestream", "poll", "other"
]
Source = Literal["automated_api", "manual_upload"]


class NormalizedAccountSnapshot(BaseModel):
    """One row's worth of account-level metrics -> historical_metrics."""

    model_config = ConfigDict(extra="forbid")

    platform: Platform
    scraped_at: datetime

    followers_count: int | None = None
    following_count: int | None = None
    posts_count: int | None = None
    impressions_total: int | None = None
    likes_total: int | None = None
    comments_total: int | None = None
    shares_total: int | None = None
    saves_total: int | None = None
    video_views_total: int | None = None
    engagement_rate: Decimal | None = None

    raw_payload: dict[str, Any]


class NormalizedPost(BaseModel):
    """One row's worth of post-level metrics -> posts (upserted by platform_post_id)."""

    model_config = ConfigDict(extra="forbid")

    platform: Platform
    platform_post_id: str
    post_type: PostType | None = None
    permalink: str | None = None
    caption: str | None = None
    media_urls: list[str] | None = None
    posted_at: datetime | None = None

    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    impressions: int | None = None
    video_views: int | None = None
    engagement_rate: Decimal | None = None

    raw_latest: dict[str, Any]


def compute_engagement_rate(
    *, likes: int = 0, comments: int = 0, shares: int = 0, saves: int = 0, followers: int | None
) -> Decimal | None:
    """Shared formula so every mapper computes engagement the same way.

    Kept as a plain function (not a DB trigger/generated column) per the
    plan's note on formula-versioning risk — if this changes, only future
    writes are affected; historical raw_payload is preserved so a change can
    be backfilled deliberately, not silently.
    """
    if not followers:
        return None
    total = likes + comments + shares + saves
    return Decimal(total) / Decimal(followers)


__all__ = [
    "NormalizedAccountSnapshot",
    "NormalizedPost",
    "Platform",
    "PostType",
    "Source",
    "compute_engagement_rate",
]
