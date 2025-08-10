from __future__ import annotations

import logging
import os
from typing import List

import joblib
import mlflow
import mlflow.exceptions
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist


class Features(BaseModel):
    features: conlist(float, min_items=1)


app = FastAPI()
logger = logging.getLogger(__name__)


def load_model():
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    try:
        client = mlflow.tracking.MlflowClient(tracking_uri)
        latest = client.get_latest_versions("model", stages=["Production"])
        if latest:
            return mlflow.pyfunc.load_model(latest[0].source)
    except mlflow.exceptions.MlflowException as e:
        logger.exception(
            "MLflowException occurred while loading model from MLflow: %s", e
        )
    except FileNotFoundError as e:
        logger.exception("Model file not found: %s", e)
    except Exception as e:
        logger.exception("Unexpected exception occurred while loading model: %s", e)
    path = os.environ.get("MODEL_PATH", "data/model.pkl")
    if os.path.exists(path):
        try:
            return joblib.load(path)
        except Exception as e:
            logger.exception("Exception occurred while loading model from file: %s", e)

    class Dummy:
        def predict(self, X):
            return [0.0 for _ in X]

    return Dummy()


model = load_model()


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict")
def predict(data: Features) -> dict[str, float]:
    try:
        pred = model.predict([data.features])[0]
        pred = float(pred)
    except (ValueError, TypeError):
        raise HTTPException(status_code=500, detail="Prediction output is not numeric")
    except Exception as e:
        logger.exception("Prediction failed: %s", e)
        raise HTTPException(status_code=500, detail="Prediction failed")
    return {"prediction": pred}
