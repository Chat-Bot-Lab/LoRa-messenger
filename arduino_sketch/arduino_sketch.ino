#include <SoftwareSerial.h>

SoftwareSerial ebyteSerial(10, 11); // RX, TX


String input;
String output;

void setup()
{
  Serial.begin(9600);
  ebyteSerial.begin(9600);
  Serial.println("Приемопередатчик готов");
  Serial.setTimeout(50);
  ebyteSerial.setTimeout(50);

  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);

  digitalWrite(8, LOW);
  digitalWrite(9, LOW);
}

void loop()
{
  if (ebyteSerial.available()) {
      input = ebyteSerial.readString();
      Serial.print("Получено:        ");
      Serial.print(input);
    }
    if (Serial.available()) {
      output = Serial.readString();
      Serial.print("Отправлено: ");
      Serial.print(output);
      ebyteSerial.print(output.c_str());
    }
}
