.PHONY: up-mlflow train-local argo-submit deploy-api perf-test lint clean

up-mlflow:
	docker-compose -f mlflow/docker-compose.yml up -d

train-local:
	python - <<'PY2'
import mlflow
import numpy as np
from sklearn.linear_model import LinearRegression
X = np.arange(0,10).reshape(-1,1)
y = np.arange(0,10)
model = LinearRegression().fit(X, y)
with mlflow.start_run():
    mlflow.sklearn.log_model(model, 'model')
    mlflow.log_metric('rmse', 0.0)
PY2

argo-submit:
	argo submit argo/workflow.yaml

deploy-api:
	kubectl apply -f k8s/api-deployment.yaml
	kubectl apply -f k8s/api-service.yaml
	kubectl apply -f k8s/hpa.yaml

perf-test:
	bash scripts/perf_test.sh

lint:
        pip install pre-commit
        pre-commit run --all-files

clean:
	docker-compose -f mlflow/docker-compose.yml down
	rm -rf __pycache__ .pytest_cache mlruns
