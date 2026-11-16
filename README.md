# Casa Control

App da casa para o Jonas executar as tarefas e para o Léo e a Bárbara acompanharem. Esta branch é a fase 1. Ela não substitui a URL de produção até você decidir o merge.

A página antiga está em `archive/legacy-index.html`. O passo a passo da contenção do Firebase e da branch eleitoral está em `docs/contencao.md`.

## O que você precisa criar

Um projeto Supabase novo. Este repositório não tem acesso à sua conta.

1. Crie o projeto em https://supabase.com/dashboard.
2. No SQL Editor, rode os arquivos de `supabase/migrations` nesta ordem:
   - `20261116115310_schema.sql`
   - `20261116115311_seed_templates.sql`
   - `20261116115313_archive_checks.sql`
3. A última migration precisa terminar sem erro. Ela confere que entraram 508 marcações antigas.
4. Em Authentication, Providers, deixe Email ligado.
5. Em Authentication, Settings, desligue o cadastro público (sign ups). O acesso é só por convite.
6. Em Authentication, URL Configuration:
   - Site URL: a URL do preview, e depois a de produção quando você trocar.
   - Redirect URLs: `https://SEU-PREVIEW.vercel.app/auth/callback` e `http://localhost:3000/auth/callback`.
7. No SQL Editor, inclua os três e-mails reais. Troque os exemplos:

```sql
insert into public.role_invites (email, full_name, role) values
  ('jonas@seu-dominio', 'Jonas', 'executor'),
  ('leo@seu-dominio', 'Léo', 'manager'),
  ('barbara@seu-dominio', 'Bárbara', 'manager');
```

8. Em Authentication, Users, convide cada e-mail. O convite só funciona depois do insert acima. Quem não está na lista não ganha perfil.
9. No primeiro acesso pelo link do convite, a pessoa cai em Senha e define a senha do celular.

## Variáveis na Vercel

No projeto `casa-control`, Environment Variables, marque Preview (e Production só quando for a hora). Não cole os valores neste repositório.

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`

Se o painel do Supabase ainda mostrar a chave anon em vez da publishable, use `NEXT_PUBLIC_SUPABASE_ANON_KEY` no lugar. O app aceita uma das duas. Não use a service role no browser.

Copie os nomes em `.env.example` para um `.env.local` se for rodar na sua máquina. `npm install`, `npm run dev`, `npm test`.

## Papéis

- Jonas, executor: vê Hoje, marca e desmarca o dia de hoje. A marcação guarda o horário real e o nome.
- Léo e Bárbara, acompanhamento: veem qualquer data, criam e editam tarefas, criam avulsas com data.
- Domingo é folga na lista recorrente. Tarefa avulsa pode cair num domingo.
- Registro importado (as 508 marcações) aparece no dia correspondente e não sai de lá pelo app.

`recurrence_interval`, `starts_on` e `ends_on` já estão na tabela para a fase 2. O app de hoje usa `active_weekdays`.
