import joblib
import pandas as pd
from pathlib import Path
from mlProject.components.data_transformation import Preprocessor 
import mlflow 
import os

class PredictionPipeline:
    def __init__(self):
        os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/hannamhiri/MlopsProject.mlflow"
        os.environ["MLFLOW_TRACKING_USERNAME"] = "hannamhiri"
        os.environ["MLFLOW_TRACKING_PASSWORD"] = "d818c76624661ed3e44ed5cd15bb08d17cd94c4d"

        mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

        # Charger le dict du préprocesseur
        preprocessor_dict = joblib.load(Path('artifacts/data_transformation/preprocessor.pkl'))

        # Recréer un objet Preprocessor avec le dict
        self.preprocessor = Preprocessor(
            num_cols=preprocessor_dict["num_cols"],
            cat_cols=preprocessor_dict["cat_cols"],
            drop_cols=preprocessor_dict.get("drop_cols", [])
        )
        self.preprocessor.label_encoders = preprocessor_dict["label_encoders"]
        with open("best_model_uri.txt", "r") as f:
            model_uri = f.read().strip()
        # Charger le modèle
        self.model = mlflow.sklearn.load_model(model_uri)

        # Charger l'ordre des features
        self.feature_order = joblib.load(Path('artifacts/data_transformation/feature_order.pkl'))

    def predict(self, data: pd.DataFrame):
        # Assurer l'ordre correct des colonnes
        data = data[self.feature_order]

        # Transformer les données avec le préprocesseur
        data_preprocessed = self.preprocessor.transform(data)

        # Faire la prédiction
        prediction = self.model.predict(data_preprocessed)
        return prediction
