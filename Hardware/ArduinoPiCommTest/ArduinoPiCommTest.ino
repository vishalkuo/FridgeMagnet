int led = 13;

void setup(){
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  Serial.flush();
}

void loop(){
  if (Serial.available()){
    dispSerial(Serial.read() - '0'); 
    Serial.println(1);
  }
  delay(1000);
}

void dispSerial(int count){
  for (int i = 0; i < count; i++){
    digitalWrite(led, HIGH);
    delay(300);
    digitalWrite(led, LOW);
    delay(300);
  }
}
