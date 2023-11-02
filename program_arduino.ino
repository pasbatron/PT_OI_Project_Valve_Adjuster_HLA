#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

SoftwareSerial mySerialLora(10, 11); //TX, RX
SoftwareSerial mySoftwareSerial(3, 2); //TX, RX

DFRobotDFPlayerMini myDFPlayer;
String dataIn;
String dt[10];
int i;
boolean parsing=false;
const int pinLed = 13;

// Core Function Start_________:
// Core Parsing Start_________:
void parsingData(){
  int j=0;
  Serial.print("data masuk : ");
  Serial.print(dataIn);
  Serial.println();
  dt[j]="";
  for(i=1;i<dataIn.length();i++){
    if((dataIn[i] == '#') || (dataIn[i] == ',')){
      j++;
      dt[j]="";
    }else{
      dt[j] = dt[j] + dataIn[i];
    }
  }
  Serial.print("data 1 : ");
  Serial.print(dt[0]);
  Serial.println();
  Serial.print("data 2 : ");
  Serial.print(dt[1]);
  Serial.println();
  Serial.print("data 3 : ");
  Serial.print(dt[2]);
  Serial.println();
  Serial.print("data 4 : ");
  Serial.print(dt[3]);
  Serial.println();
  Serial.print("data 5 : ");
  Serial.print(dt[4]);
  Serial.println();Serial.println();

  // akuisisi data
  if(dt[0] == "oke_andon"){
    digitalWrite(pinLed, HIGH);
    myDFPlayer.read();
    myDFPlayer.play(2);
  }if(dt[0] == "ng_andon"){
    digitalWrite(pinLed, LOW);
    myDFPlayer.read();
    myDFPlayer.play(1);
  }

}
// Core Parsing End_________:



// Core Function End_________:
void setup() { 
// ____________:
  Serial.begin(9600);
  mySoftwareSerial.begin(9600);
  mySerialLora.begin(9600);
// ____________:
  myDFPlayer.begin(mySoftwareSerial);
  myDFPlayer.volume(60);
// ____________:
  dataIn="";
  pinMode(pinLed, OUTPUT);
}

void loop() {
// Core Lora Start_________:
  if(Serial.available() > 0){
    String input = Serial.readString();
    dataIn = input;
    mySerialLora.println(input); 
    parsingData();
    dataIn="";  
  }if(mySerialLora.available() > 1){
    String input = mySerialLora.readString();
    Serial.println(input); 
    dataIn = input;
    Serial.println(input); 
    parsingData();
    dataIn="";   
  }
// Core Lora End_________:

  delay(2500);
}


// Sample data
// *sensor,1,23,345,5678#
