import os,sys

from src.logger.logging import logging
from src.exception.exception import CustomException
from src.constant.ymal_path import *
from src.utils.utils import read_yaml,create_dir
from src.entity.config_entity import DataIngestionConfig,BaseModelConfig


class ConfigManager:
    def __init__(self,config=config_file_path,prams=params_file_path) -> None:
        self.config=read_yaml(config)
        self.param=read_yaml(prams)

        create_dir([self.config['artifacts_root']])

    def data_ingestion_config(self):
        try:
            config=self.config['Data_ingestion']
            config_file=DataIngestionConfig(
                dir=config['dir'],
                url=config['url'],
                local_folder=config['local_folder'],
                unzip_folder=config['unzip_folder']
            )

            return config_file

        except Exception as e:
            logging.info('errron in data ingestion config',str(e))
            raise CustomException(sys,e)
        
    def base_model_config(self):
        try:
            config=self.config['Base_model']

            base_model=BaseModelConfig(
                dir=config['dir'],
                base_model=config['base_model_path'],
                update_base_model_path=config['update_base_model_path'],
                image_size=self.param['IMAGE_SIZE'],
                learning_rate=self.param['LEARNING_RATE'],
                include_top=self.param['INCLUDE_TOP'] ,
                weights=self.param['WEIGHTS'] ,
                classes=self.param['CLASSES']
            )

            return base_model
        except Exception as e:
            logging.info(f' error in base model {str(e)}')
            raise CustomException(e,sys)