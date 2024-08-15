import os,sys

from src.logger.logging import logging
from src.exception.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.base_model import BaseModel
from src.components.model_train import ModelTraining

class TrainPipline:
    def __init__(self) -> None:
        logging.info('******************* Traning Pipline ********************')

    def DataIngestionPipline(self):
        try:
            data_ingestion=DataIngestion()
            data_ingestion.initating_data_ingestion()

        except Exception as e:
            logging.info('erorr in data ingestion pipline ',str(e))
            raise CustomException(sys,e)
        
    def BaseModelPipeline(self):
        try:
            obj=BaseModel()
            obj.get_base_model()
            obj.update_base_model()
        except Exception as e:
            logging.info('erorr in base model pipline ',str(e))
            raise CustomException(sys,e)
        
    def ModelTrainPipline(self):
        try:
            obj=ModelTraining()
            obj.get_base_model()
            obj.train_valid_generator()
            obj.train()

        except Exception as e:
            logging.info('erorr in  model train pipline ',str(e))
            raise CustomException(sys,e)




if __name__=='__main__':
    try:
        obj=TrainPipline()
        obj.DataIngestionPipline()
        obj.BaseModelPipeline()
        obj.ModelTrainPipline()
        
    except Exception as e:
            logging.info('erorr in Train Pipline ',str(e))
            raise CustomException(sys,e)
