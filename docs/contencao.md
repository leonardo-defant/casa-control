# Fase 0, contenção

Nada disto foi publicado em produção. A URL https://casa-control-alpha.vercel.app continua no HTML antigo.

## Firebase

Não há credencial do Firebase neste ambiente. As regras novas estão em `database.rules.json` e ainda precisam ser publicadas por você.

1. Abra o console: https://console.firebase.google.com/
2. Entre no projeto `casa-control-9d194`.
3. No menu, abra Realtime Database e a aba Rules.
4. Substitua o conteúdo pelo arquivo `database.rules.json` deste repositório.
5. Clique em Publish.
6. Confira, sem estar logado: um GET em `https://casa-control-9d194-default-rtdb.firebaseio.com/checks.json` deve responder Permission denied.

Enquanto isso não for publicado, qualquer pessoa que veja a URL no HTML antigo lê e grava as marcações.

## Vercel, branch da pesquisa eleitoral

A branch `claude/new-session-5cnflo` não é a branch de produção. Os deploys dela até agora saíram como preview (`target` vazio). A produção segue o commit `4076a88` de `main`.

Foi enviado ao projeto `casa-control` um Ignored Build Step para ignorar só essa branch:

```
if [ "$VERCEL_GIT_COMMIT_REF" = "claude/new-session-5cnflo" ]; then exit 0; else exit 1; fi
```

No Vercel, exit 0 ignora o build e exit 1 segue. `main` e os previews deste app continuam buildando.

Confirme no painel, porque a API não devolveu o campo de volta:

1. Projeto casa-control, Settings, Git, Ignored Build Step.
2. O comando acima deve estar salvo.
3. Settings, Environments, Production, Branch Tracking. O nome tem de ser `main`. Se estiver outro, volte para `main` e salve. Não troque para a branch da pesquisa.
4. Não use Promote to Production em nenhum deploy cuja branch seja `claude/new-session-5cnflo`. O passo 1 impede builds novos dessa branch. Um deploy antigo ainda pode ser promovido à mão.

Este pull request não deve ser mergeado em `main` até o Supabase estar ligado e você decidir trocar a URL pública.
