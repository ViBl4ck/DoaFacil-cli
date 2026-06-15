from unittest.mock import patch, MagicMock

try:
    from src import database
except ImportError:
    import database


def _fake_client(data):
    client = MagicMock()
    execucao = MagicMock()
    execucao.data = data
    (client.table.return_value.select.return_value
     .eq.return_value.execute.return_value) = execucao
    (client.table.return_value.upsert.return_value
     .execute.return_value) = execucao
    return client


def test_buscar_doacao_encontra():
    fake = _fake_client(
        [{"nome": "Ana", "sexo": "F", "ultima_doacao": "10/03/2026"}]
    )
    with patch.object(database, "get_client", return_value=fake):
        resultado = database.buscar_doacao("Ana")
    assert resultado["nome"] == "Ana"


def test_buscar_doacao_nao_encontra():
    fake = _fake_client([])
    with patch.object(database, "get_client", return_value=fake):
        resultado = database.buscar_doacao("Ninguem")
    assert resultado is None


def test_registrar_doacao_usa_tabela_doacoes():
    fake = _fake_client([])
    with patch.object(database, "get_client", return_value=fake):
        database.registrar_doacao("Bob", "M", "01/01/2026")
    fake.table.assert_called_with("doacoes")
