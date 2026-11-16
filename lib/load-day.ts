import "server-only";

import { createClient } from "@/lib/supabase/server";
import type { OneOffTask, TaskCheck, TaskTemplate } from "@/lib/types";

export async function loadDay(dateKey: string): Promise<
  | { ok: true; templates: TaskTemplate[]; oneOffs: OneOffTask[]; checks: TaskCheck[] }
  | { ok: false }
> {
  const supabase = await createClient();
  const [templates, oneOffs, checks] = await Promise.all([
    supabase.from("task_templates").select("*").order("sort_order"),
    supabase
      .from("one_off_tasks")
      .select("id, title, due_on, active, sort_order")
      .eq("due_on", dateKey),
    supabase.from("checks").select("*").eq("due_on", dateKey),
  ]);

  if (templates.error || oneOffs.error || checks.error) return { ok: false };

  return {
    ok: true,
    templates: (templates.data ?? []) as TaskTemplate[],
    oneOffs: (oneOffs.data ?? []) as OneOffTask[],
    checks: (checks.data ?? []) as TaskCheck[],
  };
}
