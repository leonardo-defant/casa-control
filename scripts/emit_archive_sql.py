#!/usr/bin/env python3
"""Gera o INSERT das marcacoes historicas a partir do export do Firebase."""

import json
from pathlib import Path

SRC = Path("archive/firebase-export-2026-11-16.json")
OUT = Path("supabase/migrations/20261116115313_archive_checks.sql")


def q(value):
    return "'" + value.replace("'", "''") + "'"


data = json.loads(SRC.read_text(encoding="utf-8"))
rows = []
for day, items in sorted((data.get("checks") or {}).items()):
    if not isinstance(items, dict):
        continue
    for code, value in sorted(items.items()):
        if not isinstance(value, dict) or not value.get("checked"):
            continue
        actor = value.get("by") or ""
        at = value.get("at") or ""
        if not actor or not at:
            raise SystemExit(f"marcacao incompleta em {day} {code}")
        rows.append(
            f"  ({q(day)}::date, {q(code)}, {q(at)}::timestamptz, {q(actor)})"
        )

if len(rows) != 508:
    raise SystemExit(f"esperava 508 marcacoes, veio {len(rows)}")

sql = """-- Marcacoes copiadas de archive/firebase-export-2026-11-16.json.
-- source = archive, checked_by nulo. O nome fica em actor_name.

insert into public.checks (
  template_id, due_on, checked_at, actor_name, source, legacy_code
)
select t.id, v.due_on, v.checked_at, v.actor_name, 'archive', v.legacy_code
from (
  values
"""
sql += ",\n".join(rows)
sql += """
) as v(due_on, legacy_code, checked_at, actor_name)
join public.task_templates as t on t.code = v.legacy_code;

do $$
declare
  imported integer;
begin
  select count(*) into imported
  from public.checks
  where source = 'archive';

  if imported <> 508 then
    raise exception 'Arquivo historico esperava 508 marcacoes, veio %', imported;
  end if;
end $$;
"""
OUT.write_text(sql, encoding="utf-8")
print(f"{len(rows)} checks -> {OUT}")
