import os

import streamlit as st

# No Streamlit Cloud as credenciais vêm de st.secrets.
# Localmente, vêm do arquivo .env (carregado dentro de src/database.py).
try:
    os.environ.setdefault("SUPABASE_URL", st.secrets["SUPABASE_URL"])
    os.environ.setdefault("SUPABASE_KEY", st.secrets["SUPABASE_KEY"])
except Exception:
    pass

from src.app import calcular_proxima_doacao  # noqa: E402
from src.database import (  # noqa: E402
    registrar_doacao,
    buscar_doacao,
)

st.set_page_config(page_title="DoaFácil", page_icon="🩸")

st.title("🩸 DoaFácil")
st.caption(
    "Rastreador de doações de sangue. "
    "Projeto acadêmico (UniCEUB) — não oficial."
)

aba_registrar, aba_consultar = st.tabs(
    ["Registrar doação", "Consultar elegibilidade"]
)

with aba_registrar:
    st.subheader("Registrar uma doação")
    nome = st.text_input("Nome completo", key="nome_reg")
    sexo = st.radio(
        "Sexo biológico", ["M", "F"], horizontal=True, key="sexo_reg"
    )
    data = st.date_input(
        "Data da doação", format="DD/MM/YYYY", key="data_reg"
    )
    if st.button("Registrar", type="primary"):
        if not nome.strip():
            st.warning("Informe o nome.")
        else:
            data_str = data.strftime("%d/%m/%Y")
            try:
                registrar_doacao(nome.strip(), sexo, data_str)
                st.success(
                    f"Doação de {nome.strip()} registrada com sucesso!"
                )
            except Exception:
                st.error("Erro ao salvar no banco de dados.")

with aba_consultar:
    st.subheader("Consultar quando você poderá doar de novo")
    nome_c = st.text_input("Nome completo", key="nome_con")
    if st.button("Consultar", type="primary"):
        if not nome_c.strip():
            st.warning("Informe o nome.")
        else:
            try:
                info = buscar_doacao(nome_c.strip())
            except Exception:
                info = None
                st.error("Erro ao consultar o banco de dados.")
            else:
                if info:
                    ultima = info["ultima_doacao"]
                    proxima = calcular_proxima_doacao(
                        ultima, info["sexo"]
                    )
                    st.info(f"Última doação registrada: {ultima}")
                    st.success(
                        f"Apto(a) a doar a partir de: {proxima}"
                    )
                else:
                    st.warning("Nome não encontrado no sistema.")
