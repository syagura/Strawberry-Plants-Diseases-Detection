import asyncio
import websockets
import binascii
from io import BytesIO
from PIL import Image
from base64 import b64decode
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory, Response
from flask_socketio import SocketIO
from keras.models import load_model
from werkzeug.utils import secure_filename
import cv2 as cv
from keras.preprocessing import image
from PIL import Image
from datetime import datetime
import os
import numpy as np

app = Flask(__name__)

alexnet = load_model("../model/Alex_Net1.h5")
densenet = load_model("../model/DenseNet.h5")
resnet = load_model("../model/ResNet.h5")


UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'webp', 'jfif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_strawberry_leaf(image):
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
    
def preprocess_image_with_segmentation_rgb(img, target_size=(124, 124)):
    curr_image = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    segmented_image = segment_image_rgb(curr_image)
    image_resized = cv.resize(segmented_image, target_size)
    image_normalized = image_resized / 255.0
    image_array = image.img_to_array(image_normalized)
    image_array = np.expand_dims(image_normalized, axis=0)
    return image_array

def segment_image_rgb(image, k=3):
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv.kmeans(pixel_values, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    labels = labels.flatten()
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(image.shape)
    return segmented_image

def predict(img):
    labels = ['angular leafspot', 'leaf spot', 'powdery mildew leaf']
    image_array = np.array(img)
    detected, mask = detect_strawberry_leaf(image_array)
    
    if not detected:
        return 'None', 'None', 'None'
    
    image_array = preprocess_image_with_segmentation_rgb(mask)

    output_Alexnet = alexnet.predict(image_array)
    output_Densenet = densenet.predict(image_array)
    output_Resnet = resnet.predict(image_array)

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

def get_image():
    while True:
        try:
            with open("image.jpg", 'rb') as f:
                image_bytes = f.read()
            image = Image.open(BytesIO(image_bytes))
            img_io = BytesIO()
            image.save(img_io, 'JPEG')
            img_io.seek(0)
            img_bytes = img_io.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')
           
        
        except Exception as e:
            print("encountered an exception: ")
            print(e)
            
            with open('placeholder.jpg', 'rb') as f:
                image_bytes = f.read()
            image = Image.open(BytesIO(image_bytes))
            img_io = BytesIO()
            image.save(img_io, 'JPEG')
            img_io.seek(0)
            img_bytes = img_io.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", page='home')

@app.route("/about")
def about():
    return render_template("about.html", page='about')

@app.route("/upload")
def upload():
    return render_template("upload/index.html", page='upload')

@app.route('/submit', methods=['POST'])
def submit():
    if 'input-image' not in request.files:
        resp = jsonify({'message': 'No image in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist('input-image')
    filename = "temp_image.png"
    errors = {}
    success = False
    for file in files:
        if file and allowed_file(file.filename):
            namefile = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors["message"] = 'File type of {} is not allowed'.format(file.filename)

    if not success:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp
    img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # return img_url

    # convert image to RGB
    img = Image.open(img_url).convert('RGB')
    now = datetime.now()
    predict_image_path = 'uploads/' + now.strftime("%d%m%y-%H%M%S") + ".png"
    image_predict = predict_image_path
    img.convert('RGB').save(image_predict, format="png")
    img.close()

    img = image.load_img(predict_image_path, target_size=(124, 124, 3))
    result_Alexnet, result_Densenet, result_Resnet = predict(img)
	
    return render_template("upload/result.html", img_path = predict_image_path, 
                        predictionalexnet = result_Alexnet,
                        predictiondensenet = result_Densenet,
                        predictionresnet = result_Resnet,
                        )

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/result")
def result():
    return render_template("upload/result.html", page='upload')

@app.route("/history")
def history():
    return render_template("upload/history.html", page='history')

@app.route("/camera")
def camera():
    return render_template("camera/index.html", page='camera')

@app.route('/video_feed')
def video_feed():
    return Response(get_image(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/result_video")
def result_video():
    try:
        with open("image.jpg", 'rb') as f:
            image_bytes = f.read()
        image = Image.open(BytesIO(image_bytes))
        image = np.array(image)
        
        result_Alexnet, result_Densenet, result_Resnet = predict(image)
        
        return jsonify({
            "alexnet": result_Alexnet,
            "densenet": result_Densenet,
            "resnet": result_Resnet
        })
    except Exception as e:
        print("encountered an exception: ")
        print(e)
        return jsonify({
            "alexnet": 'None',
            "densenet": 'None',
            "resnet": 'None'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
