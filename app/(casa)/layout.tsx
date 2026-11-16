import type { ReactNode } from "react";
import { redirect } from "next/navigation";
import { Header } from "@/components/header";
import { getSessionState, supabaseConfigured } from "@/lib/auth";

export const dynamic = "force-dynamic";

export default async function CasaLayout({ children }: { children: ReactNode }) {
  if (!supabaseConfigured()) redirect("/login");
  const state = await getSessionState();
  if (state.status === "anonymous") redirect("/login");
  if (state.status === "unprovisioned") {
    return (
      <main className="mx-auto w-full max-w-lg px-4 py-10">
        <h1 className="text-2xl font-semibold">Conta sem acesso</h1>
        <p className="mt-3 text-base leading-6 text-stone-700">
          O login entrou, mas esta conta não está liberada na casa.
        </p>
      </main>
    );
  }

  return (
    <>
      <Header profile={state.profile} />
      <main className="mx-auto w-full max-w-lg px-4 py-5 pb-[calc(2rem+env(safe-area-inset-bottom))]">
        {children}
      </main>
    </>
  );
}
