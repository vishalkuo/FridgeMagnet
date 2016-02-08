#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

String input = "";
String displayString = "";
int rowPosition = 0;
int colPosition = 0;
int xPos = 0;
int yPos = 0;

void setup() {
  lcd.begin(16, 2);
  lcd.clear();
  Serial.begin(9600);
  Serial.setTimeout(500);
}

void loop() {
  if(Serial.available()){
    input = Serial.readString();
    yPos = input.substring(0, 1).toInt();
    displayString = input.substring(1);
    Serial.println(input);
  } 
  if(displayString.equals("x")){
    lcd.clear();
    displayString = "";
  }
  lcd.setCursor(xPos, yPos);
  lcd.print(displayString);
}
