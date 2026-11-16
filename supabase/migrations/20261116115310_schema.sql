-- Casa Control, fase 1.
-- Papel fica em public.profiles. Nao usar user_metadata para autorizar.
-- Funcoes privilegiadas ficam no schema private, fora da API.

create schema if not exists private;

revoke all on schema private from public;
grant usage on schema private to authenticated;
grant usage on schema private to supabase_auth_admin;

create type public.app_role as enum ('executor', 'manager');

create table public.role_invites (
  email text primary key,
  full_name text not null,
  role public.app_role not null,
  created_at timestamptz not null default now(),
  constraint role_invites_email_lower check (email = lower(email)),
  constraint role_invites_name_not_blank check (char_length(btrim(full_name)) > 0)
);

create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  full_name text not null,
  role public.app_role not null,
  created_at timestamptz not null default now(),
  constraint profiles_name_not_blank check (char_length(btrim(full_name)) > 0)
);

create table public.task_templates (
  id uuid primary key default gen_random_uuid(),
  code text unique,
  title text not null,
  category text not null,
  group_name text,
  weekday smallint,
  scheduled_time time,
  sort_order integer not null default 0,
  active boolean not null default true,
  recurrence_kind text not null default 'none',
  recurrence_interval integer not null default 1,
  active_weekdays smallint[] not null default '{}',
  starts_on date,
  ends_on date,
  created_by uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint task_templates_title_not_blank check (char_length(btrim(title)) > 0),
  constraint task_templates_category_chk check (
    category in ('fixed', 'routine', 'weekday', 'eventual')
  ),
  constraint task_templates_weekday_chk check (weekday is null or weekday between 0 and 6),
  constraint task_templates_recurrence_chk check (
    recurrence_kind in ('none', 'daily', 'weekly', 'eventual')
  ),
  constraint task_templates_interval_chk check (recurrence_interval >= 1),
  constraint task_templates_dates_chk check (
    starts_on is null or ends_on is null or starts_on <= ends_on
  )
);

create table public.one_off_tasks (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  due_on date not null,
  active boolean not null default true,
  sort_order integer not null default 0,
  created_by uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint one_off_tasks_title_not_blank check (char_length(btrim(title)) > 0)
);

create table public.checks (
  id uuid primary key default gen_random_uuid(),
  template_id uuid references public.task_templates (id) on delete restrict,
  one_off_id uuid references public.one_off_tasks (id) on delete restrict,
  due_on date not null,
  checked_at timestamptz not null,
  checked_by uuid references public.profiles (id) on delete set null,
  actor_name text not null,
  source text not null,
  legacy_code text,
  constraint checks_target_chk check (
    (template_id is not null and one_off_id is null)
    or (template_id is null and one_off_id is not null)
  ),
  constraint checks_source_chk check (source in ('app', 'archive')),
  constraint checks_actor_chk check (char_length(btrim(actor_name)) > 0),
  constraint checks_app_actor_chk check (source <> 'app' or checked_by is not null),
  constraint checks_archive_actor_chk check (source <> 'archive' or checked_by is null)
);

create unique index checks_template_day_uidx
  on public.checks (template_id, due_on)
  where template_id is not null;

create unique index checks_one_off_uidx
  on public.checks (one_off_id)
  where one_off_id is not null;

create index checks_due_on_idx on public.checks (due_on);
create index checks_checked_by_idx on public.checks (checked_by);
create index one_off_tasks_due_on_idx on public.one_off_tasks (due_on, active);
create index task_templates_active_idx on public.task_templates (active, sort_order);
create index profiles_role_idx on public.profiles (role);

create or replace function private.household_role()
returns text
language sql
stable
security definer
set search_path = ''
as $$
  select p.role::text
  from public.profiles as p
  where p.id = (select auth.uid())
$$;

revoke all on function private.household_role() from public;
grant execute on function private.household_role() to authenticated;

create or replace function private.touch_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

revoke all on function private.touch_updated_at() from public;
grant execute on function private.touch_updated_at() to authenticated;

