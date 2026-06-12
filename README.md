# DoaFácil - Rastreador de Doações de Sangue 🩸

**Versão:** 1.1.0

## Link público / Execução

- Repositório GitHub: https://github.com/ViBl4ck/DoaFacil-cli
- Execução online via GitHub Codespaces: abra o repositório no GitHub, clique em
  **Code → Codespaces → Create codespace on main** e rode `python src/app.py` no
  terminal.
- Execução via Docker: veja a seção "Como executar com Docker" abaixo.

## O Problema
Muitas pessoas desejam doar sangue regularmente para ajudar a salvar vidas, mas acabam esquecendo a data exata em que estão aptas a doar novamente devido aos diferentes prazos de carência biológica (60 dias para homens e 90 dias para mulheres).

## A Solução
O DoaFácil é uma aplicação de Linha de Comando (CLI) que registra a última data de doação do usuário, calcula automaticamente a data da próxima doação e oferece uma pré-triagem baseada nas regras dos hemocentros. Os registros são salvos localmente em um arquivo JSON (`doacoes.json`).

## Funcionalidades
* **Registrar doação:** cadastra nome, sexo biológico e data da última doação.
* **Consultar próxima data:** calcula quando o usuário estará apto a doar novamente (60 dias para homens, 90 para mulheres).
* **Pré-triagem:** questionário rápido com as principais regras impeditivas (definitivas e temporárias) usadas pelos hemocentros.
* **Consultar endereço por CEP:** consulta logradouro, bairro, cidade e UF a
  partir do CEP informado, usando a API pública ViaCEP.

## Tecnologias e Qualidade
* **Linguagem:** Python 3
* **Armazenamento:** arquivo JSON local (`doacoes.json`)
* **Testes:** `pytest`
* **Linting / Análise estática:** `flake8`
* **CI:** GitHub Actions executa linting e testes a cada push e pull request

## 🚀 Como executar localmente

1. Clone o repositório:
   `git clone https://github.com/ViBl4ck/DoaFacil-cli.git`
2. Acesse a pasta do projeto:
   `cd DoaFacil-cli`
3. Crie e ative um ambiente virtual (recomendado):
   `python -m venv venv`
   * No Linux/Mac: `source venv/bin/activate`
   * No Windows: `venv\Scripts\activate`
4. Instale as dependências:
   `pip install -r requirements.txt`
5. Execute a aplicação:
   `python src/app.py`
6. Rode os testes automatizados:
   `pytest tests/`

## Integração com API Pública

O DoaFácil consome a API pública **ViaCEP** (https://viacep.com.br) para
consultar dados de endereço a partir do CEP informado pelo usuário. A requisição
é feita via HTTP GET com timeout, e o app trata os casos de CEP inválido, CEP
inexistente e falha de conexão.

## Teste de Integração

O projeto possui um teste automatizado (`tests/test_integracao_cep.py`) que
valida o fluxo de consulta de CEP. A resposta da API é mockada para manter o CI
estável e independente de conexão, cobrindo os casos de CEP válido, CEP
inexistente, formato inválido e erro de rede.

## Como executar com Docker

1. Construa a imagem: `docker build -t doafacil .`
2. Rode em modo interativo: `docker run -it doafacil`

## Licença
Projeto licenciado sob a GNU General Public License v3.0 — veja o arquivo [LICENSE](LICENSE).
