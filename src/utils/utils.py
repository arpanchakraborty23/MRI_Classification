import os
import sys
import yaml
import requests
import tensorflow as tf

from src.logger.logging import logging
from src.exception.exception import CustomException

def read_yaml(file_path):
    try:
        with open(file_path,'r') as y:
            contant=yaml.safe_load(y)

            logging.info(f'{contant} file loaded successfully')

        return contant
    except Exception as e:
        logging.info(f'error in yaml load {str(e)}')
        raise CustomException(sys,e)
    
def create_dir(dir_path:list):
    try:
        for path in dir_path:
            os.makedirs(path,exist_ok=True)

            logging.info(f' crated dir at {path}')

    except Exception as e:
        logging.info(f'error in yaml load {str(e)}')
        raise CustomException(sys,e)
    
def get_data_dwonload(url,local_folder=None):
    try:
        logging.info('Data download started')
        data_url = url

        # Check if the URL is valid and make a request to get the data
        response = requests.get(data_url)
        response.raise_for_status()  # Raise an error for unsuccessful requests

        # Write the content to a file
        with open(local_folder, 'wb') as file:
            file.write(response.content)
        
        logging.info('Data download completed')

    except Exception as e:
        logging.info(f'error in yaml load {str(e)}')
        raise CustomException(sys,e)
    
def save_model(path,model:tf.keras.Model):
    model.save(path)
        
    
