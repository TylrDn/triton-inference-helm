# mlops-argo-mlflow

A reference MLOps project combining Argo Workflows for orchestration, MLflow for tracking and
model registry, and a FastAPI inference service. The default pipeline performs data
preparation, training, evaluation, and registration of a model promoted to the `Production`
stage when quality thresholds are met.

## Architecture
- **Argo Workflows** orchestrate the ML pipeline stages and pass artifacts through MinIO.
- **MLflow** tracks experiments and hosts the model registry.
- **FastAPI** serves the latest `Production` model and provides `/healthz` and `/predict` endpoints.
- **Kubernetes** deployment with optional Horizontal Pod Autoscaler.

## Quickstart
1. **Start MLflow and MinIO**
   ```bash
   make up-mlflow
   ```
   Visit the MLflow UI at <http://localhost:5000>.

2. **Install Argo and submit the workflow**
   ```bash
   kubectl create namespace argo
   kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo-workflows/stable/manifests/install.yaml
   argo submit argo/workflow.yaml
   ```

3. **Deploy the API**
   ```bash
   make deploy-api
   ```
   Call the service:
   ```bash
   curl -X POST http://localhost:8000/predict -H 'Content-Type: application/json' \
     -d '{"features":[1,2,3]}'
   ```

4. **Load testing**
   ```bash
   make perf-test
   ```

## Promotion Criteria
The `register` step compares metrics against thresholds and, when satisfied,
transitions the model to the `Production` stage in MLflow.

## Troubleshooting
- Check container logs with `docker-compose logs` or `kubectl logs`.
- Ensure MinIO credentials match those configured in MLflow and the API.

## Cleanup
```bash
make clean
```
