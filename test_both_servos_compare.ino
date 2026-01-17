/*
 * Compare Both Servos Side-by-Side
 * This tests both servos with identical movements
 * to see if Servo 1 is faulty or just slower
 */

#include <Servo.h>

Servo servo1;  // Positioning servo
Servo servo2;  // Flap servo

void setup() {
  Serial.begin(9600);
  
  servo1.attach(11);  // Positioning on Pin 11
  servo2.attach(10);  // Flap on Pin 10
  
  Serial.println(F("================================="));
  Serial.println(F("DUAL SERVO COMPARISON TEST"));
  Serial.println(F("================================="));
  Serial.println(F("Servo 1 (Pin 11): Positioning"));
  Serial.println(F("Servo 2 (Pin 10): Flap"));
  Serial.println(F("Both will move identically"));
  Serial.println(F("================================="));
  Serial.println();
  
  delay(2000);
}

void loop() {
  Serial.println(F(">>> BOTH SERVOS TO 0° <<<"));
  servo1.write(0);
  servo2.write(0);
  delay(3000);
  
  Serial.println(F(">>> BOTH SERVOS SWEEPING TO 180° <<<"));
  for (int angle = 0; angle <= 180; angle += 2) {
    servo1.write(angle);
    servo2.write(angle);
    
    if (angle % 30 == 0) {
      Serial.print(F("Both at: "));
      Serial.print(angle);
      Serial.println(F("°"));
    }
    
    delay(30);
  }
  
  Serial.println(F(">>> BOTH SERVOS AT 180° <<<"));
  servo1.write(180);
  servo2.write(180);
  delay(3000);
  
  Serial.println(F(">>> BOTH SERVOS SWEEPING TO 0° <<<"));
  for (int angle = 180; angle >= 0; angle -= 2) {
    servo1.write(angle);
    servo2.write(angle);
    
    if (angle % 30 == 0) {
      Serial.print(F("Both at: "));
      Serial.print(angle);
      Serial.println(F("°"));
    }
    
    delay(30);
  }
  
  Serial.println(F(">>> BOTH SERVOS BACK TO 0° <<<"));
  servo1.write(0);
  servo2.write(0);
  delay(3000);
  
  Serial.println();
  Serial.println(F("================================="));
  Serial.println(F("OBSERVATION:"));
  Serial.println(F("- Did Servo 1 move at all?"));
  Serial.println(F("- Did Servo 2 move normally?"));
  Serial.println(F("- Are they moving together?"));
  Serial.println(F("================================="));
  Serial.println();
  
  delay(3000);
}
