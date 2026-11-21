"""Gera docs/Documentacao.pdf (HTML + Mermaid -> Chrome headless -> PDF).

Uso:  .venv/bin/python docs/build_docs.py
Edite a seção CONFIG abaixo para preencher os dados da capa.
"""
import html
import os
import re
import subprocess
import sys

from pypdf import PdfReader

# ----------------------------------------------------------------- CONFIG (capa)
AUTORES = ["Antonio Pignataro"]          # dupla? adicione o outro nome na lista
INSTITUICAO = "UniFil - Centro Universitário Filadélfia"
CURSO = "Engenharia de Software"
RA = "253466044"                          # com dupla, use ex.: "Nome A (RA 1) e Nome B (RA 2)" em AUTORES e deixe RA vazio
DISCIPLINA = "Projeto de Desenvolvimento de Software I e II"
REPOSITORIO = ""                          # ex.: "https://github.com/usuario/GerenciadorTarefas"
CIDADE = "São Paulo"
ANO = "2026"
SUBTITULO = "Documentação e implementação de um sistema web de gestão de tarefas"
# -------------------------------------------------------------------------------

AQUI = os.path.dirname(os.path.abspath(__file__))
MERMAID_JS = os.path.join(AQUI, "tools", "node_modules", "mermaid", "dist", "mermaid.min.js")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML_OUT = os.path.join(AQUI, "documentacao.html")
PDF_OUT = os.path.join(AQUI, "Documentacao.pdf")

TITULO = "Gerenciador de Tarefas"

# ------------------------------------------------------------------ Diagramas
DIAGRAMAS = {}

DIAGRAMAS["der"] = """
erDiagram
    CATEGORIA ||--o{ TAREFA : "classifica"
    CATEGORIA {
        INTEGER id PK
        TEXT nome "UNIQUE, NOT NULL"
    }
    TAREFA {
        INTEGER id PK
        TEXT titulo "NOT NULL"
        TEXT descricao
        TEXT prazo "AAAA-MM-DD"
        INTEGER concluida "0 ou 1"
        INTEGER categoria_id FK "opcional"
    }
"""

DIAGRAMAS["classes"] = """
classDiagram
    class Categoria {
        -int id
        -String nome
        +cadastrar()
        +renomear(nome)
        +excluir()
        +listar() List~Categoria~
    }
    class Tarefa {
        -int id
        -String titulo
        -String descricao
        -Date prazo
        -boolean concluida
        +cadastrar()
        +editar()
        +alternarConclusao()
        +excluir()
        +listar(categoria, status) List~Tarefa~
    }
    Categoria "0..1" <-- "0..*" Tarefa : pertence a
"""

DIAGRAMAS["atividade"] = """
flowchart TD
    subgraph U["Usuário"]
        A((Início)) --> B[Clica em 'Nova tarefa']
        B --> C[Preenche título, descrição, prazo e categoria]
        C --> D[Clica em 'Salvar']
        L[Visualiza a tarefa na lista] --> M((Fim))
        K[Corrige o título]
    end
    subgraph S["Sistema"]
        E{Título preenchido?}
        F[Exibe mensagem de erro]
        G[Insere a tarefa no banco de dados]
        H[Exibe mensagem de sucesso]
        I[Redireciona para a lista de tarefas]
    end
    D --> E
    E -- Não --> F --> K --> D
    E -- Sim --> G --> H --> I --> L
"""

DIAGRAMAS["seq1"] = """
sequenceDiagram
    actor U as Usuário
    participant N as Navegador
    participant A as Aplicação Flask
    participant B as SQLite
    U->>N: Clica em "Nova tarefa"
    N->>A: GET /tarefas/nova
    A->>B: SELECT categorias
    B-->>A: lista de categorias
    A-->>N: formulário de tarefa
    U->>N: Preenche dados e clica em "Salvar"
    N->>A: POST /tarefas/nova
    alt título vazio
        A-->>N: formulário com mensagem de erro
    else título válido
        A->>B: INSERT INTO tarefa
        B-->>A: confirmação
        A-->>N: redireciona para / (mensagem de sucesso)
        N->>A: GET /
        A-->>N: lista de tarefas atualizada
    end
"""

