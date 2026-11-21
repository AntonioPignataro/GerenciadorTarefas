# Roteiro completo dos vídeos de defesa

Este arquivo tem **tudo o que você precisa falar e fazer**, na ordem, sem precisar consultar outro lugar.
Cada vídeo fica em torno de 7 a 8 minutos, dentro do limite de 10.

- Texto normal = o que **falar** (em voz alta, com a sua voz, em ritmo calmo).
- **[TELA: ...]** = o que mostrar ou fazer na tela naquele momento. Não fale essa parte.
- Pode trocar palavras para soar natural. O importante é não ler como se fosse uma leitura robótica.

> **Atenção à regra da atividade:** ela proíbe IA e leitores de texto (voz sintética) na confecção do vídeo.
> Falar com a sua própria voz é o esperado. Como este roteiro foi redigido com apoio de IA, se tiver
> dúvida, pergunte ao tutor antes de gravar se não há problema em usar um roteiro de apoio.

---

## Antes de gravar (preparação, 5 minutos)

1. **Abra estas janelas** e deixe prontas:
   - o PDF `docs/Documentacao.pdf` (para o Vídeo 1);
   - o repositório no navegador: https://github.com/AntonioPignataro/GerenciadorTarefas (Vídeo 2);
   - o terminal e o editor de código, com `schema.sql` e `app.py` abertos (Vídeo 2).
2. **Para o Vídeo 2, abra um terminal novo e não rode nada antes de gravar.** Todos os comandos, desde entrar na
   pasta do projeto, são digitados **durante** o vídeo, como está no roteiro.
3. **Gravação de tela no Mac:** `Cmd + Shift + 5` > "Gravar tela inteira" > **Opções** > Microfone: "Microfone integrado".
4. Silencie notificações (Não Perturbe) e grave em lugar silencioso.
5. Se errar, **não pare**: respire, repita a frase e siga. Pequenos tropeços são normais.
6. **Depois de gravar:** assista ao começo e ao fim para confirmar que o **som** está bem. Cada vídeo deve ter menos de 10 minutos.

---
---

# VÍDEO 1 - Defesa da documentação (Parte I)

### Abertura (0:00)

**[TELA: capa do PDF]**

Olá! Meu nome é Antonio Pignataro, meu RA é 253466044, e sou aluno do curso de Engenharia de Software da UniFil.
Neste vídeo eu vou apresentar a documentação do meu projeto da disciplina de Projeto de Desenvolvimento de Software, Parte I.
O trabalho foi feito de forma individual. O projeto se chama Gerenciador de Tarefas. A implementação dele eu apresento no segundo vídeo.

**[TELA: página do sumário]**

Aqui no sumário dá para ver a estrutura do documento: introdução, visão geral do sistema, levantamento de requisitos,
a modelagem, com todos os diagramas, a implementação, a conclusão e as referências.

### 1. Introdução (≈ 0:40)

**[TELA: seção 1 - Introdução]**

O Gerenciador de Tarefas é uma aplicação web para organizar os afazeres do dia a dia.
O usuário cadastra tarefas com título, descrição e prazo, separa as tarefas em categorias, como "Faculdade" ou "Casa",
marca o que já foi concluído e pode editar ou excluir qualquer registro.
Isso cobre as quatro operações do CRUD: criar, ler, atualizar e excluir, aplicadas a duas entidades, que são a tarefa e a categoria.

Sobre as tecnologias: usei Python como linguagem.
Para a parte web usei o Flask, que é um framework do Python. Ele recebe os pedidos que o navegador faz,
executa a função correspondente e devolve a página para o usuário.
Para o banco de dados usei o SQLite, que é um banco de dados relacional completo, mas embutido na própria aplicação,
então eu não preciso instalar um servidor de banco de dados separado.
A interface foi feita com HTML e CSS.
Escolhi essas tecnologias pela simplicidade, já que o foco do trabalho é a documentação e o CRUD.

### 2. Visão geral (≈ 1:50)

**[TELA: seção 2 - Visão Geral, quadro das telas]**

Na visão geral eu apresento as quatro telas do sistema: a lista de tarefas, a tela de nova tarefa, a de editar tarefa e a de categorias.
A arquitetura tem três camadas: o navegador, que mostra as telas; a aplicação Flask, que contém as rotas e as regras;
e o banco SQLite, que guarda os dados.
Eu não incluí login de usuário, porque o foco do trabalho é o CRUD e a modelagem.

