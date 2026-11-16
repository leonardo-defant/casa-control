import { redirect } from "next/navigation";
import { getSessionState, supabaseConfigured } from "@/lib/auth";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  if (!supabaseConfigured()) redirect("/login");
  const state = await getSessionState();
  redirect(state.status === "ready" ? "/hoje" : "/login");
}
