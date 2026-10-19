# Fase 2: tarefas, bugs e evidências

> **Tech Leader:** definiu o contrato e revisa os PRs · **Scrum Master:** distribui e acompanha os cards
> Prazo da Parte 2: **19/10/2026**

Cada arquivo marcado com `[FASE 2] TAREFA` tem no topo o que fazer e o critério "pronto quando". Quem implementar **apaga o bloco** e abre o PR.

## Como usar (Scrum Master)

1. Um card no Trello por linha da tabela de tarefas.
2. A coluna "Área" é só uma sugestão. Quem tem menos experiência pega tarefa de dificuldade baixa e faz par com quem tem mais.
3. Todas as tarefas podem **começar ao mesmo tempo**, porque o contrato abaixo já está fechado. Não é cascata.
4. Branch por card, commits no Conventional Commits em português, PR revisado antes do merge.

## Contrato (todos os arquivos assumem isto)

| Item | Valor |
| --- | --- |
| Serviços do Compose | `db` (postgres:16) e `app` (FastAPI) |
| Porta da aplicação | 8000 |
| Volume do banco | `estoque_pgdata` |
| Imagem | `sistema-estoque` |
| Python | 3.12 |
| Variáveis | `POSTGRES_HOST` (no Compose vale `db`), `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `SECRET_KEY` |
| GitHub Secrets | `POSTGRES_PASSWORD`, `SECRET_KEY` |

## Tarefas

| Arquivo | Área sugerida | Dif. | Branch |
| --- | --- | --- | --- |
| `Dockerfile` | Backend | média | `feat/dockerfile` |
| `docker-compose.yml` + `.env.example` | Dados/BD | média-alta | `feat/docker-compose` |
| `.github/workflows/pipeline.yml`, job `testes` | QA/Testes | média | `feat/pipeline-testes` |
| `.github/workflows/pipeline.yml`, job `build` | Backend | baixa-média | `feat/pipeline-build` |
| `.github/workflows/pipeline.yml`, job `sast` | Frontend | média | `feat/pipeline-sast` |
| `.github/workflows/pipeline.yml`, job `dast` | QA/Testes | alta | `feat/pipeline-dast` |
| `tests/test_unitarios.py` | QA/Testes | baixa | `test/unitarios` |
| `tests/test_smoke.py` | QA/Testes | média | `test/smoke` |
| `README.md` (seções de Docker e pipeline, testadas do zero) | Frontend | média | `docs/readme-fase2` |
| Esta página (bugs, alertas e prints) | Scrum Master | baixa | `docs/fase2` |
| Revisão dos PRs, Secrets e proteção da `main` | Tech Leader | média | n/a |

Ordem sugerida: Dockerfile, compose e job `testes` primeiro, porque destravam o teste de ponta a ponta (`dast` e smoke).

## Pistas de bugs e melhorias auditadas

As pistas abaixo foram confirmadas e as correções estão registradas na tabela de evidências.

| Pista | Onde |
| --- | --- |
| A chave do `.env.example` podia ser usada sem substituição. | `.env.example`, `backend/main.py` |
| `https_only=False` era fixo no cookie de sessão. | `backend/main.py` |
| `/api/health` não testava o banco. | `backend/main.py` |
| Faltavam cabeçalhos de segurança HTTP. | `backend/main.py` |
| `requirements.txt` misturava dependências de produção e de teste. | `requirements.txt` |
| README e `docs/arquitetura.md` divergiam do código. | `README.md`, `docs/` |

## Registro de bugs, alertas e melhorias

Uma linha por item resolvido. É o que vai para o pitch.

| Tipo (bug / segurança / melhoria) | O que foi feito | PR |
| --- | --- | --- |
| melhoria | Docker Compose aguarda o banco e a aplicação possui healthcheck; a persistência usa o volume `estoque_pgdata`. | implementado |
| segurança | O cookie de sessão respeita `SESSION_HTTPS_ONLY` e a API envia cabeçalhos HTTP de segurança. | implementado |
| melhoria | `/api/health` verifica também a conexão com o PostgreSQL e responde `503` quando o banco está indisponível. | implementado |
| melhoria | Dependências de produção e de teste foram separadas em `requirements.txt` e `requirements-dev.txt`. | implementado |
| bug | Corrigida a exibição de estoque vazio e a duplicação de listeners de busca após recarregar a tabela. | implementado |
| melhoria | README, arquitetura e pipeline foram alinhados ao repositório, aos endpoints e ao fluxo Docker Compose. | implementado |

## Prints para o pitch

Salvar em `docs/evidencias/` como `NN-descricao.png`. Conferir que não aparece senha nem `SECRET_KEY`.

- [ ] Trello com sprints e cards
- [ ] Branches e commits no padrão
- [ ] `pytest` passando
- [ ] Pipeline verde (testes, build, sast, dast) e relatório do ZAP
- [ ] `docker compose ps` com `db` e `app` rodando e o sistema aberto no navegador
- [ ] Persistência: criar produto, `docker compose down` (sem `-v`), `up` e o produto continua
- [ ] GitHub Secrets configurados (só os nomes)
- [ ] Um bug ou alerta de segurança: antes e depois
