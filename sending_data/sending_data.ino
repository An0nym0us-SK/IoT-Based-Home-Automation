#include <SoftwareSerial.h>
#include <stdlib.h>
int val;
String rf;
float temp;


// replace with your channel's thingspeak API key
String apiKey = "92BMS4S4C29XRS3I";

SoftwareSerial ser(2,3); // RX, TX connect pin10 to TX of ESP, pin11 to RX of ESP
SoftwareSerial rfid(4,5);// RX, TX for rfid 

void setup() { 
    Serial.begin(9600); 
    pinMode(A3,INPUT);
}

void loop() {


 temp=analogRead(A3);
  temp=(temp*500)/1024;

  char buf[16];
  String str=dtostrf(temp,4,1,buf);
  //Serial.println(temp);

  delay(500);
 
  val=10;
  rf="";
  
  rfid.begin(9600);
  while(rfid.available()<=0);
  
  Serial.println("Card Scaned Successfully !");
  delay(1000);
  
  while(rfid.available())
  {
    
      rf+=String(rfid.read());
      if(--val ==0)
      {
        break;
      }
    
  }
  
  rfid.end();
  delay(500);
  
  Serial.println(rf);
  delay(500);
  
  


  if(rf=="48485353505154481310")
  {
    rf="007";
    Serial.print("himanshu");
  }
  else if(rf=="48515150494856511310")
  {
    rf="009";
    Serial.print("sourabh");
  }
  else
  {
    rf="001";
    Serial.print("invalid");
  }


  if(rf=="007"||rf=="009")
  {
    ser.begin(9600);
    delay(1000);
  // TCP connection for rfid
  String cmd = "AT+CIPSTART=\"TCP\",\"";
  cmd += "184.106.153.149"; // api.thingspeak.com
  cmd += "\",80";
  ser.println(cmd);
   
  if(ser.find("Error")){
    Serial.println("AT+CIPSTAR T error");
    return;
  }
  
  // prepare GET string for rfid

  String getStr = "GET /update?api_key=";
  getStr += apiKey;
  getStr +="&field4="+rf;
  getStr +="&field2="+String(str);
  getStr += "\r\n\r\n";

  // send data length
  cmd = "AT+CIPSEND=";
  cmd += String(getStr.length());
  ser.println(cmd);

  if(ser.find(">")){
    ser.print(getStr);
    Serial.println("Card number and temp value is sended");
    
  }
  
  else{
    
    ser.println("AT+CIPCLOSE") ;
    // alert user
   // Serial.println("AT+CIPCLOS E");
  }
  ser.end();
  delay(1000);
  
}

  else
  {
    ser.begin(9600);
    // TCP connection for rfid
  String cmd = "AT+CIPSTART=\"TCP\",\"";
  cmd += "184.106.153.149"; // api.thingspeak.com
  cmd += "\",80";
  ser.println(cmd);
   
  if(ser.find("Error")){
    Serial.println("AT+CIPSTAR T error");
    return;
  }
  
  // prepare GET string for rfid

  String getStr = "GET /update?api_key=";
  getStr += apiKey;
  getStr +="&field4="+rf;
  //getStr +="&field1="+String(str);
  getStr += "\r\n\r\n";

  // send data length
  cmd = "AT+CIPSEND=";
  cmd += String(getStr.length());
  ser.println(cmd);

  if(ser.find(">")){
    ser.print(getStr);
    Serial.println("Card number and temp value is sended");
    
  }
  else{
    
    ser.println("AT+CIPCLOSE") ;
    // alert user
   // Serial.println("AT+CIPCLOS E");
  }
  ser.end();
  }

  

 
  // Thingspeak needs 15 sec delay between updates .
  // So After successful update led on Arduino board should blink twice
}


