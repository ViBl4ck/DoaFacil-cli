from src.app import calcular_proxima_doacao


def test_calcular_proxima_doacao_homem():
    # Homem deve esperar 60 dias
    resultado = calcular_proxima_doacao("01/01/2026", "M")
    assert resultado == "02/03/2026"


def test_calcular_proxima_doacao_mulher():
    # Mulher deve esperar 90 dias
    resultado = calcular_proxima_doacao("01/01/2026", "F")
    assert resultado == "01/04/2026"
  