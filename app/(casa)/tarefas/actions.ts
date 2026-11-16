"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { getSessionState } from "@/lib/auth";
import { isDateKey } from "@/lib/dates";
import { createClient } from "@/lib/supabase/server";

async function requireManager() {
  const state = await getSessionState();
  if (state.status !== "ready") redirect("/login");
  if (state.profile.role !== "manager") redirect("/hoje");
  return { state, supabase: await createClient() };
}

function cleanTitle(value: FormDataEntryValue | null): string {
  return String(value ?? "").trim().slice(0, 200);
}

function cleanTime(value: FormDataEntryValue | null): string | null {
  const time = String(value ?? "");
  if (!time) return null;
  if (!/^\d{2}:\d{2}$/.test(time)) return null;
  return time;
}

export async function updateTemplate(formData: FormData) {
  const { supabase } = await requireManager();
  const id = String(formData.get("id") ?? "");
  const title = cleanTitle(formData.get("title"));
  const time = cleanTime(formData.get("scheduledTime"));
  const active = formData.get("active") === "on";
  if (!id || !title) redirect("/tarefas?erro=titulo");

  const { error } = await supabase
    .from("task_templates")
    .update({
      title,
      scheduled_time: time,
      active,
    })
    .eq("id", id);

  if (error) redirect("/tarefas?erro=gravar");
  revalidatePath("/tarefas");
  revalidatePath("/hoje");
}

export async function createTemplate(formData: FormData) {
  const { state, supabase } = await requireManager();
  const title = cleanTitle(formData.get("title"));
  const kind = String(formData.get("kind") ?? "");
  const weekdayRaw = String(formData.get("weekday") ?? "");
  const time = cleanTime(formData.get("scheduledTime"));
  const groupName = cleanTitle(formData.get("groupName"));
  if (!title) redirect("/tarefas?erro=titulo");

  let category: "routine" | "weekday" | "eventual";
  let recurrenceKind: "daily" | "weekly" | "eventual";
  let weekday: number | null = null;
  let activeWeekdays: number[];

  if (kind === "diaria") {
    category = "routine";
    recurrenceKind = "daily";
    activeWeekdays = [1, 2, 3, 4, 5, 6];
  } else if (kind === "semanal") {
    const weekdayNumber = Number(weekdayRaw);
    if (!Number.isInteger(weekdayNumber) || weekdayNumber < 0 || weekdayNumber > 6) {
      redirect("/tarefas?erro=dia");
    }
    category = "weekday";
    recurrenceKind = "weekly";
    weekday = weekdayNumber;
    activeWeekdays = [weekdayNumber];
  } else if (kind === "eventual") {
    category = "eventual";
    recurrenceKind = "eventual";
    activeWeekdays = [1, 2, 3, 4, 5, 6];
  } else {
    redirect("/tarefas?erro=gravar");
  }

  const { data: last } = await supabase
    .from("task_templates")
    .select("sort_order")
    .order("sort_order", { ascending: false })
    .limit(1)
    .maybeSingle();

  const { error } = await supabase.from("task_templates").insert({
    title,
    category,
    group_name:
      category === "eventual" ? groupName || "Quando precisar" : category === "routine" ? "Rotina do dia" : null,
    weekday,
    scheduled_time: time,
    sort_order: (last?.sort_order ?? 0) + 1,
    active: true,
    recurrence_kind: recurrenceKind,
    recurrence_interval: 1,
    active_weekdays: activeWeekdays,
    created_by: state.profile.id,
  });

  if (error) redirect("/tarefas?erro=gravar");
  revalidatePath("/tarefas");
  revalidatePath("/hoje");
}

export async function createOneOff(formData: FormData) {
  const { state, supabase } = await requireManager();
  const title = cleanTitle(formData.get("title"));
  const dueOn = String(formData.get("dueOn") ?? "");
  if (!title) redirect("/tarefas?erro=titulo");
  if (!isDateKey(dueOn)) redirect("/tarefas?erro=data");

  const { error } = await supabase.from("one_off_tasks").insert({
    title,
    due_on: dueOn,
    active: true,
    created_by: state.profile.id,
  });

  if (error) redirect("/tarefas?erro=gravar");
  revalidatePath("/tarefas");
  revalidatePath("/hoje");
  revalidatePath(`/dia/${dueOn}`);
}

export async function pauseOneOff(formData: FormData) {
  const { supabase } = await requireManager();
  const id = String(formData.get("id") ?? "");
  if (!id) redirect("/tarefas?erro=gravar");
  const { error } = await supabase
    .from("one_off_tasks")
    .update({ active: false })
    .eq("id", id);
  if (error) redirect("/tarefas?erro=gravar");
  revalidatePath("/tarefas");
  revalidatePath("/hoje");
}
