"""Testes unitarios: nao precisam de banco nem da aplicacao no ar."""

import os

# backend/auth.py importa backend/database.py, que le estas variaveis no import.
# setdefault nao sobrescreve as variaveis reais (.env ou CI).
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "teste")
os.environ.setdefault("POSTGRES_USER", "teste")
os.environ.setdefault("POSTGRES_PASSWORD", "teste")
os.environ.setdefault("SECRET_KEY", "x" * 32)

import pytest  # noqa: E402
from pydantic import ValidationError  # noqa: E402

from backend.auth import UsuarioCadastro  # noqa: E402
from backend.produtos import ProdutoCadastro  # noqa: E402
from backend.security import gerar_hash_senha, verificar_senha  # noqa: E402


def _usuario(**mudancas):
    dados = {"nome": "Ana", "email": "ana@email.com", "senha": "Senha1234"}
    dados.update(mudancas)
    return UsuarioCadastro(**dados)


def test_hash_nao_guarda_senha_em_texto_puro():
    senha = "Senha1234"
    senha_hash = gerar_hash_senha(senha)

    assert senha_hash != senha
    assert senha not in senha_hash
    assert verificar_senha(senha, senha_hash) is True
    assert verificar_senha("SenhaErrada1", senha_hash) is False


def test_senha_acima_de_72_bytes_gera_erro():
    with pytest.raises(ValueError):
        gerar_hash_senha("A" * 73)


@pytest.mark.parametrize(
    "senha",
    [
        "Ab1",           # curta
        "senha1234",     # sem maiuscula
        "SENHA1234",     # sem minuscula
        "SenhaSemNum",   # sem numero
    ],
)
def test_senha_fraca_e_recusada(senha):
    with pytest.raises(ValidationError):
        _usuario(senha=senha)


def test_senha_forte_e_aceita():
    assert _usuario(senha="Senha1234").senha == "Senha1234"


def test_email_e_normalizado_para_minusculas():
    assert _usuario(email="  Ana@Email.com ").email == "ana@email.com"


def test_produto_recusa_preco_ou_quantidade_negativos():
    with pytest.raises(ValidationError):
        ProdutoCadastro(nome="Caneta", preco="-0.01", quantidade=1)

    with pytest.raises(ValidationError):
        ProdutoCadastro(nome="Caneta", preco="2.50", quantidade=-1)

    # Sem quantidade, vale 0
    produto = ProdutoCadastro(nome="Caneta", preco="2.50")
    assert produto.quantidade == 0