from unittest.mock import patch, MagicMock

import requests

from src.app import consultar_cep


def _resposta_falsa(json_data):
    mock_resp = MagicMock()
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status.return_value = None
    return mock_resp


def test_consultar_cep_valido():
    fake = {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
    }
    with patch("src.app.requests.get",
               return_value=_resposta_falsa(fake)):
        resultado = consultar_cep("01001000")
    assert resultado["sucesso"] is True
    assert resultado["cidade"] == "São Paulo"
    assert resultado["uf"] == "SP"


def test_consultar_cep_inexistente():
    with patch("src.app.requests.get",
               return_value=_resposta_falsa({"erro": True})):
        resultado = consultar_cep("00000000")
    assert resultado["sucesso"] is False


def test_consultar_cep_formato_invalido():
    resultado = consultar_cep("123")
    assert resultado["sucesso"] is False


def test_consultar_cep_erro_de_rede():
    with patch("src.app.requests.get",
               side_effect=requests.RequestException):
        resultado = consultar_cep("01001000")
    assert resultado["sucesso"] is False
