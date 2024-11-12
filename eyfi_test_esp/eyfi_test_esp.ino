#include <LiquidCrystal_I2C.h>
#include <LiquidCrystal.h>
#include <Wire.h>
#include <WiFi.h>



// WiFi credentials
char* ssid = "OnePlus Nord";                    //Enter your wifi hotspot ssid
const char* password =  "Taehyung";               //Enter your wifi hotspot password
const uint16_t port = 8002;
const char * host = "192.168.240.200";                   //Enter the ip address of your laptop after connecting it to wifi hotspot



char incomingPacket[80];
WiFiClient client;

String msg = "0%\n";
String holdMsg = "0";

LiquidCrystal_I2C lcd(0x27,16,2);



void setup(){
  Wire.begin();
  Serial.begin(115200);                          //Serial to print data on Serial Monitor 
  
  //Connecting to wifi
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
   lcd.init();
  lcd.clear();         
  lcd.backlight();      // Make sure backlight is on
  
  // Print a message on both lines of the LCD.
  lcd.setCursor(3,0);   //Set cursor to character 2 on line 0
  lcd.print("Automated");
  
  lcd.setCursor(2,1);   //Move cursor to character 2 on line 1
  lcd.print("Billing Cart");

  delay(600);
  lcd.clear();
}


void loop() {

  if (!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    delay(200);
    return;
  }
  while (true){
      msg = client.readStringUntil('\n');         //Read the message through the socket until new line char(\n)
      
      client.print("Hello from ESP32!");          //Send an acknowledgement to host(laptop)
       if(msg!=""){
         if(holdMsg!=msg){
            lcd.clear();
            holdMsg = msg;
         } 
       }
      Serial.println("Total: " + holdMsg); 
      lcd.setCursor(1,0);
      lcd.print("Generated Bill");
      lcd.setCursor(2, 1);
      lcd.print("Total:" + holdMsg);
    }
}
