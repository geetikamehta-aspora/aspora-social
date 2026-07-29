# Supabase schema migrations

Apply in order against the Supabase project (SQL editor, or `supabase db push` /
`psql` with the connection string):

1. `001_extensions.sql`
2. `002_schema.sql`
3. `003_rls.sql` — **permissive by design**, see the comment at the top of that file for why (Firebase-only auth model, no Third-Party Auth registration)
4. `004_seed.sql` — replace every `TODO_SET_HANDLE` with the real handle/channel ID first
5. `005_rpc.sql`
6. `006_views.sql`
7. `008_youtube_cron.sql` — after deploying the `youtube-ingest` Edge Function (see `/supabase/functions/youtube-ingest/README.md`)
8. `009_invited_users.sql` — **the live project already has 001-006+008 applied**, so run this now via the SQL editor. Fresh installs get this via `002_schema.sql` instead and can skip it.
9. `010_open_access.sql` — **run this now too**, immediately after `009`. Supersedes `003_rls.sql`'s original (identity-based) policies with permissive ones — see that file's header comment for the full reasoning. Fresh installs get this directly via the rewritten `003_rls.sql` and can skip it.

## Manual one-time setup (Supabase dashboard, not SQL)

- **Vault**: store the service-role key as a Vault secret (used by
  `008_youtube_cron.sql` to call the Edge Function without hardcoding the key
  in a committed SQL file). Dashboard -> Project Settings -> Vault.
- Uploaded files live in **Google Drive**, not Supabase Storage — no bucket
  needed. See `/gas/README.md` for the Apps Script bridge setup.
- ~~Authentication -> Third-Party Auth -> Firebase~~ — **no longer needed.**
  The auth model changed to Firebase-only + app-layer checks (see
  `003_rls.sql`'s header comment); Supabase never needs to verify a Firebase
  token at all now.
