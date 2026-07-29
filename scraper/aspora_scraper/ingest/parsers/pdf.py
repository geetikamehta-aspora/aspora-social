"""PDF table extraction — lower confidence than CSV/XLSX, always routes to a
full editable review before anything is trusted (plan Section 5).
"""

from __future__ import annotations

import io
from typing import Any

import pdfplumber


def parse(file_bytes: bytes, *, platform: str) -> dict[str, Any]:
    tables: list[list[list[str | None]]] = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                tables.append(table)

    if not tables:
        raise ValueError(
            "No tables could be extracted from this PDF. It may be image-based "
            "(scanned) rather than text-based — consider uploading a screenshot instead."
        )

    return {
        "format": "pdf",
        "platform": platform,
        "tables": tables,
        "note": "Raw extracted tables — review and map values manually before approving.",
    }
