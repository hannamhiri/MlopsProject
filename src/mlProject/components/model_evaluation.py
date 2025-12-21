import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from pathlib import Path
from mlProject.entity.config_entity import ModelEvaluationConfig
from mlProject.utils.common import save_json
from mlProject import logger

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

        # 🔹 Définir les variables d'environnement pour MLflow distant
        os.environ["MLFLOW_TRACKING_URI"] = self.config.mlflow_uri
        os.environ["MLFLOW_TRACKING_USERNAME"] = "hannamhiri"  # ton user DagsHub
        os.environ["MLFLOW_TRACKING_PASSWORD"] = "d818c76624661ed3e44ed5cd15bb08d17cd94c4d"  # token perso

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def log_into_mlflow(self):
        test_data = pd.read_csv(self.config.test_data_path)
        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[self.config.target_column]

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        logger.info(f"Tracking URI: {mlflow.get_tracking_uri()}")

        for model_file in os.listdir(self.config.model_dir):
            if not model_file.endswith(".pkl"):
                continue

            model_name = model_file.replace(".pkl", "")
            model_path = os.path.join(self.config.model_dir, model_file)
            logger.info(f"Evaluating model: {model_name}")

            model = joblib.load(model_path)

            with mlflow.start_run(run_name=model_name):
                predictions = model.predict(test_x)
                rmse, mae, r2 = self.eval_metrics(test_y, predictions)

                scores = {"rmse": rmse, "mae": mae, "r2": r2}
                save_json(
                    path=Path(os.path.join(self.config.root_dir, f"{model_name}_metrics.json")),
                    data=scores
                )

                if model_name in self.config.all_params:
                    mlflow.log_params(self.config.all_params[model_name])

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("mae", mae)
                mlflow.log_metric("r2", r2)

                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name=f"{model_name}Model")
                else:
                    mlflow.sklearn.log_model(model, "model")
