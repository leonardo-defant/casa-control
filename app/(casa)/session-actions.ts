"use server";

import { redirect } from "next/navigation";
import { getSessionState } from "@/lib/auth";
import { isDateKey } from "@/lib/dates";
import { createClient } from "@/lib/supabase/server";

export async function signOut() {
  const supabase = await createClient();
  await supabase.auth.signOut();
  redirect("/login");
}

export async function openDate(formData: FormData) {
  const state = await getSessionState();
  if (state.status !== "ready" || state.profile.role !== "manager") {
    redirect("/hoje");
  }
  const date = String(formData.get("date") ?? "");
  if (!isDateKey(date)) redirect("/hoje?erro=data");
  redirect(`/dia/${date}`);
}

export async function updatePassword(formData: FormData) {
  const state = await getSessionState();
  if (state.status !== "ready") redirect("/login");

  const password = String(formData.get("password") ?? "");
  const confirm = String(formData.get("confirm") ?? "");
  if (password.length < 8) redirect("/conta?erro=curta");
  if (password !== confirm) redirect("/conta?erro=diferente");

  const supabase = await createClient();
  const { error } = await supabase.auth.updateUser({ password });
  if (error) redirect("/conta?erro=gravar");
  redirect("/conta?ok=1");
}
