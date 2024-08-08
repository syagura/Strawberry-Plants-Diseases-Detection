# 1. Strawberry Plants Diseases Detection
> "Using Alexnet, DenseNet 121 and ResNet50"

# 2. Project Description
"Proyek ini bertujuan untuk mendeteksi penyakit pada tanaman strawberry menggunakan kamera ESP32-CAM dan mengirimkan data ke aplikasi berbasis web Flask melalui WebSocket."

# 3. Features
* Deteksi penyakit pada tanaman strawberry menggunakan machine learning dengan model Alexnet, ResNet50 dan DenseNet 121.
* Pengambilan tanaman secara realtime menggunakan ESP32-CAM.
* Komunikasi antara ESP32-CAM dan Flask menggunakan Websocket.
* Menampilkan hasil deteksi di aplikasi web.

# 4. Hardware & Software Requirements
* Hardware
> * Arduino UNO R3
> * ESP32-CAM
> * Power Suplay
> * Kabel Jumper
> * Breadboard (Optional)
* Software
> * Arduino IDE
> * Python 3.x
> * Flask
> * Library Python: `Flask-SocketIO`, `OpenCV`, `TensorFlow/Keras`, `Pickle5`, `WebSocket`

# 5. Circuit Diagram
Berikut adalah penjelasan mengenai rangkaian yang ditunjukkan pada gambar antara Arduino UNO dan ESP32-CAM:
![Circuit Diagram]("/sketch_arduino/Untitled-Sketch_bb.png")
