import os,sys
from pathlib import Path
import tensorflow as tf
from tensorflow import keras 


from src.configure.config_manager import ConfigManager
from src.logger.logging import logging
from src.exception.exception import CustomException

class ModelTraining:
    def __init__(self, config= ConfigManager()) -> None:
        self.config = config.model_train_config()
        logging.info('<------------------ Model Traning -------------------------->')

    def get_base_model(self):
        self.model =keras.models.load_model(
            self.config.update_base_model_path
        )

    def train_valid_generator(self):
        datagenerator_kwargs = dict(
            rescale=1./255,
            validation_split=0.25
        )

        data_flow = dict(
            target_size=self.config.image_size[:-1],
            batch_size=self.config.batch_size,
            interpolation="bilinear"
        )

        valid_generator = keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )
        self.valid_generator = valid_generator.flow_from_directory(
            directory=self.config.validation_data,
            subset='validation',
            shuffle=False,
            **data_flow
        )

        if self.config.augmentation:
            train_datagenerator = keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                **datagenerator_kwargs
            )
        else:
            train_datagenerator = valid_generator

        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.train_data,
            subset='training',
            shuffle=True,
            **data_flow
        )

    @staticmethod
    def save_model(path: Path, model: keras.Model):
        model.save(path)

    def train(self):
        self.steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size
       
        optimizer = tf.keras.optimizers.SGD(learning_rate=0.003)
        loss=keras.losses.categorical_crossentropy

        self.model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

        self.model.fit(
        self.train_generator,
        epochs=self.config.epochs,
        steps_per_epoch=self.steps_per_epoch,
        validation_steps=self.validation_steps,
        validation_data=self.valid_generator
    )
        print(self.model.history)
        logging(self.model.history)

        
        self.save_model(
            self.config.model_path,  
            self.model
        )

        logging.info('<------------------  Model Train Completed --------------------->')

       