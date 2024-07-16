import os
import cv2 as cv
import numpy as np
import datetime
from PIL import Image
from keras.models import load_model
from keras.preprocessing import image
from flask_socketio import SocketIO
import base64

class Recognizer():
    def __init__(self, socketio, alexnet="model/Aelx_Net.h5", densenet="model/DenseNet121.h5", resnet="model/ResNet.h5"):
        self.socketio = socketio
        self.labels = ['angular leafspot', 'leaf spot', 'powdery mildew leaf']
        self.model_Alexnet = load_model(alexnet)
        self.model_Densenet = load_model(densenet)
        self.model_Resnet = load_model(resnet)

    def preprocessing(self, img):
        image_array = image.img_to_array(img)
        image_array = np.expand_dims(image_array, axis=0)
        image_array /= 255.0
        return image_array

    def predict(self, image_path):
        img = image.load_img(image_path, target_size=(227, 227, 3))
        img_array = self.preprocessing(img)
        output_Alexnet = self.model_Alexnet.predict(img_array)
        output_Densenet = self.model_Densenet.predict(img_array)
        output_Resnet = self.model_Resnet.predict(img_array)

        idx_Alexnet = output_Alexnet.argmax(axis=1)[0]
        idx_Densenet = output_Densenet.argmax(axis=1)[0]
        idx_Resnet = output_Resnet.argmax(axis=1)[0]

        result_Alexnet = self.labels[idx_Alexnet]
        result_Densenet = self.labels[idx_Densenet]
        result_Resnet = self.labels[idx_Resnet]

        with open(image_path, "rb") as img_file:
            encoded_img = base64.b64encode(img_file.read()).decode('utf-8')

        self.socketio.emit("prediction", {
            'image': encoded_img,
            'result_Alexnet': result_Alexnet,
            'result_Densenet': result_Densenet,
            'result_Resnet': result_Resnet
        })