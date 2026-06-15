import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


def get_client() -> Client:
    """Cria o cliente Supabase a partir das variáveis do .env."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError(
            "Defina SUPABASE_URL e SUPABASE_KEY no arquivo .env"
        )
    return create_client(url, key)


def registrar_doacao(nome, sexo, ultima_doacao):
    """Insere ou atualiza a doação de uma pessoa (upsert por nome)."""
    registro = {
        "nome": nome,
        "sexo": sexo,
        "ultima_doacao": ultima_doacao,
    }
    get_client().table("doacoes").upsert(
        registro, on_conflict="nome"
    ).execute()


def buscar_doacao(nome):
    """Busca a doação pelo nome. Retorna um dict ou None."""
    resposta = (
        get_client()
        .table("doacoes")
        .select("*")
        .eq("nome", nome)
        .execute()
    )
    if resposta.data:
        return resposta.data[0]
    return None
