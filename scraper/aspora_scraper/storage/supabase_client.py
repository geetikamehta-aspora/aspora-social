"""The ONLY module allowed to hold or use the Supabase service-role key.

Everything in this package's ingest/ calls through here rather than importing
`supabase` directly, so the security boundary stays auditable in one place.
Every write here bypasses RLS by design — this is the trusted automation
path (upload parsing), not a user-facing request.

YouTube ingestion lives in a Supabase Edge Function
(/supabase/functions/youtube-ingest/), not here — Python is only needed for
the manual-upload parsing pipeline (pandas/pdfplumber/OpenAI vision).
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Any

import httpx
from supabase import Client, create_client


@lru_cache(maxsize=1)
def get_client() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    return create_client(url, key)


def get_configuration(key: str, default: Any = None) -> Any:
    result = get_client().table("configurations").select("value").eq("key", key).limit(1).execute()
    if not result.data:
        return default
    return result.data[0]["value"]


# ============================================================================
# file_uploads — used by the ingest/ parsing pipeline (process-uploads.yml)
# ============================================================================


def get_pending_uploads() -> list[dict[str, Any]]:
    result = get_client().table("file_uploads").select("*").eq("status", "pending").execute()
    return result.data


def get_upload(upload_id: str) -> dict[str, Any]:
    result = get_client().table("file_uploads").select("*").eq("id", upload_id).single().execute()
    return result.data


def download_upload_file(drive_file_id: str) -> bytes:
    """Files live in Google Drive (uploaded via the Apps Script bridge, see
    /gas/), set to "anyone with the link" — a plain GET is enough, no Drive
    API auth needed here.
    """
    url = f"https://drive.google.com/uc?export=download&id={drive_file_id}"
    response = httpx.get(url, follow_redirects=True, timeout=30)
    response.raise_for_status()
    return response.content


def mark_upload_processing(upload_id: str) -> None:
    get_client().table("file_uploads").update({"status": "processing"}).eq("id", upload_id).execute()


def mark_upload_awaiting_review(
    upload_id: str,
    *,
    extracted_preview: dict[str, Any],
    column_mapping: dict[str, str] | None,
    confidence: str,
) -> None:
    get_client().table("file_uploads").update(
        {
            "status": "awaiting_review",
            "extracted_preview": extracted_preview,
            "column_mapping": column_mapping,
            "confidence": confidence,
        }
    ).eq("id", upload_id).execute()


def mark_upload_failed(upload_id: str, *, error: str) -> None:
    get_client().table("file_uploads").update(
        {"status": "failed", "error_message": error}
    ).eq("id", upload_id).execute()


def get_stale_platform_accounts(*, threshold_hours: float) -> list[dict[str, Any]]:
    """Accounts whose last_ingested_at is older than the threshold (or null,
    meaning never ingested). Drives the "no upload received" Slack nudge —
    the process-risk equivalent of the old anti-bot alerting.
    """
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=threshold_hours)).isoformat()
    result = (
        get_client()
        .table("platform_accounts")
        .select("*, brands(name)")
        .eq("is_active", True)
        .or_(f"last_ingested_at.is.null,last_ingested_at.lt.{cutoff}")
        .execute()
    )
    return result.data
