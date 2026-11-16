import { redirect } from "next/navigation";
import { DayList } from "@/components/day-list";
import { getSessionState } from "@/lib/auth";
import { buildDay, buildOverdue } from "@/lib/day";
import { formatLongDate, houseToday, parseDateKey } from "@/lib/dates";
import { ensureHouseDay } from "@/lib/ensure-day";
import { loadDay } from "@/lib/load-day";
import { createClient } from "@/lib/supabase/server";
import type { TaskInstance } from "@/lib/types";

export const dynamic = "force-dynamic";

export default async function HojePage({
  searchParams,
}: {
  searchParams: Promise<{ erro?: string }>;
}) {
  const state = await getSessionState();
  if (state.status !== "ready") redirect("/login");

  const today = houseToday();
  const supabase = await createClient();
  await ensureHouseDay(supabase, today);
  const [loaded, overdueResult] = await Promise.all([
    loadDay(today),
    supabase
      .from("task_instances")
      .select("id, template_id, one_off_id, due_on, title, scheduled_time, category, sort_order, status")
      .eq("status", "pending")
      .lt("due_on", today)
      .order("due_on")
      .order("sort_order"),
  ]);
  const overdue = overdueResult.error ? [] : ((overdueResult.data ?? []) as TaskInstance[]);
  const { erro } = await searchParams;
  const sunday = parseDateKey(today)?.getDay() === 0;
  const sections = loaded.ok
    ? [
        ...buildOverdue({
          instances: overdue,
          todayKey: today,
          role: state.profile.role,
        }),
        ...buildDay({
          templates: loaded.templates,
          oneOffs: loaded.oneOffs,
          checks: loaded.checks,
          dateKey: today,
          todayKey: today,
          role: state.profile.role,
        }),
      ]
    : [];

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-semibold">Hoje</h1>
        <p className="text-base text-stone-600">{formatLongDate(today)}</p>
      </div>
      {erro === "gravar" || erro === "cedo" ? (
        <p className="rounded-2xl bg-white px-4 py-3 text-sm text-stone-800 ring-1 ring-stone-200">
          {erro === "cedo"
            ? "Ainda não chegou a hora desta tarefa."
            : "Não deu para gravar esta marcação. Tente de novo."}
        </p>
      ) : null}
      {sunday ? (
        <p className="text-base text-stone-700">
          Domingo é folga. As tarefas da semana aparecem de segunda a sábado.
        </p>
      ) : null}
      {loaded.ok ? (
        <DayList
          sections={sections}
          returnTo="/hoje"
          empty={
            sunday
              ? "Nenhuma tarefa avulsa neste domingo."
              : "Nenhuma tarefa para hoje."
          }
        />
      ) : (
        <p className="text-base text-stone-700">Não foi possível carregar o dia.</p>
      )}
    </div>
  );
}
