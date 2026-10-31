-- Postgrad Funding Radar: Supabase setup.
-- Run once: Supabase dashboard -> SQL Editor -> New query -> paste all -> Run.
-- Security model: the public (anon) key can only INSERT waitlist entries and problem reports.
-- Nobody can read them through the public key; you read them in the Supabase dashboard (Table Editor).

create table if not exists public.waitlist (
  id            uuid primary key default gen_random_uuid(),
  created_at    timestamptz not null default now(),
  name          text not null check (char_length(name) between 1 and 120),
  contact       text not null check (char_length(contact) between 3 and 160),
  plan          text check (char_length(plan) <= 80),
  max_monthly   text check (char_length(max_monthly) <= 20),
  pain          text check (char_length(pain) <= 1000),
  nationality   text check (char_length(nationality) <= 60),
  study_country text check (char_length(study_country) <= 60),
  level         text check (level in ('MSc','PhD')),
  field         text check (char_length(field) <= 40),
  consent       boolean not null check (consent = true),
  source        text check (char_length(source) <= 60)
);

create table if not exists public.reports (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  programme   text not null check (char_length(programme) <= 90),
  kind        text not null check (char_length(kind) <= 60),
  details     text check (char_length(details) <= 2000),
  status      text not null default 'new' check (status in ('new','checking','fixed','rejected'))
);

alter table public.waitlist enable row level security;
alter table public.reports  enable row level security;

-- Public may add rows, never read, change or delete them.
drop policy if exists "public can join waitlist" on public.waitlist;
create policy "public can join waitlist" on public.waitlist
  for insert to anon with check (consent = true);

drop policy if exists "public can send reports" on public.reports;
create policy "public can send reports" on public.reports
  for insert to anon with check (status = 'new');

-- Make sure the anon role has no read access at the privilege level either.
revoke select, update, delete on public.waitlist from anon;
revoke select, update, delete on public.reports  from anon;
grant insert on public.waitlist to anon;
grant insert on public.reports  to anon;

-- Handy views for you in the dashboard
create or replace view public.waitlist_summary with (security_invoker = true) as
  select plan, max_monthly, count(*) as people
  from public.waitlist group by plan, max_monthly order by people desc;
revoke all on public.waitlist_summary from anon;
