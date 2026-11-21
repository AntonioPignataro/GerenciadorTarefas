# Roteiro dos vídeos de defesa

Cada vídeo tem no máximo 10 minutos. O roteiro prevê **dois vídeos** (Parte I e Parte II).
Se o seu tutor aceitar um único vídeo para as duas partes, junte os dois, mas confira que não passa de 10 min
(os tempos abaixo somam ~13 min, então corte a demonstração de código).

> **Regras da atividade:** o vídeo precisa ser gravado por você, com a sua voz. Não é permitido usar IA nem leitor de
> texto na confecção do vídeo. Por isso, este roteiro é um **guia de tópicos**: leia, entenda e fale com as suas
> próprias palavras. Ensaie uma vez antes de gravar. As frases entre aspas são só sugestões.

**Como gravar (Mac):** `Cmd + Shift + 5` > "Gravar tela inteira" > Opções > Microfone: "Microfone integrado".
Grave em um ambiente silencioso, feche notificações, abra com antecedência: o PDF, o app no navegador
(`http://127.0.0.1:5000`) e o código no editor. **Depois de gravar, assista ao começo e ao fim para confirmar que há som.**

---

## VÍDEO 1 - Defesa da documentação (Parte I) - alvo: 6 a 7 min

Na tela: `docs/Documentacao.pdf` aberto.

| Tempo | O que mostrar | O que falar (tópicos) |
|---|---|---|
| 0:00 - 0:30 | Capa | Apresente-se: nome, curso, disciplina. "Este é o projeto Gerenciador de Tarefas, feito de forma individual (ou em dupla com ...)". |
| 0:30 - 1:30 | Introdução / Seção 1 | O que é o sistema: organizar afazeres com título, descrição, prazo e categorias. Stack: Python, Flask, SQLite, HTML/CSS. Por que essa escolha: simples, sem servidor de banco, fácil de executar. Mencione o CRUD sobre duas entidades: Tarefa e Categoria. |
| 1:30 - 2:30 | Requisitos / Seção 3 | Explique a diferença: funcionais = o que o sistema faz (ex.: RF01 cadastrar tarefa, RF03 filtrar); não funcionais = como ele é (ex.: RNF03 usa SQLite, RNF08 consultas parametrizadas). Cite 2 ou 3 de cada, não precisa ler todos. |
| 2:30 - 3:30 | Caso de uso / Seção 4.1 | Um ator, o Usuário, e 5 casos de uso: cadastrar, consultar, editar, excluir tarefa e gerenciar categorias. Diga que "concluir tarefa" faz parte de editar. |
| 3:30 - 4:30 | DER e Classes / 4.2 e 4.3 | Duas entidades, relação 1:N: uma categoria tem várias tarefas, cada tarefa tem no máximo uma categoria (FK opcional). Explique `ON DELETE SET NULL`: ao excluir uma categoria, as tarefas continuam, só ficam sem categoria. Mostre que o diagrama de classes é o mesmo modelo visto como objetos. |
| 4:30 - 5:30 | Diagrama de atividade / 4.4 | Percorra o fluxo do cadastro: clicar em Nova tarefa > preencher > salvar > o sistema valida o título > se vazio, mostra erro e volta; se válido, grava e volta para a lista. |
| 5:30 - 6:30 | Sequência / 4.5 | Escolha UC01 e explique a ordem das mensagens: Usuário > Navegador > Flask > SQLite e o retorno. Mostre o `alt` (título vazio x válido). Diga que os outros quatro diagramas seguem a mesma ideia, e cite uma diferença (ex.: UC04 tem a confirmação antes de excluir). |
| 6:30 - 7:00 | Conclusão / Seção 6 | O que você aprendeu: a modelagem ajuda a decidir a implementação (o DER virou as tabelas, as sequências viraram rotas); importância de tratar erros; testes automatizados. Agradeça e encerre. |

---

## VÍDEO 2 - Defesa da implementação (Parte II) - alvo: 6 a 7 min

Na tela: terminal, navegador com o app e editor com o código.

| Tempo | O que mostrar | O que falar (tópicos) |
|---|---|---|
| 0:00 - 0:30 | Repositório no GitHub | Apresente-se. Mostre o repositório: README, pastas e o commit/tag da entrega. Diga que o tutor e o `fernandonakagawa-unifil` têm acesso. |
| 0:30 - 1:15 | Terminal | Mostre como rodar: `pip install -r requirements.txt` e `python app.py`. Diga que o banco `tarefas.db` é criado automaticamente a partir do `schema.sql`. |
| 1:15 - 2:00 | Código: `schema.sql` | Duas tabelas, `categoria` e `tarefa`, com a chave estrangeira e `ON DELETE SET NULL`. Relacione com o DER da documentação. |
| 2:00 - 3:00 | Demo: categorias | Em Categorias: **cadastre** "Faculdade" e "Casa" (Create); mostre a lista com a contagem (Read); **renomeie** uma (Update). Tente cadastrar uma repetida para mostrar a mensagem de erro. |
| 3:00 - 4:30 | Demo: tarefas | **Cadastre** uma tarefa com título, descrição, prazo e categoria. Tente salvar sem título e mostre a validação. **Edite** uma tarefa. Marque outra como **concluída**. Use os **filtros** (por categoria e por situação). **Exclua** uma tarefa (mostre a confirmação). |
| 4:30 - 5:45 | Código: `app.py` | Mostre 2 ou 3 rotas: `criar_tarefa` (INSERT com `?` parametrizado, o que evita injeção de SQL), `listar_tarefas` (SELECT com LEFT JOIN e filtros) e `excluir_categoria`. Explique como cada uma vira uma operação do CRUD e um diagrama de sequência. |
| 5:45 - 6:30 | Testes | Rode `python -m unittest discover tests` e mostre os 4 testes passando. Diga que eles cobrem o CRUD de tarefas e de categorias. |
| 6:30 - 7:00 | Fechamento | Resuma: documentação e implementação coerentes, CRUD completo com SQLite. Cite o que aprendeu e uma melhoria futura (ex.: login de usuários). Encerre. |

---

## Checklist antes de enviar

- [ ] O vídeo abre e **tem som** (assista do começo ao fim, ao menos o início e o fim).
- [ ] Menos de 10 minutos cada.
- [ ] Se o arquivo for grande: suba no YouTube como **Não listado** e envie o link.
- [ ] Você não usou voz sintética nem leitor de texto.
