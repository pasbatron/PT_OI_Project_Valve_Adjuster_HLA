import cv2
from ultralytics import YOLO
from imutils.video import VideoStream
from sqlite3 import Error
from openpyxl.styles import Font
import time

rtsp_url = "rtsp://admin:pt_otics1*@192.168.1.108"
vidio_streaming = VideoStream(rtsp_url).start()
box_position = [50, 50]
box_size = 5
box_color = (0, 255, 0)
movement_speed = 5

def draw_box(frame, position, size, color):
    cv2.rectangle(frame, (position[0], position[1]), (position[0] + size, position[1] + size), color, -1)

def main():
    try:
        while True:
            time.sleep(0.1)
            frame = vidio_streaming.read()
            draw_box(frame, box_position, box_size, box_color)
            frame_sizing = cv2.resize(frame, (1280, 720))
            cv2.imshow("Box Game", frame_sizing)
            key = cv2.waitKey(1)
            if key == ord('w'):
                box_position[1] -= movement_speed
            elif key == ord('s'):
                box_position[1] += movement_speed
            elif key == ord('a'):
                box_position[0] -= movement_speed
            elif key == ord('d'):
                box_position[0] += movement_speed
            elif key == ord('q'):
                break
            print(box_position)
        vidio_streaming.stop()
        cv2.destroyAllWindows()
    except ValueError:
        print("Ada Error..!!!")
if __name__ == "__main__":
    main()
