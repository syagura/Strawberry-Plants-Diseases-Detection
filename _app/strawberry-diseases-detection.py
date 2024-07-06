import os
import cv2 as cv
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array, load_img

class Recognizer():
    def __init__(self, alexnet_model = 'model/forzen_graph_alexnet.pb',
                       densenet_model = 'model/forzen_graph_densenet.pb',
                       resnet_model = 'model/forzen_graph_resnet.pb'):
        
        path = os.path.join(os.getcwd(), os.path.dirname(__file__))
        
        self.labels = ['angular leafdpot',
                       'leaf spot',
                       'powdery mildew leaf']
        
        self.alexnet = cv2.dnn.readNet(os.path.join(path, alexnet_model))
        self.densenet = cv2.dnn.readNet(os.path.join(path, densenet_model))
        self.resnet = cv2.dnn.readNet(os.path.join(path, resnet_model))
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self.layerOutput_alexnet = self.alexnet.getUnconnectedOutLayersNames()
        self.layerOutput_densenet = self.densenet.getUnconnectedOutLayersNames()
        self.layerOutput_resnet = self.resnet.getUnconnectedOutLayersNames()


    def predict(img):
        img = load_img(image_path, (227, 227))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        blob = cv2.dnn.blobFromImage(img_array, 1.0, (50, 50), (0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        output = self.alexnet.forward(self.layerOutput)

        idx = output[0].argmax(axis=1)[0]
            confidence = output[0].max(axis=1)[0]*100

            if confidence > 80:
                label_text = "%s (%.2f %%)" % (self.labels[idx], confidence)
            else :
                label_text = "N/A"
            result = label_text
            
        return result