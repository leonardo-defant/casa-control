import { createBrowserClient } from "@supabase/ssr";
import { supabaseEnv } from "@/lib/env";

export function createClient() {
  const env = supabaseEnv();
  if (!env) {
    throw new Error("Supabase nao configurado");
  }
  return createBrowserClient(env.url, env.key);
}
