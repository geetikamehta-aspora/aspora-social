# Drive-upload bridge (Google Apps Script)

Replaces Supabase Storage as where uploaded files (Instagram screenshots,
LinkedIn/X/YouTube CSV/XLSX/PDF exports) actually live. The dashboard's
upload form is unchanged — an admin still picks brand/platform/account/period
and a file — but the bytes get routed through this script into a Drive
folder instead of a Supabase Storage bucket.

## Why a shared secret

This Web App is deployed with "Who has access: Anyone," which means anyone
who discovers the `/exec` URL could call it directly unless we check
something. The Next.js `/api/uploads` route (server-side only) is the sole
caller and sends a shared secret in the request body — never exposed to the
browser. Treat both copies (Script Properties here, `GAS_UPLOAD_SHARED_SECRET`
in `web/.env`) as real secrets.

## Setup

1. Open **script.google.com/d/`<YOUR_SCRIPT_ID>`/edit**, paste `Code.gs` in as the
   project's `Code.gs`.
2. **Project Settings → Script Properties**, add:
   - `SHARED_SECRET` — `2b70371ac1d7d33a5cefd208f1eb4c16c90380d6defb89d99224c50ba76864a8`
     (already set as `GAS_UPLOAD_SHARED_SECRET` in `web/.env` — must match exactly)
   - `DEFAULT_FOLDER_ID` — `1EHnr0R53edAY9XFy3KkNV5okGmgPhLzy` (root uploads folder)
3. **Deploy → New deployment → type "Web app"**:
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Copy the resulting `/exec` URL.
5. In `web/.env`, set:
   ```
   GAS_UPLOAD_WEBHOOK_URL=<the /exec URL>
   GAS_UPLOAD_SHARED_SECRET=<same value as SHARED_SECRET above>
   ```

## Folder structure

Files land at `<DEFAULT_FOLDER_ID>/<period_end date>/<platform>/<brand slug>/<filename>`
— e.g. `2026-07-29/instagram/aspora/report.png`. Folders are created on
demand and reused on repeat uploads for the same date/platform/brand (no
duplicate folders).

## Notes

- Files are set to Drive's "anyone with the link can view" sharing — not
  indexed/discoverable, but fetchable by anyone who has the link. That's
  what lets the Python parser download by plain HTTP GET without Drive API
  auth. If that's more exposure than you want for a given file, don't rely
  on link-obscurity as the only protection — this is a reasonable trade for
  internal analytics exports, but worth knowing.
- Apps Script Web Apps cap request size in the tens-of-MB range — plenty for
  CSV/XLSX/PDF/screenshot exports, not intended for video files.
- Redeploying after editing `Code.gs` requires **Deploy → Manage deployments
  → Edit → New version** — saving the file alone does not update the live
  `/exec` endpoint.
