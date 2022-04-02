import pickle
import numpy as np
from flask import Flask
from PIL import Image
import tensorflow as tf
from tensorflow import keras

app = Flask(__name__)

@app.route("/")
def play():
    with open('./data/car_classification_model_alexey.pkl', 'rb') as f:
        model = pickle.load(f)   
    
    image = np.array(Image.open('https://avcdn.av.by/advertbig/0000/5390/3944.jpeg').convert('RGB').resize(img_size)) #.convert('RGB') нужен на случай, если изображение черно-белое
    img_size = np.array(model.input.shape)[[2, 1]]

    image = image[None, ...]
    pred = model.predict(image)[0]
    class_idx = pred.argmax()

    class_names = [
      'Приора', #0
      'Ford Focus', #1
      'Самара', #2
      'ВАЗ-2110', #3
      'Жигули', #4
      'Нива', #5
      'Калина', #6
      'ВАЗ-2109', #7
      'Volkswagen Passat', #8
      'ВАЗ-21099' #9
    ]

    return class_names[class_idx]