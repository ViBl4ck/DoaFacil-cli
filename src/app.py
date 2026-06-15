import re
from datetime import datetime, timedelta

import requests

try:
    from database import registrar_doacao, buscar_doacao
except ImportError:
    from src.database import registrar_doacao, buscar_doacao


def calcular_proxima_doacao(data_ultima, sexo):
    data_obj = datetime.strptime(data_ultima, "%d/%m/%Y")
    dias_espera = 60 if sexo.upper() == 'M' else 90
    proxima_data = data_obj + timedelta(days=dias_espera)
    return proxima_data.strftime("%d/%m/%Y")


def fazer_triagem():
    """Realiza um questionario rapido com as regras do hemocentro."""
    print("\n" + "=" * 40)
    print("📋 PRÉ-TRIAGEM DE DOAÇÃO")
    print("Responda com 'S' para Sim e 'N' para Não.")
    print("=" * 40)

    # Regras Impeditivas Definitivas
    perg_1 = "1. Você morou na Europa após 1980? (S/N): "
    if input(perg_1).strip().upper() == 'S':
        msg = ("❌ Inapto: Necessário verificar aptidão pelo "
               "Alô Pró-Sangue (11) 4573-7800.")
        return False, msg

    perg_2 = "2. Você está grávida no momento? (S/N): "
    if input(perg_2).strip().upper() == 'S':
        return False, "❌ Inapto: Gestantes não podem doar sangue."

    # Regras Temporárias (Acumulativas)
    inaptidoes = []

    perg_3 = "3. Teve resfriado nos últimos 7 dias? (S/N): "
    if input(perg_3).strip().upper() == 'S':
        inaptidoes.append("Resfriado (aguardar 7 dias)")

    perg_4 = "4. Ingeriu bebida alcoólica nas últimas 12 horas? (S/N): "
    if input(perg_4).strip().upper() == 'S':
        inaptidoes.append("Álcool (aguardar 12 horas)")

    perg_5 = ("5. Fez tatuagem ou piercing nos últimos "
              "12 meses? (S/N): ")
    if input(perg_5).strip().upper() == 'S':
        inaptidoes.append("Tatuagem/Piercing (aguardar 6 a 12 meses)")

    perg_6 = "6. Tomou vacina contra Covid-19 nos últimos 7 dias? (S/N): "
    if input(perg_6).strip().upper() == 'S':
        inaptidoes.append("Vacina Covid-19 (aguardar 7 dias)")

    # Analisando os resultados
    if inaptidoes:
        motivos = "\n  - ".join(inaptidoes)
        return False, f"❌ Inapto no momento pelos motivos:\n  - {motivos}"

    msg_aprov = ("✅ Você passou na pré-triagem básica! "
                 "A decisão final é do médico.")
    return True, msg_aprov


def consultar_cep(cep):
    """Consulta endereço por CEP usando a API pública ViaCEP."""
    cep_numerico = re.sub(r"\D", "", cep)
    if len(cep_numerico) != 8:
        return {
            "sucesso": False,
            "erro": "CEP inválido. Informe 8 dígitos.",
        }

    url = f"https://viacep.com.br/ws/{cep_numerico}/json/"
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
    except requests.RequestException:
        return {
            "sucesso": False,
            "erro": "Erro de conexão. Tente novamente mais tarde.",
        }

    if dados.get("erro"):
        return {"sucesso": False, "erro": "CEP não encontrado."}

    return {
        "sucesso": True,
        "cep": dados.get("cep", ""),
        "logradouro": dados.get("logradouro", ""),
        "bairro": dados.get("bairro", ""),
        "cidade": dados.get("localidade", ""),
        "uf": dados.get("uf", ""),
    }


def main():
    while True:
        print("\n" + "-" * 50)
        print("🩸 Bem-vindo ao DoaFácil v2.0.0 🩸")
        print("-" * 50)
        print("1. Registrar nova doação")
        print("2. Verificar próxima data disponível")
        print("3. Fazer pré-triagem (Questionário)")
        print("4. Consultar endereço por CEP")
        print("5. Sair")

        opcao = input("\nEscolha uma opção (1/2/3/4/5): ")

        if opcao == '1':
            nome = input("Qual o seu nome? ").strip()
            sexo = input("Sexo biológico (M/F)? ").strip().upper()

            if sexo not in ['M', 'F']:
                print("❌ Por favor, digite apenas M ou F.")
                continue

            perg_data = "Data da doação (Ex: 15/04/2026)? "
            data_str = input(perg_data).strip()
            try:
                datetime.strptime(data_str, "%d/%m/%Y")
            except ValueError:
                print("❌ Formato de data inválido. Use DD/MM/AAAA.")
            else:
                try:
                    registrar_doacao(nome, sexo, data_str)
                    print(f"✅ Sucesso! Doação de {nome} registrada.")
                except Exception:
                    print("❌ Erro ao salvar no banco de dados.")

        elif opcao == '2':
            nome = input("Qual o seu nome para consulta? ").strip()
            try:
                info = buscar_doacao(nome)
            except Exception:
                print("❌ Erro ao consultar o banco de dados.")
                info = None
            if info:
                ultima = info["ultima_doacao"]
                proxima = calcular_proxima_doacao(
                    ultima, info["sexo"]
                )
                print(f"\n📅 Olá {nome}, última doação: {ultima}.")
                print(f"➡️  Próxima doação a partir de: {proxima}")
            else:
                print("❌ Nome não encontrado no sistema.")

        elif opcao == '3':
            aprovado, mensagem = fazer_triagem()
            print("\nResultado da Triagem:")
            print(mensagem)

        elif opcao == '4':
            cep = input("Digite o CEP (somente números): ").strip()
            resultado = consultar_cep(cep)
            if resultado["sucesso"]:
                print("\n📍 Endereço encontrado:")
                print(f"  CEP: {resultado['cep']}")
                print(f"  Logradouro: {resultado['logradouro']}")
                print(f"  Bairro: {resultado['bairro']}")
                print(f"  Cidade: {resultado['cidade']}")
                print(f"  UF: {resultado['uf']}")
            else:
                print(f"\n❌ {resultado['erro']}")

        elif opcao == '5':
            print("\n👋 Obrigado por salvar vidas! Até logo.\n")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
