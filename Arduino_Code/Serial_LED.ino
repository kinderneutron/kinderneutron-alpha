const int ledPin = 3;  // Connect an LED to digital pin 3

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  pinMode(ledPin, OUTPUT);  // Set the LED pin as an output
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();

    if (signal == '1') {
      digitalWrite(ledPin, HIGH);  // Turn on the LED
    } else if (signal == '0') {
      digitalWrite(ledPin, LOW);   // Turn off the LED
    }
  }
}
