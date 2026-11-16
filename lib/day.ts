import { formatClock, parseDateKey, weekdayName } from "@/lib/dates";
import { appliesOn } from "@/lib/schedule";
import type { AppRole, OneOffTask, TaskCheck, TaskTemplate } from "@/lib/types";

export type DayItem = {
  key: string;
  title: string;
  timeLabel: string | null;
  detail: string | null;
  checked: boolean;
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

function detailFor(check: TaskCheck): string {
  const prefix = check.source === "archive" ? "Registro importado" : "Feito";
  return `${prefix} às ${formatClock(check.checked_at)} por ${check.actor_name}`;
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

export function progress(sections: DaySection[]): { done: number; total: number } {
  const items = sections
    .filter((section) => section.countsTowardProgress)
    .flatMap((section) => section.items);
  return {
    done: items.filter((item) => item.checked).length,
    total: items.length,
  };
}

export function buildDay(input: {
  templates: TaskTemplate[];
  oneOffs: OneOffTask[];
  checks: TaskCheck[];
  dateKey: string;
  todayKey: string;
  role: AppRole;
}): DaySection[] {
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
    return {
      key: `t-${template.id}`,
      title: template.title,
      timeLabel: clockLabel(template.scheduled_time),
      detail: check ? detailFor(check) : null,
      checked: Boolean(check),
      source: check?.source ?? null,
      templateId: template.id,
      oneOffId: null,
      canToggle: allowToggle({
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
      return {
        key: `o-${task.id}`,
        title: task.title,
        timeLabel: null,
        detail: check ? detailFor(check) : null,
        checked: Boolean(check),
        source: check?.source ?? null,
        templateId: null,
        oneOffId: task.id,
        canToggle: allowToggle({
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
