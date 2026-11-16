-- Lista copiada de archive/legacy-index.html.
-- O horario saiu do texto e foi para scheduled_time.
-- recurrence_interval fica em 1. A fase 2 passa a usar esse campo.

insert into public.task_templates (
  code, title, category, group_name, weekday, scheduled_time,
  sort_order, recurrence_kind, active_weekdays
) values
  ('d1', 'Buscar a Letícia e levar para o trabalho', 'fixed', 'Compromissos fixos', null, '07:30'::time, 1, 'daily', '{1,2,3,4,5,6}'::smallint[]),
  ('d2', 'Alimentar os cachorros e aplicar medicações da Bulma', 'fixed', 'Compromissos fixos', null, '07:40'::time, 2, 'daily', '{1,2,3,4,5,6}'::smallint[]),
  ('dr1', 'Checagem rápida das áreas externas', 'routine', 'Rotina do dia', null, null, 3, 'daily', '{1,2,3,4,5,6}'::smallint[]),
  ('dr2', 'Piscina: retirada de folhas e sujeira visível', 'routine', 'Rotina do dia', null, null, 4, 'daily', '{1,2,3,4,5,6}'::smallint[]),
  ('dr3', 'Jardim: recolher folhas e resíduos', 'routine', 'Rotina do dia', null, null, 5, 'daily', '{1,2,3,4,5,6}'::smallint[]),
  ('dr4', 'Depósito: guardar ferramentas e manter organização', 'routine', 'Rotina do dia', null, null, 6, 'daily', '{1,2,3,4,5,6}'::smallint[]),
  ('dr5', 'Monitorar insumos: cloro, produtos, peças, combustível', 'routine', 'Rotina do dia', null, null, 7, 'daily', '{1,2,3,4,5,6}'::smallint[]),
  ('w_seg1', 'Levar cachorros na creche', 'weekday', null, 1, '08:00'::time, 8, 'weekly', '{1}'::smallint[]),
  ('w_seg2', 'Buscar cachorros na creche', 'weekday', null, 1, '14:00'::time, 9, 'weekly', '{1}'::smallint[]),
  ('w_qua1', 'Levar cachorros na creche', 'weekday', null, 3, '08:00'::time, 10, 'weekly', '{3}'::smallint[]),
  ('w_qua2', 'Levar Gabriel para aula de música', 'weekday', null, 3, '10:00'::time, 11, 'weekly', '{3}'::smallint[]),
  ('w_qua3', 'Buscar cachorros na creche', 'weekday', null, 3, '14:00'::time, 12, 'weekly', '{3}'::smallint[]),
  ('w_sex1', 'Levar cachorros na creche', 'weekday', null, 5, '08:00'::time, 13, 'weekly', '{5}'::smallint[]),
  ('w_sex2', 'Levar Gabriel para aula de música', 'weekday', null, 5, '10:00'::time, 14, 'weekly', '{5}'::smallint[]),
  ('w_sex3', 'Buscar cachorros na creche', 'weekday', null, 5, '14:00'::time, 15, 'weekly', '{5}'::smallint[]),
  ('w_sex4', 'Carro do Léo: lava a jato + abastecer + calibrar (manhã)', 'weekday', null, 5, null, 16, 'weekly', '{5}'::smallint[]),
  ('w_sex5', 'Carro da Bárbara: lava a jato + abastecer + calibrar (tarde)', 'weekday', null, 5, null, 17, 'weekly', '{5}'::smallint[]),
  ('w_sex6', 'Piscina: preparação para o fim de semana', 'weekday', null, 5, null, 18, 'weekly', '{5}'::smallint[]),
  ('w_sab1', 'Antes de sair: encher galão de água dos cachorros', 'weekday', null, 6, null, 19, 'weekly', '{6}'::smallint[]),
  ('w_sab2', 'Revisão geral: piscina, irrigação, iluminação, portões', 'weekday', null, 6, null, 20, 'weekly', '{6}'::smallint[]),
  ('ej1', 'Cortar grama', 'eventual', 'Jardim', null, null, 21, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ej2', 'Podas maiores', 'eventual', 'Jardim', null, null, 22, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ej3', 'Adubação e controle de pragas', 'eventual', 'Jardim', null, null, 23, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ej4', 'Troca/manutenção ferramentas de jardinagem', 'eventual', 'Jardim', null, null, 24, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ei1', 'Ajuste de programação por clima/estação/chuvas', 'eventual', 'Irrigação', null, null, 25, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ei2', 'Desentupir bicos, trocar aspersores, revisar vazamentos', 'eventual', 'Irrigação', null, null, 26, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ei3', 'Ajustes de sensores e setores com falha', 'eventual', 'Irrigação', null, null, 27, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ep1', 'Limpeza pesada e manutenção corretiva', 'eventual', 'Piscina', null, null, 28, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ep2', 'Ajustes finos de tratamento (uso, clima, chuva)', 'eventual', 'Piscina', null, null, 29, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ep3', 'Troca de componentes / chamar assistência', 'eventual', 'Piscina', null, null, 30, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ein1', 'Pequenos reparos (torneiras, trincos, dobradiças)', 'eventual', 'Infra externa', null, null, 31, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ein2', 'Troca de lâmpadas e ajustes de iluminação', 'eventual', 'Infra externa', null, null, 32, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ein3', 'Manutenção de portões e interfone', 'eventual', 'Infra externa', null, null, 33, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ec1', 'Mercado', 'eventual', 'Compras e recados', null, null, 34, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ec2', 'Farmácia', 'eventual', 'Compras e recados', null, null, 35, 'eventual', '{1,2,3,4,5,6}'::smallint[]),
  ('ec3', 'Buscar encomendas / entregas sob demanda', 'eventual', 'Compras e recados', null, null, 36, 'eventual', '{1,2,3,4,5,6}'::smallint[]);
