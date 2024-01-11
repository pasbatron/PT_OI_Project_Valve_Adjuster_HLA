
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

int x; 
const int pinLed = 5;
SoftwareSerial mySerial(10, 11); //TX, RX
SoftwareSerial mySoftwareSerial(3, 2);
DFRobotDFPlayerMini myDFPlayer;

void setup() { 
	Serial.begin(115200); 
  mySoftwareSerial.begin(9600);
  mySerial.begin(9600);


	Serial.setTimeout(1); 
  myDFPlayer.begin(mySoftwareSerial);
  myDFPlayer.volume(60);
  pinMode(pinLed, OUTPUT);
} 
void loop() { 
	while (!Serial.available()); 
	x = Serial.readString().toInt();


  if(x == 1){
    digitalWrite(pinLed, HIGH);  myDFPlayer.play(1);
    myDFPlayer.read();
    delay(3000);
    digitalWrite(pinLed, LOW);
  }else {
    digitalWrite(pinLed, LOW);
  }


  if(Serial.available() > 0){
    String input = Serial.readString();
    mySerial.println(input);    
  }
 
  if(mySerial.available() > 1){
    String input = mySerial.readString();
    Serial.println(input);    
  }
  delay(1000);

} 
