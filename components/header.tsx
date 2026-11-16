import Link from "next/link";
import { signOut } from "@/app/(casa)/session-actions";
import { houseToday } from "@/lib/dates";
import type { Profile } from "@/lib/types";

export function Header({ profile }: { profile: Profile }) {
  const today = houseToday();
  const roleLabel = profile.role === "manager" ? "acompanhamento" : "execução";

  return (
    <header className="sticky top-0 z-10 border-b border-stone-200 bg-[#f3f0e8]">
      <div className="mx-auto flex w-full max-w-lg items-center justify-between gap-3 px-4 py-3">
        <div>
          <p className="text-base font-semibold text-stone-900">Casa Control</p>
          <p className="text-sm text-stone-600">
            {profile.full_name}, {roleLabel}
          </p>
        </div>
        <form action={signOut}>
          <button
            type="submit"
            className="min-h-11 rounded-xl px-3 text-sm font-medium text-stone-700"
          >
            Sair
          </button>
        </form>
      </div>
      <nav className="mx-auto flex w-full max-w-lg gap-2 overflow-x-auto px-4 pb-3">
        <NavLink href="/hoje">Hoje</NavLink>
        {profile.role === "manager" ? (
          <>
            <NavLink href={`/dia/${today}`}>Outro dia</NavLink>
            <NavLink href="/tarefas">Tarefas</NavLink>
          </>
        ) : null}
        <NavLink href="/conta">Senha</NavLink>
      </nav>
    </header>
  );
}

function NavLink({ href, children }: { href: string; children: string }) {
  return (
    <Link
      href={href}
      className="inline-flex min-h-11 items-center rounded-full bg-white px-4 text-sm font-medium text-stone-800 ring-1 ring-stone-200"
    >
      {children}
    </Link>
  );
}
