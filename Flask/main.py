import os
import cv2 as cv
import numpy as np
import datetime
from PIL import Image
from keras.models import load_model
from keras.preprocessing import image
from flask_socketio import SocketIO
import base64

class Prediction():
    def __init__(self, socketio, alexnet="model/Alex_Net.h5", densenet="model/DenseNet.h5", resnet="model/ResNet.h5"):
        self.socketio = socketio
        self.labels = ['angular leafspot', 'leaf spot', 'powdery mildew leaf']
        self.model_Alexnet = load_model(alexnet)
        self.model_Densenet = load_model(densenet)
        self.model_Resnet = load_model(resnet)

    def detect_strawberry_leaf(self, image):
        # Convert image to HSV color space
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        
        # Define range of green color in HSV
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        
        # Threshold the HSV image to get only green colors
        mask = cv.inRange(hsv, lower_green, upper_green)
        
        # Find contours in the mask
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # If any contours are found, consider it as a detected leaf
            return True, mask
        else:
            return False, mask
    
    def segment_image_rgb(self, image, k=3):
        pixel_values = image.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv.kmeans(pixel_values, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        labels = labels.flatten()
        segmented_image = centers[labels.flatten()]
        segmented_image = segmented_image.reshape(image.shape)
        return segmented_image

    def preprocess_image_with_segmentation_rgb(self, img, target_size=(124, 124)):
        curr_image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        segmented_image = self.segment_image_rgb(curr_image)
        image_resized = cv.resize(segmented_image, target_size)
        image_normalized = image_resized / 255.0
        image_array = image.img_to_array(image_normalized)
        image_array = np.expand_dims(image_normalized, axis=0)
        return image_array
    
    def predict(self, img):
        labels = ['angular leafspot', 'leaf spot', 'powdery mildew leaf']
        image_array = np.array(img)
        detected, mask = self.detect_strawberry_leaf(image_array)
        
        if not detected:
            return 'None', 'None', 'None'
        
        image_array = self.preprocess_image_with_segmentation_rgb(mask)

        output_Alexnet = self.model_Alexnet.predict(image_array)
        output_Densenet = self.model_Densenet.predict(image_array)
        output_Resnet = self.model_Resnet.predict(image_array)

        idx_Alexnet = output_Alexnet.argmax(axis=1)[0]
        confidence_Alexnet = output_Alexnet.max(axis=1)[0] * 100
        
        idx_Densenet = output_Densenet.argmax(axis=1)[0]
        confidence_Densenet = output_Densenet.max(axis=1)[0] * 100
        
        idx_Resnet = output_Resnet.argmax(axis=1)[0]
        confidence_Resnet = output_Resnet.max(axis=1)[0] * 100

        result_Alexnet = labels[idx_Alexnet] if confidence_Alexnet >= 85 else 'None'
        result_Densenet = labels[idx_Densenet] if confidence_Densenet >= 85 else 'None'
        result_Resnet = labels[idx_Resnet] if confidence_Resnet >= 85 else 'None'
        
        return result_Alexnet, result_Densenet, result_Resnet

    # def preprocessing(self, img):
    #     image_array = image.img_to_array(img)
    #     image_array = np.expand_dims(image_array, axis=0)
    #     image_array /= 255.0
    #     return image_array

    # def predict(self, image_path):
    #     img = image.load_img(image_path, target_size=(227, 227, 3))
    #     img_array = self.preprocessing(img)
    #     output_Alexnet = self.model_Alexnet.predict(img_array)
    #     output_Densenet = self.model_Densenet.predict(img_array)
    #     output_Resnet = self.model_Resnet.predict(img_array)

    #     idx_Alexnet = output_Alexnet.argmax(axis=1)[0]
    #     idx_Densenet = output_Densenet.argmax(axis=1)[0]
    #     idx_Resnet = output_Resnet.argmax(axis=1)[0]

    #     result_Alexnet = self.labels[idx_Alexnet]
    #     result_Densenet = self.labels[idx_Densenet]
    #     result_Resnet = self.labels[idx_Resnet]

    #     with open(image_path, "rb") as img_file:
    #         encoded_img = base64.b64encode(img_file.read()).decode('utf-8')

    #     self.socketio.emit("prediction", {
    #         'image': encoded_img,
    #         'result_Alexnet': result_Alexnet,
    #         'result_Densenet': result_Densenet,
    #         'result_Resnet': result_Resnet
    #     })