import cv2
import numpy
import subprocess
import os

# opencv
def put_text_on_frame(frame, text, position, font_scale, font_thickness, box_size):
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
    box_width = text_width + 20
    box_height = text_height + 20
    box = numpy.ones((box_height, box_width, 3), dtype=numpy.uint8) * 255
    cv2.putText(box, text, (10, box_height - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), font_thickness, cv2.LINE_AA)
    x, y = position
    frame[y:y + box_height, x:x + box_width] = box
    cv2.rectangle(frame, (x, y), (x + box_width, y + box_height), (56, 10, 0), 1)

def save_image_ng(annotated_frame, date_time, data_date):
    save_dir = os.path.join("/home/otics/Desktop/HASIL_DETEKSI_KAMERA/NG/", data_date)
    file_name = os.path.join(save_dir, f"HLA_{date_time}.png")
    os.makedirs(save_dir, exist_ok=True)
    cv2.imwrite(file_name, annotated_frame)

def save_image_oke(annotated_frame, date_time, data_date):
    save_dir = os.path.join("/home/otics/Desktop/HASIL_DETEKSI_KAMERA/", data_date)
    file_name = os.path.join(save_dir, f"HLA_{date_time}.png")
    os.makedirs(save_dir, exist_ok=True)
    cv2.imwrite(file_name, annotated_frame)

#os
def shutdown():
        subprocess.run(["shutdown", "/s", "/t", "0"])
        
