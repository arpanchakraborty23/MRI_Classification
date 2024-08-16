import os,sys

from src.logger.logging import logging
from src.exception.exception import CustomException
from src.constant.ymal_path import *
from src.utils.utils import read_yaml,create_dir
from src.entity.config_entity import DataIngestionConfig,BaseModelConfig,ModelTrainConfig,Evaluation


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
            logging.info(f'base model {config}')

           

            base_model_config=BaseModelConfig(
                dir=Path(config['dir']),
                base_model=Path(config['base_model_path']),
                update_base_model_path=Path(config['update_base_model_path']),
                image_size=self.param['IMAGE_SIZE'],
                learning_rate=self.param['LEARNING_RATE'],
                include_top=self.param['INCLUDE_TOP'] ,
                weights=self.param['WEIGHTS'] ,
                classes=self.param['CLASSES'] 
                                    )

            return base_model_config
        except Exception as e:
            logging.info(f' error in base model {str(e)}')
            raise CustomException(e,sys)
        
    def model_train_config(self):
        try:
            train=self.config['Model_Train']
            base_model=self.config['Base_model']
            
            
            
            train_config=ModelTrainConfig(
                dir=Path(train['dir']),
                model_path=Path(train['model_path']),
                update_base_model_path=Path(base_model['update_base_model_path']),
                train_data=Path(train['train_data']),
                validation_data=train['validation_data'],
                epochs=self.param['EPOCHS'],
                batch_size=self.param['BATCH_SIZE'],
                augmentation=self.param['AUGMENTATION'],
                image_size=self.param['IMAGE_SIZE']
            )

            return train_config 

        except Exception as e:
            logging.info(' error in Model Train config')
            raise CustomException(sys,e)

    def evaluation_config(self):
        try:
            config=self.config['Model_Evaluation']

            evaluation_config=Evaluation(    
                dir=config['dir'],
                test_data=config['test_data'],
                mlflow_uri=config['mlflow_url'],
                batch_size=self.param['BATCH_SIZE'],
                image_size=self.param['IMAGE_SIZE']
                )
               
                
            

            return evaluation_config

        except Exception as e:
            logging.info(f'error in evaluation config {str(e)}')
            raise CustomException(sys,e)