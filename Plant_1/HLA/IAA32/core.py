import cv2
from imutils.video import VideoStream
import time
from ultralytics import YOLO
import os
from datetime import datetime
import serial  # Import pyserial

# Initialize serial communication
serial_port = '/dev/ttyUSB0'  # Change this to your serial port
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

model = YOLO("best.pt")
rtsp_base_url = "rtsp://admin:pt_otics1*@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0"
common_paths = ["/cam/realmonitor?channel=1&subtype=0"]
class_names = ['hla', 'off', 'altar', 'box_after']
media_folder = "media"

if not os.path.exists(media_folder):
    os.makedirs(media_folder)

def test_stream(path):
    rtsp_url = rtsp_base_url + path
    vs = VideoStream(rtsp_url).start()
    time.sleep(2.0)
    frame = vs.read()
    vs.stop()
    return frame is not None

for path in common_paths:
    if test_stream(path):
        print(f"[INFO] stream path found: {path}")
        rtsp_url = rtsp_base_url + path
        break
else:
    print("[ERROR] no valid stream path found")
    exit()

print("[INFO] starting video stream...")
camera_stream = VideoStream(rtsp_url).start()
time.sleep(2.0)

def capture_image(frame):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_save_path = os.path.join(media_folder, f"hla_capture_{current_time}.jpg")
    print(f"[INFO] Capturing image: {image_save_path}")
    cv2.imwrite(image_save_path, frame)
    print(f"[INFO] Image saved to {image_save_path}")

capture_history = []
last_capture_time = 0
capture_cooldown = 10

while True:
    time.sleep(0.1)
    frame = camera_stream.read()
    if frame is None:
        break
    else:
        try:
            results = model(frame, conf=0.65)
        except Exception as e:
            print(f"[ERROR] Error during model inference: {e}")
            continue
        
        detected_objects = results[0].boxes.data.cpu().numpy()
        hla_count = 0
        for obj in detected_objects:
            class_id = int(obj[5])
            if class_id < len(class_names):
                class_name = class_names[class_id]
                if class_name == 'hla':
                    hla_count += 1
            else:
                print(f"[WARNING] Detected class_id {class_id} out of bounds for class_names")

        print(f"Number of 'hla' objects detected: {hla_count}")
        
        # Check for serial input
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').strip()
            if command == "ON":
                print("[INFO] Judgment triggered.")
                # Check HLA count and send appropriate value via serial
                if hla_count == 88:
                    ser.write(b'8')  # Send string "8"
                    capture_image(frame)  # Optionally capture image
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    capture_history.append((timestamp, hla_count))
                    if len(capture_history) > 30:
                        capture_history.pop(0)
                else:
                    ser.write(b'1')  # Send string "1"
        
        current_time = time.time()
        if (current_time - last_capture_time) >= capture_cooldown:
            if hla_count == 88:
                capture_image(frame)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                capture_history.append((timestamp, hla_count))
                if len(capture_history) > 30:
                    capture_history.pop(0)
            last_capture_time = current_time
            
        annotated_frame = results[0].plot(line_width=1, labels=True, conf=True)
        sidebar_width = 500
        sidebar_color = (142, 112, 0)
        cv2.rectangle(annotated_frame, (0, 0), (sidebar_width, annotated_frame.shape[0]), sidebar_color, -1)
        red_bg_color = (0, 0, 255)
        cv2.rectangle(annotated_frame, (20, 30), (sidebar_width - 20, 100), red_bg_color, -1)
        white_text_color = (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(annotated_frame, f"HLA Count: {hla_count}", (30, 80), font, 1.5, white_text_color, 5)
        history_start_y = 150
        for idx, (timestamp, count) in enumerate(capture_history):
            history_text = f"{idx + 1}: {timestamp} | HLA: {count}"
            cv2.putText(annotated_frame, history_text, (30, history_start_y + (idx * 30)), font, 0.7, white_text_color, 2)
        frame_color = (184, 132, 0)
        frame_thickness = 20
        cv2.rectangle(annotated_frame, (0, 0), (annotated_frame.shape[1] - 1, annotated_frame.shape[0] - 1), frame_color, frame_thickness)
        resized_frame = cv2.resize(annotated_frame, (1395, 770))
        cv2.imshow("Deteksi Part HLA", resized_frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

camera_stream.stop()
cv2.destroyAllWindows()
ser.close()  # Close the serial port when done
