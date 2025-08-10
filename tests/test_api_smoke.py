from fastapi.testclient import TestClient

from api.app import app


def test_predict_smoke():
    client = TestClient(app)
    response = client.post("/predict", json={"features": [1, 2, 3]})
    assert response.status_code == 200
    assert "prediction" in response.json()


def test_predict_missing_features():
    client = TestClient(app)
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_wrong_type_features():
    client = TestClient(app)
    response = client.post("/predict", json={"features": "not_a_list"})
    assert response.status_code == 422


def test_predict_non_numeric_features():
    client = TestClient(app)
    response = client.post("/predict", json={"features": [1, "a", 3]})
    assert response.status_code == 422


def test_predict_empty_features():
    client = TestClient(app)
    response = client.post("/predict", json={"features": []})
    assert response.status_code == 422


def test_predict_non_numeric_output(monkeypatch):
    from api import app as api_app

    class BadModel:
        def predict(self, X):
            return ["not_a_number"]

    monkeypatch.setattr(api_app, "model", BadModel())
    client = TestClient(app)
    response = client.post("/predict", json={"features": [1, 2, 3]})
    assert response.status_code == 500
    assert response.json()["detail"] == "Prediction output is not numeric"


def test_predict_internal_error(monkeypatch):
    from api import app as api_app

    class ErrorModel:
        def predict(self, X):
            raise Exception("boom")

    monkeypatch.setattr(api_app, "model", ErrorModel())
    client = TestClient(app)
    response = client.post("/predict", json={"features": [1, 2, 3]})
    assert response.status_code == 500
    data = response.json()
    assert "boom" in data.get("detail", "")
