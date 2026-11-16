import { redirect } from "next/navigation";
import { updatePassword } from "@/app/(casa)/session-actions";
import { getSessionState } from "@/lib/auth";

export const dynamic = "force-dynamic";

const ERRORS: Record<string, string> = {
  curta: "Use pelo menos 8 caracteres.",
  diferente: "As senhas não são iguais.",
  gravar: "Não deu para salvar a senha. Tente de novo.",
};

export default async function ContaPage({
  searchParams,
}: {
  searchParams: Promise<{ erro?: string; ok?: string }>;
}) {
  const state = await getSessionState();
  if (state.status !== "ready") redirect("/login");
  const { erro, ok } = await searchParams;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Senha</h1>
      <p className="text-base text-stone-600">
        Defina uma senha para entrar de novo neste celular, mesmo depois de
        fechar o app.
      </p>
      {ok ? (
        <p className="rounded-2xl bg-white px-4 py-3 text-sm text-stone-800 ring-1 ring-stone-200">
          Senha salva.
        </p>
      ) : null}
      {erro && ERRORS[erro] ? (
        <p className="rounded-2xl bg-white px-4 py-3 text-sm text-stone-800 ring-1 ring-stone-200">
          {ERRORS[erro]}
        </p>
      ) : null}
      <form action={updatePassword} className="space-y-4">
        <label className="block text-sm font-medium text-stone-700" htmlFor="password">
          Nova senha
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="new-password"
            minLength={8}
            required
            className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 bg-white px-3"
          />
        </label>
        <label className="block text-sm font-medium text-stone-700" htmlFor="confirm">
          Repetir senha
          <input
            id="confirm"
            name="confirm"
            type="password"
            autoComplete="new-password"
            minLength={8}
            required
            className="mt-1 min-h-12 w-full rounded-xl border border-stone-300 bg-white px-3"
          />
        </label>
        <button
          type="submit"
          className="min-h-12 w-full rounded-xl bg-emerald-900 font-medium text-white"
        >
          Salvar senha
        </button>
      </form>
    </div>
  );
}
