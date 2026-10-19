"""Testes de fumaca: falam com a aplicacao no ar por HTTP, como um usuario.

Nao importam o backend. Rodar com a app no ar (docker compose up):
    python -m pytest tests/test_smoke.py -v
Outro endereco: defina BASE_URL (ex.: BASE_URL=http://localhost:8080).
"""

import os
import uuid

import httpx

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def test_health_responde_ok():
    resposta = httpx.get(f"{BASE_URL}/api/health", timeout=10)

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok", "database": "ok"}


def test_pagina_de_login_e_servida():
    resposta = httpx.get(f"{BASE_URL}/", timeout=10)

    assert resposta.status_code == 200
    assert "text/html" in resposta.headers["content-type"]
    assert "<html" in resposta.text.lower()


def test_fluxo_cadastro_login_produto():
    email = f"smoke-{uuid.uuid4().hex}@example.com"
    senha = "Smoke1234"
    nome_produto = f"Produto smoke {uuid.uuid4().hex[:8]}"

    # httpx.Client guarda o cookie de sessao entre as chamadas
    with httpx.Client(base_url=BASE_URL, timeout=10) as cliente:
        cadastro = cliente.post(
            "/api/auth/register",
            json={"nome": "Usuario Smoke", "email": email, "senha": senha},
        )
        assert cadastro.status_code == 201

        login = cliente.post(
            "/api/auth/login", json={"email": email, "senha": senha}
        )
        assert login.status_code == 200

        criado = cliente.post(
            "/api/produtos",
            json={
                "nome": nome_produto,
                "descricao": "Criado pelo teste de fumaca",
                "preco": "9.90",
                "quantidade": 3,
            },
        )
        assert criado.status_code == 201
        produto_id = criado.json()["id"]

        # A listagem e paginada (max. 100 por pagina) e o estoque e
        # compartilhado, entao percorre as paginas ate achar o produto.
        encontrado = False
        for pagina in range(1, 51):
            listagem = cliente.get(
                "/api/produtos", params={"page": pagina, "limit": 100}
            )
            assert listagem.status_code == 200

            itens = listagem.json()

            if any(item["id"] == produto_id for item in itens):
                encontrado = True
                break
            if len(itens) < 100:
                break

        assert encontrado, "produto criado nao apareceu na listagem"

        # Limpeza: remove o produto criado pelo teste
        cliente.delete(f"/api/produtos/{produto_id}")