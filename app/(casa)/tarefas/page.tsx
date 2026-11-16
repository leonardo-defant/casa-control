import { redirect } from "next/navigation";
import {
  createOneOff,
  createTemplate,
  pauseOneOff,
  updateTemplate,
} from "@/app/(casa)/tarefas/actions";
import { getSessionState } from "@/lib/auth";
import { WEEKDAY_NAMES, dateKeyInSaoPaulo } from "@/lib/dates";
import { createClient } from "@/lib/supabase/server";
import type { OneOffTask, TaskTemplate } from "@/lib/types";

export const dynamic = "force-dynamic";

const ERRORS: Record<string, string> = {
  titulo: "Escreva o nome da tarefa.",
  dia: "Escolha o dia da semana.",
  data: "Escolha uma data válida.",
  gravar: "Não deu para salvar. Tente de novo.",
};

export default async function TarefasPage({
  searchParams,
}: {
  searchParams: Promise<{ erro?: string }>;
}) {
  const state = await getSessionState();
  if (state.status !== "ready") redirect("/login");
  if (state.profile.role !== "manager") redirect("/hoje");

  const { erro } = await searchParams;
  const supabase = await createClient();
  const today = dateKeyInSaoPaulo();
  const [templatesResult, oneOffResult] = await Promise.all([
    supabase.from("task_templates").select("*").order("sort_order"),
    supabase
      .from("one_off_tasks")
      .select("id, title, due_on, active, sort_order")
      .eq("active", true)
      .gte("due_on", today)
      .order("due_on"),
  ]);

  const templates = (templatesResult.data ?? []) as TaskTemplate[];
  const oneOffs = (oneOffResult.data ?? []) as OneOffTask[];
  const groups = [
    { title: "Compromissos fixos", items: templates.filter((item) => item.category === "fixed") },
    { title: "Rotina do dia", items: templates.filter((item) => item.category === "routine") },
    { title: "Dias da semana", items: templates.filter((item) => item.category === "weekday") },
    { title: "Quando precisar", items: templates.filter((item) => item.category === "eventual") },
  ];

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-semibold">Tarefas</h1>
      {erro && ERRORS[erro] ? (
        <p className="rounded-2xl bg-white px-4 py-3 text-sm text-stone-800 ring-1 ring-stone-200">
          {ERRORS[erro]}
        </p>
      ) : null}

      <section className="space-y-3 rounded-2xl bg-white p-4 ring-1 ring-stone-200">
        <h2 className="text-lg font-semibold">Nova tarefa avulsa</h2>
        <form action={createOneOff} className="space-y-3">
          <label className="block text-sm font-medium" htmlFor="oneoff-title">
            Nome
            <input
              id="oneoff-title"
              name="title"
              required
              className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 px-3"
            />
          </label>
          <label className="block text-sm font-medium" htmlFor="oneoff-date">
            Data
            <input
              id="oneoff-date"
              name="dueOn"
              type="date"
              required
              defaultValue={today}
              className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 px-3"
            />
          </label>
          <button type="submit" className="min-h-12 w-full rounded-xl bg-emerald-900 font-medium text-white">
            Criar avulsa
          </button>
        </form>
        {oneOffs.length > 0 ? (
          <ul className="space-y-2">
            {oneOffs.map((task) => (
              <li key={task.id} className="flex items-center justify-between gap-3 text-sm">
                <span>
                  {task.due_on}: {task.title}
                </span>
                <form action={pauseOneOff}>
                  <input type="hidden" name="id" value={task.id} />
                  <button type="submit" className="min-h-11 px-2 font-medium text-stone-700">
                    Cancelar
                  </button>
                </form>
              </li>
            ))}
          </ul>
        ) : null}
      </section>

      <section className="space-y-3 rounded-2xl bg-white p-4 ring-1 ring-stone-200">
        <h2 className="text-lg font-semibold">Nova tarefa da lista</h2>
        <form action={createTemplate} className="space-y-3">
          <label className="block text-sm font-medium" htmlFor="template-title">
            Nome
            <input
              id="template-title"
              name="title"
              required
              className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 px-3"
            />
          </label>
          <label className="block text-sm font-medium" htmlFor="template-kind">
            Tipo
            <select
              id="template-kind"
              name="kind"
              defaultValue="diaria"
              className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 bg-white px-3"
            >
              <option value="diaria">Todo dia, de segunda a sábado</option>
              <option value="semanal">Um dia da semana</option>
              <option value="eventual">Quando precisar</option>
            </select>
          </label>
          <label className="block text-sm font-medium" htmlFor="template-weekday">
            Dia, se for semanal
            <select
              id="template-weekday"
              name="weekday"
              defaultValue="1"
              className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 bg-white px-3"
            >
              {WEEKDAY_NAMES.map((name, index) => (
                <option key={name} value={index}>
                  {name}
                </option>
              ))}
            </select>
          </label>
          <label className="block text-sm font-medium" htmlFor="template-time">
            Horário, se tiver
            <input
              id="template-time"
              name="scheduledTime"
              type="time"
              className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 px-3"
            />
          </label>
          <label className="block text-sm font-medium" htmlFor="template-group">
            Grupo, se for quando precisar
            <input
              id="template-group"
              name="groupName"
              className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 px-3"
            />
          </label>
          <button type="submit" className="min-h-12 w-full rounded-xl bg-emerald-900 font-medium text-white">
            Criar tarefa
          </button>
        </form>
      </section>

      {groups.map((group) => (
        <section key={group.title} className="space-y-3">
          <h2 className="text-lg font-semibold">{group.title}</h2>
          {group.items.map((template) => (
            <form
              key={template.id}
              action={updateTemplate}
              className="space-y-3 rounded-2xl bg-white p-4 ring-1 ring-stone-200"
            >
              <input type="hidden" name="id" value={template.id} />
              <label className="block text-sm font-medium" htmlFor={`title-${template.id}`}>
                Nome
                <input
                  id={`title-${template.id}`}
                  name="title"
                  defaultValue={template.title}
                  required
                  className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 px-3"
                />
              </label>
              <label className="block text-sm font-medium" htmlFor={`time-${template.id}`}>
                Horário
                <input
                  id={`time-${template.id}`}
                  name="scheduledTime"
                  type="time"
                  defaultValue={template.scheduled_time?.slice(0, 5) ?? ""}
                  className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 px-3"
                />
              </label>
              <label className="flex min-h-11 items-center gap-2 text-sm font-medium">
                <input
                  type="checkbox"
                  name="active"
                  value="on"
                  defaultChecked={template.active}
                />
                Ativa
              </label>
              <button type="submit" className="min-h-11 rounded-xl px-3 font-medium text-emerald-900">
                Salvar
              </button>
            </form>
          ))}
        </section>
      ))}
    </div>
  );
}
