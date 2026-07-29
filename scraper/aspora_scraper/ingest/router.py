"""Decides which parser handles a given file_uploads row."""

from __future__ import annotations

from typing import Any

from aspora_scraper.ingest.parsers import pdf, tabular, vision

# csv/xlsx are deterministic parses -> fast one-click review UI.
# pdf/image are lower-confidence -> full editable review UI.
CONFIDENCE_BY_FILE_TYPE = {
    "csv": "high",
    "xlsx": "high",
    "pdf": "low",
    "image": "low",
}


def parse_upload(file_bytes: bytes, *, platform: str, file_type: str) -> tuple[dict[str, Any], str]:
    """Returns (extracted_preview, confidence)."""
    confidence = CONFIDENCE_BY_FILE_TYPE[file_type]

    if file_type in ("csv", "xlsx"):
        return tabular.parse(file_bytes, platform=platform, file_type=file_type), confidence
    if file_type == "pdf":
        return pdf.parse(file_bytes, platform=platform), confidence
    if file_type == "image":
        return vision.parse(file_bytes, platform=platform), confidence

    raise ValueError(f"Unknown file_type: {file_type!r}")
