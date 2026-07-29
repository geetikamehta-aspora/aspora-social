"""Daily staleness nudge: alerts when an account hasn't been ingested recently.

Run alongside process_upload.py from process-uploads.yml. This is the
process-risk equivalent of the old anti-bot alerting — catching a missed
human upload instead of a broken selector (plan Section 6).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from aspora_scraper.alerts.notifier import notify_stale_account
from aspora_scraper.storage.supabase_client import get_stale_platform_accounts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STALE_THRESHOLD_HOURS = 40  # a bit under 48h so a missed single day is caught, not just two


def run() -> None:
    stale_accounts = get_stale_platform_accounts(threshold_hours=STALE_THRESHOLD_HOURS)
    for account in stale_accounts:
        last_ingested_at = account.get("last_ingested_at")
        hours_since = (
            (datetime.now(timezone.utc) - datetime.fromisoformat(last_ingested_at)).total_seconds()
            / 3600
            if last_ingested_at
            else float("inf")
        )
        brand_name = (account.get("brands") or {}).get("name", "unknown brand")
        logger.info("Stale: %s / %s (%.0fh)", brand_name, account["platform"], hours_since)
        notify_stale_account(
            brand_name=brand_name, platform=account["platform"], hours_since_ingest=hours_since
        )


if __name__ == "__main__":
    run()
