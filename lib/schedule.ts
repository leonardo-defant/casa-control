import { parseDateKey } from "@/lib/dates";
import type { TaskTemplate } from "@/lib/types";

type ScheduleTemplate = Pick<
  TaskTemplate,
  "active" | "recurrence_kind" | "active_weekdays" | "starts_on" | "ends_on"
>;

// recurrence_interval fica gravado para a fase 2.
// Nesta fase a lista do dia usa active_weekdays, starts_on e ends_on.
export function appliesOn(template: ScheduleTemplate, dateKey: string): boolean {
  if (!template.active) return false;
  if (template.starts_on && dateKey < template.starts_on) return false;
  if (template.ends_on && dateKey > template.ends_on) return false;
  const date = parseDateKey(dateKey);
  if (!date) return false;
  if (template.recurrence_kind === "none") return false;
  return template.active_weekdays.includes(date.getDay());
}
