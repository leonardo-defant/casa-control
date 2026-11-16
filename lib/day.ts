import {
  formatClock,
  formatHouseClock,
  formatLongDate,
  isBeforeWindow,
  markTiming,
  parseDateKey,
  releaseAt,
  weekdayName,
} from "@/lib/dates";
import { appliesOn } from "@/lib/schedule";
import type { AppRole, OneOffTask, TaskCheck, TaskInstance, TaskTemplate } from "@/lib/types";

export type DayItem = {
  key: string;
  dueOn: string;
  title: string;
  timeLabel: string | null;
  dateLabel: string | null;
  detail: string | null;
  checked: boolean;
  countsAsDone: boolean;
  source: "app" | "archive" | null;
  templateId: string | null;
  oneOffId: string | null;
  canToggle: boolean;
};

export type DaySection = {
  id: string;
  title: string;
  countsTowardProgress: boolean;
  items: DayItem[];
};

function clockLabel(value: string | null): string | null {
  if (!value) return null;
  return value.slice(0, 5);
}

function detailFor(input: {
  check: TaskCheck;
  dueOn: string;
  scheduled: string | null;
}): string {
  const clock = formatClock(input.check.checked_at);
  const who = input.check.actor_name;
  if (input.check.source === "archive") {
    return `Registro importado às ${clock} por ${who}`;
  }
  const timing = markTiming({
    dueOn: input.dueOn,
    scheduled: input.scheduled,
    checkedAt: input.check.checked_at,
  });
  if (timing === "early") {
    return `Marcado antes do horário, às ${clock}, por ${who}. Toque para desfazer.`;
  }
  if (timing === "late") {
    return `Feito com atraso às ${clock} por ${who}`;
  }
  return `Feito às ${clock} por ${who}`;
}

function countsAsDone(input: {
  check: TaskCheck | null;
  dueOn: string;
  scheduled: string | null;
}): boolean {
  if (!input.check) return false;
  if (input.check.source === "archive") return true;
  return (
    markTiming({
      dueOn: input.dueOn,
      scheduled: input.scheduled,
      checkedAt: input.check.checked_at,
    }) !== "early"
  );
}

export function progress(sections: DaySection[]): { done: number; total: number } {
  const items = sections
    .filter((section) => section.countsTowardProgress)
    .flatMap((section) => section.items);
  return {
    done: items.filter((item) => item.countsAsDone).length,
    total: items.length,
  };
}

export function buildOverdue(input: {
  instances: TaskInstance[];
  todayKey: string;
  role: AppRole;
}): DaySection[] {
  const items = input.instances
    .filter((instance) => instance.status === "pending" && instance.due_on < input.todayKey)
    .map((instance): DayItem => ({
      key: `late-${instance.id}`,
      dueOn: instance.due_on,
      title: instance.title,
      timeLabel: clockLabel(instance.scheduled_time),
      dateLabel: formatLongDate(instance.due_on),
      detail: null,
      checked: false,
      countsAsDone: false,
      source: null,
      templateId: instance.template_id,
      oneOffId: instance.one_off_id,
      canToggle: input.role === "manager" || input.role === "executor",
    }));

  if (items.length === 0) return [];
  return [
    {
      id: "overdue",
      title: "Atrasadas",
      countsTowardProgress: true,
      items,
    },
  ];
}

