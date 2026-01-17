/*
 * Simple test to check if Servo 1 hardware is faulty
 * This tests Pin 10 (which we know works)
 */

#include <Servo.h>

Servo testServo;

void setup() {
  Serial.begin(9600);
  
  // Connect Servo 1 to Pin 10 (the working pin)
  testServo.attach(10);
  
  Serial.println(F("Testing Servo 1 on Pin 10"));
  Serial.println(F("If it moves, Servo 1 is OK, Pin 9 is bad"));
  Serial.println(F("If it doesn't move, Servo 1 is faulty"));
  
  delay(2000);
}

void loop() {
  Serial.println(F("Moving to 0°"));
  testServo.write(0);
  delay(2000);
  
  Serial.println(F("Moving to 90°"));
  testServo.write(90);
  delay(2000);
  
  Serial.println(F("Moving to 180°"));
  testServo.write(180);
  delay(2000);
}
