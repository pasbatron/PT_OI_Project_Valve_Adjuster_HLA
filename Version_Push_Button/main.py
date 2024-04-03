import cv2
from ultralytics import YOLO
from imutils.video import VideoStream
import serial
import sparepart
import subprocess

def main():
    ser_arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600) 
    model = YOLO('/home/otics/on/core_engine/best_31_03_2024_150_ym.pt')
    rtsp_url = "rtsp://admin:pt_otics1*@192.168.1.108"
    vidio_streaming = VideoStream(rtsp_url).start()
    previous_input = None
    sum_hla = 0
    data_time = '0'
    data_date = '0'
    suhu = '0'
    hla_terlentang = '0'
    hla_terbalik = '0'
    tray = '0'
    print("Tunggu Proses...")
    while True:
        try:
            frame = vidio_streaming.read()
            results = model(frame, conf=0.5)
            annotated_frame = results[0].plot(line_width=1, labels=True, conf=False)
            result = results[0]
            output_serial = ser_arduino.readline()
            get_source_serial = output_serial.decode().strip()
            get_serial = get_source_serial.split(';')
            print(get_serial)
		
            if(get_serial[0] == "on_time"):
                data_time = get_serial[3]
                get_date = get_serial[1].split('_')
                data_date_day = int(get_date[2]) + 4
                data_date = get_date[0] + '_' + get_date[1] + '_' + str(data_date_day)
                suhu = get_serial[4]
                lux = get_serial[6]

            hla_terlentang = '0'
            hla_terbalik = '0'
            tray = '0'
            input_hla = 0
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                if class_id == "hla":
                    input_hla += 1
                if class_id == "p_tray_ng":
                    tray = 'ng'
                if class_id == "hla_terlentang":
                    hla_terlentang = 'ng'
                if class_id == "hla_terbalik":
                    hla_terbalik = 'ng'
                if class_id == "indikator_off":
                    subprocess.Popen(["python", "/home/otics/on/core_engine/shutdown.py"])
                    exit()
            if input_hla == 0:
                previous_input = None
            else:
                if previous_input is None or input_hla > previous_input:
                    sum_hla += 1
                    previous_input = input_hla

            if(get_serial[5] == "ON_BUTTON"):
                if(tray == 'ng'):
                    ser_arduino.write(b"2")
                    sparepart.save_image_ng(annotated_frame, data_time, data_date)
                    input_hla = 0
                if(hla_terlentang == 'ng'):
                    ser_arduino.write(b"2")
                    sparepart.save_image_ng(annotated_frame, data_time, data_date)
                    input_hla = 0
                if(hla_terbalik == 'ng'):
                    ser_arduino.write(b"2")
                    sparepart.save_image_ng(annotated_frame, data_time, data_date)
                    input_hla = 0
                if(input_hla < 192):
                    ser_arduino.write(b"2")
                    sparepart.save_image_ng(annotated_frame, data_time, data_date)
                    input_hla = 0
                if(input_hla > 192):
                    ser_arduino.write(b"2")
                    sparepart.save_image_ng(annotated_frame, data_time, data_date)
                    input_hla = 0
                if(input_hla == 192):
                    ser_arduino.write(b"1")
                    sparepart.save_image_oke(annotated_frame, data_time, data_date)

            # text_date_time ="Date Time :" + str(data_date)
            # text_position = (30, 20)
            # text_font_scale = 0.7
            # text_font_thickness = 1
            # box_size = (50, 50)
            # sparepart.put_text_on_frame(annotated_frame, text_date_time, text_position, text_font_scale, text_font_thickness, box_size)

            text_hla ="Unit :" + str(input_hla) + " Pcs"
            text_position = (30, 20)
            text_font_scale = 0.7
            text_font_thickness = 1
            box_size = (50, 50)
            sparepart.put_text_on_frame(annotated_frame, text_hla, text_position, text_font_scale, text_font_thickness, box_size)

            text_suhu ="Suhu :" + str(suhu) + " Derajat"
            text_position = (1650, 20)
            text_font_scale = 0.7
            text_font_thickness = 1
            box_size = (50, 50)
            sparepart.put_text_on_frame(annotated_frame, text_suhu, text_position, text_font_scale, text_font_thickness, box_size)

            text_lux ="Cahaya :" + str(lux) + " Lux"
            text_position = (1650, 65)
            text_font_scale = 0.7
            text_font_thickness = 1
            box_size = (50, 50)
            sparepart.put_text_on_frame(annotated_frame, text_lux, text_position, text_font_scale, text_font_thickness, box_size)

            resize_frame = cv2.resize(annotated_frame, (1280, 720))           
            cv2.imshow("Hasil Deteksi Part HLA", resize_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break       
        except ValueError:
            print("Ada Error, Hubungi Member TPS.")
if __name__ == "__main__":
    main()



