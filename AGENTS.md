You are scaffolding a complete repo named mlops-argo-mlflow demonstrating a practical MLOps flow.

Objectives
Argo Workflows pipeline: data prep → train → evaluate → register.

MLflow tracking & registry (docker-compose local, K8s manifest option).

FastAPI service that loads the latest “Production” model.

HPA; Makefile; CI; pre-commit; Apache-2.0 license.

Create this structure
bash
Copy
Edit
README.md
LICENSE
.gitignore
.pre-commit-config.yaml
.github/workflows/ci.yaml
Makefile
docker/
  Dockerfile.train
  Dockerfile.api
argo/
  workflow.yaml
  templates/prep.yaml
  templates/train.yaml
  templates/eval.yaml
  templates/register.yaml
mlflow/
  docker-compose.yml
  server-deploy.yaml
api/
  app.py
  requirements.txt
k8s/
  api-deployment.yaml
  api-service.yaml
  hpa.yaml
data/
  README.md
tests/
  test_api_smoke.py
scripts/
  perf_test.sh
ACCEPTANCE.md
File requirements (high level)
docker-compose.yml: MLflow + backend store (SQLite or Postgres) + MinIO; env vars documented.

workflow.yaml: DAG using artifacts via S3/MinIO; parameters for dataset path; outputs metrics and model artifact URI.

register.yaml: sets MLflow stage to “Production” on passing thresholds.

app.py: FastAPI /healthz and /predict; loads model by querying MLflow for latest “Production” version; fallback to local artifact path.

api-deployment.yaml: Deployment + Service; readiness probe; envs for MLFLOW_TRACKING_URI & S3 creds; hpa.yaml based on CPU or QPS.

Makefile: up-mlflow, train-local, argo-submit, deploy-api, perf-test, lint, clean.

perf_test.sh: simple wrk/hey loop issuing predictions and summarizing latency.

README.md: architecture, local quickstart (compose up), Argo install commands, submit workflow, view MLflow UI, deploy API, call /predict, promotion criteria, troubleshooting, cleanup.

ci.yaml: pre-commit + pytest (run test_api_smoke.py against local app).

.gitignore: Python base + .kube/, node_modules/, charts/*, *.tgz.

Acceptance checks
make up-mlflow starts tracking + MinIO; UI reachable.

argo submit ... completes; MLflow shows run with metrics and artifacts.

make deploy-api exposes /predict that returns a valid response.

make perf-test prints basic latency stats.

CI & pre-commit pass.

Output format
Use:

pgsql
Copy
Edit
=== path/to/file ===
<contents>
