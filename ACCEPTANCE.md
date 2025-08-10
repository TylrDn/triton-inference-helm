# Acceptance Checks

- `make up-mlflow` starts MLflow tracking server and MinIO; the UI is reachable at http://localhost:5000.
- `argo submit argo/workflow.yaml` completes the pipeline and registers a model with metrics and artifacts in MLflow.
- `make deploy-api` deploys the FastAPI service and exposes `/predict` which returns a valid response.
- `make perf-test` runs a basic load test printing latency statistics.
- CI (`.github/workflows/ci.yaml`) runs pre-commit and pytest successfully.
