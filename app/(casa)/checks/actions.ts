"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { getSessionState } from "@/lib/auth";
import { houseToday, isDateKey } from "@/lib/dates";
import { createClient } from "@/lib/supabase/server";

function safeReturnTo(value: string, dueOn: string): string {
  if (value === "/hoje") return "/hoje";
  if (value === `/dia/${dueOn}`) return value;
  return dueOn === houseToday() ? "/hoje" : `/dia/${dueOn}`;
}

export async function toggleCheck(formData: FormData) {
  const state = await getSessionState();
  if (state.status !== "ready") redirect("/login");

  const dueOn = String(formData.get("dueOn") ?? "");
  const intent = String(formData.get("intent") ?? "");
  const templateId = String(formData.get("templateId") ?? "");
  const oneOffId = String(formData.get("oneOffId") ?? "");
  const returnTo = safeReturnTo(String(formData.get("returnTo") ?? ""), dueOn);

  if (!isDateKey(dueOn) || (intent !== "check" && intent !== "uncheck")) {
    redirect(`${returnTo}?erro=gravar`);
  }

  const today = houseToday();
  if (state.profile.role !== "manager" && dueOn > today) {
    redirect("/hoje");
  }

  const hasTemplate = templateId.length > 0;
  const hasOneOff = oneOffId.length > 0;
  if (hasTemplate === hasOneOff) redirect(`${returnTo}?erro=gravar`);

  const supabase = await createClient();

  if (intent === "uncheck") {
    let query = supabase
      .from("checks")
      .delete()
      .eq("due_on", dueOn)
      .eq("source", "app");
    query = hasTemplate
      ? query.eq("template_id", templateId)
      : query.eq("one_off_id", oneOffId);
    if (state.profile.role !== "manager") {
      query = query.eq("checked_by", state.profile.id);
    }
    const { error } = await query;
    if (error) redirect(`${returnTo}?erro=gravar`);
  } else {
    const { error } = await supabase.from("checks").insert({
      due_on: dueOn,
      checked_at: new Date().toISOString(),
      checked_by: state.profile.id,
      actor_name: state.profile.full_name,
      source: "app",
      template_id: hasTemplate ? templateId : null,
      one_off_id: hasOneOff ? oneOffId : null,
    });
    if (error && error.code !== "23505") {
      redirect(`${returnTo}?erro=${error.code === "42501" ? "cedo" : "gravar"}`);
    }
  }

  revalidatePath("/hoje");
  revalidatePath(`/dia/${dueOn}`);
}
