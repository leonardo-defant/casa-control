import { NextResponse } from "next/server";
import { supabaseEnv } from "@/lib/env";
import { createClient } from "@/lib/supabase/server";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  if (!supabaseEnv()) {
    return NextResponse.redirect(new URL("/login?erro=config", url.origin));
  }
  const next = url.searchParams.get("next") ?? "/hoje";
  const safeNext = next.startsWith("/") && !next.startsWith("//") ? next : "/hoje";

  if (code) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) {
      return NextResponse.redirect(new URL(safeNext, url.origin));
    }
  }

  return NextResponse.redirect(new URL("/login?erro=credencial", url.origin));
}
