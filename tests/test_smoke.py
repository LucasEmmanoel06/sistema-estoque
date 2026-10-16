# [FASE 2] TAREFA - testes de fumaca (aplicacao ja no ar)
# Area sugerida: QA/Testes | Dificuldade: media | Branch: test/smoke
# Commit: test: adiciona testes de fumaca contra a aplicacao no ar
# Apague este bloco quando terminar.
#
# Diferenca para os testes que ja existem: aqui NAO se importa o backend.
# Fala-se com a aplicacao por HTTP (httpx), como um usuario faria, usando
# BASE_URL (padrao http://localhost:8000). Rodar com a app no ar
# (docker compose up). Tirar o @pytest.mark.skip e escrever o corpo.

import os

import pytest

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@pytest.mark.skip(reason="TODO fase 2")
def test_health_responde_ok():
    """GET /api/health -> 200 e {"status": "ok"}."""


@pytest.mark.skip(reason="TODO fase 2")
def test_pagina_de_login_e_servida():
    """GET / -> 200 com HTML."""


@pytest.mark.skip(reason="TODO fase 2")
def test_fluxo_cadastro_login_produto():
    """Cadastra usuario (e-mail unico), faz login, cria um produto e o encontra
    na listagem. Usar httpx.Client(base_url=BASE_URL) para manter o cookie."""
