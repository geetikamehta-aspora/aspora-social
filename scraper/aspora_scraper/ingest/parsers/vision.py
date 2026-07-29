"""Screenshot extraction via OpenAI's Responses API (GPT-5.5 vision, structured
output). Always routes to a full editable review — a misread digit here
would otherwise become a wrong number on the leadership dashboard with no one
checking it (plan Section 5).

Requires OPENAI_API_KEY, which is not yet available (see plan Section 7) —
raises a clear, actionable error until it's set as a GitHub Actions secret,
so an admin sees "OpenAI API key not configured" rather than a stack trace.
"""

from __future__ import annotations

import base64
import json
import os
from typing import Any

from openai import OpenAI

EXTRACTION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "followers_count": {"type": ["integer", "null"]},
        "following_count": {"type": ["integer", "null"]},
        "posts_count": {"type": ["integer", "null"]},
        "impressions_total": {"type": ["integer", "null"]},
        "likes_total": {"type": ["integer", "null"]},
        "comments_total": {"type": ["integer", "null"]},
        "shares_total": {"type": ["integer", "null"]},
        "saves_total": {"type": ["integer", "null"]},
        "video_views_total": {"type": ["integer", "null"]},
        "notes": {
            "type": "string",
            "description": "Anything ambiguous or hard to read in the screenshot.",
        },
    },
    "required": [
        "followers_count",
        "following_count",
        "posts_count",
        "impressions_total",
        "likes_total",
        "comments_total",
        "shares_total",
        "saves_total",
        "video_views_total",
        "notes",
    ],
}


def parse(file_bytes: bytes, *, platform: str) -> dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not configured yet — the vision parser can't run "
            "until it's added as a GitHub Actions secret (see plan Section 7)."
        )

    client = OpenAI(api_key=api_key)
    b64_image = base64.b64encode(file_bytes).decode("ascii")

    response = client.responses.create(
        model="gpt-5.5",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            f"This is a screenshot of {platform} analytics/insights. "
                            "Read off every metric you can see and return it in the "
                            "requested structured format. Use null for anything not visible "
                            "— never guess a number."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{b64_image}",
                    },
                ],
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "extracted_metrics",
                "schema": EXTRACTION_SCHEMA,
                "strict": True,
            }
        },
    )

    extracted = json.loads(response.output_text)

    return {
        "format": "image",
        "platform": platform,
        "extracted": extracted,
        "model": "gpt-5.5",
        "tokens_used": getattr(response.usage, "total_tokens", None),
    }
