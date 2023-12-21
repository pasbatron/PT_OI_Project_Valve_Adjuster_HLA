import cv2
import imutils
from imutils.video import VideoStream
from ultralytics import YOLO
import time
import mysql.connector
import serial
import os

rtsp_url = "rtsp://admin:pt_otics1*@192.168.1.108"
model = YOLO("D:\\on\Project_PT_Otics_Image_Processing_HLA\\best_161223_ym_50.pt")
ser_arduino = serial.Serial(
    port='COM3',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="tps"
)
cursor = db.cursor()
condition_1 = 1

def main():
    vidio_streaming = VideoStream(rtsp_url).start()
    while True:
        frame = vidio_streaming.read()
        results = model.predict(frame, conf=0.6)
        result = results[0]
        sum_hla = 0
        for box in result.boxes:
            class_id = result.names[box.cls[0].item()]
            if class_id == "hla":
                sum_hla += 1
        if(sum_hla == 192):
            ser_arduino.write(b"*oke_andon,192,Unit-Full-#")
            time.sleep(1)
            sql = "INSERT INTO table_adjuster_valve_hla (name_line, name_part, quantity, delay, status, andon) VALUES (%s, %s, %s, %s, %s, %s)"
            val = ("Packing_HLA", "Adjuster Valve HLA", str(sum_hla), "-", "1", "oke_andon")
            cursor.execute(sql, val)
            db.commit()
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            folder_name = f"{sub_directory}_{timestamp}"
            path = os.path.join(parent_directory, folder_name)
            try:
                os.mkdir(path)
            except FileExistsError:
                print(f"Directory '{folder_name}' already exists")
            frame = cv2.resize(frame, (750, 500))
            file_name = f"D:\on\Project_PT_Otics_Image_Processing_HLA\Hasil_Deteksi\{folder_name}\HLA_{timestamp}.png"
            cv2.imwrite(file_name, frame)          
            print("Gambar berhasil disimpan:", file_name)
        else:
            ser_arduino.write(b"*ng_andon,-192,Unit-Full-#")
            sql = "UPDATE table_adjuster_valve_hla_update SET name_line=%s, name_part=%s, quantity=%s, delay=%s, status=%s, andon=%s WHERE name_line=%s"
            val = ("Packing_HLA", "Adjuster_Valve", str(sum_hla), "-", "0", "ng_andon", "Packing_HLA")
            cursor.execute(sql, val)
            db.commit()
            time.sleep(1)
        cv2.imshow('Deteksi HLA', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    vidio_streaming.stop()


if __name__ == "__main__":
    parent_directory = r"D:\on\Project_PT_OTICS_Image_Processing_HLA\Hasil_Deteksi"
    sub_directory = "Hasil_Deteksi"
    main()