DIAGRAMAS["seq2"] = """
sequenceDiagram
    actor U as Usuário
    participant N as Navegador
    participant A as Aplicação Flask
    participant B as SQLite
    U->>N: Abre a página inicial (ou aplica filtros)
    N->>A: GET / ?categoria=&status=
    A->>B: SELECT tarefa LEFT JOIN categoria (com filtros)
    B-->>A: tarefas
    A->>B: SELECT categorias (para o filtro)
    B-->>A: categorias
    A-->>N: página HTML com a tabela de tarefas
    N-->>U: exibe a lista
"""

DIAGRAMAS["seq3"] = """
sequenceDiagram
    actor U as Usuário
    participant N as Navegador
    participant A as Aplicação Flask
    participant B as SQLite
    U->>N: Clica em "Editar"
    N->>A: GET /tarefas/{id}/editar
    A->>B: SELECT tarefa WHERE id
    B-->>A: dados da tarefa
    A-->>N: formulário preenchido
    U->>N: Altera os dados e clica em "Salvar"
    N->>A: POST /tarefas/{id}/editar
    alt título vazio
        A-->>N: formulário com mensagem de erro
    else título válido
        A->>B: UPDATE tarefa
        B-->>A: confirmação
        A-->>N: redireciona para a lista
    end
    opt Concluir / reabrir
        U->>N: Clica na caixa de seleção da tarefa
        N->>A: POST /tarefas/{id}/concluir
        A->>B: UPDATE tarefa SET concluida = 1 - concluida
        A-->>N: redireciona para a lista
    end
"""

DIAGRAMAS["seq4"] = """
sequenceDiagram
    actor U as Usuário
    participant N as Navegador
    participant A as Aplicação Flask
    participant B as SQLite
    U->>N: Clica em "Excluir"
    N-->>U: pede confirmação
    alt usuário confirma
        U->>N: Confirma
        N->>A: POST /tarefas/{id}/excluir
        A->>B: DELETE FROM tarefa WHERE id
        B-->>A: confirmação
        A-->>N: redireciona para a lista (mensagem de sucesso)
    else usuário cancela
        U->>N: Cancela
        N-->>U: nada é alterado
    end
"""

DIAGRAMAS["seq5"] = """
sequenceDiagram
    actor U as Usuário
    participant N as Navegador
    participant A as Aplicação Flask
    participant B as SQLite
    U->>N: Abre "Categorias"
    N->>A: GET /categorias
    A->>B: SELECT categorias com contagem de tarefas
    B-->>A: categorias
    A-->>N: página de categorias
    alt Cadastrar
        U->>N: Informa o nome e clica em "Adicionar"
        N->>A: POST /categorias
        A->>B: INSERT INTO categoria
        alt nome já existe
            B-->>A: erro de unicidade
            A-->>N: mensagem "já existe uma categoria"
        else nome inédito
            B-->>A: confirmação
            A-->>N: redireciona para /categorias
        end
    else Renomear
        U->>N: Altera o nome e clica em "Renomear"
        N->>A: POST /categorias/{id}/editar
        A->>B: UPDATE categoria
        A-->>N: redireciona para /categorias
    else Excluir
        U->>N: Clica em "Excluir" e confirma
        N->>A: POST /categorias/{id}/excluir
        A->>B: DELETE FROM categoria (tarefas ficam sem categoria)
        A-->>N: redireciona para /categorias
    end
"""


def fig(chave, legenda):
    return (
        f'<figure><figcaption>{legenda}</figcaption>'
        f'<pre class="mermaid">{html.escape(DIAGRAMAS[chave].strip())}</pre>'
        f'<p class="fonte">Fonte: Elaborado pelo autor ({ANO}).</p></figure>'
    )


