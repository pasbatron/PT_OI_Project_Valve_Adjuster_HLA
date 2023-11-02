from ultralytics import YOLO
import serial
import time
import cv2
import os
from subprocess import call

ser_lora = serial.Serial(
    port='COM3',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)

statement = 2

while statement > 0:
    print("Program Running!!!")
    model = YOLO("D:\\on\Project_PT_Otics_Image_Processing_HLA\\Version 1.1\\best.pt")
    results = model.predict(task="detect", mode="predict", conf=0.8, source="D:\\on\Project_PT_Otics_Image_Processing_HLA\\Version 1.1\\3.jpg", hide_labels=False, save=True)
    for r in results:
        print(r.boxes.shape[0])
        print(type(r.boxes.shape[0]))
        condition = r.boxes.shape[0]
        if(condition == 192):
            ser_lora.write(b"*oke_andon,12,12")
            time.sleep(0.5)
        else:
            ser_lora.write(b"*ng_andon,12,12")
            time.sleep(0.5)
    statement = statement - 1


# on_good,12,12,12,12,12,12,12,12,12,12











'''
import cv2
import os
import time

def capture_image():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Kamera tidak dapat diakses.")
        return
    condition = 1
    while condition < 2:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame.")
            break
        frame = cv2.resize(frame, (1920, 1080))
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"D:\on\Project_PT_Otics_Image_Processing_HLA\Version 1.1\data_trial\images\Adjustercaptured_image_{timestamp}.png"
        cv2.imwrite(file_name, frame)
        print("Gambar berhasil disimpan:", file_name)
        condition += 1
    cap.release()

if __name__ == "__main__":
    capture_image()

'''