import serial
import sqlite3
import subprocess
import time

def main():
    
    conn = sqlite3.connect('/home/otics/on/project_pt_otics_ai_hla/core_engine/hla.db')
    cursor = conn.cursor()
    perintah_sql = "SELECT * FROM data_pokayoke ORDER BY date DESC LIMIT 1"
    cursor.execute(perintah_sql)
    date_sqlite = ''
    data_date = ''
    data_time = ''
    pokayoke = ''
    while True:
        try:
            ser_arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
            output_serial = ser_arduino.readline()
            get_source_datetime = output_serial.decode().strip()
            get_datetime = get_source_datetime.split(';')
            if(get_datetime[0] == "on_time"):
                data_time = get_datetime[3]
                data_date = get_datetime[1]
            print(data_date)
            print(data_time)
            hasil = cursor.fetchall()
            for data in hasil:
                date_sqlite = data[2]
                pokayoke = data[1]
            print(date_sqlite)

            if((date_sqlite == data_date) and (pokayoke == "sudah")):
                time.sleep(1)
                print("Berhasil, Program Utama Akan Dijalankan...")
                subprocess.run(["python", "/home/otics/on/project_pt_otics_ai_hla/core_engine/main.py"])
                time.sleep(1)
                exit()
            if(date_sqlite != data_date):
                time.sleep(1)
                print("Berhasil, Program Pokayoke Akan Dijalankan...")
                time.sleep(1)
                subprocess.run(["python", "/home/otics/on/project_pt_otics_ai_hla/core_engine/pokayoke.py"])
                time.sleep(1)
                exit()
            else:
                print("Hubungi Kang Gilang TPS")
                print("Ada Kesalahan")
        except ValueError:
            cursor.close()
            conn.close()
            print("Hubungi Kang Gilang TPS")
            print("Ada Kesalahan")
if __name__ == "__main__":
    main()
