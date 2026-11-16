import { redirect } from "next/navigation";
import { DayList } from "@/components/day-list";
import { getSessionState } from "@/lib/auth";
import { buildDay } from "@/lib/day";
import { dateKeyInSaoPaulo, formatLongDate, parseDateKey } from "@/lib/dates";
import { loadDay } from "@/lib/load-day";

export const dynamic = "force-dynamic";

export default async function HojePage({
  searchParams,
}: {
  searchParams: Promise<{ erro?: string }>;
}) {
  const state = await getSessionState();
  if (state.status !== "ready") redirect("/login");

  const today = dateKeyInSaoPaulo();
  const loaded = await loadDay(today);
  const { erro } = await searchParams;
  const sunday = parseDateKey(today)?.getDay() === 0;

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-semibold">Hoje</h1>
        <p className="text-base text-stone-600">{formatLongDate(today)}</p>
      </div>
      {erro === "gravar" ? (
        <p className="rounded-2xl bg-white px-4 py-3 text-sm text-stone-800 ring-1 ring-stone-200">
          Não deu para gravar esta marcação. Tente de novo.
        </p>
      ) : null}
      {sunday ? (
        <p className="text-base text-stone-700">
          Domingo é folga. As tarefas da semana aparecem de segunda a sábado.
        </p>
      ) : null}
      {loaded.ok ? (
        <DayList
          sections={buildDay({
            templates: loaded.templates,
            oneOffs: loaded.oneOffs,
            checks: loaded.checks,
            dateKey: today,
            todayKey: today,
            role: state.profile.role,
          })}
          dueOn={today}
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
