import os,sys
import tensorflow
from tensorflow import keras
from keras.applications.resnet50 import ResNet50 

from src.logger.logging import logging
from src.exception.exception import CustomException
from src.configure.config_manager import ConfigManager
from src.utils.utils import save_model

class BaseModel:
    def __init__(self) -> None:
        self.config=ConfigManager().base_model_config()

        logging.info('<---------------- Base Model ---------------->')

    def get_base_model(self):
        try:
            # getting base model RESNET50 
            self.model=ResNet50(
                input_shape=self.config.image_size,
                include_top=self.config.include_top,
                weights=self.config.weights,
                classes=self.config.classes,
            )

            # save base model
            return save_model(self.config.base_model,self.model)

        except Exception as e:
            logging.info(f'error in base model {str(e)}')
            raise CustomException(sys,e)
        
    def resnet50_model(self,model,classes,freeze_all,freeze_till,learning_rate):
        try:
                if freeze_all:
                    for layers in model.layers:
                        model.trainable=False
                elif (freeze_till is not None) and  (freeze_till > 0):
                        for layers in model.layers[:-freeze_till] :
                            model.trainable=False

                flatten_in=keras.layers.Flatten()(model.output)

                prediction=keras.layers.Dense(
                    units=classes,
                    activation='sigmoid'
                )(flatten_in)

                full_model=keras.models.Model(
                    inputs=model.input,
                    outputs=prediction
                    )

                full_model.compile(
                    optimizer=keras.optimizers.SGD(learning_rate=learning_rate),
                loss='crossentropy',
                metrics=["accuracy"]
                )
                full_model.summary()
                print(full_model.summary())
                return full_model

        except Exception as e:
            logging.info('error in resnet model ')
            raise CustomException(sys,e)
        
    def updated_model(self):
         self.full_model=self.resnet50_model(
                                             model=self.model,
                                             classes=self.config.classes,
                                             freeze_all=True,
                                             freeze_till=None,
                                             learning_rate=self.config.learning_rate
                                             )
         
         return save_model(path=self.config.update_base_model_path,model=self.full_model)