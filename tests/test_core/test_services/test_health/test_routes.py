from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "app_name" in response.json()
    assert "version" in response.json()
    assert "mode" in response.json()
    assert "debug" in response.json()
