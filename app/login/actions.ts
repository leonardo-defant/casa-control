"use server";

import { redirect } from "next/navigation";
import { supabaseConfigured } from "@/lib/auth";
import { emailForUsername } from "@/lib/usernames";
import { createClient } from "@/lib/supabase/server";

export async function login(formData: FormData) {
  if (!supabaseConfigured()) redirect("/login?erro=config");

  const email = emailForUsername(String(formData.get("username") ?? ""));
  const password = String(formData.get("password") ?? "");
  if (!email || !password) redirect("/login?erro=credencial");

  const supabase = await createClient();
  const { error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) redirect("/login?erro=credencial");
  redirect("/hoje");
}