def use_case_svg():
    """Diagrama de casos de uso com os 5 casos (gerado em SVG)."""
    casos = [
        ("UC01 - Cadastrar tarefa", "inclui validar título"),
        ("UC02 - Consultar tarefas", "filtros por categoria e situação"),
        ("UC03 - Editar tarefa", "inclui concluir / reabrir"),
        ("UC04 - Excluir tarefa", "com confirmação"),
        ("UC05 - Gerenciar categorias", "cadastrar, renomear e excluir"),
    ]
    ys = [95, 185, 275, 365, 455]
    partes = [
        '<svg viewBox="0 0 760 520" xmlns="http://www.w3.org/2000/svg" font-family="Helvetica, Arial, sans-serif" font-size="14">',
        '<rect x="230" y="10" width="515" height="500" rx="8" fill="#fafbfd" stroke="#444" stroke-width="1.5"/>',
        '<text x="487" y="38" text-anchor="middle" font-weight="bold">Sistema Gerenciador de Tarefas</text>',
        '<g stroke="#222" stroke-width="2" fill="none"><circle cx="80" cy="250" r="16"/>'
        '<line x1="80" y1="266" x2="80" y2="320"/><line x1="45" y1="285" x2="115" y2="285"/>'
        '<line x1="80" y1="320" x2="50" y2="365"/><line x1="80" y1="320" x2="110" y2="365"/></g>',
        '<text x="80" y="392" text-anchor="middle" font-weight="bold">Usuário</text>',
    ]
    for (nome, nota), y in zip(casos, ys):
        partes.append(f'<line x1="112" y1="285" x2="347" y2="{y}" stroke="#222" stroke-width="1.5"/>')
    for (nome, nota), y in zip(casos, ys):
        partes.append(
            f'<ellipse cx="487" cy="{y}" rx="145" ry="36" fill="#e8f0fb" stroke="#2b4c7e" stroke-width="1.5"/>'
            f'<text x="487" y="{y - 2}" text-anchor="middle">{nome}</text>'
            f'<text x="487" y="{y + 16}" text-anchor="middle" font-size="11" fill="#555">({nota})</text>'
        )
    partes.append("</svg>")
    return "".join(partes)


CSS = open(os.path.join(AQUI, "estilo_abnt.css"), encoding="utf-8").read()


def requisitos():
    rf = [
        ("RF01", "O sistema deve permitir cadastrar uma tarefa informando título (obrigatório), descrição, prazo e categoria (opcionais)."),
        ("RF02", "O sistema deve listar as tarefas cadastradas, exibindo título, descrição, categoria, prazo e situação."),
        ("RF03", "O sistema deve permitir filtrar a lista de tarefas por categoria e por situação (pendentes ou concluídas)."),
        ("RF04", "O sistema deve permitir editar os dados de uma tarefa existente."),
        ("RF05", "O sistema deve permitir marcar uma tarefa como concluída e reabri-la."),
        ("RF06", "O sistema deve permitir excluir uma tarefa, mediante confirmação do usuário."),
        ("RF07", "O sistema deve permitir cadastrar categorias com nome único e obrigatório."),
        ("RF08", "O sistema deve listar as categorias, informando quantas tarefas pertencem a cada uma."),
        ("RF09", "O sistema deve permitir renomear uma categoria."),
        ("RF10", "O sistema deve permitir excluir uma categoria; as tarefas dela devem permanecer, porém sem categoria."),
        ("RF11", "O sistema deve exibir mensagens de sucesso ou de erro após cada operação."),
    ]
    rnf = [
        ("RNF01", "Usabilidade", "A interface deve ser web e dispensar treinamento: cadastrar uma tarefa deve exigir no máximo 3 cliques a partir da tela inicial, sem contar o preenchimento dos campos."),
        ("RNF02", "Restrição de implementação", "O sistema deve ser desenvolvido em Python 3 com o micro-framework Flask."),
        ("RNF03", "Restrição de implementação", "Os dados devem ser armazenados em um banco de dados relacional SQLite."),
        ("RNF04", "Integridade", "O banco deve garantir a integridade referencial entre tarefa e categoria por meio de chave estrangeira."),
        ("RNF05", "Desempenho", "A listagem de tarefas deve responder em menos de 1 segundo com até 5.000 tarefas cadastradas."),
        ("RNF06", "Portabilidade", "O sistema deve executar em qualquer sistema operacional com Python 3 instalado."),
        ("RNF07", "Manutenibilidade", "O código deve possuir testes automatizados que cubram as operações de CRUD."),
        ("RNF08", "Segurança", "O sistema deve ser protegido contra injeção de SQL, utilizando consultas parametrizadas em todos os acessos ao banco."),
    ]
    linhas_rf = "".join(f"<tr><td>{c}</td><td>{d}</td></tr>" for c, d in rf)
    linhas_rnf = "".join(f"<tr><td>{c}</td><td>{t}</td><td>{d}</td></tr>" for c, t, d in rnf)
    return (
        "<h3>3.1 Requisitos Funcionais</h3>"
        f"<table><tr><th style='width:16%'>Código</th><th>Descrição</th></tr>{linhas_rf}</table>"
        "<h3>3.2 Requisitos Não Funcionais</h3>"
        f"<table><tr><th style='width:16%'>Código</th><th style='width:22%'>Categoria</th><th>Descrição</th></tr>{linhas_rnf}</table>"
    )


