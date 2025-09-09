#include <WiFi.h>
#include <Arduino.h>
#include <HTTPClient.h>
#include <iostream>

#include <cstdlib>
#include "dotenv.h"
 const char *url = "http://192.168.1.132:8000/test";
void setup()
{
  const char *ssid = std::getenv("SSID");
  const char *pass = std::getenv("PASSWORD");
 

  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
}

void loop()
{
  if (WiFi.status() == WL_CONNECTED)
  {
    HTTPClient http;
    http.begin(url);
    int code = http.GET();
    if (code == 200)
    {
      String payload = http.getString();
      Serial.println("Got: " + payload);
    }
    else
    {
      Serial.printf("GET failed: %d\n", code);
    }
    http.end();
  }
  delay(5000);
}
