"""CSV/XLSX parsing — deterministic, column-mapping driven.

Column mappings live in `configurations` (key: `import_column_map_{platform}_{file_type}`)
so a platform renaming an export header is a config edit, not a redeploy. See
plan Section 5. This parser never writes to historical_metrics/posts itself —
it only produces `extracted_preview` + `column_mapping` for the review-queue
UI; the actual commit happens when an admin approves it there.
"""

from __future__ import annotations

import io
from typing import Any

import pandas as pd

from aspora_scraper.storage.supabase_client import get_configuration

CANONICAL_ACCOUNT_FIELDS = {
    "followers_count",
    "following_count",
    "posts_count",
    "impressions_total",
    "likes_total",
    "comments_total",
    "shares_total",
    "saves_total",
    "video_views_total",
}


def _read_dataframe(file_bytes: bytes, file_type: str) -> pd.DataFrame:
    buf = io.BytesIO(file_bytes)
    if file_type == "csv":
        return pd.read_csv(buf)
    if file_type == "xlsx":
        return pd.read_excel(buf)
    raise ValueError(f"tabular parser does not handle file_type={file_type!r}")


def _coerce_number(value: Any) -> float | int | None:
    """Handles locale-formatted numbers like '12,345' or '12.3K'."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, (int, float)):
        return value

    s = str(value).strip().replace(",", "")
    if not s:
        return None

    multiplier = 1
    upper = s.upper()
    if upper.endswith("K"):
        multiplier, s = 1_000, s[:-1]
    elif upper.endswith("M"):
        multiplier, s = 1_000_000, s[:-1]

    try:
        num = float(s) * multiplier
        return int(num) if num.is_integer() else num
    except ValueError:
        return None


def parse(file_bytes: bytes, *, platform: str, file_type: str) -> dict[str, Any]:
    df = _read_dataframe(file_bytes, file_type)

    mapping_key = f"import_column_map_{platform}_{file_type}"
    mapping: dict[str, str] | None = get_configuration(mapping_key)
    if not mapping:
        raise ValueError(
            f"No column mapping configured for '{mapping_key}'. "
            "Add one via /settings/configurations before retrying this upload."
        )

    date_column = mapping.get("__date_column__")
    field_mapping = {k: v for k, v in mapping.items() if not k.startswith("__")}

    unknown_targets = set(field_mapping.values()) - CANONICAL_ACCOUNT_FIELDS
    if unknown_targets:
        raise ValueError(
            f"'{mapping_key}' maps to unknown canonical field(s): {sorted(unknown_targets)}"
        )

    missing_columns = [c for c in field_mapping if c not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Columns configured in '{mapping_key}' are missing from the uploaded file: "
            f"{missing_columns}. The platform may have renamed its export headers — "
            "update the mapping in /settings/configurations."
        )

    rows: list[dict[str, Any]] = []
    for _, source_row in df.iterrows():
        row: dict[str, Any] = {}
        if date_column and date_column in df.columns:
            row["date"] = str(source_row[date_column])
        for source_col, canonical_field in field_mapping.items():
            row[canonical_field] = _coerce_number(source_row[source_col])
        rows.append(row)

    unmapped_columns = [c for c in df.columns if c not in field_mapping and c != date_column]

    return {
        "format": file_type,
        "row_count": len(rows),
        "column_mapping": field_mapping,
        "date_column": date_column,
        "unmapped_columns": unmapped_columns,
        "rows": rows,
    }
