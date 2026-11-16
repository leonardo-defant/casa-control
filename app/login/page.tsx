import { redirect } from "next/navigation";
import { getSessionState, supabaseConfigured } from "@/lib/auth";
import { login } from "@/app/login/actions";

export const dynamic = "force-dynamic";

const ERRORS: Record<string, string> = {
  credencial: "E-mail ou senha não conferem.",
  convite: "O convite não abriu. Peça um novo ao Léo.",
  config: "O app ainda não está ligado a um projeto Supabase.",
};

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ erro?: string }>;
}) {
  const configured = supabaseConfigured();
  if (configured) {
    const state = await getSessionState();
    if (state.status === "ready") redirect("/hoje");
  }

  const { erro } = await searchParams;
  const message = erro ? ERRORS[erro] : null;

  return (
    <main className="mx-auto flex min-h-dvh w-full max-w-lg flex-col justify-center px-4 py-10">
      <h1 className="text-3xl font-semibold text-stone-900">Casa Control</h1>
      <p className="mt-2 text-base text-stone-600">
        Entre com o e-mail e a senha da sua conta.
      </p>
      {message ? (
        <p className="mt-4 rounded-2xl bg-white px-4 py-3 text-sm text-stone-800 ring-1 ring-stone-200">
          {message}
        </p>
      ) : null}
      {configured ? (
        <form action={login} className="mt-6 space-y-4">
          <label className="block text-sm font-medium text-stone-700" htmlFor="email">
            E-mail
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="username"
              required
              className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 bg-white px-3"
            />
          </label>
          <label className="block text-sm font-medium text-stone-700" htmlFor="password">
            Senha
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 bg-white px-3"
            />
          </label>
          <button
            type="submit"
            className="min-h-12 w-full rounded-xl bg-emerald-900 font-medium text-white"
          >
            Entrar
          </button>
        </form>
      ) : (
        <div className="mt-6 space-y-3 rounded-2xl bg-white p-4 text-sm leading-6 text-stone-700 ring-1 ring-stone-200">
          <p>Faltam as variáveis de ambiente do Supabase:</p>
          <ul className="list-disc pl-5">
            <li>NEXT_PUBLIC_SUPABASE_URL</li>
            <li>NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY</li>
          </ul>
          <p>
            Se o projeto ainda mostrar a chave anon, use NEXT_PUBLIC_SUPABASE_ANON_KEY
            no lugar da publishable.
          </p>
        </div>
      )}
    </main>
  );
}
