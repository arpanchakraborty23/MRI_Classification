import numpy as np
from tensorflow import keras
from src.utils.utils import load_h5_model
from keras.preprocessing import image
import os

class PredictionPipline:
    def __init__(self,filename) -> None:
        self.filename=filename

    def predict(self):

        # load model
        model=load_h5_model(os.path.join('artifacts/model/model.h5'))

        imagename=self.filename

        test_image=image.load_img(imagename,target_size=(224,224))
        test_image=image.img_to_array(test_image)
        test_image=np.expand_dims(test_image,axis=0)
        result=np.argmax(model.predict(test_image),axis=1)

        print(result)

        if result==[1]:
            prediction='Has Dementia'
            return [{'image':prediction}]
        else:
            prediction='Non-Demented'
            return [{'image':prediction}]
            