def corpo():
    autores = " e ".join(AUTORES)
    ident = "dupla" if len(AUTORES) > 1 else "individual"
    return f"""
<section id="s1" class="sem-quebra" style="page-break-before: always">
<h2>1. Introdução</h2>
<p>Este documento descreve o projeto <b>{TITULO}</b>, desenvolvido por {autores} (trabalho {ident}) para a disciplina
{DISCIPLINA}. O objetivo é projetar e implementar um sistema de software completo, passando pelo levantamento de
requisitos, pela modelagem com diagramas da UML e do modelo de dados e pela implementação com acesso a banco de dados.</p>
<p>O <b>Gerenciador de Tarefas</b> é uma aplicação web para organização de afazeres pessoais. O usuário cadastra tarefas
com título, descrição e prazo, agrupa-as em categorias (por exemplo, "Faculdade", "Casa" ou "Trabalho"), acompanha quais
estão pendentes ou concluídas e pode editar ou excluir qualquer registro. O sistema contempla as quatro operações de CRUD
(<i>Create, Read, Update, Delete</i>) sobre duas entidades: <b>Tarefa</b> e <b>Categoria</b>.</p>
<h3>1.1 Tecnologias utilizadas (stack)</h3>
<ul>
<li><b>Linguagem:</b> Python 3;</li>
<li><b>Framework web:</b> Flask, responsável pelas rotas e pela renderização das páginas com o motor de templates Jinja2 (PALLETS PROJECTS, [s. d.]);</li>
<li><b>Banco de dados:</b> SQLite (relacional) (SQLITE, [s. d.]), acessado pelo módulo <code>sqlite3</code> da biblioteca padrão do Python (PYTHON SOFTWARE FOUNDATION, [s. d.]);</li>
<li><b>Front-end:</b> HTML5 e CSS3 simples, sem bibliotecas externas;</li>
<li><b>Testes:</b> módulo <code>unittest</code> com o cliente de testes do Flask;</li>
<li><b>Controle de versão:</b> Git e GitHub{(" (" + html.escape(REPOSITORIO) + ")") if REPOSITORIO else ""}.</li>
</ul>
<h3>1.2 Escolha do tema e das tecnologias</h3>
<p>O tema foi escolhido por ser de fácil entendimento e por permitir exercitar todos os conceitos pedidos com poucas
entidades. As tecnologias foram escolhidas pela simplicidade: o SQLite dispensa a instalação de um servidor de banco de
dados e o Flask permite construir a aplicação com poucos arquivos, o que facilita a execução e a avaliação do projeto.</p>
</section>

<section id="s2">
<h2>2. Visão Geral do Sistema</h2>
<p>O sistema possui um único perfil de usuário, que realiza todas as operações. Não há autenticação, já que o foco do
trabalho é a modelagem e o CRUD. A aplicação é composta pelas seguintes telas:</p>
<table>
<tr><th>Tela</th><th>Rota</th><th>Função</th></tr>
<tr><td>Lista de tarefas</td><td><code>/</code></td><td>Exibe as tarefas, permite filtrar, concluir, editar e excluir.</td></tr>
<tr><td>Nova tarefa</td><td><code>/tarefas/nova</code></td><td>Formulário de cadastro de tarefa.</td></tr>
<tr><td>Editar tarefa</td><td><code>/tarefas/&lt;id&gt;/editar</code></td><td>Formulário de alteração de tarefa.</td></tr>
<tr><td>Categorias</td><td><code>/categorias</code></td><td>Cadastro, listagem, renomeação e exclusão de categorias.</td></tr>
</table>
<p>A arquitetura segue o padrão de uma aplicação web de três camadas: o navegador (apresentação), a aplicação Flask
(regras de negócio e rotas) e o banco SQLite (persistência).</p>
</section>

<section id="s3">
<h2>3. Levantamento de Requisitos</h2>
<p>Os requisitos foram divididos em funcionais, que descrevem o que o sistema deve fazer, e não funcionais, que descrevem restrições e qualidades do sistema, conforme a distinção apresentada por Sommerville (2018). Entre os requisitos não funcionais, dois são restrições de implementação, que fixam a tecnologia utilizada, e os demais são qualidades do produto, como usabilidade, desempenho e segurança.</p>
{requisitos()}
</section>

<section id="s4">
<h2>4. Modelagem</h2>
<h3>4.1 Diagrama de Casos de Uso</h3>
<p>A modelagem utilizou diagramas da UML (FOWLER, 2005), desenhados com a ferramenta Mermaid (MERMAID, [s. d.]). O diagrama abaixo apresenta os cinco casos de uso do sistema e o ator <b>Usuário</b>, que interage com todos eles.</p>
<figure><figcaption>Figura 1 – Diagrama de casos de uso.</figcaption>{use_case_svg()}<p class="fonte">Fonte: Elaborado pelo autor ({ANO}).</p></figure>
<table>
<tr><th style="width:26%">Caso de uso</th><th>Descrição</th><th style="width:20%">Requisitos</th></tr>
<tr><td>UC01 - Cadastrar tarefa</td><td>O usuário informa os dados da tarefa e o sistema a grava, validando que o título foi preenchido.</td><td>RF01, RF11</td></tr>
<tr><td>UC02 - Consultar tarefas</td><td>O usuário visualiza a lista de tarefas, podendo filtrar por categoria e situação.</td><td>RF02, RF03</td></tr>
<tr><td>UC03 - Editar tarefa</td><td>O usuário altera os dados de uma tarefa ou a marca como concluída / pendente.</td><td>RF04, RF05, RF11</td></tr>
<tr><td>UC04 - Excluir tarefa</td><td>O usuário remove uma tarefa após confirmar a operação.</td><td>RF06, RF11</td></tr>
<tr><td>UC05 - Gerenciar categorias</td><td>O usuário cadastra, lista, renomeia e exclui categorias.</td><td>RF07 a RF11</td></tr>
</table>
</section>

<section id="s5">
<h3>4.2 Diagrama Entidade-Relacionamento (DER)</h3>
<p>O modelo de dados, elaborado segundo a abordagem entidade-relacionamento (ELMASRI; NAVATHE, 2018), possui duas entidades. Uma categoria pode classificar várias tarefas (relacionamento 1:N) e cada
tarefa pertence a no máximo uma categoria, pois a chave estrangeira é opcional. Ao excluir uma categoria, a chave
estrangeira das tarefas é definida como nula (<code>ON DELETE SET NULL</code>).</p>
{fig("der", "Figura 2 – Diagrama Entidade-Relacionamento.")}
<h3>4.3 Diagrama de Classes</h3>
<p>O diagrama de classes está focado nas entidades do domínio. A classe <b>Tarefa</b> referencia a classe
<b>Categoria</b>; uma categoria pode ter zero ou mais tarefas.</p>
{fig("classes", "Figura 3 – Diagrama de classes das entidades.")}
</section>

<section id="s6">
<h3>4.4 Diagrama de Atividade</h3>
<p>O diagrama de atividade descreve o fluxo do caso de uso UC01 (Cadastrar tarefa), incluindo o desvio que ocorre quando
o título não é informado.</p>
{fig("atividade", "Figura 4 – Diagrama de atividade do cadastro de tarefa.")}
</section>

<section id="s7">
<h3>4.5 Diagramas de Sequência</h3>
<p>Cada caso de uso possui um diagrama de sequência que mostra a troca de mensagens entre o usuário, o navegador, a
aplicação Flask e o banco de dados SQLite.</p>
<h3>4.5.1 UC01 - Cadastrar tarefa</h3>
{fig("seq1", "Figura 5 – Sequência do UC01.")}
</section>
<section id="s8">
<h3>4.5.2 UC02 - Consultar tarefas</h3>
{fig("seq2", "Figura 6 – Sequência do UC02.")}
<h3>4.5.3 UC03 - Editar tarefa</h3>
{fig("seq3", "Figura 7 – Sequência do UC03.")}
</section>
<section id="s9">
<h3>4.5.4 UC04 - Excluir tarefa</h3>
{fig("seq4", "Figura 8 – Sequência do UC04.")}
<h3>4.5.5 UC05 - Gerenciar categorias</h3>
{fig("seq5", "Figura 9 – Sequência do UC05.")}
</section>

<section id="s10">
<h2>5. Implementação</h2>
<p>A implementação está no repositório do projeto e segue a documentação acima. A estrutura de arquivos é:</p>
<table>
<tr><th>Arquivo</th><th>Função</th></tr>
<tr><td><code>app.py</code></td><td>Aplicação Flask: rotas, regras e acesso ao banco.</td></tr>
<tr><td><code>schema.sql</code></td><td>Script de criação das tabelas (<code>categoria</code> e <code>tarefa</code>).</td></tr>
<tr><td><code>templates/</code></td><td>Páginas HTML (Jinja2): base, lista, formulário de tarefa e categorias.</td></tr>
<tr><td><code>static/style.css</code></td><td>Estilos da interface.</td></tr>
<tr><td><code>tests/test_app.py</code></td><td>Testes automatizados do CRUD.</td></tr>
</table>
<h3>5.1 Mapeamento do CRUD</h3>
<table>
<tr><th>Operação</th><th>Tarefa</th><th>Categoria</th></tr>
<tr><td>Create</td><td><code>POST /tarefas/nova</code></td><td><code>POST /categorias</code></td></tr>
<tr><td>Read</td><td><code>GET /</code></td><td><code>GET /categorias</code></td></tr>
<tr><td>Update</td><td><code>POST /tarefas/&lt;id&gt;/editar</code> e <code>/concluir</code></td><td><code>POST /categorias/&lt;id&gt;/editar</code></td></tr>
<tr><td>Delete</td><td><code>POST /tarefas/&lt;id&gt;/excluir</code></td><td><code>POST /categorias/&lt;id&gt;/excluir</code></td></tr>
</table>
<h3>5.2 Como executar</h3>
<ol>
<li>Instalar as dependências: <code>pip install -r requirements.txt</code>;</li>
<li>Executar: <code>python app.py</code> (o banco <code>tarefas.db</code> é criado automaticamente);</li>
<li>Acessar <code>http://127.0.0.1:5001</code> no navegador;</li>
<li>Rodar os testes: <code>python -m unittest discover tests</code>.</li>
</ol>
</section>

<section id="s11">
<h2>6. Conclusão</h2>
<p>Com este projeto foi possível percorrer, na prática, as etapas principais do desenvolvimento de um software: levantar
requisitos funcionais e não funcionais, modelar o comportamento com casos de uso, atividade e sequência, modelar os dados
com o DER e o diagrama de classes e, por fim, implementar o sistema de acordo com essa documentação.</p>
<p>O principal aprendizado foi perceber como a modelagem antecipa decisões da implementação: o DER definiu diretamente as
tabelas e a chave estrangeira, e os diagramas de sequência indicaram quais rotas e consultas SQL seriam necessárias.
Também foi importante tratar casos de erro, como o título vazio e o nome de categoria repetido, e decidir o que acontece
com as tarefas quando uma categoria é excluída. Por fim, os testes automatizados mostraram que é possível verificar o
CRUD de forma rápida e repetível.</p>
<p>Como melhorias futuras, o sistema poderia ganhar autenticação de usuários, prioridades para as tarefas, lembretes de
prazo e uma API para integração com aplicativos móveis.</p>
</section>

<section id="s12" class="refs">
<h2 style="text-align:center">REFERÊNCIAS</h2>
<p>ELMASRI, R.; NAVATHE, S. B. <b>Sistemas de banco de dados</b>. 7. ed. São Paulo: Pearson, 2018.</p>
<p>FOWLER, M. <b>UML essencial</b>: um breve guia para a linguagem-padrão de modelagem de objetos. 3. ed. Porto Alegre: Bookman, 2005.</p>
<p>MERMAID. <b>Mermaid documentation</b>. [S. l.], [s. d.]. Disponível em: https://mermaid.js.org/. Acesso em: 21 nov. 2026.</p>
<p>PALLETS PROJECTS. <b>Flask documentation</b>. [S. l.], [s. d.]. Disponível em: https://flask.palletsprojects.com/. Acesso em: 21 nov. 2026.</p>
<p>PYTHON SOFTWARE FOUNDATION. <b>sqlite3</b>: DB-API 2.0 interface for SQLite databases. [S. l.], [s. d.]. Disponível em: https://docs.python.org/3/library/sqlite3.html. Acesso em: 21 nov. 2026.</p>
<p>SOMMERVILLE, I. <b>Engenharia de software</b>. 10. ed. São Paulo: Pearson, 2018.</p>
<p>SQLITE. <b>SQLite documentation</b>. [S. l.], [s. d.]. Disponível em: https://www.sqlite.org/docs.html. Acesso em: 21 nov. 2026.</p>
</section>
"""


