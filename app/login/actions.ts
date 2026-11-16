"use server";

import { redirect } from "next/navigation";
import { supabaseConfigured } from "@/lib/auth";
import { createClient } from "@/lib/supabase/server";

export async function login(formData: FormData) {
  if (!supabaseConfigured()) redirect("/login?erro=config");

  const email = String(formData.get("email") ?? "").trim().toLowerCase();
  const password = String(formData.get("password") ?? "");
  const supabase = await createClient();
  const { error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) redirect("/login?erro=credencial");
  redirect("/hoje");
}
