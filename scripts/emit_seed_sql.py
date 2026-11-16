#!/usr/bin/env python3
"""Gera o SQL das tarefas copiadas da lista antiga."""

from pathlib import Path

OUT = Path("supabase/migrations/20261116115311_seed_templates.sql")

WEEKDAYS = "{1,2,3,4,5,6}"


def row(
    code,
    title,
    category,
    group_name,
    weekday,
    scheduled_time,
    sort_order,
    recurrence_kind,
    active_weekdays,
):
    def q(value):
        if value is None:
            return "null"
        return "'" + value.replace("'", "''") + "'"

    weekday_sql = "null" if weekday is None else str(weekday)
    time_sql = "null" if scheduled_time is None else f"{q(scheduled_time)}::time"
    return (
        f"  ({q(code)}, {q(title)}, {q(category)}, {q(group_name)}, "
        f"{weekday_sql}, {time_sql}, {sort_order}, {q(recurrence_kind)}, "
        f"'{active_weekdays}'::smallint[])"
    )


items = []
order = 1


def add(code, title, category, group, weekday, time_value, kind, days):
    global order
    items.append(row(code, title, category, group, weekday, time_value, order, kind, days))
    order += 1


add("d1", "Buscar a Letícia e levar para o trabalho", "fixed", "Compromissos fixos", None, "07:30", "daily", WEEKDAYS)
add("d2", "Alimentar os cachorros e aplicar medicações da Bulma", "fixed", "Compromissos fixos", None, "07:40", "daily", WEEKDAYS)
add("dr1", "Checagem rápida das áreas externas", "routine", "Rotina do dia", None, None, "daily", WEEKDAYS)
add("dr2", "Piscina: retirada de folhas e sujeira visível", "routine", "Rotina do dia", None, None, "daily", WEEKDAYS)
add("dr3", "Jardim: recolher folhas e resíduos", "routine", "Rotina do dia", None, None, "daily", WEEKDAYS)
add("dr4", "Depósito: guardar ferramentas e manter organização", "routine", "Rotina do dia", None, None, "daily", WEEKDAYS)
add("dr5", "Monitorar insumos: cloro, produtos, peças, combustível", "routine", "Rotina do dia", None, None, "daily", WEEKDAYS)
add("w_seg1", "Levar cachorros na creche", "weekday", None, 1, "08:00", "weekly", "{1}")
add("w_seg2", "Buscar cachorros na creche", "weekday", None, 1, "14:00", "weekly", "{1}")
add("w_qua1", "Levar cachorros na creche", "weekday", None, 3, "08:00", "weekly", "{3}")
add("w_qua2", "Levar Gabriel para aula de música", "weekday", None, 3, "10:00", "weekly", "{3}")
add("w_qua3", "Buscar cachorros na creche", "weekday", None, 3, "14:00", "weekly", "{3}")
add("w_sex1", "Levar cachorros na creche", "weekday", None, 5, "08:00", "weekly", "{5}")
add("w_sex2", "Levar Gabriel para aula de música", "weekday", None, 5, "10:00", "weekly", "{5}")
add("w_sex3", "Buscar cachorros na creche", "weekday", None, 5, "14:00", "weekly", "{5}")
add("w_sex4", "Carro do Léo: lava a jato + abastecer + calibrar (manhã)", "weekday", None, 5, None, "weekly", "{5}")
add("w_sex5", "Carro da Bárbara: lava a jato + abastecer + calibrar (tarde)", "weekday", None, 5, None, "weekly", "{5}")
add("w_sex6", "Piscina: preparação para o fim de semana", "weekday", None, 5, None, "weekly", "{5}")
add("w_sab1", "Antes de sair: encher galão de água dos cachorros", "weekday", None, 6, None, "weekly", "{6}")
add("w_sab2", "Revisão geral: piscina, irrigação, iluminação, portões", "weekday", None, 6, None, "weekly", "{6}")

eventual = [
    ("ej1", "Cortar grama", "Jardim"),
    ("ej2", "Podas maiores", "Jardim"),
    ("ej3", "Adubação e controle de pragas", "Jardim"),
    ("ej4", "Troca/manutenção ferramentas de jardinagem", "Jardim"),
    ("ei1", "Ajuste de programação por clima/estação/chuvas", "Irrigação"),
    ("ei2", "Desentupir bicos, trocar aspersores, revisar vazamentos", "Irrigação"),
    ("ei3", "Ajustes de sensores e setores com falha", "Irrigação"),
    ("ep1", "Limpeza pesada e manutenção corretiva", "Piscina"),
    ("ep2", "Ajustes finos de tratamento (uso, clima, chuva)", "Piscina"),
    ("ep3", "Troca de componentes / chamar assistência", "Piscina"),
    ("ein1", "Pequenos reparos (torneiras, trincos, dobradiças)", "Infra externa"),
    ("ein2", "Troca de lâmpadas e ajustes de iluminação", "Infra externa"),
    ("ein3", "Manutenção de portões e interfone", "Infra externa"),
    ("ec1", "Mercado", "Compras e recados"),
    ("ec2", "Farmácia", "Compras e recados"),
    ("ec3", "Buscar encomendas / entregas sob demanda", "Compras e recados"),
]
for code, title, group in eventual:
    add(code, title, "eventual", group, None, None, "eventual", WEEKDAYS)

sql = """-- Lista copiada de archive/legacy-index.html.
-- O horario saiu do texto e foi para scheduled_time.
-- recurrence_interval fica em 1. A fase 2 passa a usar esse campo.

insert into public.task_templates (
  code, title, category, group_name, weekday, scheduled_time,
  sort_order, recurrence_kind, active_weekdays
) values
"""
sql += ",\n".join(items)
sql += ";\n"
OUT.write_text(sql, encoding="utf-8")
print(f"{len(items)} templates -> {OUT}")
