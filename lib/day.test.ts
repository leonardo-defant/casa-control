import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { houseToday, isBeforeWindow, isDateKey, markTiming } from "@/lib/dates";
import { buildDay, buildOverdue, progress } from "@/lib/day";
import { appliesOn } from "@/lib/schedule";
import type { TaskTemplate } from "@/lib/types";

function template(partial: Partial<TaskTemplate> & Pick<TaskTemplate, "id" | "title">): TaskTemplate {
  return {
    code: null,
    category: "routine",
    group_name: "Rotina do dia",
    weekday: null,
    scheduled_time: null,
    sort_order: 1,
    active: true,
    recurrence_kind: "daily",
    recurrence_interval: 1,
    active_weekdays: [1, 2, 3, 4, 5, 6],
    starts_on: null,
    ends_on: null,
    ...partial,
  };
}

test("domingo nao entra na rotina de segunda a sabado", () => {
  const daily = template({ id: "1", title: "Rotina" });
  assert.equal(appliesOn(daily, "2026-11-15"), false);
  assert.equal(appliesOn(daily, "2026-11-16"), true);
});

test("tarefa semanal so aparece no dia marcado", () => {
  const friday = template({
    id: "2",
    title: "Sexta",
    category: "weekday",
    recurrence_kind: "weekly",
    weekday: 5,
    active_weekdays: [5],
  });
  assert.equal(appliesOn(friday, "2026-11-20"), true);
  assert.equal(appliesOn(friday, "2026-11-16"), false);
});

test("lista de hoje marca quem fez e o horario real", () => {
  const sections = buildDay({
    templates: [template({ id: "1", title: "Piscina", scheduled_time: "08:00:00" })],
    oneOffs: [],
    checks: [
      {
        id: "c1",
        template_id: "1",
        one_off_id: null,
        due_on: "2026-11-16",
        checked_at: "2026-11-16T14:05:00.000Z",
        checked_by: "user",
        actor_name: "Jonas",
        source: "app",
        legacy_code: null,
      },
    ],
    dateKey: "2026-11-16",
    todayKey: "2026-11-16",
    role: "executor",
  });
  const item = sections[0]?.items[0];
  assert.equal(item?.checked, true);
  assert.equal(item?.timeLabel, "08:00");
  assert.match(item?.detail ?? "", /Feito às 10:05 por Jonas/);
  assert.equal(progress(sections).done, 1);
});

test("registro importado nao pode ser desmarcado", () => {
  const sections = buildDay({
    templates: [template({ id: "1", title: "Rotina" })],
    oneOffs: [],
    checks: [
      {
        id: "c1",
        template_id: "1",
        one_off_id: null,
        due_on: "2026-03-02",
        checked_at: "2026-03-02T11:00:00.000Z",
        checked_by: null,
        actor_name: "Jonas",
        source: "archive",
        legacy_code: "dr1",
      },
    ],
    dateKey: "2026-03-02",
    todayKey: "2026-11-16",
    role: "manager",
  });
  assert.equal(sections[0]?.items[0]?.canToggle, false);
  assert.match(sections[0]?.items[0]?.detail ?? "", /Registro importado/);
});

test("executor nao marca dia passado", () => {
  const sections = buildDay({
    templates: [template({ id: "1", title: "Rotina" })],
    oneOffs: [],
    checks: [],
    dateKey: "2026-03-02",
    todayKey: "2026-11-16",
    role: "executor",
  });
  assert.equal(sections[0]?.items[0]?.canToggle, false);
});

test("o dia da casa e o de Cuiaba", () => {
  assert.equal(houseToday(new Date("2026-11-16T02:30:00.000Z")), "2026-11-15");
  assert.equal(houseToday(new Date("2026-11-16T03:30:00.000Z")), "2026-11-15");
  assert.equal(isDateKey("2026-02-31"), false);
  assert.equal(isDateKey("2026-11-16"), true);
});

test("tarefa com hora fica fechada ate uma hora antes", () => {
  const sections = buildDay({
    templates: [template({ id: "1", title: "Creche", scheduled_time: "14:00:00", category: "weekday" })],
    oneOffs: [],
    checks: [],
    dateKey: "2026-11-16",
    todayKey: "2026-11-16",
    role: "executor",
    now: new Date("2026-11-16T15:00:00.000Z"),
  });
  const item = sections[0]?.items[0];
  assert.equal(item?.canToggle, false);
  assert.match(item?.detail ?? "", /Libera às 13:00/);
  assert.equal(
    isBeforeWindow({
      dueOn: "2026-11-16",
      todayKey: "2026-11-16",
      scheduled: "14:00:00",
      now: new Date("2026-11-16T17:30:00.000Z"),
    }),
    false,
  );
});

test("marcacao muito antes nao conta e atraso fica visivel", () => {
  assert.equal(
    markTiming({
      dueOn: "2026-11-16",
      scheduled: "14:00:00",
      checkedAt: "2026-11-16T12:00:00.000Z",
    }),
    "early",
  );
  assert.equal(
    markTiming({
      dueOn: "2026-11-16",
      scheduled: "08:00:00",
      checkedAt: "2026-11-16T16:30:00.000Z",
    }),
    "late",
  );
  const sections = buildDay({
    templates: [template({ id: "1", title: "Creche", scheduled_time: "14:00:00" })],
    oneOffs: [],
    checks: [
      {
        id: "c1",
        template_id: "1",
        one_off_id: null,
        due_on: "2026-11-16",
        checked_at: "2026-11-16T12:00:00.000Z",
        checked_by: "user",
        actor_name: "Jonas",
        source: "app",
        legacy_code: null,
      },
    ],
    dateKey: "2026-11-16",
    todayKey: "2026-11-16",
    role: "executor",
    now: new Date("2026-11-16T12:00:00.000Z"),
  });
  assert.equal(sections[0]?.items[0]?.countsAsDone, false);
  assert.equal(progress(sections).done, 0);
  assert.match(sections[0]?.items[0]?.detail ?? "", /antes do horário/);
});

test("atrasada de ontem continua na lista de hoje", () => {
  const sections = buildOverdue({
    instances: [
      {
        id: "i1",
        template_id: "t1",
        one_off_id: null,
        due_on: "2026-11-15",
        title: "Piscina",
        scheduled_time: "08:00:00",
        category: "routine",
        sort_order: 1,
        status: "pending",
      },
    ],
    todayKey: "2026-11-16",
    role: "executor",
  });
  assert.equal(sections[0]?.title, "Atrasadas");
  assert.equal(sections[0]?.items[0]?.canToggle, true);
  assert.equal(sections[0]?.items[0]?.dueOn, "2026-11-15");
});

test("arquivo sql traz 508 marcacoes", () => {
  const sql = readFileSync(
    new URL("../supabase/migrations/20261116115313_archive_checks.sql", import.meta.url),
    "utf8",
  );
  const rows = sql.match(/::date/g) ?? [];
  assert.equal(rows.length, 508);
});
