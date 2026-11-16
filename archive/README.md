# Arquivo do Firebase, 16 de novembro de 2026

`firebase-export-2026-11-16.json` é a cópia completa do Realtime Database do projeto `casa-control-9d194`, lida por GET anônimo. Há dois nós: `checks` (508 marcações, de 20 de fevereiro a 17 de setembro de 2026) e `notes` (6 textos).

`legacy-index.html` é a página antiga que estava em produção. A lista de tarefas da fase 1 foi copiada daqui. O horário, que estava no texto, foi para a coluna `scheduled_time`.

O arquivo tem a rotina da casa. O repositório precisa continuar privado.

A migration `supabase/migrations/20261116115313_archive_checks.sql` recoloca as 508 marcações no Postgres, com `source = archive`. As notas ficam só neste JSON.
