"""Modelo de urna pelo número de série (faixas inferidas, seção 3.3 do documento)."""
FAIXAS = {
    2022: [(999000, 1220500, 'UE2009'), (1220501, 1345500, 'UE2010'), (1345501, 1649999, 'UE2011'),
           (1650000, 1749999, 'UE2013'), (1750000, 1999999, 'UE2015'), (2000000, 2299999, 'UE2020')],
    2026: [(1650000, 1749999, 'UE2013'), (1750000, 1999999, 'UE2015'), (2000000, 2249999, 'UE2020'),
           (2250000, 2599999, 'UE2022')],
}


def modelo(serie, ano):
    for a, b, m in FAIXAS[ano]:
        if a <= serie <= b:
            return m
    return None
