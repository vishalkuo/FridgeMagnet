#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup(){
  lcd.begin(16, 2);
   Serial.begin(9600); 
}

void loop() {
  if (Serial.available()) {
    lcd.print(Serial.readString());
    Serial.println(1);
  }
  delay(1000);
}
