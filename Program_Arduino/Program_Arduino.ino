#include <Arduino.h>
#include "RTClib.h"
#include <SPI.h>
#include <Adafruit_I2CDevice.h>
#include <DFRobotDFPlayerMini.h>
#include <SoftwareSerial.h>
#include <BH1750.h>

int x;
float lux;
const byte rxPinDfplayer = 2;
const byte txPinDfplayer = 3;
const byte txPinLora = 10;
const byte rxPinLora = 11;
const int pinLedKuning = 4;
const int pinLedMerah = 12;
const int pinLedBiru = 9;
const int pinLedHijau = 13;
const int pinButton = 7;
int statusButton = 0;

SoftwareSerial lora(txPinLora, rxPinLora);
SoftwareSerial dfplayer(rxPinDfplayer, txPinDfplayer);
DFRobotDFPlayerMini myDFPlayer;
RTC_DS3231 rtc;
BH1750 lightMeter(0x23);
char daysOfTheWeek[7][12] = {"Ahad", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"};

void setup()
{

  Serial.begin(9600);
  Wire.begin();
  dfplayer.begin(9600);
  lora.begin(9600);
  Serial.setTimeout(1);
  myDFPlayer.begin(dfplayer);
  lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE);
  if (!rtc.begin())
  {
    Serial.flush();
    while (1)
      delay(10);
  }
  if (rtc.lostPower())
  {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  pinMode(rxPinDfplayer, INPUT);
  pinMode(txPinDfplayer, OUTPUT);
  pinMode(pinLedKuning, OUTPUT);
  pinMode(pinLedMerah, OUTPUT);
  pinMode(pinLedHijau, OUTPUT);
  pinMode(pinLedBiru, OUTPUT);
  pinMode(pinButton, INPUT_PULLUP);
  digitalWrite(pinLedKuning, HIGH);
  digitalWrite(pinLedMerah, HIGH);
  digitalWrite(pinLedHijau, HIGH);
  digitalWrite(pinLedBiru, HIGH);
  delay(1000);
}

void loop()
{

  digitalWrite(pinLedKuning, LOW);
  digitalWrite(pinLedHijau, HIGH);
  x = Serial.readString().toInt();
  if (x == 1)
  {
    myDFPlayer.play(2);
    myDFPlayer.read();
    digitalWrite(pinLedHijau, LOW);
    digitalWrite(pinLedKuning, HIGH);
    lora.println("Data Dari Kamera, OKE,");
    delay(2000);
  }
  if (x == 2)
  {
    myDFPlayer.play(0);
    myDFPlayer.read();
    digitalWrite(pinLedMerah, LOW);
    digitalWrite(pinLedKuning, HIGH);
    delay(2000);
    digitalWrite(pinLedMerah, HIGH);
  }

  if (lightMeter.measurementReady())
  {
    lux = lightMeter.readLightLevel();
  }

  statusButton = digitalRead(pinButton);
  if (statusButton == LOW)
  {
    DateTime now = rtc.now();
    // 0
    Serial.print("on_time");
    Serial.print(";");
    Serial.print(now.year(), DEC);
    Serial.print('_');
    Serial.print(now.month(), DEC);
    Serial.print('_');
    Serial.print(now.day(), DEC);
    // 1
    Serial.print(";");
    Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
    // 2
    Serial.print(";");
    Serial.print(now.hour(), DEC);
    Serial.print('_');
    Serial.print(now.minute(), DEC);
    Serial.print('_');
    Serial.print(now.second(), DEC);
    // 3
    Serial.print(";");
    Serial.print(rtc.getTemperature());
    // 4
    Serial.print(";");
    Serial.print("ON_BUTTON");
    // 5
    Serial.print(";");
    Serial.print(String(lux));
    // 6
    Serial.print(";");
    Serial.println();
    delay(300);
  }

  else if (statusButton == HIGH)
  {

    DateTime now = rtc.now();
    // 0
    Serial.print("on_time");
    Serial.print(";");
    Serial.print(now.year(), DEC);
    Serial.print('_');
    Serial.print(now.month(), DEC);
    Serial.print('_');
    Serial.print(now.day(), DEC);
    // 1
    Serial.print(";");
    Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
    // 2
    Serial.print(";");
    Serial.print(now.hour(), DEC);
    Serial.print('_');
    Serial.print(now.minute(), DEC);
    Serial.print('_');
    Serial.print(now.second(), DEC);
    // 3
    Serial.print(";");
    Serial.print(rtc.getTemperature());
    // 4
    Serial.print(";");
    Serial.print("OFF_BUTTON");
    // 5
    Serial.print(";");
    Serial.print(String(lux));
    // 6
    Serial.print(";");
    Serial.println();
    delay(300);
  }
}

