from flask import Flask, render_template, Response, request, flash, jsonify
from flask_socketio import SocketIO, emit
from keras.models import load_model
import tensorflow as tf 
from tensorflow import keras
from skimage import transform, io
from PIL import Image
from datetime import datetime
from keras.preprocessing import image
# from flask_cors import CORS
import numpy as np
import os
import cv2 as cv
from strawberry-diseases-detection import Recognizer()

app = Flask(__name__)

alexnet = load_model("model/Aelx_Net.h5")
densenet = load_model("model/DenseNet121.h5")
resnet = load_model("model/ResNet.h5")

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'webp', 'jfif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods = ['GET', 'POST'])
def main():
	return render_template("result.html")

@app.route('/submit', methods=['POST'])
def predict():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No image in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('file')
    filename = "temp_image.png"
    errors = {}
    success = False
    for file in files:
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors["message"] = 'File type of {} is not allowed'.format(file.filename)

    if not success:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp
    img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # convert image to RGB
    img = Image.open(img_url).convert('RGB')
    now = datetime.now()
    predict_image_path = 'uploads/' + now.strftime("%d%m%y-%H%M%S") + ".png"
    image_predict = predict_image_path
    img.convert('RGB').save(image_predict, format="png")
    img.close()

    # prepare image for prediction
    img = image.load_img(predict_image_path, target_size=(227, 227, 3))
    # images = np.vstack([img_array])
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Menambahkan dimensi batch
    img_array /= 255.0
    # img_array = np.expand_dims(img_array, axis=0)

    # predict
    prediction_alexnet = alexnet.predict(img_array)
    prediction_densenet = densenet.predict(img_array)
    prediction_resnet = resnet.predict(img_array)

    # prepare api response
    class_names = ['angular leafspot', 'leaf spot', 'powdery mildew leaf']
    # result = {
    #     "filename" : predict_image_path,
    #     "prediction": class_names[np.argmax(prediction_array)],
    #     "confidence": '{:2.0f}%'.format(100 * np.max(prediction_array))
    # }
	
    return render_template("result.html", img_path = predict_image_path, 
                        predictionalexnet = class_names[np.argmax(prediction_alexnet)],
                        confidencealexnet = '{:2.0f}%'.format(100 * np.max(prediction_alexnet)),
                        predictiondensenet = class_names[np.argmax(prediction_densenet)],
                        confidencedensenet = '{:2.0f}%'.format(100 * np.max(prediction_densenet)),
                        predictionresnet = class_names[np.argmax(prediction_resnet)],
                        confidenceeresnet = '{:2.0f}%'.format(100 * np.max(prediction_resnet)),
                        )

if __name__ == '__main__':
    app.run(debug=True)