create trigger task_templates_touch
  before update on public.task_templates
  for each row execute function private.touch_updated_at();

create trigger one_off_tasks_touch
  before update on public.one_off_tasks
  for each row execute function private.touch_updated_at();

create or replace function private.prevent_role_change()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if current_user = 'authenticated' and new.role is distinct from old.role then
    raise exception 'O papel da conta não muda por aqui';
  end if;
  if current_user = 'authenticated' and new.id is distinct from old.id then
    raise exception 'O id da conta não muda';
  end if;
  return new;
end;
$$;

revoke all on function private.prevent_role_change() from public;
grant execute on function private.prevent_role_change() to authenticated;

create trigger profiles_lock_role
  before update on public.profiles
  for each row execute function private.prevent_role_change();

create or replace function private.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  invite public.role_invites%rowtype;
begin
  if new.email is null then
    raise exception 'Conta sem e-mail';
  end if;

  select *
    into invite
  from public.role_invites
  where email = lower(new.email);

  if not found then
    raise exception 'Este e-mail não está na lista de convites da casa';
  end if;

  insert into public.profiles (id, full_name, role)
  values (new.id, invite.full_name, invite.role);

  return new;
end;
$$;

revoke all on function private.handle_new_user() from public, anon, authenticated;
grant execute on function private.handle_new_user() to supabase_auth_admin;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function private.handle_new_user();

alter table public.role_invites enable row level security;
alter table public.profiles enable row level security;
alter table public.task_templates enable row level security;
alter table public.one_off_tasks enable row level security;
alter table public.checks enable row level security;

alter table public.role_invites force row level security;
alter table public.profiles force row level security;
alter table public.task_templates force row level security;
alter table public.one_off_tasks force row level security;
alter table public.checks force row level security;

revoke all on public.role_invites from anon, authenticated;
revoke all on public.profiles from anon;
revoke all on public.task_templates from anon;
revoke all on public.one_off_tasks from anon;
revoke all on public.checks from anon;

grant select on public.profiles to authenticated;
grant select, insert, update on public.task_templates to authenticated;
grant select, insert, update on public.one_off_tasks to authenticated;
grant select, insert, delete on public.checks to authenticated;

create policy profiles_select
  on public.profiles
  for select
  to authenticated
  using ((select private.household_role()) is not null);

create policy task_templates_select
  on public.task_templates
  for select
  to authenticated
  using ((select private.household_role()) is not null);

create policy task_templates_write
  on public.task_templates
  for insert
  to authenticated
  with check ((select private.household_role()) = 'manager');

create policy task_templates_update
  on public.task_templates
  for update
  to authenticated
  using ((select private.household_role()) = 'manager')
  with check ((select private.household_role()) = 'manager');

create policy one_off_select
  on public.one_off_tasks
  for select
  to authenticated
  using ((select private.household_role()) is not null);

create policy one_off_insert
  on public.one_off_tasks
  for insert
  to authenticated
  with check ((select private.household_role()) = 'manager');

create policy one_off_update
  on public.one_off_tasks
  for update
  to authenticated
  using ((select private.household_role()) = 'manager')
  with check ((select private.household_role()) = 'manager');

create policy checks_select
  on public.checks
  for select
  to authenticated
  using ((select private.household_role()) is not null);

create policy checks_insert
  on public.checks
  for insert
  to authenticated
  with check (
    source = 'app'
    and checked_by = (select auth.uid())
    and actor_name = (
      select p.full_name
      from public.profiles as p
      where p.id = (select auth.uid())
    )
    and (
      (select private.household_role()) = 'manager'
      or due_on = (timezone('America/Sao_Paulo', now()))::date
    )
    and (
      (template_id is not null and one_off_id is null)
      or (template_id is null and one_off_id is not null)
    )
  );

create policy checks_delete
  on public.checks
  for delete
  to authenticated
  using (
    source = 'app'
    and (
      (select private.household_role()) = 'manager'
      or (
        checked_by = (select auth.uid())
        and due_on = (timezone('America/Sao_Paulo', now()))::date
      )
    )
  );
