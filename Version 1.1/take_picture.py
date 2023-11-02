import cv2
import os
import time

def capture_image():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Kamera tidak dapat diakses.")
        return
    kondisi = 1
    while kondisi < 2:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame.")
            break
        frame = cv2.resize(frame, (1920, 1080))
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"D:\on\Project_PT_Otics_Image_Processing_HLA\Version 1.1\data_trial\images\Adjustercaptured_image_{timestamp}.png"
        cv2.imwrite(file_name, frame)
        print("Gambar berhasil disimpan:", file_name)
        kondisi += 1
    cap.release()

if __name__ == "__main__":
    capture_image()
