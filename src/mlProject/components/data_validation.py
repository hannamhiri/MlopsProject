import os
from mlProject import logger
import pandas as pd
from mlProject.entity.config_entity import DataValidationConfig

class DataValiadtion:
    def __init__(self, config : DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = True

            # Lire le dataset
            data = pd.read_csv(self.config.unzip_data_dir)
            data_columns = set(data.columns)

            schema_columns = set(self.config.all_schema.keys())

            # 1️⃣ Colonnes manquantes
            missing_columns = schema_columns - data_columns
            if missing_columns:
                logger.error(f"Missing columns: {missing_columns}")
                validation_status = False

            # 2️⃣ Colonnes inconnues
            extra_columns = data_columns - schema_columns
            if extra_columns:
                logger.error(f"Extra columns: {extra_columns}")
                validation_status = False

            # 3️⃣ Écriture du status UNE SEULE FOIS
            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            logger.exception(e)
            raise e
