"""Entrypoint: given a file_uploads.id, downloads the file, routes it to a
parser, and stores the result for human review. Never writes to
historical_metrics/posts directly — that commit only happens when an admin
approves the preview in /settings/uploads/[uploadId] (plan Section 5).

Run by `.github/workflows/process-uploads.yml` on a ~10-15 min poll.
"""

from __future__ import annotations

import logging
import sys

from aspora_scraper.ingest.router import parse_upload
from aspora_scraper.storage.supabase_client import (
    download_upload_file,
    get_pending_uploads,
    get_upload,
    mark_upload_awaiting_review,
    mark_upload_failed,
    mark_upload_processing,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_one(upload_id: str) -> None:
    upload = get_upload(upload_id)
    mark_upload_processing(upload_id)

    try:
        file_bytes = download_upload_file(upload["drive_file_id"])
        extracted_preview, confidence = parse_upload(
            file_bytes, platform=upload["platform"], file_type=upload["file_type"]
        )
        column_mapping = extracted_preview.get("column_mapping")
        mark_upload_awaiting_review(
            upload_id,
            extracted_preview=extracted_preview,
            column_mapping=column_mapping,
            confidence=confidence,
        )
        logger.info("Upload %s parsed successfully (confidence=%s)", upload_id, confidence)
    except Exception as exc:  # noqa: BLE001 — one bad file shouldn't kill the batch
        logger.exception("Failed to process upload %s", upload_id)
        mark_upload_failed(upload_id, error=str(exc))


def run_pending() -> None:
    pending = get_pending_uploads()
    if not pending:
        logger.info("No pending uploads.")
        return

    logger.info("Processing %d pending upload(s).", len(pending))
    for upload in pending:
        process_one(upload["id"])


if __name__ == "__main__":
    if "--upload-id" in sys.argv:
        idx = sys.argv.index("--upload-id")
        process_one(sys.argv[idx + 1])
    else:
        run_pending()
