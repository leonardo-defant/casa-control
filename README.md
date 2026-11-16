# Casa Control

App da casa para o Jonas executar as tarefas e para o Léo e a Bárbara acompanharem. O dia da casa é o de Cuiabá.

A página antiga está em `archive/legacy-index.html`. O passo a passo da contenção do Firebase e da branch eleitoral está em `docs/contencao.md`.

## O que você precisa criar

Um projeto Supabase novo. Este repositório não tem acesso à sua conta.

1. Crie o projeto em https://supabase.com/dashboard.
2. No SQL Editor, rode os arquivos de `supabase/migrations` nesta ordem:
   - `20261116115310_schema.sql`
   - `20261116115311_seed_templates.sql`
   - `20261116115313_archive_checks.sql`
   - `20261116121049_fase2_instancias_e_horario.sql`
   - `20261116130426_login_usuario_senha.sql`
3. A terceira migration confere que entraram 508 marcações antigas. A quarta cria o dia que não some. A quinta grava Leo e Barbara como manager e Jonas como executor.
4. Em Authentication, Providers, deixe Email ligado. A tela pede usuário e senha. O Auth guarda um endereço sintético.
5. Em Authentication, Settings, desligue o cadastro público e desligue a confirmação de endereço. Ninguém se cadastra sozinho e não existe link de confirmação.
6. Crie os três usuários com senha, sem colocar a senha no repositório:

```bash
export NEXT_PUBLIC_SUPABASE_URL=...
export SUPABASE_SERVICE_ROLE_KEY=...
export CASA_PWD_LEO=...
export CASA_PWD_BARBARA=...
export CASA_PWD_JONAS=...
npm run auth:users
```

O script chama a Admin API com `email_confirm=true`. Usuários na tela: Leo, Barbara e Jonas. Maiúscula e acento não importam.

## Variáveis na Vercel

No projeto `casa-control`, Environment Variables, marque Preview (e Production só quando for a hora). Não cole os valores neste repositório.

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`

Se o painel do Supabase ainda mostrar a chave anon em vez da publishable, use `NEXT_PUBLIC_SUPABASE_ANON_KEY` no lugar. O app aceita uma das duas. Não use a service role no browser.

Para o cron das 6h de Cuiabá gerar o dia mesmo sem ninguém abrir o app, coloque também em Production, só no servidor:

- `CRON_SECRET`
- `SUPABASE_SERVICE_ROLE_KEY`

Sem essas duas, a lista do dia nasce quando alguém abre Hoje.

Copie os nomes em `.env.example` para um `.env.local` se for rodar na sua máquina. `npm install`, `npm run dev`, `npm test`.

## Papéis

- Jonas, executor: vê Hoje, marca o que já pode ser feito e o que ficou de ontem. A marcação guarda o horário real e o nome.
- Tarefa com hora só libera 60 minutos antes. Marcação anterior não entra na conta e pede para desfazer. Se passar de 3 horas, o texto diz que foi com atraso.
- O que ficou pendente continua em Atrasadas no dia seguinte.
- Léo e Bárbara, acompanhamento: veem qualquer data, criam e editam tarefas, criam avulsas com data.
- Domingo é folga na lista recorrente. Tarefa avulsa pode cair num domingo.
- Registro importado (as 508 marcações) aparece no dia correspondente e não sai de lá pelo app.

`recurrence_interval`, `starts_on` e `ends_on` continuam prontos para uma recorrência mais fina. O app usa `active_weekdays`.
