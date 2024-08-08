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
![Circuit Diagram](/sketch_arduino/Sketch_esp32-cam.png)

## Koneksi Pin
1. GND (Ground)
   * Arduino: Terhubung ke pin GND
   * ESP32-CAM: Terhubung ke pin GND
   * Fungsi: koneksi ground yang merupakan referensi tegangan 0V untuk kedua perangkat. Menyambungkan kedua perangkat ke ground yang sama penting untuk memastikan ada jalur referensi yang sama.

2. 5V
   * Arduino: Terhubung ke pin 5V.
   * ESP32-CAM: Terhubung ke pin 5V
   * Fungsi: digunakan untuk menyediakan daya ke ESP32-CAM dari Arduino.

3. TX (Transmit)
   * Arduino: Terhubung ke pin TX.
   * ESP32-CAM: Terhubung ke pin U0T (UART0 TX).
   * Funsi: ini adalah jalur komunikasi serial untuk mengirimkan data dari Arduino ke ESP32-CAM. TX pada Arduino mengirimkan data ke RX (U0R) pada ESP32-CAM.

4. RX (Receive)
   * Arduino: Terhubung ke pin RX.
   * ESP32-CAM: Terhubung ke pin U0T (UART0 TX)
   * Fungsi: ini adalah jalur komunikasi serial untuk menerima data dari ESP32-CAM ke Arduino. TX pada ESP32-CAM menirimkan data ke RX pada Arduino.

5. Reset
   * Pada Arduino terdapat kabel yang terhubung antara pin Reset pada Arduino dan pin GND pada Arduino. Ini berfungsi untuk mengaktifkan reset pada ESP32-CAM.

