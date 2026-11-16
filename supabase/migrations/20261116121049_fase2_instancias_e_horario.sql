-- Fase 2. O dia de Cuiaba gera instancias. Pendencia fica no dia seguinte.
-- Tarefa com hora so pode ser marcada a partir de 60 minutos antes.

create table public.task_instances (
  id uuid primary key default gen_random_uuid(),
  template_id uuid references public.task_templates (id) on delete restrict,
  one_off_id uuid references public.one_off_tasks (id) on delete restrict,
  due_on date not null,
  title text not null,
  scheduled_time time,
  category text not null,
  sort_order integer not null default 0,
  status text not null default 'pending',
  created_at timestamptz not null default now(),
  constraint task_instances_target_chk check (
    (template_id is not null and one_off_id is null)
    or (template_id is null and one_off_id is not null)
  ),
  constraint task_instances_status_chk check (status in ('pending', 'done')),
  constraint task_instances_title_chk check (char_length(btrim(title)) > 0)
);

create unique index task_instances_template_day_uidx
  on public.task_instances (template_id, due_on)
  where template_id is not null;

create unique index task_instances_one_off_uidx
  on public.task_instances (one_off_id)
  where one_off_id is not null;

create index task_instances_open_idx
  on public.task_instances (status, due_on);

alter table public.task_instances enable row level security;
alter table public.task_instances force row level security;

revoke all on public.task_instances from anon;
grant select, insert on public.task_instances to authenticated;

create policy task_instances_select
  on public.task_instances
  for select
  to authenticated
  using ((select private.household_role()) is not null);

create policy task_instances_insert
  on public.task_instances
  for insert
  to authenticated
  with check (
    (select private.household_role()) is not null
    and status in ('pending', 'done')
    and due_on = (timezone('America/Cuiaba', now()))::date
    and (
      (
        template_id is not null
        and one_off_id is null
        and exists (
          select 1
          from public.task_templates as t
          where t.id = template_id
            and t.active
            and t.category <> 'eventual'
            and t.title = task_instances.title
            and t.category = task_instances.category
            and t.sort_order = task_instances.sort_order
            and t.scheduled_time is not distinct from task_instances.scheduled_time
            and (t.starts_on is null or t.starts_on <= task_instances.due_on)
            and (t.ends_on is null or t.ends_on >= task_instances.due_on)
            and extract(dow from task_instances.due_on)::smallint = any (t.active_weekdays)
            and (
              status = 'pending'
              or exists (
                select 1
                from public.checks as c
                where c.template_id = t.id
                  and c.due_on = task_instances.due_on
              )
            )
        )
      )
      or (
        one_off_id is not null
        and template_id is null
        and exists (
          select 1
          from public.one_off_tasks as o
          where o.id = one_off_id
            and o.active
            and o.due_on = task_instances.due_on
            and o.title = task_instances.title
            and o.sort_order = task_instances.sort_order
        )
      )
    )
  );

create or replace function private.executor_may_check(
  template uuid,
  one_off uuid,
  target_due date
)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select case
    when target_due < (timezone('America/Cuiaba', now()))::date then
      exists (
        select 1
        from public.task_instances as i
        where i.due_on = target_due
          and i.status = 'pending'
          and (
            (template is not null and i.template_id = template)
            or (one_off is not null and i.one_off_id = one_off)
          )
      )
    when target_due = (timezone('America/Cuiaba', now()))::date and template is not null then
      exists (
        select 1
        from public.task_templates as t
        where t.id = template
          and (
            t.scheduled_time is null
            or timezone('America/Cuiaba', now())
              >= (target_due + t.scheduled_time) - interval '60 minutes'
          )
      )
    when target_due = (timezone('America/Cuiaba', now()))::date and one_off is not null then
      exists (
        select 1
        from public.one_off_tasks as o
        where o.id = one_off
          and o.due_on = target_due
          and o.active
      )
    else false
  end
$$;

revoke all on function private.executor_may_check(uuid, uuid, date) from public;
grant execute on function private.executor_may_check(uuid, uuid, date) to authenticated;

drop policy checks_insert on public.checks;
drop policy checks_delete on public.checks;

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
      or (select private.executor_may_check(template_id, one_off_id, due_on))
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
        and due_on <= (timezone('America/Cuiaba', now()))::date
      )
    )
  );

create or replace function private.sync_instance_from_check()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
declare
  target_due date;
  target_template uuid;
  target_one_off uuid;
begin
  if tg_op = 'DELETE' then
    target_due := old.due_on;
    target_template := old.template_id;
    target_one_off := old.one_off_id;
  else
    target_due := new.due_on;
    target_template := new.template_id;
    target_one_off := new.one_off_id;
  end if;

  update public.task_instances as i
    set status = case
      when exists (
        select 1
        from public.checks as c
        where c.due_on = i.due_on
          and (
            (i.template_id is not null and c.template_id = i.template_id)
            or (i.one_off_id is not null and c.one_off_id = i.one_off_id)
          )
      ) then 'done'
      else 'pending'
    end
  where i.due_on = target_due
    and (
      (target_template is not null and i.template_id = target_template)
      or (target_one_off is not null and i.one_off_id = target_one_off)
    );

  return null;
end;
$$;

revoke all on function private.sync_instance_from_check() from public;
grant execute on function private.sync_instance_from_check() to authenticated;

create trigger checks_sync_instance
  after insert or delete on public.checks
  for each row execute function private.sync_instance_from_check();
