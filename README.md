# Strawberry Plants Diseases Detection
> "Using Alexnet, DenseNet 121 and ResNet50"

## Project Description
"Proyek ini bertujuan untuk mendeteksi penyakit pada tanaman strawberry menggunakan kamera ESP32-CAM dan mengirimkan data ke aplikasi berbasis web Flask melalui WebSocket."

## Features
* Deteksi penyakit pada tanaman strawberry menggunakan machine learning dengan model Alexnet, ResNet50 dan DenseNet 121.
* Pengambilan tanaman secara realtime menggunakan ESP32-CAM.
* Komunikasi antara ESP32-CAM dan Flask menggunakan Websocket.
* Menampilkan hasil deteksi di aplikasi web.

## Hardware & Software Requirements
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

## Circuit Diagram
Berikut adalah penjelasan mengenai rangkaian yang ditunjukkan pada gambar antara Arduino UNO dan ESP32-CAM:

![Circuit Diagram](/image/Sketch_esp32-cam.png)

## Koneksi Pin
1. GND (Ground)
   * Arduino: Terhubung ke pin GND
   * ESP32-CAM: Terhubung ke pin GND
   * Fungsi: koneksi ground yang merupakan referensi tegangan `0V` untuk kedua perangkat. Menyambungkan kedua perangkat ke ground yang sama penting untuk memastikan ada jalur referensi yang sama.

2. 5V
   * Arduino: Terhubung ke pin 5V.
   * ESP32-CAM: Terhubung ke pin 5V
   * Fungsi: digunakan untuk menyediakan daya ke ESP32-CAM dari Arduino.

3. TX (Transmit)
   * Arduino: Terhubung ke pin `TX`.
   * ESP32-CAM: Terhubung ke pin `U0T` (UART0 TX).
   * Funsi: ini adalah jalur komunikasi serial untuk mengirimkan data dari Arduino ke ESP32-CAM. `TX` pada Arduino mengirimkan data ke `RX` (U0R) pada ESP32-CAM.

4. RX (Receive)
   * Arduino: Terhubung ke pin `RX`.
   * ESP32-CAM: Terhubung ke pin `U0T` (UART0 TX)
   * Fungsi: ini adalah jalur komunikasi serial untuk menerima data dari ESP32-CAM ke Arduino. `TX` pada ESP32-CAM menirimkan data ke `RX` pada Arduino.

5. Reset
   * Pada Arduino terdapat kabel yang terhubung antara pin Reset pada Arduino dan pin `GND` (ground) pada Arduino. Ini berfungsi untuk mengaktifkan reset pada ESP32-CAM.

## Arsitektur Sistem
Berikut adalah arsitektur sistem yang dibuat:

![Arsitektur Sistem](/image/diagram-arsitektur-sistem.png)

Cara kerja sistem, kamera menggunakan ESP32-Cam yang dihubungkan dengan webserver (WebSocket) untuk mengirimkan data kepala Client, sehingga user dapat mengakses kamera menggunakan web untuk mendeteksi hama pada tanaman Strawberi.

## Arsitektur Pembuatan Sistem
Berikut adalah arsitektur pembuatan sistem pengenalan hama pada tanaman strawberi:

![Arsitektur Pembuatan Sistem](/image/diagram-flowchart-model.png)

Pembuatan sistem deteksi hama ini diawali dengan preprocessing yang melibatkan teknik segmentasi menggunakan KNN (K-Nearest Neighbor) dan Augmentasi untuk menghasilkan data yang digunakan dalam training model, proses selanjutnya adalah split data dengan rasio 80% data train dan 20% data test. Setelah itu proses pembuatan model, model yang digunakan pada project ini menggunakan 3 model yaitu Alexnet, Densenet dan Resnet, terakhir evaluasi model menggunakan classification report dan confusion matrix.

### Arsitektur traning model
Berikut adalah arsitektur training model

![Arsitektur Training Model](/image/diagram-flowchart-train-model.png)

Pembuatan model diawali dengan input data yang sudah dikumpulkan, kemudian proses preprocessing menggunakan segementasi dan augmentasi, setelah itu label encoder yang berfungsi untuk mengubah label text menjadi numerik dengan tujuan agar komputer bisa memproses label, setelah itu split data yang sudah dilakukan preprocessing dengan rasio 80% data train dan 20% data test. Selanjutnya membuat model Alexnet, Densenet, dan Resnet. Pada project ini diterapkan KFold untuk untuk mengukur kinerja model dengan lebih akurat. Prosesnya melibatkan membagi dataset menjadi beberapa segmen (fold) yang sama besar, di mana model dilatih dan diuji secara bergantian pada tiap fold, sehingga semua data digunakan baik untuk pelatihan maupun pengujian. Ini membantu dalam meminimalkan overfitting dan memberikan estimasi kinerja model yang lebih robust terhadap data baru.

## Installation and Setup
* Clone Repository: Intruksi untuk meng-clone repository dari GitHub.
```
git clone https://github.com/username/repository-name.git
cd repository-name
```
* Setup Arduino IDE: Langkah-langkah untuk memprogram ESP32-CAM menggunakan Arduino IDE.
  * Instalasi board ESP32 di Arduino IDE.
  * Gunakan board `AI Thinker`.
  * Menyambungkan dan meng-upload program ke ESP32-CAM.

* Setup Flask:
  * Install depencies python
* WebSocket Configuration:
  *Jalankan `stream_image.py`: File ini perlu dijalankan karena ini digunakan untuk mengubungkan flask dan juga ESP32-CAM.
```
python stream_image.py
```

## Usage
* Berikut adalah intruksi menjalankan aplikasi dan alat.
  * Jalankan Aplikasi Flask (jalankan `file app.py` dan `stream_image.py`).
  * Pastikan ada Wifi yang dihubungkan dengan ESP32-CAM.
  * Hubungkan Arduino pada power suply (bisa ke laptop menggunakan USB).
  * Jika terhubung maka aplikasi dapat dijalankan untuk deteksi.
