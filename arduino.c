#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>

// Replace with your WiFi SSID and Password
const char* ssid = "rosify";
const char* password = "12345678";

// Server URL (the IP address of the Python server)
const String serverName = "http://192.168.174.155:8000/insert_data";

// Create a WiFiClient object
WiFiClient client;

// Function to connect to WiFi
void connectToWiFi() {
  WiFi.begin(ssid, password);

  // Wait until connected to WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}

// Function to read LDR sensor value and convert to voltage
float readLDRSensor() {
  int sensorValue = analogRead(A0);  // Read LDR sensor value
  return sensorValue * (3.3 / 1023.0);  // Convert to voltage (0-3.3V)
}

// Function to send data to the server
void sendDataToServer(float ldrValue) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(client, serverName); // Initialize the connection to the server
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    // Prepare the POST data
    String postData = "ldr_value=" + String(ldrValue, 2); // Send voltage value with 2 decimal places

    // Send the POST request
    int httpResponseCode = http.POST(postData);

    // Check the server response
    if (httpResponseCode > 0) {
      Serial.println("Data sent successfully, HTTP Response Code: " + String(httpResponseCode));
    } else {
      Serial.println("Error sending data, HTTP Response Code: " + String(httpResponseCode));
    }

    http.end(); // Close the HTTP connection
  } else {
    Serial.println("Error in WiFi connection");
  }
}

void setup() {
  Serial.begin(9600);
  
  // Connect to WiFi
  connectToWiFi();
}

void loop() {
  // Read LDR sensor value
  float voltage = readLDRSensor();

  // Output the LDR sensor value
  Serial.print("Sensor LDR Value: ");
  Serial.println(voltage, 2);  // Print voltage with 2 decimal places

  // Send data to the server
  sendDataToServer(voltage);

  // Wait for 5 seconds before sending data again
  delay(5000);
}
