# Arquitetura

Responsavel: Tech Lead (Filipe)

## Visao geral

Uma unica aplicacao FastAPI que entrega a API e tambem os arquivos do frontend.
O banco e PostgreSQL.

```
Navegador  ->  FastAPI (porta 8000)  ->  PostgreSQL (porta 5432)
               /api/...   API em JSON
               /          frontend (HTML, CSS, JS)
```

## Decisoes

| Decisao | Motivo |
| --- | --- |
| FastAPI serve o frontend | Mesma origem, sem CORS e com cookie de sessao simples |
| Login por sessao em cookie assinado | Mais simples que JWT para tres features |
| Senha sempre com hash (bcrypt) | Nunca salvar senha em texto puro |
| Configuracao por variavel de ambiente | Nada depende da maquina de um aluno |
| Tabelas criadas pelo `db.sql` | E o arquivo que a outra equipe vai usar nos containers |

## Escopo fechado

- Banco: 2 tabelas, `usuarios` e `produtos`.
- Features: cadastro, login e produtos (cadastrar, consultar, editar e excluir).
- Estoque compartilhado: todo usuario logado ve todos os produtos.

## Rotas combinadas

| Metodo | Rota | Dono |
| --- | --- | --- |
| GET | `/api/health` | Tech Lead (API e PostgreSQL) |
| POST | `/api/auth/register` | Backend |
| POST | `/api/auth/login` | Backend |
| POST | `/api/auth/logout` | Backend |
| GET | `/api/produtos` | Backend |
| POST | `/api/produtos` | Backend |
| PUT | `/api/produtos/{id}` | Backend |
| DELETE | `/api/produtos/{id}` | Backend |

## Estrutura de pastas

| Caminho | O que vai aqui | Dono |
| --- | --- | --- |
| `backend/` | API, conexao com o banco e regras | Backend |
| `frontend/` | HTML, CSS e JS | Frontend |
| `tests/` | Testes automatizados (pytest) | Quem escreve o codigo testa |
| `docs/` | Documentacao | Cada area documenta a sua parte |
| `db.sql` | Script de criacao das tabelas | Dados |

## Documentos que faltam

| Arquivo | Dono |
| --- | --- |
| `docs/api.md` (rotas com exemplos) | Backend |
| `docs/banco.md` (modelo do banco) | Dados |
| `docs/limitacoes.md` (limitacoes conhecidas) | Todos |
