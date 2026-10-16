# [FASE 2] TAREFA - testes unitarios (nao precisam de banco)
# Area sugerida: QA/Testes | Dificuldade: baixa | Branch: test/unitarios
# Commit: test: adiciona testes unitarios de senha e validacoes
# Apague este bloco quando terminar.
#
# Como fazer: tirar o @pytest.mark.skip e escrever o corpo de cada teste.
#  - Senha: importar gerar_hash_senha e verificar_senha de backend.security.
#  - Validacoes: UsuarioCadastro (backend/auth.py) e ProdutoCadastro
#    (backend/produtos.py); casos invalidos com pytest.raises(ValidationError).
#
# ATENCAO: backend/auth.py importa backend/database.py, que le variaveis de
# ambiente no import (KeyError se faltar). Para o teste rodar sem .env, no
# topo deste arquivo, ANTES de importar backend, usar os.environ.setdefault
# para POSTGRES_HOST/PORT/DB/USER/PASSWORD (valores ficticios) e SECRET_KEY
# (32+ caracteres). O setdefault nao sobrescreve as variaveis reais do CI.

import pytest


@pytest.mark.skip(reason="TODO fase 2")
def test_hash_nao_guarda_senha_em_texto_puro():
    """O hash e diferente da senha; verificar_senha aceita a certa e recusa a errada."""


@pytest.mark.skip(reason="TODO fase 2")
def test_senha_acima_de_72_bytes_gera_erro():
    """gerar_hash_senha levanta ValueError."""


@pytest.mark.skip(reason="TODO fase 2")
def test_senha_fraca_e_recusada():
    """UsuarioCadastro: curta, sem maiuscula, sem minuscula ou sem numero."""


@pytest.mark.skip(reason="TODO fase 2")
def test_email_e_normalizado_para_minusculas():
    """'  Ana@Email.com ' vira 'ana@email.com'."""


@pytest.mark.skip(reason="TODO fase 2")
def test_produto_recusa_preco_ou_quantidade_negativos():
    """ProdutoCadastro: preco -0.01 e quantidade -1 falham; sem quantidade, vale 0."""
