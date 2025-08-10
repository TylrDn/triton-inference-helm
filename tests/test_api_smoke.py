from fastapi.testclient import TestClient

from api.app import app


def test_predict_smoke():
    client = TestClient(app)
    response = client.post("/predict", json={"features": [1, 2, 3]})
    assert response.status_code == 200
    assert "prediction" in response.json()
