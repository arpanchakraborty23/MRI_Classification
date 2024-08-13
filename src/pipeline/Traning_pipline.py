import os,sys

from src.logger.logging import logging
from src.exception.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.base_model import BaseModel

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
            obj.updated_model()
        except Exception as e:
            logging.info('erorr in base model pipline ',str(e))
            raise CustomException(sys,e)



if __name__=='__main__':
    try:
        obj=TrainPipline()
        obj.DataIngestionPipline()
        obj.BaseModelPipeline()
        
    except Exception as e:
            logging.info('erorr in data ingestion ',str(e))
            raise CustomException(sys,e)