export function buildDay(input: {
  templates: TaskTemplate[];
  oneOffs: OneOffTask[];
  checks: TaskCheck[];
  dateKey: string;
  todayKey: string;
  role: AppRole;
  now?: Date;
}): DaySection[] {
  const now = input.now ?? new Date();
  const checkByTemplate = new Map<string, TaskCheck>();
  const checkByOneOff = new Map<string, TaskCheck>();
  for (const check of input.checks) {
    if (check.template_id) checkByTemplate.set(check.template_id, check);
    if (check.one_off_id) checkByOneOff.set(check.one_off_id, check);
  }

  const applicable = input.templates.filter(
    (template) => template.active && appliesOn(template, input.dateKey),
  );
  const applicableIds = new Set(applicable.map((template) => template.id));
  const extras = input.templates.filter(
    (template) => !applicableIds.has(template.id) && checkByTemplate.has(template.id),
  );
  const templates = [...applicable, ...extras].sort((a, b) => a.sort_order - b.sort_order);

  const toTemplateItem = (template: TaskTemplate): DayItem => {
    const check = checkByTemplate.get(template.id) ?? null;
    const locked =
      !check &&
      isBeforeWindow({
        dueOn: input.dateKey,
        todayKey: input.todayKey,
        scheduled: template.scheduled_time,
        now,
      });
    const release = releaseAt(input.dateKey, template.scheduled_time);
    const done = countsAsDone({
      check,
      dueOn: input.dateKey,
      scheduled: template.scheduled_time,
    });
    return {
      key: `t-${template.id}`,
      dueOn: input.dateKey,
      title: template.title,
      timeLabel: clockLabel(template.scheduled_time),
      dateLabel: null,
      detail: check
        ? detailFor({
            check,
            dueOn: input.dateKey,
            scheduled: template.scheduled_time,
          })
        : locked && release
          ? `Libera às ${formatHouseClock(release)}`
          : null,
      checked: Boolean(check),
      countsAsDone: done,
      source: check?.source ?? null,
      templateId: template.id,
      oneOffId: null,
      canToggle: !locked && allowToggle({
        role: input.role,
        dateKey: input.dateKey,
        todayKey: input.todayKey,
        checked: Boolean(check),
        source: check?.source ?? null,
      }),
    };
  };

  const sections: DaySection[] = [];
  const pushCategory = (
    id: string,
    title: string,
    category: TaskTemplate["category"],
    countsTowardProgress: boolean,
  ) => {
    const items = templates
      .filter((template) => template.category === category)
      .map(toTemplateItem);
    if (items.length === 0) return;
    sections.push({ id, title, countsTowardProgress, items });
  };

  pushCategory("fixed", "Compromissos fixos", "fixed", true);
  pushCategory("routine", "Rotina do dia", "routine", true);

  const weekdayItems = templates
    .filter((template) => template.category === "weekday")
    .map(toTemplateItem);
  if (weekdayItems.length > 0) {
    const date = parseDateKey(input.dateKey);
    const name = weekdayName(date ? date.getDay() : -1).toLowerCase();
    sections.push({
      id: "weekday",
      title: name ? `Tarefas de ${name}` : "Tarefas do dia",
      countsTowardProgress: true,
      items: weekdayItems,
    });
  }

  const oneOffItems = input.oneOffs
    .filter(
      (task) =>
        task.due_on === input.dateKey && (task.active || checkByOneOff.has(task.id)),
    )
    .sort((a, b) => a.sort_order - b.sort_order)
    .map((task): DayItem => {
      const check = checkByOneOff.get(task.id) ?? null;
      const locked =
        !check &&
        isBeforeWindow({
          dueOn: input.dateKey,
          todayKey: input.todayKey,
          scheduled: null,
          now,
        });
      return {
        key: `o-${task.id}`,
        dueOn: input.dateKey,
        title: task.title,
        timeLabel: null,
        dateLabel: null,
        detail: check
          ? detailFor({ check, dueOn: input.dateKey, scheduled: null })
          : null,
        checked: Boolean(check),
        countsAsDone: countsAsDone({ check, dueOn: input.dateKey, scheduled: null }),
        source: check?.source ?? null,
        templateId: null,
        oneOffId: task.id,
        canToggle: !locked && allowToggle({
          role: input.role,
          dateKey: input.dateKey,
          todayKey: input.todayKey,
          checked: Boolean(check),
          source: check?.source ?? null,
        }),
      };
    });
  if (oneOffItems.length > 0) {
    sections.push({
      id: "oneoff",
      title: "Avulsas",
      countsTowardProgress: true,
      items: oneOffItems,
    });
  }

  const groups = new Map<string, DayItem[]>();
  for (const template of templates.filter((item) => item.category === "eventual")) {
    const name = template.group_name || "Quando precisar";
    const list = groups.get(name) ?? [];
    list.push(toTemplateItem(template));
    groups.set(name, list);
  }
  for (const [name, items] of groups) {
    sections.push({
      id: `eventual-${name}`,
      title: name,
      countsTowardProgress: false,
      items,
    });
  }

  return sections;
}

function allowToggle(input: {
  role: AppRole;
  dateKey: string;
  todayKey: string;
  checked: boolean;
  source: "app" | "archive" | null;
}): boolean {
  if (input.checked && input.source === "archive") return false;
  if (input.role === "manager") return true;
  return input.dateKey === input.todayKey;
}
