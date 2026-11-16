import "server-only";

import { supabaseEnv } from "@/lib/env";
import { createClient } from "@/lib/supabase/server";
import type { Profile } from "@/lib/types";

export type SessionState =
  | { status: "anonymous" }
  | { status: "unprovisioned" }
  | { status: "ready"; profile: Profile };

export function supabaseConfigured(): boolean {
  return supabaseEnv() !== null;
}

export async function getSessionState(): Promise<SessionState> {
  if (!supabaseConfigured()) return { status: "anonymous" };

  const supabase = await createClient();
  const { data, error } = await supabase.auth.getClaims();
  const userId = data?.claims?.sub;
  if (error || !userId) return { status: "anonymous" };

  const { data: profile } = await supabase
    .from("profiles")
    .select("id, full_name, role")
    .eq("id", userId)
    .maybeSingle();

  if (!profile) return { status: "unprovisioned" };
  return { status: "ready", profile: profile as Profile };
}
