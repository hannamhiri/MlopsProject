from mlProject.config.configuration import ConfigurationManager
from mlProject.components.model_trainer import ModelTrainer
from mlProject import logger



STAGE_NAME = "Model Trainer stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config_obj = config.get_model_trainer_config()  # config spécifique du trainer
        all_params = config.get_all_model_params()  # méthode à créer ou utiliser pour récupérer les params du YAML

        model_trainer = ModelTrainer(
            config=model_trainer_config_obj,
            all_params=all_params
        )
        model_trainer.train()




if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainerTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
