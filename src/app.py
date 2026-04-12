import json
import os
from datetime import datetime, timedelta

DATA_FILE = "doacoes.json"

def carregar_dados():
    """Carrega os dados salvos no arquivo JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def salvar_dados(dados):
    """Salva os dados no arquivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(dados, file, indent=4)

def calcular_proxima_doacao(data_ultima, sexo):
    """Calcula a próxima data permitida baseado no sexo biológico (M=60 dias, F=90 dias)."""
    data_obj = datetime.strptime(data_ultima, "%d/%m/%Y")
    dias_espera = 60 if sexo.upper() == 'M' else 90
    proxima_data = data_obj + timedelta(days=dias_espera)
    return proxima_data.strftime("%d/%m/%Y")

def main():
    print("-" * 50)
    print("🩸 Bem-vindo ao DoaFácil - Rastreador de Doações 🩸")
    print("-" * 50)
    
    dados = carregar_dados()

    while True:
        print("\nMenu Principal:")
        print("1. Registrar nova doação")
        print("2. Verificar próxima data disponível")
        print("3. Sair")
        
        opcao = input("\nEscolha uma opção (1/2/3): ")

        if opcao == '1':
            nome = input("Qual o seu nome? ").strip()
            sexo = input("Qual o seu sexo biológico (M/F)? ").strip().upper()
            
            if sexo not in ['M', 'F']:
                print("❌ Por favor, digite apenas M ou F.")
                continue
                
            data_str = input("Qual a data da doação (Ex: 15/04/2026)? ").strip()
            
            try:
                # Tenta converter a data para validar se o formato está certo
                datetime.strptime(data_str, "%d/%m/%Y")
                dados[nome] = {"sexo": sexo, "ultima_doacao": data_str}
                salvar_dados(dados)
                print(f"✅ Sucesso! Doação de {nome} registrada.")
            except ValueError:
                print("❌ Formato de data inválido. Use DD/MM/AAAA.")

        elif opcao == '2':
            nome = input("Qual o seu nome para consulta? ").strip()
            if nome in dados:
                info = dados[nome]
                proxima = calcular_proxima_doacao(info["ultima_doacao"], info["sexo"])
                print(f"\n📅 Olá {nome}, sua última doação foi em {info['ultima_doacao']}.")
                print(f"🟢 Sua próxima doação poderá ser feita a partir de: {proxima}")
            else:
                print("❌ Usuário não encontrado no sistema.")

        elif opcao == '3':
            print("\n👋 Obrigado por usar o DoaFácil e por salvar vidas! Até logo.\n")
            break
            
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()