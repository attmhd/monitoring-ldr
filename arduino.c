#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>

// Ganti dengan SSID dan Password WiFi Anda
const char* ssid = "SSID_WIFI";
const char* password = "PASSWORD_WIFI";

// IP Server (alamat IP komputer yang menjalankan server Python)
const String serverName = "http://localhost:8000/insert_data"; 

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Tunggu sampai terkoneksi ke WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
}

void loop() {
  int sensorValue = analogRead(A0);  // Membaca nilai LDR
  float voltage = sensorValue * (3.3 / 1023.0);  // Menghitung tegangan dari nilai sensor

  Serial.print("Sensor LDR Value: ");
  Serial.println(voltage);

  // Kirim data ke server Python
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName); // Inisialisasi koneksi ke server
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    // Kirim data LDR sebagai POST request
    String postData = "ldr_value=" + String(voltage);
    int httpResponseCode = http.POST(postData);

    // Cek respons dari server
    if (httpResponseCode > 0) {
      Serial.println("Data sent successfully");
    } else {
      Serial.println("Error sending data");
    }

    http.end();  // Menutup koneksi
  } else {
    Serial.println("Error in WiFi connection");
  }

  delay(60000);  // Kirim data setiap 1 menit
}