def capa():
    autor = " e ".join(html.escape(a.upper()) for a in AUTORES)
    return f"""
<div class="capa">
  <div class="logo"><img src="assets/logo_unifil.jpeg" alt="UniFil - Centro Universitário Filadélfia"></div>
  <p class="autor">{autor}</p>
  <div class="miolo"><p class="titulo">{TITULO}:</p><p class="subtitulo">{html.escape(SUBTITULO)}</p></div>
  <div class="base"><p>{html.escape(CIDADE)}<br>{html.escape(ANO)}</p></div>
</div>"""


def folha_rosto():
    autor = " e ".join(html.escape(a.upper()) for a in AUTORES)
    ra = f" (RA {html.escape(RA)})" if RA else ""
    nota = (
        f"Documentação do projeto de software desenvolvido na disciplina {html.escape(DISCIPLINA)}, "
        f"do curso de {html.escape(CURSO)} do {html.escape(INSTITUICAO)}. "
        f"Aluno: {' e '.join(html.escape(a) for a in AUTORES)}{ra}."
    )
    return f"""
<div class="rosto">
  <p class="autor">{autor}</p>
  <div class="miolo"><p class="titulo">{TITULO}:</p><p class="subtitulo">{html.escape(SUBTITULO)}</p>
  <p class="nota">{nota}</p></div>
  <div class="base"><p>{html.escape(CIDADE)}<br>{html.escape(ANO)}</p></div>
</div>"""


