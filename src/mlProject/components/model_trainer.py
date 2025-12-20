import pandas as pd
import os
from mlProject import logger
import joblib
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from mlProject.entity.config_entity import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        # 1️⃣ Charger les données
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        # 2️⃣ Séparer X / y
        X_train = train_data.drop([self.config.target_column], axis=1)
        y_train = train_data[self.config.target_column]

        X_test = test_data.drop([self.config.target_column], axis=1)
        y_test = test_data[self.config.target_column]

        # 3️⃣ Appliquer SMOTE uniquement sur le train
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

        logger.info("Target distribution AFTER SMOTE:")
        logger.info(pd.Series(y_train_res).value_counts().to_string())

        logger.info(f"Train before SMOTE: {X_train.shape}")
        logger.info(f"Train after SMOTE: {X_train_res.shape}")

        # 4️⃣ Entraîner RandomForest
        model = RandomForestClassifier(
            n_estimators=self.config.n_estimators,
            max_depth=self.config.max_depth,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train_res, y_train_res)

        # 5️⃣ Sauvegarde du modèle
        os.makedirs(self.config.root_dir, exist_ok=True)
        model_path = os.path.join(self.config.root_dir, self.config.model_name)

        joblib.dump(model, model_path)

        logger.info(f"RandomForest model saved at {model_path}")


