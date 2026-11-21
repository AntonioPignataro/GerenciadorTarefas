# Gerenciador de Tarefas

Projeto de Desenvolvimento de Software I e II.
**Autor:** Antonio Pignataro (trabalho individual)

Aplicação web simples para organizar tarefas e categorias, com CRUD completo e banco de dados relacional.

## Tecnologias

- Python 3 + Flask
- SQLite (módulo `sqlite3` da biblioteca padrão)
- HTML/CSS (templates Jinja2)

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acesse <http://127.0.0.1:5000>. O banco `tarefas.db` é criado automaticamente.

## Testes

```bash
python -m unittest discover tests
```

## Funcionalidades (CRUD)

| Operação | Tarefas | Categorias |
|---|---|---|
| Create | `POST /tarefas/nova` | `POST /categorias` |
| Read | `GET /` (com filtros) | `GET /categorias` |
| Update | `POST /tarefas/<id>/editar`, `/concluir` | `POST /categorias/<id>/editar` |
| Delete | `POST /tarefas/<id>/excluir` | `POST /categorias/<id>/excluir` |

## Estrutura

```
app.py            rotas e acesso ao banco
schema.sql        criação das tabelas
templates/        páginas HTML
static/           CSS
tests/            testes automatizados
docs/             documentação (PDF), roteiro dos vídeos e script que gera o PDF
```

## Documentação

`docs/Documentacao.pdf` (requisitos, casos de uso, DER, atividade, classes e sequência).
Para regenerar: `.venv/bin/pip install pypdf && cd docs/tools && npm install && cd ../.. && .venv/bin/python docs/build_docs.py`
(os dados da capa ficam no início de `docs/build_docs.py`).