### 3. Requisitos (≈ 2:15)

**[TELA: seção 3 - quadros de requisitos funcionais e não funcionais]**

Agora os requisitos. Os requisitos funcionais descrevem o que o sistema faz.
Por exemplo: o RF01 é cadastrar uma tarefa, com o título obrigatório; o RF03 é filtrar a lista por categoria e por situação;
e o RF10 é excluir uma categoria sem apagar as tarefas dela. Ao todo, são onze requisitos funcionais.

Já os requisitos não funcionais não são novas funcionalidades: eles descrevem como o sistema deve ser, ou seja, as qualidades e as restrições.
Por exemplo: o RNF05, de desempenho, diz que a listagem de tarefas deve responder em menos de um segundo com até cinco mil tarefas;
o RNF01, de usabilidade, diz que cadastrar uma tarefa deve exigir no máximo três cliques a partir da tela inicial;
e o RNF08, de segurança, diz que o sistema deve ser protegido contra injeção de SQL, com consultas parametrizadas.
Dois deles, o RNF02 e o RNF03, são restrições de implementação: eles fixam o uso de Python com Flask e do banco SQLite.
São oito requisitos não funcionais.

### 4.1 Casos de uso (≈ 3:10)

**[TELA: seção 4.1 - Figura 1, diagrama de casos de uso]**

Este é o diagrama de casos de uso. Ele mostra o que o usuário consegue fazer no sistema.
Existe um único ator, o Usuário, e cinco casos de uso: cadastrar tarefa, consultar tarefas, editar tarefa,
excluir tarefa e gerenciar categorias.
Marcar uma tarefa como concluída faz parte da edição.

**[TELA: Quadro 4 - descrição dos casos de uso]**

Neste quadro, cada caso de uso tem uma descrição e a indicação dos requisitos que ele atende.

### 4.2 DER (≈ 3:45)

**[TELA: seção 4.2 - Figura 2, DER]**

O DER, que é o diagrama entidade-relacionamento, representa o banco de dados.
Eu tenho duas tabelas. A tabela categoria tem o identificador e o nome, que é único.
A tabela tarefa tem o identificador, o título, a descrição, o prazo, um campo que indica se está concluída
e o identificador da categoria.

A relação é de um para muitos: uma categoria pode ter várias tarefas, e cada tarefa pertence a no máximo uma categoria,
porque essa chave estrangeira é opcional.
Quando uma categoria é excluída, as tarefas dela não são apagadas: o campo de categoria apenas fica vazio.
Essa regra se chama ON DELETE SET NULL.

### 4.3 Diagrama de classes (≈ 4:25)

**[TELA: seção 4.3 - Figura 3, diagrama de classes]**

O diagrama de classes mostra essas mesmas duas entidades do ponto de vista de objetos.
Temos a classe Categoria e a classe Tarefa, com seus atributos e suas operações,
e a ligação entre elas: uma categoria tem zero ou mais tarefas, e uma tarefa tem zero ou uma categoria.

### 4.4 Diagrama de atividade (≈ 4:50)

**[TELA: seção 4.4 - Figura 4, diagrama de atividade]**

O diagrama de atividade mostra o fluxo de cadastrar uma tarefa. Ele está dividido em duas raias: a do usuário e a do sistema.
O usuário clica em "Nova tarefa", preenche os dados e clica em "Salvar".
O sistema, então, verifica se o título foi preenchido.
Se não foi, mostra uma mensagem de erro e o usuário corrige o título.
Se foi, o sistema grava no banco, mostra uma mensagem de sucesso e volta para a lista, onde o usuário vê a tarefa cadastrada.

### 4.5 Diagramas de sequência (≈ 5:35)

**[TELA: seção 4.5.1 - Figura 5, sequência do UC01]**

Para cada caso de uso eu fiz um diagrama de sequência, que mostra a ordem das mensagens entre
o usuário, o navegador, a aplicação Flask e o banco SQLite.
Vou explicar o primeiro, o de cadastrar tarefa.
O usuário clica em "Nova tarefa". O navegador pede a página ao Flask, o Flask consulta as categorias no banco para montar o formulário
e devolve a página.
O usuário preenche e clica em "Salvar", e o navegador envia os dados por POST.
Aqui existe uma decisão: se o título estiver vazio, o Flask devolve o formulário com uma mensagem de erro.
Se estiver válido, o Flask executa um INSERT no banco, recebe a confirmação e redireciona o usuário para a lista de tarefas.

