#include <SoftwareSerial.h>
#include <ArduinoJson.h>

SoftwareSerial ebyteSerial(10, 11); // RX, TX


String input;
String output;
StaticJsonDocument<1000> jsonDoc;
String jsonString;
int Number = 1984;

void setup()
{
  Serial.begin(9600);
  ebyteSerial.begin(9600);
  Serial.print("Aбонент ");
  Serial.println(Number);
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
      Serial.print(input);
    }
    if (Serial.available()) {
      output = Serial.readString();
      jsonDoc["username"] = Number;
      jsonDoc["message"] = output;

      serializeJson(jsonDoc,Serial);
      serializeJson(jsonDoc,ebyteSerial);
      Serial.println();
      ebyteSerial.println();
    }
}
