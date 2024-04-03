from ultralytics import YOLO
from ultralytics.solutions import object_counter
import cv2
import time
import subprocess
from imutils.video import VideoStream
import serial
import sqlite3

conn = sqlite3.connect('/home/otics/on/project_pt_otics_ai_hla/core_engine/hla.db')
connection_sqlite = conn.cursor()
model = YOLO('/home/otics/on/project_pt_otics_ai_hla/core_engine/best_pokayoke.pt')
rtsp_url = "rtsp://admin:pt_otics1*@192.168.1.108"
vidio_streaming = VideoStream(rtsp_url).start()
counter = object_counter.ObjectCounter()
ser_arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600) 
def mastering_pokayoke_oke_step_1():
    region_points = [(845, 740), (890, 740), (890, 695), (845, 695)]
    counter.set_args(view_img=False,
                    reg_pts=region_points,
                    classes_names=model.names,  
                    draw_tracks=True,
                    view_in_counts=False,
                    view_out_counts=False)    
def mastering_pokayoke_oke_step_2():
    region_points = [(1270, 740), (1325, 740), (1325, 680), (1270, 680)]
    counter.set_args(view_img=False,
                    reg_pts=region_points,
                    classes_names=model.names,
                    draw_tracks=True,
                    view_in_counts=False,
                    view_out_counts=False)
def mastering_pokayoke_oke_step_3():
    region_points = [(1265, 150), (1320, 150), (1320, 100), (1265, 100)]
    counter.set_args(view_img=False,
                    reg_pts=region_points,
                    classes_names=model.names,
                    draw_tracks=True,
                    view_in_counts=False,
                    view_out_counts=False)   
def mastering_pokayoke_oke_step_4():
    region_points = [(825, 145), (880, 145), (880, 100), (825, 100)]
    counter.set_args(view_img=False,
                    reg_pts=region_points,
                    classes_names=model.names,
                    draw_tracks=True,
                    view_in_counts=False,
                    view_out_counts=False)

    
def mastering_pokayoke_ng_step_1():
    region_points = [(750, 765), (830, 765), (830, 625), (740, 625)]
    counter.set_args(view_img=False,
                    reg_pts=region_points,
                    classes_names=model.names,
                    draw_tracks=True,
                    view_in_counts=False,
                    view_out_counts=False)
def mastering_pokayoke_ng_step_2():
    region_points = [(1315, 755), (1400, 755), (1400, 615), (1325, 615)]
    counter.set_args(view_img=False,
                    reg_pts=region_points,
                    classes_names=model.names,
                    draw_tracks=True,
                    view_in_counts=False,
                    view_out_counts=False)
def mastering_pokayoke_ng_step_3():
    region_points = [(1325, 225), (1395, 225), (1395, 85), (1315, 85)]
    counter.set_args(view_img=False,
                    reg_pts=region_points,
                    classes_names=model.names,
                    draw_tracks=True,
                    view_in_counts=False,
                    view_out_counts=False)
def mastering_pokayoke_ng_step_4():
    region_points = [(735, 215), (825, 215), (825, 120), (735, 120)]
    counter.set_args(view_img=False,
                    reg_pts=region_points,
                    classes_names=model.names,
                    draw_tracks=True,
                    view_in_counts=False,
                    view_out_counts=False)
    
    
mastering_pokayoke_oke_step_1()
condition_input = 0

while True:
    time.sleep(0.1)
    ser_arduino.write(b"50")
    im0 = vidio_streaming.read()
    tracks = model.track(im0, persist=True, show=False, classes=0)
    frame_tracks = counter.start_counting(im0, tracks)
    output_serial = ser_arduino.readline()
    get_source_datetime = output_serial.decode().strip()
    get_datetime = get_source_datetime.split(';')
    if(get_datetime[0] == "on_time"):
        data_date = get_datetime[1]
        data_time = get_datetime[3]
    print(data_date)    

    if (condition_input == 0 and (counter.in_counts == 1 or counter.out_counts == 1)):
            condition_input = condition_input + 1
            counter.in_counts = 0
            counter.out_counts = 0
            mastering_pokayoke_oke_step_2()
    if (condition_input == 1 and (counter.in_counts == 1 or counter.out_counts == 1)):
            condition_input = condition_input + 1
            counter.in_counts = 0
            counter.out_counts = 0
            mastering_pokayoke_oke_step_3()

    if (condition_input == 2 and (counter.in_counts == 1 or counter.out_counts == 1)):
            condition_input = condition_input + 1
            counter.in_counts = 0
            counter.out_counts = 0
            mastering_pokayoke_oke_step_4()
    if (condition_input == 3 and (counter.in_counts == 1 or counter.out_counts == 1)):
            condition_input = condition_input + 1
            counter.in_counts = 0
            counter.out_counts = 0
            mastering_pokayoke_ng_step_1()
    if (condition_input == 4 and (counter.in_counts == 1 or counter.out_counts == 1)):
            condition_input = condition_input + 1
            counter.in_counts = 0
            counter.out_counts = 0
            mastering_pokayoke_ng_step_2()
    if (condition_input == 5 and (counter.in_counts == 1 or counter.out_counts == 1)):
            condition_input = condition_input + 1
            counter.in_counts = 0
            counter.out_counts = 0
            mastering_pokayoke_ng_step_3()
    if (condition_input == 6 and (counter.in_counts == 1 or counter.out_counts == 1)):
            condition_input = condition_input + 1
            counter.in_counts = 0
            counter.out_counts = 0
            mastering_pokayoke_ng_step_4()

    if (condition_input == 7 and (counter.in_counts == 1 or counter.out_counts == 1)):
            condition_input = 0
            counter.in_counts = 0
            counter.out_counts = 0
            pokayoke = "sudah"
            date_pokayoke = data_date
            time_pokayoke = data_time
            connection_sqlite.execute("INSERT INTO data_pokayoke (pokayoke, date, time) VALUES (?,?,?)", (pokayoke, date_pokayoke, time_pokayoke))
            conn.commit()
            ser_arduino.write(b"50")
            vidio_streaming.stop()
            cv2.destroyAllWindows()
            time.sleep(1)
            print("Berhasil, Program Utama Akan Dijalankan...")
            subprocess.run(["python", "/home/otics/on/project_pt_otics_ai_hla/core_engine/main.py"])
            exit() 

    print(condition_input)
    print(counter.out_counts)
    print(counter.in_counts)
    resize = cv2.resize(frame_tracks, (1280, 720), interpolation = cv2.INTER_LINEAR)
    cv2.imshow("Hasil Deteksi HLA", resize)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
