import mlflow
import numpy as np
from sklearn.linear_model import LinearRegression

def main() -> None:
    X = np.arange(0, 10).reshape(-1, 1)
    y = np.arange(0, 10)
    model = LinearRegression().fit(X, y)
    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "model")
        mlflow.log_metric("rmse", 0.0)


if __name__ == "__main__":
    main()
