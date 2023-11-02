from ultralytics import YOLO
import cv2
import serial
import time
from subprocess import call
import os

ser_lora = serial.Serial(
    port='COM3',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1)


model = YOLO("D:\\on\Project_PT_Otics_Image_Processing_HLA\\Version 1.1\\best.pt")
# model.predict(task="detect", mode="predict", conf=0.8, save=True)
video_path = 1
cap = cv2.VideoCapture(video_path)
while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model(frame)
        for r in results:
            print(r.boxes.shape[0])
            print(type(r.boxes.shape[0]))
            condition = r.boxes.shape[0]
            if(condition == 192):
                ser_lora.write(b"*oke_andon,12,12,12,12#")
                time.sleep(0.3)
            else:
                ser_lora.write(b"*ng_andon,12,12,12,12#")
                time.sleep(0.3)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inference", annotated_frame)
        time.sleep(0.4)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()