**[TELA: role rapidamente pelas figuras 6, 7, 8 e 9]**

Os outros quatro diagramas seguem a mesma lógica.
O de consultar tarefas tem apenas leituras no banco, com SELECT, e aceita filtros.
O de editar tem um UPDATE, e também mostra a opção de concluir ou reabrir a tarefa.
O de excluir tem uma confirmação do usuário antes do DELETE.
E o de gerenciar categorias tem três caminhos: cadastrar, renomear e excluir, incluindo o tratamento de nome repetido.

### 5. Implementação (≈ 6:35)

**[TELA: seção 5 - quadros de arquivos e de CRUD]**

Na parte de implementação, o documento lista os arquivos do projeto e mostra qual rota corresponde a cada operação do CRUD,
tanto para tarefas quanto para categorias, e explica como executar o sistema.
O sistema funcionando eu mostro no segundo vídeo.

### 6. Conclusão e encerramento (≈ 6:55)

**[TELA: seção 6 - Conclusão]**

Como conclusão, o que eu mais aprendi foi que a modelagem ajuda a decidir a implementação.
O DER virou diretamente as tabelas e a chave estrangeira, e os diagramas de sequência mostraram quais rotas e consultas SQL eu precisava criar.
Também aprendi a pensar nos casos de erro, como o título vazio e o nome de categoria repetido,
e a decidir o que acontece com as tarefas quando uma categoria é excluída.
Por fim, percebi que testes automatizados ajudam a conferir o CRUD de forma rápida e repetível.
Como melhorias futuras, o sistema poderia ganhar login de usuários, prioridade nas tarefas e lembretes de prazo.

**[TELA: seção de referências]**

As referências incluem livros de engenharia de software, de UML e de banco de dados,
além da documentação oficial do Flask e do SQLite.
Obrigado por assistir!

---
---

# VÍDEO 2 - Defesa da implementação (Parte II)

**Resumo dos comandos do vídeo, na ordem** (cada um é digitado no momento indicado no roteiro):

