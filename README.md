# Sistema de Estoque

Projeto "DevOps para projetos web" da turma Aponti FAP DevOps 5 (2026), Grupo 4.

Sistema web simples de estoque: o usuário se cadastra, faz login e, logado, cadastra, consulta, edita e exclui produtos.

## Sumário

1. [Visão geral](#visão-geral)
2. [Como rodar](#como-rodar)
3. [Como testar](#como-testar)
4. [Regras de negócio](#regras-de-negócio)
5. [Rotas da API](#rotas-da-api)
6. [Variáveis de ambiente](#variáveis-de-ambiente)
7. [Estrutura do projeto](#estrutura-do-projeto)
8. [Limitações conhecidas](#limitações-conhecidas)
9. [Para a parte 2 (DevOps)](#para-a-parte-2-devops)
10. [Como contribuir](#como-contribuir)
11. [Equipe](#equipe)

## Visão geral

O sistema tem 3 peças:

```
Navegador  ->  FastAPI (porta 8000)  ->  PostgreSQL (porta 5432)
               /api/...  API em JSON
               /         telas (HTML, CSS e JS)
```

| Peça | O que faz | Onde fica |
| --- | --- | --- |
| Banco | Guarda usuários e produtos | PostgreSQL |
| API | Regras de negócio: cadastro, login, produtos | `backend/` |
| Telas | Login, cadastro e painel de produtos, chamando a API | `frontend/` |

A própria API entrega as telas. Por isso front e API ficam na mesma origem e o login funciona com um cookie de sessão, sem configurar CORS.

| Camada | Tecnologia |
| --- | --- |
| Backend e API | Python 3.12+ com FastAPI (validado no 3.14) |
| Banco de dados | PostgreSQL 16 |
| Frontend | HTML, CSS e JavaScript puro, com Bootstrap via CDN |
| Testes | pytest |

## Como rodar

Você precisa de: **Git**, **Python 3.12+** e **Docker** (só para subir o banco). Os comandos abaixo são para Linux e macOS. No Windows, veja as diferenças no fim desta seção.

### 1. Baixar o projeto

```bash
git clone https://github.com/Fililpe/Projeto-DevOps-para-projetos-web.git
cd Projeto-DevOps-para-projetos-web
```

### 2. Instalar as dependências

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

O `.venv` é um ambiente isolado só deste projeto. Sempre que abrir um terminal novo, ative de novo com `source .venv/bin/activate`. O terminal mostra `(.venv)` no começo da linha quando está ativo.

### 3. Subir o banco

```bash
docker run -d --name estoque-db \
  -e POSTGRES_USER=estoque_app \
  -e POSTGRES_PASSWORD=estoque123 \
  -e POSTGRES_DB=sistema_estoque \
  -p 5432:5432 postgres:16
```

Isso cria um container com o PostgreSQL, já com o usuário, a senha e o banco `sistema_estoque`. Se você já tem um PostgreSQL instalado, pode usar ele: crie o banco e o usuário e ajuste o `.env` do próximo passo.

Para ligar o banco de novo depois de reiniciar o PC: `docker start estoque-db`.

### 4. Configurar o `.env`

```bash
cp .env.example .env
```

Abra o `.env` e preencha. Para o banco do passo 3, fica assim:

```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=sistema_estoque
POSTGRES_USER=estoque_app
POSTGRES_PASSWORD=estoque123
SECRET_KEY=cole_aqui_a_chave_gerada
```

Para gerar a `SECRET_KEY` (precisa ter pelo menos 32 caracteres, senão a API não sobe):

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

O `.env` nunca vai para o Git (está no `.gitignore`).

### 5. Criar as tabelas e os produtos de exemplo

```bash
docker exec -i estoque-db psql -U estoque_app -d sistema_estoque < backend/db.sql
docker exec -i estoque-db psql -U estoque_app -d sistema_estoque < backend/seed.sql
```

O `db.sql` cria as tabelas `usuarios` e `produtos`. O `seed.sql` cadastra 5 produtos de exemplo. Rode cada um só uma vez: rodar de novo dá erro de tabela já existente e duplica os produtos.

### 6. Subir a aplicação

```bash
python -m uvicorn backend.main:app --reload
```

| Endereço | O que abre |
| --- | --- |
| http://localhost:8000 | Sistema (tela de login) |
| http://localhost:8000/docs | Documentação interativa da API |
| http://localhost:8000/api/health | Teste rápido, responde `{"status":"ok"}` |

Não existe usuário pronto: crie um pela tela de cadastro.

### Diferenças no Windows (PowerShell)

| Passo | Comando no Windows |
| --- | --- |
| Criar o venv | `python -m venv .venv` |
| Ativar o venv | `.\.venv\Scripts\Activate.ps1` |
| Copiar o `.env` | `copy .env.example .env` |
| Rodar o `db.sql` | `Get-Content backend/db.sql \| docker exec -i estoque-db psql -U estoque_app -d sistema_estoque` |

No comando do `docker run`, troque as `\` do fim das linhas por `` ` `` (crase), ou escreva tudo numa linha só.

### Problemas comuns

| Erro | Causa e solução |
| --- | --- |
| `ModuleNotFoundError: No module named 'fastapi'` | O venv não está ativo. Rode `source .venv/bin/activate`. |
| `KeyError: 'POSTGRES_USER'` | Falta o `.env` ou ele está vazio. Volte ao passo 4. |
| `SECRET_KEY deve ter pelo menos 32 caracteres` | Gere uma chave nova como no passo 4. |
| `connection refused` na porta 5432 | O banco está desligado. Rode `docker start estoque-db`. |
| `relation "usuarios" does not exist` | As tabelas não foram criadas. Volte ao passo 5. |
| Porta 5432 já em uso no `docker run` | Já existe um PostgreSQL na máquina. Use `-p 5433:5432` e `POSTGRES_PORT=5433`. |

## Como testar

Com o banco ligado, o `.env` preenchido e o venv ativo:

```bash
python -m pytest -v
```

O resultado esperado é `9 passed`.

| Arquivo | O que testa |
| --- | --- |
| `tests/test_health.py` | A API está no ar |
| `tests/test_database.py` | A API consegue falar com o PostgreSQL |
| `tests/test_auth.py` | Cadastro, e-mail repetido, senha errada, login e logout |
| `tests/test_produtos.py` | Bloqueio sem login, cadastrar, listar, paginação, editar, excluir, preço e quantidade negativos |

Atenção: são testes de integração. Eles usam o banco de verdade do `.env` e deixam usuários e produtos de teste gravados nele.

## Regras de negócio

As regras com mais detalhe estão em [docs/database_documentation.md](docs/database_documentation.md).

### Usuários

- **Nome:** obrigatório, até 100 caracteres.
- **E-mail:** precisa ser válido e é único no sistema. É salvo em minúsculas, então `Ana@Email.com` e `ana@email.com` são o mesmo e-mail. Repetido responde **409**.
- **Senha:** mínimo de 8 caracteres, com pelo menos uma letra maiúscula, uma minúscula e um número. Nunca é salva em texto puro, só o hash (bcrypt).
- **Login errado:** responde **401** com a mesma mensagem ("E-mail ou senha incorretos") se o e-mail não existe ou se a senha está errada. Assim ninguém descobre quais e-mails estão cadastrados.
- **Sessão:** depois do login, a API guarda um cookie assinado (`estoque_session`) que vale **1 hora**. O logout apaga a sessão.

### Produtos

- **Todas as rotas de produto exigem login.** Sem sessão, a API responde **401**.
- **O estoque é compartilhado:** todo usuário logado vê, cadastra, edita e exclui qualquer produto. Não existe dono do produto.
- **Nome:** obrigatório, até 150 caracteres.
- **Descrição:** opcional. Vazia vira "sem descrição".
- **Preço:** obrigatório, nunca negativo, com até 2 casas decimais.
- **Quantidade:** número inteiro, nunca negativo. Se não for informada, vale 0.
- **Valores negativos** são recusados pela API (**422**) e também pelo banco (`CHECK`).
- **Listagem:** paginada. Padrão de 20 itens por página, máximo de 100.
- **Editar ou excluir** um produto que não existe responde **404**.

## Rotas da API

A documentação interativa, com todos os campos e onde dá para testar cada rota, fica em http://localhost:8000/docs com a aplicação rodando.

| Método | Rota | Login? | O que faz | Respostas |
| --- | --- | --- | --- | --- |
| GET | `/api/health` | Não | Verifica se a API está no ar | 200 |
| POST | `/api/auth/register` | Não | Cadastra um usuário | 201, 409, 422 |
| POST | `/api/auth/login` | Não | Faz login e cria a sessão | 200, 401 |
| POST | `/api/auth/logout` | Não | Encerra a sessão | 200 |
| GET | `/api/produtos?page=1&limit=20` | Sim | Lista os produtos | 200, 401, 422 |
| POST | `/api/produtos` | Sim | Cadastra um produto | 201, 401, 422 |
| PUT | `/api/produtos/{id}` | Sim | Edita um produto | 200, 401, 404, 422 |
| DELETE | `/api/produtos/{id}` | Sim | Exclui um produto | 204, 401, 404 |

Exemplo de corpo para cadastrar ou editar um produto:

```json
{
  "nome": "Caneta Azul",
  "descricao": "Ponta fina",
  "preco": "2.50",
  "quantidade": 7
}
```

Exemplo de corpo para cadastro de usuário:

```json
{
  "nome": "Ana",
  "email": "ana@email.com",
  "senha": "Senha1234"
}
```

## Variáveis de ambiente

Todas ficam no `.env` (modelo em `.env.example`). Nenhum valor real vai para o repositório.

| Variável | Obrigatória | Exemplo | Para que serve |
| --- | --- | --- | --- |
| `POSTGRES_HOST` | Sim | `localhost` | Endereço do banco |
| `POSTGRES_PORT` | Sim | `5432` | Porta do banco |
| `POSTGRES_DB` | Sim | `sistema_estoque` | Nome do banco |
| `POSTGRES_USER` | Sim | `estoque_app` | Usuário do banco |
| `POSTGRES_PASSWORD` | Sim | (segredo) | Senha do banco |
| `SECRET_KEY` | Sim | (segredo, 32+ caracteres) | Assina o cookie de sessão |

## Estrutura do projeto

| Caminho | O que tem |
| --- | --- |
| `backend/main.py` | Ponto de entrada: cria a API, liga a sessão, registra as rotas e serve o front |
| `backend/auth.py` | Rotas de cadastro, login e logout |
| `backend/produtos.py` | Rotas de produtos |
| `backend/dependencies.py` | Verificação de login usada pelas rotas de produto |
| `backend/security.py` | Hash e verificação de senha |
| `backend/database.py` | Conexão com o PostgreSQL, lida do `.env` |
| `backend/db.sql` | Criação das tabelas |
| `backend/seed.sql` | Produtos de exemplo |
| `frontend/` | Telas: `index.html` (login), `cadastro.html`, `dashboard.html` |
| `tests/` | Testes automatizados |
| `docs/` | Arquitetura, modelo do banco (MER) e regras de negócio |

## Limitações conhecidas

| Limitação | Impacto |
| --- | --- |
| Não há perfis de usuário (admin, comum) | Qualquer usuário logado edita e exclui qualquer produto |
| O produto não guarda quem o cadastrou | Não dá para saber quem criou ou alterou um item |
| Não há edição nem exclusão de usuário | Só cadastro, login e logout |
| Os testes usam o banco real e não limpam os dados | Cada execução deixa usuários e produtos de teste no banco |
| Não há migrations | Qualquer mudança no banco é feita à mão no `db.sql` |
| O cookie de sessão não exige HTTPS (`https_only=False`) | Certo para rodar local. Em produção com HTTPS, mudar para `True` em `backend/main.py` |
| O front busca todos os produtos e filtra no navegador | Com muitos produtos, a tela fica lenta |
| O front depende do Bootstrap via CDN | Sem internet, as telas aparecem sem estilo |
| A doc de regras cita baixa de estoque e controle de concorrência (RN04 e RN07) | Ainda não implementado. Hoje a quantidade é só editada direto |
| Editar e excluir produto passaram do escopo mínimo (cadastrar e consultar) | Funcionam e têm teste, mas foram as últimas a entrar |

## Para a parte 2 (DevOps)

O que vocês vão precisar saber para containerizar e automatizar:

- **Como a aplicação inicia:** `python -m uvicorn backend.main:app`. Dentro de um container, use `--host 0.0.0.0` para aceitar conexões de fora.
- **Dependências:** todas em `requirements.txt`, com versão fixa.
- **Banco:** a API só lê as variáveis do `.env` (ou do ambiente). No Docker Compose, o `POSTGRES_HOST` passa a ser o nome do serviço do banco, não `localhost`.
- **Tabelas:** o `db.sql` e o `seed.sql` podem ser montados em `/docker-entrypoint-initdb.d/` na imagem oficial do PostgreSQL para rodar sozinhos na primeira subida.
- **Testes:** precisam de um PostgreSQL rodando com as tabelas criadas. No GitHub Actions, dá para usar um `service` de PostgreSQL.
- **Segredos:** a `SECRET_KEY` e a senha do banco devem ir para o GitHub Secrets, nunca para o código.

## Como contribuir

1. Ninguém faz push direto na `main`. Todo código entra por Pull Request.
2. Uma branch por card do Trello, saindo da `main` atualizada:

| Tipo | Exemplo de branch |
| --- | --- |
| Funcionalidade | `feat/login` |
| Correção | `fix/validacao-email` |
| Documentação | `docs/rotas-api` |
| Ajuste de estrutura | `chore/dependencias` |

3. Commits no padrão Conventional Commits, em português:

```
feat: adiciona rota de login
fix: corrige senha sem hash no cadastro
docs: documenta rotas de produtos
test: adiciona testes do cadastro
```

4. Antes de abrir o PR, rode `python -m pytest` e confira que passou.
5. O Tech Lead revisa e faz o merge.

## Documentação

- [Arquitetura e decisões](docs/arquitetura.md)
- [Modelo do banco e regras de negócio](docs/database_documentation.md)

## Equipe

| Papel | Pessoa |
| --- | --- |
| Tech Lead | Filipe |
| Scrum Master | Pedro |
| Backend | Vitor, Otávio |
| Dados | Felipe Gomes |
| Frontend | Nelson |

<!--
[FASE 2] TAREFA (Frontend): preencher as secoes abaixo DEPOIS que o compose e a
pipeline funcionarem, testando os passos do zero. Tambem: trocar a URL do
"git clone" pela do repositorio da equipe e atualizar a contagem de testes.
Apague este comentario ao terminar.
-->

## Execução com Docker Compose

Sobe o banco e a aplicação juntos, sem instalar Python nem criar as tabelas à mão. Você precisa só de **Git** e **Docker** (com o Docker Compose, que já vem no Docker Desktop e no pacote `docker-compose-plugin` do Linux).

### 1. Configurar o `.env`

```bash
cp .env.example .env
```

No Windows (PowerShell): `copy .env.example .env`.

Os valores do `.env.example` já funcionam para rodar local. Repare que `POSTGRES_HOST=db`: dentro do compose, o banco é encontrado pelo nome do serviço, não por `localhost`. A `SECRET_KEY` do exemplo é só para desenvolvimento. Para gerar uma sua:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Subir

```bash
docker compose up --build
```

| Serviço | O que faz |
| --- | --- |
| `db` | PostgreSQL 16. Na primeira subida, roda o `backend/db.sql` (tabelas) e o `backend/seed.sql` (5 produtos de exemplo) sozinho. Os dados ficam no volume `estoque_pgdata` |
| `app` | Monta a imagem do `Dockerfile` e sobe a API na porta 8000. Só inicia depois que o banco responde (healthcheck) |

O terminal fica preso mostrando os logs. Para subir em segundo plano, use `docker compose up --build -d` e veja os logs com `docker compose logs -f`.

### 3. Acessar

| Endereço | O que abre |
| --- | --- |
| http://localhost:8000 | Sistema (tela de login) |
| http://localhost:8000/docs | Documentação interativa da API |
| http://localhost:8000/api/health | Teste rápido, responde `{"status":"ok"}` |

O banco não fica exposto na máquina (o serviço `db` não tem `ports`), só a aplicação. Para abrir o `psql` dentro dele:

```bash
docker compose exec db psql -U estoque_app -d sistema_estoque
```

Com a aplicação no ar, os testes de fumaça conferem o fluxo completo pelo HTTP (precisa do venv da seção [Como rodar](#como-rodar)):

```bash
python -m pytest tests/test_smoke.py -v
```

### 4. Derrubar e apagar os dados

| Comando | O que faz |
| --- | --- |
| `docker compose stop` | Para os containers. Volta com `docker compose start` |
| `docker compose down` | Remove os containers e a rede. **Os dados continuam** no volume |
| `docker compose down -v` | Remove também o volume: **apaga todos os usuários e produtos** |

O `db.sql` e o `seed.sql` só rodam quando o volume está vazio. Mudou algum deles ou quer o banco zerado com os produtos de exemplo? Rode `docker compose down -v` e suba de novo.

| Erro | Causa e solução |
| --- | --- |
| Porta 8000 já em uso | Tem um `uvicorn` local ou outro container rodando. Pare ele ou troque para `"8080:8000"` no `docker-compose.yml` |
| `SECRET_KEY deve ter pelo menos 32 caracteres` nos logs do `app` | Falta o `.env` ou a chave está curta. Volte ao passo 1 |
| Mudou usuário ou senha do banco no `.env` e o `app` não conecta | O volume foi criado com os valores antigos. Rode `docker compose down -v` e suba de novo |

## Pipeline (CI/CD)

A pipeline fica em [`.github/workflows/pipeline.yml`](.github/workflows/pipeline.yml) e roda no GitHub Actions:

- a cada push na `main`;
- a cada Pull Request para a `main`;
- manualmente, pela aba **Actions** do GitHub (botão **Run workflow**).

Os 4 jobs rodam em paralelo, cada um numa máquina `ubuntu-latest` nova:

| Job | O que faz | Quebra a pipeline se... |
| --- | --- | --- |
| `build` | Monta a imagem Docker a partir do `Dockerfile` (`docker build`) | A imagem não monta |
| `testes` | Sobe um PostgreSQL 16 como `service`, instala o Python 3.12 e as dependências, cria as tabelas com o `db.sql` e roda o `pytest` (todos os testes, menos o `test_smoke.py`) | Algum teste falha |
| `sast` | Análise estática de segurança: o **Bandit** procura falhas no código de `backend/` e o **pip-audit** procura vulnerabilidades conhecidas nas versões do `requirements.txt`. Os relatórios em JSON ficam no artefato `sast-reports` | Nunca. Os achados são só relatados, para análise |
| `dast` | Cria o `.env` a partir dos secrets, sobe tudo com `docker compose up --build`, roda os testes de fumaça (`test_smoke.py`) contra a aplicação no ar e depois o **OWASP ZAP** (baseline), que testa a aplicação rodando como um atacante faria. O relatório fica no artefato `zap-report`. No fim, derruba tudo com `docker compose down -v` | A aplicação não sobe ou um teste de fumaça falha. Os achados do ZAP não quebram |

Se o `dast` falhar, o passo **Logs dos containers** mostra a saída do `docker compose logs`.

Os relatórios (`sast-reports` e `zap-report`) ficam para baixar na página da execução, em **Actions**, na parte de **Artifacts**.

### Secrets necessários

Configurados em **Settings > Secrets and variables > Actions** do repositório. Sem eles, os jobs `testes` e `dast` falham.

| Secret | Usado em | Para que serve |
| --- | --- | --- |
| `POSTGRES_PASSWORD` | `testes`, `dast` | Senha do banco criado na pipeline |
| `SECRET_KEY` | `testes`, `dast` | Assina o cookie de sessão (32+ caracteres) |

Plano de tarefas, bugs e evidências da Fase 2: [docs/fase2.md](docs/fase2.md)
