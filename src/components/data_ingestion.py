import os,sys
import zipfile

from src.logger.logging import logging
from src.exception.exception import CustomException
from src.utils.utils import get_data_dwonload
from src.configure.config_manager import ConfigManager

class DataIngestion:
    def __init__(self) -> None:
        self.config=ConfigManager().data_ingestion_config()

        logging.info('<----------------- Data Ingestion ------------------->')

    def initating_data_ingestion(self):
        try:
            # create data ingestion dir
            os.makedirs(self.config.dir,exist_ok=True)

            # data url
            dataset_url=self.config.url
            
            # download data to local folder
            local_folder=self.config.local_folder
            
            # unzip data
            unzip_folder=self.config.unzip_folder

            get_data_dwonload(url=dataset_url,local_folder=local_folder)


            # unziping data
            with zipfile.ZipFile(local_folder, 'r') as z:
                z.extractall(unzip_folder)

            logging.info('<------------------- Data Ingestion Completed ------------------------>')

           

        except Exception as e:
            logging.info('erorr in data ingestion ',str(e))
            raise CustomException(sys,e)