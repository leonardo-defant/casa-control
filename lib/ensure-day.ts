import type { SupabaseClient } from "@supabase/supabase-js";
import { appliesOn } from "@/lib/schedule";
import type { OneOffTask, TaskCheck, TaskTemplate } from "@/lib/types";

export async function ensureHouseDay(
  supabase: SupabaseClient,
  dateKey: string,
): Promise<boolean> {
  const [templatesResult, oneOffResult, checksResult, existingResult] = await Promise.all([
    supabase.from("task_templates").select("*").eq("active", true),
    supabase
      .from("one_off_tasks")
      .select("id, title, due_on, active, sort_order")
      .eq("due_on", dateKey)
      .eq("active", true),
    supabase.from("checks").select("template_id, one_off_id").eq("due_on", dateKey),
    supabase.from("task_instances").select("template_id, one_off_id").eq("due_on", dateKey),
  ]);

  if (
    templatesResult.error ||
    oneOffResult.error ||
    checksResult.error ||
    existingResult.error
  ) {
    return false;
  }

  const templates = (templatesResult.data ?? []) as TaskTemplate[];
  const oneOffs = (oneOffResult.data ?? []) as OneOffTask[];
  const checks = (checksResult.data ?? []) as Pick<TaskCheck, "template_id" | "one_off_id">[];
  const existingTemplates = new Set(
    (existingResult.data ?? [])
      .map((row) => row.template_id as string | null)
      .filter((id): id is string => Boolean(id)),
  );
  const existingOneOffs = new Set(
    (existingResult.data ?? [])
      .map((row) => row.one_off_id as string | null)
      .filter((id): id is string => Boolean(id)),
  );
  const doneTemplates = new Set(
    checks.map((row) => row.template_id).filter((id): id is string => Boolean(id)),
  );
  const doneOneOffs = new Set(
    checks.map((row) => row.one_off_id).filter((id): id is string => Boolean(id)),
  );

  const rows = [
    ...templates
      .filter(
        (template) =>
          template.category !== "eventual" &&
          appliesOn(template, dateKey) &&
          !existingTemplates.has(template.id),
      )
      .map((template) => ({
        template_id: template.id,
        one_off_id: null,
        due_on: dateKey,
        title: template.title,
        scheduled_time: template.scheduled_time,
        category: template.category,
        sort_order: template.sort_order,
        status: doneTemplates.has(template.id) ? "done" : "pending",
      })),
    ...oneOffs
      .filter((task) => !existingOneOffs.has(task.id))
      .map((task) => ({
        template_id: null,
        one_off_id: task.id,
        due_on: dateKey,
        title: task.title,
        scheduled_time: null,
        category: "one_off",
        sort_order: task.sort_order,
        status: doneOneOffs.has(task.id) ? "done" : "pending",
      })),
  ];

  if (rows.length === 0) return true;
  const { error } = await supabase.from("task_instances").insert(rows);
  return !error || error.code === "23505";
}
