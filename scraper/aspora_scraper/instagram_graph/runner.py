"""OPTIONAL, per-account: Instagram Graph API ingestion.

Not wired into any workflow yet. Only becomes relevant once it's confirmed,
per brand, that:
  1. the Instagram account is a Business/Creator account linked to a
     Facebook Page, and
  2. a Meta Developer App with Instagram Graph API access + a long-lived
     Business Manager System User token has been set up.

Once confirmed for a given `platform_accounts` row, flip its
`ingestion_method` to 'automated_api'. YouTube's equivalent pull was moved
from Python to a Supabase Edge Function (/supabase/functions/youtube-ingest/,
scheduled via pg_cron) since it's just REST calls with no Python-specific
library dependency — Instagram Graph API access is the same shape (plain
HTTPS + an access token), so implement this as a sibling Edge Function
instead of a Python module when the time comes; this file is a placeholder
marker, not the intended implementation site.

Until Graph API access is confirmed, that brand's Instagram stays on the
screenshot upload path (aspora_scraper.ingest, platform='instagram',
file_type='image').
"""

from __future__ import annotations


def run(*, triggered_by: str = "schedule") -> None:
    raise NotImplementedError(
        "Instagram Graph API access has not been confirmed for any account yet. "
        "See this module's docstring and plan Section 5 before implementing."
    )
