# DoaFácil - Rastreador de Doações de Sangue 🩸

**Versão:** 1.0.0

## O Problema
Muitas pessoas desejam doar sangue regularmente para ajudar a salvar vidas, mas acabam esquecendo a data exata em que estão aptas a doar novamente devido aos diferentes prazos de carência biológica (60 dias para homens e 90 dias para mulheres).

## A Solução
O DoaFácil é uma aplicação de Linha de Comando (CLI) que registra a última data de doação do usuário, calcula automaticamente a data da próxima doação e oferece uma pré-triagem baseada nas regras dos hemocentros. Os registros são salvos localmente em um arquivo JSON (`doacoes.json`).

## Funcionalidades
* **Registrar doação:** cadastra nome, sexo biológico e data da última doação.
* **Consultar próxima data:** calcula quando o usuário estará apto a doar novamente (60 dias para homens, 90 para mulheres).
* **Pré-triagem:** questionário rápido com as principais regras impeditivas (definitivas e temporárias) usadas pelos hemocentros.

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

## Licença
Projeto licenciado sob a GNU General Public License v3.0 — veja o arquivo [LICENSE](LICENSE).
