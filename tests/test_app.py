from src.app import calcular_proxima_doacao

def test_calcular_proxima_doacao_homem():
    # Homens: intervalo de 60 dias
    # 01/04/2026 + 60 dias = 31/05/2026
    resultado = calcular_proxima_doacao("01/04/2026", "M")
    assert resultado == "31/05/2026"

def test_calcular_proxima_doacao_mulher():
    # Mulheres: intervalo de 90 dias
    # 01/04/2026 + 90 dias = 30/06/2026
    resultado = calcular_proxima_doacao("01/04/2026", "F")
    assert resultado == "30/06/2026"
    