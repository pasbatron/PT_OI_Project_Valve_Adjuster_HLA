import cv2
from ultralytics import YOLO
from imutils.video import VideoStream
import time
import serial
import os
import sparepart
import sqlite3

def main():
    conn = sqlite3.connect("/home/otics/on/project_pt_otics_ai_hla/core_engine/hla.db")
    ser_arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600) 
    model = YOLO('/home/otics/on/project_pt_otics_ai_hla/core_engine/best_25_01_2024_100_ym.pt')
    rtsp_url = "rtsp://admin:pt_otics1*@192.168.1.108"
    vidio_streaming = VideoStream(rtsp_url).start()
    previous_input = None
    sum_hla = 0
    condition_take_picture = 0
    insert_database = 0
    data_time = ''
    data_date = ''
    date_time = ''
    suhu = ''
    line = 'Packing'
    part = 'HLA'
    total_box= '0'
    cycle_time= '0'
    target= '0'
    actual= '0'
    loading_time= '0'
    name_hikitori= '0'
    capacity_hour= '0'

    print("Running....")
    print("Tunggu Proses")
    while True:
        try:
            time.sleep(0.1)
            frame = vidio_streaming.read()
            results = model(frame)
            annotated_frame = results[0].plot(line_width=1, labels=True, conf=False)
            result = results[0]
            output_serial = ser_arduino.readline()
            get_source_datetime = output_serial.decode().strip()
            get_datetime = get_source_datetime.split(';')           
            
            if(get_datetime[0] == "on_time"):
                data_time = get_datetime[3]
                data_date = get_datetime[1]
                suhu = get_datetime[4]
                date_time = data_date + "--" + data_time

            input_hla = 0
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                if class_id == "hla":
                    input_hla += 1
                if class_id == "p_tray_ng":
                    part = 'p_tray_ng'
                    sparepart.insert_data_ng(line,part,input_hla,total_box,capacity_hour,sum_hla,cycle_time,target,actual,loading_time,name_hikitori,data_date,data_time)
                if class_id == "hla_terlentang":
                    ser_arduino.write(b"2")
                if class_id == "hla_terbalik":
                    ser_arduino.write(b"2")
            if input_hla == 0:
                previous_input = None
            else:
                if previous_input is None or input_hla > previous_input:
                    sum_hla += 1
                    previous_input = input_hla
            name_file_exel = f"/home/otics/on/project_pt_otics_ai_hla/core_engine/runs/laporan_project_hla_{data_date}.xlsx"
            laporan_data = [data_time, 'HLA', input_hla, "-", sum_hla]

            if(input_hla == 192):
                ser_arduino.write(b"1")
                if(condition_take_picture <= 4):
                    save_dir = os.path.join("/home/otics/on/project_pt_otics_ai_hla/core_engine/runs/hasil_deteksi_kamera_hla/", data_date)
                    file_name = os.path.join(save_dir, f"HLA_{date_time}.png")
                    os.makedirs(save_dir, exist_ok=True)
                    cv2.imwrite(file_name, annotated_frame)
                    condition_take_picture = condition_take_picture + 1
                    sparepart.make_report(name_file_exel, laporan_data)
                if(insert_database == 0):
                    sparepart.insert_data_oke(line,part,input_hla,total_box,capacity_hour,sum_hla,cycle_time,target,actual,loading_time,name_hikitori,data_date,data_time)
                    insert_database = insert_database + 1

            if(input_hla > 192):
                if(condition_take_picture <= 4):
                    save_dir = os.path.join("/home/otics/on/project_pt_otics_ai_hla/core_engine/runs/hasil_deteksi_kamera_hla/", data_date)
                    file_name = os.path.join(save_dir, f"HLA_{date_time}.png")
                    os.makedirs(save_dir, exist_ok=True)
                    cv2.imwrite(file_name, annotated_frame)
                    condition_take_picture = condition_take_picture + 1
                    sparepart.make_report(name_file_exel, laporan_data)
                    sparepart.insert_data_oke(line,part,input_hla,total_box,capacity_hour,sum_hla,cycle_time,target,actual,loading_time,name_hikitori,data_date,data_time)
            if(input_hla < 192):
                condition_take_picture = 0 
                insert_database = 0


            # Time : 
            text ="Date Time :" + str(date_time)
            text_position = (30, 20)
            text_font_scale = 0.7
            text_font_thickness = 1
            box_size = (50, 50)
            sparepart.put_text_on_frame(annotated_frame, text, text_position, text_font_scale, text_font_thickness, box_size)

            text ="Unit :" + str(input_hla) + " Pcs"
            text_position = (30, 65)
            text_font_scale = 0.7
            text_font_thickness = 1
            box_size = (50, 50)
            sparepart.put_text_on_frame(annotated_frame, text, text_position, text_font_scale, text_font_thickness, box_size)

            text ="Suhu :" + str(suhu) + " Derajat"
            text_position = (1550, 20)
            text_font_scale = 0.7
            text_font_thickness = 1
            box_size = (50, 50)
            sparepart.put_text_on_frame(annotated_frame, text, text_position, text_font_scale, text_font_thickness, box_size)

            resize_frame = cv2.resize(annotated_frame, (1280, 720))           
            cv2.imshow("Hasil Deteksi Part HLA", resize_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                conn.close()
                break       
        except ValueError:
            print("Ada Error, Hubungi Member TPS.")
            conn.close()
if __name__ == "__main__":
    main()



