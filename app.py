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
from main import Recognizer

app = Flask(__name__)
# app.secret_key = 'supersecretkey'  # Ganti dengan kunci rahasia yang aman
# socketio = SocketIO(app)


alexnet = load_model("model/Aelx_Net.h5")
densenet = load_model("model/DenseNet121.h5")
resnet = load_model("model/ResNet.h5")


UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'webp', 'jfif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# recognizer = Recognizer(socketio=socketio)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/upload")
def upload():
    return render_template("upload/index.html")

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
	
    return render_template("upload/result.html", img_path = predict_image_path, 
                        predictionalexnet = class_names[np.argmax(prediction_alexnet)],
                        confidencealexnet = '{:2.0f}%'.format(100 * np.max(prediction_alexnet)),
                        predictiondensenet = class_names[np.argmax(prediction_densenet)],
                        confidencedensenet = '{:2.0f}%'.format(100 * np.max(prediction_densenet)),
                        predictionresnet = class_names[np.argmax(prediction_resnet)],
                        confidenceeresnet = '{:2.0f}%'.format(100 * np.max(prediction_resnet)),
                        )

	# 		recognizer.predict(predict_image_path)

    #     return redirect(url_for('result'))

    # else:
    #     flash('File type is not allowed', 'danger')
    #     return redirect(url_for('upload'))

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/result")
def result():
    return render_template("upload/result.html")

@app.route("/history")
def history():
    return render_template("upload/history.html")

@app.route("/camera")
def camera():
    return render_template("camera/index.html")

def gen_frames():
    camera = cv.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
