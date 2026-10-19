from fastapi.testclient import TestClient

from backend.main import app


def test_api_no_ar():
    resposta = TestClient(app).get("/api/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok", "database": "ok"}
