# [FASE 2] TAREFA - Dockerfile
# Area sugerida: Backend | Dificuldade: media | Branch: feat/dockerfile
# Commit: feat: adiciona Dockerfile da aplicacao
# Apague este bloco quando terminar.
#
# TODO:
#  1. Fixar a versao da imagem base (nada de "latest").
#  2. WORKDIR /app; copiar primeiro o requirements.txt e instalar
#     (pip install --no-cache-dir); depois copiar backend/ e frontend/
#     (o main.py procura ../frontend, entao manter /app/backend e /app/frontend).
#  3. NAO copiar o .env nem colocar senha/SECRET_KEY em ENV. As variaveis
#     chegam pelo docker compose.
#  4. Criar um usuario sem privilegios e usar USER (nao rodar como root).
#  5. EXPOSE 8000 e CMD uvicorn backend.main:app --host 0.0.0.0 --port 8000
#     (sem --reload).
#
# PRONTO QUANDO: docker build -t sistema-estoque . funciona e
# docker run --rm sistema-estoque whoami  nao responde "root".

FROM python:3.12-slim
