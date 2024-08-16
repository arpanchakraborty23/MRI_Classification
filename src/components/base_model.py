import os,sys
import urllib.request as request
import tensorflow as tf
from tensorflow import keras
from pathlib import Path
from keras.applications.vgg16 import VGG16
from keras.applications.resnet50 import ResNet50

from src.configure.config_manager import ConfigManager
from src.exception.exception import CustomException
from src.logger.logging import logging

class BaseModel:
    def __init__(self,config=ConfigManager()) -> None: 
        self.config=config.base_model_config()

    def get_base_model(self):
        try:
            logging.info('<------------------ Base Model --------------------->')

            self.model=VGG16(
                input_shape=self.config.image_size,
                include_top=self.config.include_top,
                weights=self.config.weights,
            )

            self.save_model(path=self.config.base_model,model=self.model)


        except Exception as e:
            logging.info('error occured ', str(e))
            raise CustomException(sys,e) 

    @staticmethod
    def Vgg16_model(self,model,classes,freeze_all,freeze_till,learning_rate):
      
            if freeze_all:
                for layers in model.layers:
                    model.trainable=False
            elif (freeze_till is not None) and  (freeze_till > 0):
                for layers in model.layers[:-freeze_till] :
                    model.trainable=False

            flatten_in=keras.layers.Flatten()(model.output)
           
            prediction=keras.layers.Dense(
                units=classes,
                activation='softmax'
            )(flatten_in)
            full_model=keras.models.Model(
                inputs=model.input,
                outputs=prediction
            )
            full_model.compile(
                optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
                loss=tf.keras.losses.CategoricalCrossentropy(),
                metrics=["accuracy"]
            )

            full_model.summary()
            print(full_model.summary())

            logging.info(full_model.summary())
            return full_model

      

    def update_base_model(self):
        self.full_model=self.Vgg16_model(self,
            model=self.model,
            classes=self.config.classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.learning_rate
        )

        self.save_model(path=self.config.update_base_model_path,model=self.full_model)
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    logging.info('<------------------ Base Model Completed --------------------->') 