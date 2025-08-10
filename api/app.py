from __future__ import annotations

import os
from typing import List

import joblib
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel


class Features(BaseModel):
    features: List[float]


app = FastAPI()


def load_model():
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    try:
        client = mlflow.tracking.MlflowClient(tracking_uri)
        latest = client.get_latest_versions("model", stages=["Production"])
        if latest:
            return mlflow.pyfunc.load_model(latest[0].source)
    except Exception:
        pass
    path = os.environ.get("MODEL_PATH", "data/model.pkl")
    if os.path.exists(path):
        return joblib.load(path)

    class Dummy:
        def predict(self, X):
            return [0.0 for _ in X]

    return Dummy()


model = load_model()


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict")
def predict(data: Features) -> dict[str, float | None]:
    pred = model.predict([data.features])[0]
    try:
        pred = float(pred)
    except Exception:
        pred = None
    return {"prediction": pred}
