import os,sys
import json
import tensorflow as tf
from tensorflow import keras
from urllib.parse import urlparse
import mlflow.sklearn
import mlflow.keras
from keras.models import load_model
from pathlib import Path

from src.logger.logging import logging
from src.exception.exception import CustomException
from src.utils.utils import save_model,save_json
from src.configure.config_manager import ConfigManager

class Evaluation:
    def __init__(self) -> None:
        self.config=ConfigManager().evaluation_config()
        self.model=self.config.model_path

        logging.info('<----------------- Model Evaluation ------------->')

    def valid_genarator(self):
        try:
            datagenerator_kwargs = dict(
                rescale = 1./255,
                validation_split=0.30
            )

            dataflow_kwargs = dict(
                target_size=self.config.image_size[:-1],
                batch_size=self.config.batch_size,
                interpolation="bilinear"
            )

            valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                **datagenerator_kwargs
            )

            self.valid_generator = valid_datagenerator.flow_from_directory(
                directory=self.config.test_data,
                subset="validation",
                shuffle=False,
                **dataflow_kwargs
            )
        except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise CustomException(sys,e)
        
    def save_score(self):
        scores = {"loss": self.score[0], "accuracy": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)
        
    def log_to_mlflow(self):
        try:
            mlflow.set_registry_uri(self.config.mlflow_uri)

            track_uri_type=urlparse(mlflow.get_tracking_uri()).scheme
            with mlflow.start_run():
                
                mlflow.log_metrics(
                    {'loss ':self.score[0], 'accuracy': self.score[1] }
                )
                if track_uri_type !='file':
                    mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16Model")
                else:
                    mlflow.keras.log_model(self.model, "model")
        except Exception as e:
            logging.info(f' Error occured {str(e)}')
            raise CustomException(sys,e)