def sumario(paginas):
    itens = [
        ("n2", "1. Introdução"), ("n3", "1.1 Tecnologias utilizadas (stack)"), ("n3", "1.2 Escolha do tema e das tecnologias"),
        ("n2", "2. Visão Geral do Sistema"),
        ("n2", "3. Levantamento de Requisitos"), ("n3", "3.1 Requisitos Funcionais"), ("n3", "3.2 Requisitos Não Funcionais"),
        ("n2", "4. Modelagem"), ("n3", "4.1 Diagrama de Casos de Uso"), ("n3", "4.2 Diagrama Entidade-Relacionamento (DER)"),
        ("n3", "4.3 Diagrama de Classes"), ("n3", "4.4 Diagrama de Atividade"), ("n3", "4.5 Diagramas de Sequência"),
        ("n3", "4.5.1 UC01 - Cadastrar tarefa"), ("n3", "4.5.2 UC02 - Consultar tarefas"), ("n3", "4.5.3 UC03 - Editar tarefa"),
        ("n3", "4.5.4 UC04 - Excluir tarefa"), ("n3", "4.5.5 UC05 - Gerenciar categorias"),
        ("n2", "5. Implementação"), ("n3", "5.1 Mapeamento do CRUD"), ("n3", "5.2 Como executar"),
        ("n2", "6. Conclusão"), ("n2", "REFERÊNCIAS"),
    ]
    lis = "".join(
        f'<li class="{c}"><span class="t">{html.escape(t)}</span><span class="p"></span><span>{paginas.get(t, "")}</span></li>'
        for c, t in itens
    )
    return f'<section class="toc"><h2>SUMÁRIO</h2><ul style="margin-left:0">{lis}</ul></section>', [t for _, t in itens]


