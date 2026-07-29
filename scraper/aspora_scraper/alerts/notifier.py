"""Slack alerting: ingestion failures, and the "no upload received" staleness nudge."""

from __future__ import annotations

import os

import httpx


def _post_to_slack(text: str) -> None:
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return
    httpx.post(webhook_url, json={"text": text}, timeout=10)


def notify_ingestion_failure(*, platform: str, error: str, github_run_url: str | None) -> None:
    lines = [f":rotating_light: *{platform}* ingestion failed", f"```{error}```"]
    if github_run_url:
        lines.append(f"<{github_run_url}|View run>")
    _post_to_slack("\n".join(lines))


def notify_stale_account(*, brand_name: str, platform: str, hours_since_ingest: float) -> None:
    _post_to_slack(
        f":warning: No *{platform}* data received for *{brand_name}* in "
        f"{hours_since_ingest:.0f}h — someone needs to upload the latest export."
    )
