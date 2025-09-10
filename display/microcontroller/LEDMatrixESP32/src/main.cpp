#include <WiFi.h>
#include <Arduino.h>
#include <HTTPClient.h>
#define LED_PIN 2
#include <LiquidCrystal_I2C.h>


LiquidCrystal_I2C lcd(0x27, 16, 2);
 const char *url = "http://192.168.1.132:8000/test";

void setup()
{
  loadDotEnv();
  const char *ssid = std::getenv("SSID");
  const char *pass = std::getenv("PASSWORD");
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  
  
  
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");

  pinMode(LED_PIN, OUTPUT);
}

void loop()
{
  lcd.setCursor(0,0);
  digitalWrite(LED_PIN, HIGH);
  delay(500);                  
  digitalWrite(LED_PIN, LOW);  
  delay(500);                  

  if (WiFi.status() == WL_CONNECTED)
  {
    HTTPClient http;
    http.begin(url);
    int code = http.GET();
    if (code == 200)
    {
      String payload = http.getString();
      Serial.println("Got: " + payload);
      lcd.print(payload);
      //Test 2nd Row
      lcd.setCursor(0,1);
      lcd.print("N-Train  05 mins");
      
    }
    else
    {
      Serial.printf("GET failed: %d\n", code);
    }
    http.end();
  }
  delay(1000);
}