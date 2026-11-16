import { notFound, redirect } from "next/navigation";
import { DayList } from "@/components/day-list";
import { openDate } from "@/app/(casa)/session-actions";
import { getSessionState } from "@/lib/auth";
import { buildDay } from "@/lib/day";
import { dateKeyInSaoPaulo, formatLongDate, isDateKey, parseDateKey } from "@/lib/dates";
import { loadDay } from "@/lib/load-day";

export const dynamic = "force-dynamic";

export default async function DiaPage({
  params,
  searchParams,
}: {
  params: Promise<{ date: string }>;
  searchParams: Promise<{ erro?: string }>;
}) {
  const state = await getSessionState();
  if (state.status !== "ready") redirect("/login");
  if (state.profile.role !== "manager") redirect("/hoje");

  const { date } = await params;
  if (!isDateKey(date)) notFound();

  const today = dateKeyInSaoPaulo();
  const loaded = await loadDay(date);
  const { erro } = await searchParams;
  const sunday = parseDateKey(date)?.getDay() === 0;

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-semibold">{date === today ? "Hoje" : "Dia"}</h1>
        <p className="text-base text-stone-600">{formatLongDate(date)}</p>
      </div>
      <form action={openDate} className="flex items-end gap-2">
        <label className="block flex-1 text-sm font-medium text-stone-700" htmlFor="date">
          Escolher data
          <input
            id="date"
            name="date"
            type="date"
            required
            defaultValue={date}
            className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 bg-white px-3"
          />
        </label>
        <button
          type="submit"
          className="min-h-12 rounded-xl bg-emerald-900 px-4 font-medium text-white"
        >
          Ver
        </button>
      </form>
      {erro === "gravar" ? (
        <p className="rounded-2xl bg-white px-4 py-3 text-sm text-stone-800 ring-1 ring-stone-200">
          Não deu para gravar esta marcação. Tente de novo.
        </p>
      ) : null}
      {sunday ? (
        <p className="text-base text-stone-700">Domingo é folga na lista recorrente.</p>
      ) : null}
      {loaded.ok ? (
        <DayList
          sections={buildDay({
            templates: loaded.templates,
            oneOffs: loaded.oneOffs,
            checks: loaded.checks,
            dateKey: date,
            todayKey: today,
            role: state.profile.role,
          })}
          dueOn={date}
          returnTo={`/dia/${date}`}
          empty="Nenhuma tarefa nesta data."
        />
      ) : (
        <p className="text-base text-stone-700">Não foi possível carregar o dia.</p>
      )}
    </div>
  );
}
