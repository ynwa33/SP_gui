#include "DHT.h"

// Define the DHT type and the pin where it's connected
#define DHTPIN 34       // Pin 34 where the DHT sensor is connected
#define DHTTYPE DHT11   // Change this to DHT22 if you are using the DHT22 sensor

// Initialize the DHT sensor
DHT dht(DHTPIN, DHTTYPE);

int ldrPin = A1;   // Define the pin for the LDR sensor
int ledPin = 9;    // Define the pin for the LED

void setup() {
  Serial.begin(9600);
  dht.begin();  // Start the DHT sensor
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Reading temperature and humidity from DHT sensor
  float humidity = dht.readHumidity();
  float temperatureC = dht.readTemperature();

  // Reading the light level from the LDR
  int lightValue = analogRead(ldrPin);

  // Print the temperature, humidity, and light level to the serial monitor
  Serial.print("Temperature: ");
  Serial.print(temperatureC);
  Serial.print(" C, Humidity: ");
  Serial.print(humidity);
  Serial.print(" %, Light Level: ");
  Serial.println(lightValue);

  // Control LED based on light level
  if (lightValue < 500) {  // Assuming dark condition
    digitalWrite(ledPin, HIGH);  // Turn on the LED
  } else {
    digitalWrite(ledPin, LOW);   // Turn off the LED
  }

  delay(1000);  // Delay between readings
}
evel from LDR sensor
  int lightLevel = analogRead(lightSensorPin);      // Read light sensor value from LDR

  // Check if the DHT22 sensor failed to read the values
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Error: Failed to read from DHT sensor!");  // Print error message
  } else {
    // Send sensor data in CSV format: Temperature, Humidity, Light level
    Serial.print(temperature);        // Print temperature value
    Serial.print(",");                // Print separator (CSV format)
    Serial.print(humidity);           // Print humidity value
    Serial.print(",");                // Print separator (CSV format)
    Serial.println(lightLevel);       // Print light level value
  }

  // Control LED based on the light level (dark = LED on)
  if (lightLevel < lightThreshold) {    // If the environment is dark (light level < threshold)
    digitalWrite(ledPin, HIGH);         // Turn on LED
  } else {                              // Otherwise (bright environment)
    digitalWrite(ledPin, LOW);          // Turn off LED
  }

  delay(500);  // Wait for 0.5 seconds before taking another reading
}