QUADROS = [
    "Telas do sistema", "Requisitos funcionais", "Requisitos não funcionais", "Descrição dos casos de uso",
    "Estrutura de arquivos do projeto", "Mapeamento das operações de CRUD",
]


def numerar_quadros(h):
    it = iter(enumerate(QUADROS, 1))

    def sub(m):
        n, t = next(it)
        return (f'<div class="quadro"><p class="cap">Quadro {n} – {t}</p>{m.group(0)}'
                f'<p class="fonte">Fonte: Elaborado pelo autor ({ANO}).</p></div>')

    out = re.sub(r"<table.*?</table>", sub, h, flags=re.S)
    assert next(it, None) is None, "faltam tabelas para os quadros"
    return out


def montar(paginas):
    toc_html, titulos = sumario(paginas)
    corpo_html = numerar_quadros(corpo()).replace('<section id="s1" class="sem-quebra" style="page-break-before: always">', '<section id="s1">')
    pagina = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Documentação - {TITULO}</title>
<style>{CSS}</style></head><body>
{capa()}{folha_rosto()}{toc_html}{corpo_html}
<script src="tools/node_modules/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad: true, theme: 'neutral', securityLevel: 'loose', themeVariables: {{fontSize: '15px'}}}});</script>
</body></html>"""
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(pagina)
    return titulos


def gerar_pdf():
    cmd = [
        CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
        "--virtual-time-budget=30000", f"--print-to-pdf={PDF_OUT}", "file://" + HTML_OUT,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)


def achar_paginas(titulos):
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    leitor = PdfReader(PDF_OUT)
    textos = [norm(p.extract_text() or "") for p in leitor.pages]
    # começa na página 4: pula capa (1), folha de rosto (2) e sumário (3)
    paginas = {}
    for t in titulos:
        for i in range(3, len(textos)):
            if norm(t) in textos[i]:
                paginas[t] = i + 1
                break
    return paginas, len(textos)


def main():
    if not os.path.exists(MERMAID_JS):
        sys.exit("Mermaid não encontrado. Rode: cd docs/tools && npm install mermaid@11.4.1")
    titulos = montar({})
    gerar_pdf()
    paginas, total = achar_paginas(titulos)
    montar(paginas)
    gerar_pdf()
    faltando = [t for t in titulos if t not in paginas]
    print(f"PDF gerado: {PDF_OUT} ({total} páginas)")
    if faltando:
        print("Títulos não localizados no PDF:", faltando)


if __name__ == "__main__":
    main()
