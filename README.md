# DoaFácil - Rastreador de Doações de Sangue 🩸

## Versão: 1.0.0

## O Problema
Muitas pessoas desejam doar sangue regularmente para ajudar a salvar vidas, mas acabam esquecendo a data exata em que estão aptas a doar novamente devido aos diferentes prazos de carência biológica (60 dias para homens e 90 dias para mulheres).

## A Solução
O DoaFácil é uma aplicação de Linha de Comando (CLI) simples que cadastra a última data de doação do usuário, calcula automaticamente a data da próxima doação e armazena esse registro localmente usando JSON.

## Tecnologias e Qualidade
* **Linguagem:** Python 3
* **Armazenamento:** JSON (em memória local)
* **Testes:** `pytest`
* **Linting:** `flake8`
* **CI/CD:** GitHub Actions configurado no repositório.
* 
## 🚀 Como testar este projeto localmente

1. Abra o terminal e clone o repositório:
   `git clone https://github.com/SEU_USUARIO/doafacil-cli.git`
2. Acesse a pasta do projeto:
   `cd doafacil-cli`
3. Crie e ative um ambiente virtual (recomendado):
   `python -m venv venv`
   * No Linux/Mac: `source venv/bin/activate`
   * No Windows: `venv\Scripts\activate`
4. Instale as dependências declaradas:
   `pip install -r requirements.txt`
5. Para rodar a aplicação:
   `python src/app.py`
6. Para rodar os testes automatizados que comprovam a lógica:
   `pytest tests/`
