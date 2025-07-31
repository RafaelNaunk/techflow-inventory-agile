TechFlow Inventory – Sistema de Gerenciamento de Tarefas Ágil



Cliente fictício: Startup de Logística

Fornecedor: TechFlow Solutions

Disciplina: Engenharia de Software – Metodologias Ágeis

🎯 Objetivo

Criar um MVP (Minimum Viable Product) de um sistema web que permita gerir produtos de estoque e usuários, aplicando práticas de Kanban, CI/CD e qualidade de software dentro do ecossistema GitHub. O repositório serve de vitrine para o processo completo – planejamento, desenvolvimento, testes, gestão de mudanças e documentação – reproduzindo os desafios de um projeto real.

🗺️ Escopo Inicial

Módulo

Descrição

Autenticação

Login, logout, perfis ADM e COMUM

Produtos

CRUD completo (nome, quantidade, quantidade mínima, descrição)

Usuários (ADM)

Listar, criar e gerenciar usuários

Dashboard

Página inicial diferenciada por perfil

Banco

MySQL 8 + SQLAlchemy ORM

✨ Mudança de Escopo (Simulação)

Depois da sprint 1, o cliente solicitou alertas de estoque baixo. Essa alteração foi documentada na seção Changes deste README, acompanhada de um card na coluna A Fazer do quadro Projects ▶ Kanban e de um novo teste automatizado para garantir a regra de negócio.

🚀 Metodologia & Gestão

Kanban com três colunas: A Fazer, Em Progresso, Concluído (GitHub ▶ Projects).

Issues descrevem as tarefas; cada commit referencia a issue correspondente (fixes #id).

Definição de Pronto (Definition of Done):

Código compila e testes locais passam.

Pipeline do GitHub Actions é verde.

Documentação/README atualizada se necessário.

Acesse o quadro em Projects → Kanban para acompanhar o fluxo em tempo real.

🏗️ Estrutura do Repositório

techflow-inventory-agile/
├── app.py                # ponto de entrada Flask
├── requirements.txt      # dependências Python
├── script.sql            # criação do schema MySQL
├── src/                  # templates HTML e assets estáticos
├── tests/                # testes unitários + integração
├── docs/
│   └── uml/
│       ├── use_case.png  # Diagrama de Casos de Uso (draw.io)
│       └── class.png     # Diagrama de Classes (draw.io)
└── .github/
    └── workflows/
        └── python-app.yml # CI – lint + pytest

⚙️ Como Executar Localmente

Clone & venv

git clone https://github.com/RafaelNaunk/techflow-inventory-agile.git
cd techflow-inventory-agile
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

Banco de Dados

CREATE DATABASE db_controle CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SOURCE script.sql;  -- importa tabelas iniciais

Variáveis de Ambiente (opcional)

Variável

Padrão (app.py)

Sugestão

DB_USER

root

Conta só‑leitura

DB_PASSWORD

adminfecaf123!

Use secrets

SECRET_KEY

uma_chave_secreta_qualquer

openssl rand -hex 16

Run

flask --app app.py --debug run
# http://127.0.0.1:5000

Dica: crie um usuário ADM diretamente na tabela usuario ou via formulário /usuarios/novo após migração.

🔬 Qualidade & DevOps

Testes: pytest tests/ cobre regras de negócio e rotas.

Lint: flake8 verifica PEP 8.

CI: Workflow python-app.yml roda em pull‑requests & push na main.

name: Python CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest -q

Logs completos em Actions.

📋 Requisitos Funcionais

RF‑01 – O sistema deve permitir autenticação de usuário com perfis ADM e COMUM.

RF‑02 – O usuário ADM deve cadastrar, editar e excluir produtos.

RF‑03 – Qualquer usuário autenticado deve listar produtos.

RF‑04 – (Mudança de Escopo) Exibir alerta visual quando qtde < quantidade_minima.

Requisitos Não Funcionais

RNF‑01 – Aplicação deve responder em < 300 ms para operações CRUD locais.

RNF‑02 – Código deve seguir PEP 8 (Python).

RNF‑03 – Pipeline CI deve executar testes em < 2 min.

🖼️ UML & Documentação

Imagens geradas no draw.io estão em docs/uml/ e versionadas no repositório.

Diagrama

Arquivo

Casos de Uso

use_case.png

Classes

class.png

🔄 Changes (Gestão de Mudanças)

Data

Descrição

Justificativa

Status

2025‑07‑28

Nova regra de alerta de estoque baixo

Evitar rupturas críticas para operação da startup

Concluído

Todas as mudanças seguem o workflow: Issue → Pull Request → Review → Merge, com documentação nesta seção.

🤝 Contribuição

Siga o padrão Conventional Commits:

tipo(escopo): resumo

[corpo opcional]

Tipos mais usados: feat, fix, docs, refactor, test, chore.

Branching

main ← dev ← feature/descrição‑curta

Crie pull requests para dev; merge em main apenas quando o CI estiver verde.

📜 Licença

MIT – uso acadêmico e educacional livre.# techflow-inventory-agile
