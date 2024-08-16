import os
import sys
import yaml
import requests
import tensorflow as tf
import json
from pathlib import Path
import base64
from keras.models import load_model
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

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

def load_h5_model(file_path):
    model = load_model(file_path)
    print(f"Model loaded from {file_path}")
    return model

def plot_metrics(history):
         # Retrieve the history from the model
        epochs = range(1, len(history['accuracy']) + 1)

        # Plotting training and validation accuracy
        plt.figure(figsize=(10, 6))
        plt.plot(epochs, history['accuracy'], 'bo-', label='Training Accuracy')
        plt.plot(epochs, history['val_accuracy'], 'go-', label='Validation Accuracy')

        plt.title('Training and Validation Accuracy over Epochs')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.grid(True)
        plt.show()

        logging.info('Training and Validation Accuracy plot generated.')

def save_json(path: Path, data: dict):

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


        logging.info(f' Created dir {path}')
        
def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()
