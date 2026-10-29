"""Conferência L8: extração própria, direto dos zips do bweb, só o cargo Presidente.
Uso: unzip -p ZIP '*.csv' | grep -a ';1;"Presidente";' | python3 -I extrair.py TURNO SAIDA.json.gz
(o cabeçalho é conhecido; as linhas chegam sem ele)."""
import csv, gzip, io, json, sys

HDR = ["DT_GERACAO", "HH_GERACAO", "ANO_ELEICAO", "CD_TIPO_ELEICAO", "NM_TIPO_ELEICAO", "CD_PLEITO", "DT_PLEITO", "NR_TURNO",
       "CD_ELEICAO", "DS_ELEICAO", "SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_LOCAL_VOTACAO",
       "CD_CARGO_PERGUNTA", "DS_CARGO_PERGUNTA", "NR_PARTIDO", "SG_PARTIDO", "NM_PARTIDO", "DT_BU_RECEBIDO", "QT_APTOS",
       "QT_COMPARECIMENTO", "QT_ABSTENCOES", "CD_TIPO_URNA", "DS_TIPO_URNA", "CD_TIPO_VOTAVEL", "DS_TIPO_VOTAVEL", "NR_VOTAVEL",
       "NM_VOTAVEL", "QT_VOTOS", "NR_URNA_EFETIVADA", "CD_CARGA_1_URNA_EFETIVADA", "CD_CARGA_2_URNA_EFETIVADA",
       "CD_FLASHCARD_URNA_EFETIVADA", "DT_CARGA_URNA_EFETIVADA", "DS_CARGO_PERGUNTA_SECAO", "DS_SECOES_AGREGADAS",
       "DT_ABERTURA", "DT_ENCERRAMENTO", "QT_ELEI_BIOM_SEM_HABILITACAO", "DT_EMISSAO_BU", "NR_JUNTA_APURADORA",
       "NR_TURMA_APURADORA"]
IX = {c: i for i, c in enumerate(HDR)}


def main():
    turno, saida = sys.argv[1], sys.argv[2]
    out = {}
    linhas = 0
    rd = csv.reader(io.TextIOWrapper(sys.stdin.buffer, encoding='latin1'), delimiter=';', quotechar='"')
    for r in rd:
        if len(r) != len(HDR):
            continue
        if r[IX['CD_CARGO_PERGUNTA']] != '1' or r[IX['NR_TURNO']] != turno:
            continue
        linhas += 1
        k = f"{r[IX['SG_UF']]}|{r[IX['CD_MUNICIPIO']]}|{r[IX['NR_ZONA']]}|{r[IX['NR_SECAO']]}"
        s = out.get(k)
        if s is None:
            s = out[k] = {'mun': r[IX['NM_MUNICIPIO']], 'loc': r[IX['NR_LOCAL_VOTACAO']], 'apt': int(r[IX['QT_APTOS']]),
                          'comp': int(r[IX['QT_COMPARECIMENTO']]), 'tipo': r[IX['CD_TIPO_URNA']],
                          'rec': r[IX['DT_BU_RECEBIDO']], 'ab': r[IX['DT_ABERTURA']], 'enc': r[IX['DT_ENCERRAMENTO']],
                          'emi': r[IX['DT_EMISSAO_BU']], 'junta': r[IX['NR_JUNTA_APURADORA']],
                          'agreg': r[IX['DS_SECOES_AGREGADAS']], 'urna': r[IX['NR_URNA_EFETIVADA']],
                          'L': 0, 'R': 0, 'O': 0, 'B': 0, 'N': 0, 'nlin': 0, 'conflito': 0}
        else:
            # mesma seção em outra linha: os campos da seção têm de ser iguais
            if (s['rec'], s['apt'], s['comp'], s['enc']) != (r[IX['DT_BU_RECEBIDO']], int(r[IX['QT_APTOS']]),
                                                             int(r[IX['QT_COMPARECIMENTO']]), r[IX['DT_ENCERRAMENTO']]):
                s['conflito'] += 1
        s['nlin'] += 1
        tv = r[IX['CD_TIPO_VOTAVEL']]; nv = r[IX['NR_VOTAVEL']]; q = int(r[IX['QT_VOTOS']])
        if tv == '1':
            if nv == '13':
                s['L'] += q
            elif nv == '22':
                s['R'] += q
            else:
                s['O'] += q
        elif tv == '2':
            s['B'] += q
        elif tv == '3':
            s['N'] += q
        else:
            s['O'] += q
    with gzip.open(saida, 'wt') as f:
        json.dump(out, f)
    print(saida, linhas, len(out), file=sys.stderr)


if __name__ == '__main__':
    main()
