-- Incremental patch for a database that already has 001-006 + 008 applied
-- (confirmed applied to the live project — brands/platform_accounts/users
-- already exist and are seeded). Fresh installs get this automatically via
-- the updated 002_schema.sql / 003_rls.sql; run this file only if you
-- already applied those before invited_users existed.
--
-- SUPERSEDED, run anyway: this file creates invited_users (still used) and
-- the enforce_user_role_immutable trigger/requesting_role()-based policies
-- (no longer live — 010_open_access.sql drops all of that right after, as
-- part of the switch to a Firebase-only auth model). Keeping this file
-- as-is rather than rewriting it, since it's an accurate record of what was
-- actually run against the live project, in order.

create table public.invited_users (
  id            uuid primary key default gen_random_uuid(),
  email         text not null unique,
  display_name  text,
  role          text not null default 'viewer' check (role in ('admin', 'viewer')),
  invited_by    text references public.users(id),
  created_at    timestamptz not null default now()
);

alter table public.invited_users enable row level security;

create policy invited_users_admin_all on public.invited_users
  for all
  using (public.requesting_role() = 'admin')
  with check (public.requesting_role() = 'admin');

-- Restricts self-provisioning to @aspora.com addresses or a matching
-- invited_users row (the existing policy only checked id = own uid, which
-- let literally any Google account self-provision as a viewer).
alter policy users_insert_self on public.users
  with check (
    id = public.requesting_firebase_uid()
    and (
      email like '%@aspora.com'
      or exists (select 1 from public.invited_users iu where iu.email = email)
    )
  );

-- Replaces the existing function body — the trigger already attached to
-- public.users (trg_enforce_user_role_immutable) picks up this new behavior
-- automatically, no need to touch the trigger itself.
create or replace function public.enforce_user_role_immutable()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  caller_role text := auth.role();
  invited public.invited_users;
begin
  if caller_role is null or caller_role = 'service_role' then
    return new;
  end if;

  if tg_op = 'INSERT' then
    select * into invited from public.invited_users where email = new.email limit 1;
    if invited.id is not null then
      new.role := invited.role;
      if new.display_name is null then
        new.display_name := invited.display_name;
      end if;
      delete from public.invited_users where id = invited.id;
    elsif new.role is distinct from 'viewer' and public.requesting_role() is distinct from 'admin' then
      new.role := 'viewer';
    end if;
  elsif tg_op = 'UPDATE' then
    if new.role is distinct from old.role and public.requesting_role() is distinct from 'admin' then
      new.role := old.role;
    end if;
  end if;
  return new;
end;
$$;
