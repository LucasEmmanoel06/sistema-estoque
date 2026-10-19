
"""Ponto de entrada da aplicacao FastAPI."""

import os
from collections.abc import Callable

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.sessions import SessionMiddleware

from backend.auth import router as auth_router
from backend.database import testar_conexao
from backend.produtos import router as produtos_router

from pathlib import Path
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

load_dotenv()

app = FastAPI(
    title="Sistema de Estoque",
    version="0.1.0"
)

secret_key = os.environ["SECRET_KEY"]
https_only = os.getenv("SESSION_HTTPS_ONLY", "false").strip().lower() == "true"

if len(secret_key) < 32:
    raise RuntimeError(
        "SECRET_KEY deve ter pelo menos 32 caracteres"
    )

if secret_key == "INSEGURA_apenas_dev_local_NAO_USE_EM_PRODUCAO":
    raise RuntimeError(
        "Troque a SECRET_KEY de exemplo antes de iniciar a aplicacao"
    )

# Configuracao das sessoes de autenticacao
app.add_middleware(
    SessionMiddleware,
    secret_key=secret_key,
    session_cookie="estoque_session",
    max_age=3600,
    same_site="lax",
    https_only=https_only
)

# Registra as rotas de autenticacao
app.include_router(auth_router)
app.include_router(produtos_router)


@app.middleware("http")
async def cabecalhos_de_seguranca(
    request: Request, call_next: Callable[[Request], Response]
) -> Response:
    resposta = await call_next(request)
    resposta.headers["X-Content-Type-Options"] = "nosniff"
    resposta.headers["X-Frame-Options"] = "DENY"
    resposta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resposta.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' https://cdn.jsdelivr.net; "
        "script-src 'self' https://cdn.jsdelivr.net; "
        "img-src 'self' data:; "
        "font-src 'self' https://cdn.jsdelivr.net"
    )
    resposta.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if https_only:
        resposta.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
    return resposta


@app.get("/api/health", tags=["infra"])
def health():
    """Verifica se a API e o banco de dados estao funcionando."""
    try:
        banco_disponivel = testar_conexao()
    except SQLAlchemyError:
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "database": "unavailable"},
        )

    if not banco_disponivel:
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "database": "unavailable"},
        )

    return {"status": "ok", "database": "ok"}

# Precisa ficar sempre no final do arquivo
app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)
