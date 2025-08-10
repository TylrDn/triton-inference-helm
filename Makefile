.PHONY: up-mlflow train-local argo-submit deploy-api perf-test lint clean

up-mlflow:
	docker-compose -f mlflow/docker-compose.yml up -d

train-local:
	python scripts/train.py

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
