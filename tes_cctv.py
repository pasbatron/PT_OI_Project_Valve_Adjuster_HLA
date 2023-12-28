import cv2
from imutils.video import VideoStream
import os

rtsp_url = "rtsp://admin:pt_otics1*@192.168.1.108"

def main():
    vidio_streaming = VideoStream(rtsp_url).start()
    while True:
        frame = vidio_streaming.read()
        cv2.imshow('Deteksi HLA', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    vidio_streaming.stop()


if __name__ == "__main__":
    parent_directory = r"/home/wanda/Documents/on/PT_Otics_Indonesia/Project_Kamera_Part_HLA/Project_PT.Otics_Indonesia_Kamera_HLA/runs/hasil"
    sub_directory = "Hasil_Deteksi"
    main()


    