```bash
cd ~/GerenciadorTarefas
rm -f tarefas.db
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Logo depois de iniciar o servidor, em uma **nova aba** do terminal (`Cmd + T`), ainda na parte do banco de dados:

```bash
cd ~/GerenciadorTarefas
sqlite3 tarefas.db ".tables"
sqlite3 tarefas.db ".schema"
sqlite3 -header -column tarefas.db "SELECT * FROM tarefa;"
sqlite3 -header -column tarefas.db "SELECT * FROM categoria;"
```

Depois, volte ao navegador para a demonstração. No final, volte para a aba do servidor, dê `Ctrl + C` para pará-lo e então:

```bash
python -m unittest discover tests
```

### Abertura (0:00)

**[TELA: página do repositório no GitHub]**

Olá! Eu sou o Antonio Pignataro, RA 253466044, do curso de Engenharia de Software da UniFil.
Este é o segundo vídeo, com a defesa da implementação do Gerenciador de Tarefas, que segue a documentação apresentada no primeiro vídeo.

Aqui está o repositório no GitHub. Ele é público, então o tutor e o usuário fernandonakagawa-unifil têm acesso.
No repositório estão o código da aplicação, o README com as instruções, a documentação em PDF dentro da pasta docs e a pasta de testes.
O último commit é o que estou entregando.

### Executando o sistema (≈ 0:40)

**[TELA: terminal novo, aberto e vazio]**

Vou executar o sistema, a partir do terminal. Primeiro entro na pasta do projeto.

**[TELA: digite e dê Enter]**

```bash
cd ~/GerenciadorTarefas
```

Para começar do zero, apago o banco de dados de testes anterior, se existir. Ele será criado de novo automaticamente.

**[TELA: digite e dê Enter. Não aparece mensagem nenhuma, é normal]**

```bash
rm -f tarefas.db
```

Agora ativo o ambiente virtual, que é um ambiente isolado do Python onde ficam as bibliotecas do projeto.

**[TELA: digite este comando e dê Enter. A linha do terminal passa a começar com `(.venv)`]**

```bash
source .venv/bin/activate
```

Agora instalo as dependências do projeto, que é só o Flask.

**[TELA: digite e dê Enter]**

```bash
pip install -r requirements.txt
```

E agora executo o sistema.

**[TELA: digite e dê Enter. Aparece "Running on http://127.0.0.1:5001". Deixe esse terminal aberto]**

```bash
python app.py
```

O banco de dados, que é o arquivo `tarefas.db`, é criado automaticamente na primeira execução,
a partir do arquivo `schema.sql`. O sistema agora está no ar, no endereço 127.0.0.1, porta 5001.

### O banco de dados (≈ 1:10)

**[TELA: editor, arquivo schema.sql]**

Antes de usar, mostro o esquema do banco. Este é o `schema.sql`.
Temos a tabela categoria, com um id e um nome único e obrigatório.
E a tabela tarefa, com id, título obrigatório, descrição, prazo, um campo concluída, que vale zero ou um,
e o categoria_id, que é a chave estrangeira apontando para a categoria, com ON DELETE SET NULL.
Isso é exatamente o DER que apresentei na documentação.

**[TELA: terminal; abra uma NOVA aba com `Cmd + T`. O servidor continua rodando na aba anterior. Digite e dê Enter]**

```bash
cd ~/GerenciadorTarefas
```

Além do arquivo, posso conferir o banco de verdade pelo terminal. O banco é o arquivo `tarefas.db`, que foi criado agora há pouco,
quando o sistema iniciou. Primeiro, listo as tabelas que existem nele.

**[TELA: digite e dê Enter. Aparecem as tabelas `categoria` e `tarefa`]**

```bash
sqlite3 tarefas.db ".tables"
```

Estão aqui as duas tabelas do DER: categoria e tarefa.
Agora peço o schema, que é a estrutura do banco.

**[TELA: digite e dê Enter. Aparecem os dois `CREATE TABLE`, com a chave estrangeira e o `ON DELETE SET NULL`]**

```bash
sqlite3 tarefas.db ".schema"
```

Aqui aparecem os comandos que criaram as tabelas, os mesmos do arquivo schema.sql, incluindo a chave estrangeira com ON DELETE SET NULL.
A tabela sqlite_sequence é uma tabela interna que o próprio SQLite cria por causa do AUTOINCREMENT.

Agora vou consultar os dados de cada tabela.

**[TELA: digite e dê Enter. Não aparece nada, porque o banco ainda está vazio]**

```bash
sqlite3 -header -column tarefas.db "SELECT * FROM tarefa;"
```

**[TELA: digite e dê Enter. Também não aparece nada]**

```bash
sqlite3 -header -column tarefas.db "SELECT * FROM categoria;"
```

Não aparece nada, porque o banco acabou de ser criado e ainda está vazio. Agora vou usar o sistema para cadastrar os dados.

### Demonstração: categorias (≈ 2:40)

**[TELA: navegador em http://127.0.0.1:5001 ; clique em "Categorias"]**

Agora vou usar o sistema. Começo pelas categorias.

**[TELA: digite `Faculdade` no campo e clique em "Adicionar"; depois `Casa` e "Adicionar"]**

Vou cadastrar a categoria "Faculdade" e depois a categoria "Casa". Isso é o Create do CRUD.
A lista mostra o nome de cada categoria e quantas tarefas ela tem. Por enquanto, zero. Isso é o Read.

**[TELA: na linha "Casa", troque o nome para `Pessoal` e clique em "Renomear"]**

Vou renomear "Casa" para "Pessoal". Esse é o Update.

**[TELA: digite `Faculdade` de novo e clique em "Adicionar"]**

Agora vou tentar cadastrar "Faculdade" outra vez. O sistema avisa que já existe uma categoria com esse nome,
porque o nome é único no banco.

### Demonstração: tarefas (≈ 3:40)

**[TELA: clique em "Tarefas" e depois em "+ Nova tarefa"]**

Vamos às tarefas. Clico em "Nova tarefa".

**[TELA: Título `Entregar projeto de software`; Descrição `Enviar PDF e vídeo na plataforma`; Prazo 21/11/2026; Categoria `Faculdade`; clique em "Salvar"]**

Preencho o título, a descrição, o prazo e escolho a categoria "Faculdade". Clico em "Salvar".
O sistema mostra a mensagem de sucesso, e a tarefa aparece na lista.

**[TELA: "+ Nova tarefa" > Título `Lavar o carro`; Categoria `Pessoal`; sem prazo; "Salvar"]**

Cadastro mais uma: "Lavar o carro", na categoria "Pessoal", sem prazo.

**[TELA: "+ Nova tarefa" > no título digite apenas três espaços; clique em "Salvar"]**

Agora a validação. Se eu tentar salvar sem título, o próprio navegador já avisa.
Mas o servidor também valida: se eu digitar só espaços, o sistema recusa e mostra a mensagem "O título é obrigatório".

**[TELA: clique em "Cancelar"; na tarefa do carro, clique em "Editar"]**

Vou editar a tarefa do carro.

**[TELA: mude o título para `Lavar o carro e aspirar`; clique em "Salvar"]**

Mudo o título para "Lavar o carro e aspirar" e salvo. Esse é o Update das tarefas.

**[TELA: clique na caixa de seleção (☐) dessa tarefa]**

Agora clico na caixa de seleção para marcar a tarefa como concluída.
Ela fica riscada e vai para o final da lista.

**[TELA: use os filtros: categoria `Faculdade` > "Filtrar"; depois "Todas as categorias" + situação `Concluídas` > "Filtrar"; depois `Pendentes` > "Filtrar"]**

Aqui estão os filtros. Posso filtrar por categoria, por exemplo só "Faculdade",
e por situação: só as concluídas, ou só as pendentes.

**[TELA: vá em "Categorias", clique em "Excluir" na categoria "Pessoal" e confirme; depois volte em "Tarefas"]**

Agora vou excluir a categoria "Pessoal". O navegador pede confirmação, e eu confirmo.
Voltando às tarefas, a tarefa do carro continua lá, só que sem categoria, aparecendo com um traço.
Isso acontece por causa do ON DELETE SET NULL que vimos no esquema.

**[TELA: na tarefa do carro, clique em "Excluir" e confirme]**

Por fim, vou excluir essa tarefa. Mais uma vez o navegador pede confirmação, e eu confirmo.
Esse é o Delete. Com isso, mostrei as quatro operações do CRUD.

### O código (≈ 5:45)

**[TELA: editor, arquivo app.py, no início]**

Vamos ver o código. Este é o `app.py`. Ele começa criando a aplicação Flask.
A função `get_db` abre a conexão com o SQLite e liga o controle de chaves estrangeiras.

**[TELA: rola até a função criar_tarefa]**

Aqui está a rota de cadastrar tarefa. Se a requisição for um GET, ela mostra o formulário.
Se for um POST, ela lê os campos, verifica se o título foi preenchido
e executa um INSERT INTO tarefa. Repare que os valores entram por pontos de interrogação.
São parâmetros, e isso evita injeção de SQL. Depois ela salva com commit e redireciona para a lista.

**[TELA: rola até listar_tarefas]**

Esta é a rota que lista as tarefas. Ela monta um SELECT com LEFT JOIN na tabela categoria,
para trazer o nome da categoria junto, e acrescenta os filtros de categoria e de situação
conforme os parâmetros da URL. As pendentes aparecem primeiro, ordenadas por prazo.

**[TELA: rola até excluir_categoria]**

E esta é a rota de excluir categoria, que executa um DELETE.
Como o banco tem ON DELETE SET NULL, as tarefas dessa categoria continuam existindo, apenas sem categoria.
As rotas de editar e de concluir usam UPDATE. Cada uma dessas rotas corresponde a um dos diagramas de sequência da documentação.

### Testes (≈ 6:20)

**[TELA: volte para a aba do terminal onde o servidor está rodando; pare-o com `Ctrl + C`; depois digite este comando e dê Enter]**

```bash
python -m unittest discover tests
```

Para terminar, os testes automatizados. Eu paro o servidor com Ctrl + C e executo o comando `python -m unittest discover tests`.
São quatro testes, e todos passaram. Eles verificam o CRUD de categorias, o CRUD de tarefas com filtro e conclusão,
a obrigatoriedade do título e que excluir uma categoria não apaga as tarefas.
Eles usam um banco de dados temporário, então não mexem nos dados reais.

### Encerramento (≈ 6:50)

**[TELA: repositório no GitHub ou terminal]**

Resumindo: o sistema tem CRUD completo de tarefas e categorias, usa um banco de dados relacional SQLite
e está de acordo com a documentação que apresentei no primeiro vídeo.
Com este projeto eu aprendi como a modelagem se transforma em código, e a importância de validar dados e de testar.
Como melhoria futura, eu adicionaria login de usuários. Obrigado por assistir!

---

## Checklist final

- [ ] O vídeo abre e **tem som** (assista ao começo e ao fim).
- [ ] Cada vídeo tem **menos de 10 minutos**.
- [ ] Se o arquivo for grande, suba no YouTube como **Não listado** e envie o link.
- [ ] A voz é a sua, sem voz sintética nem leitor de texto.
