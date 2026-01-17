/*
 * Full Sweep Test for Servo 1 (Positioning Servo)
 * This does a SLOW, VISIBLE sweep from 0° to 180° and back
 * Similar to the flap servo test that works
 */

#include <Servo.h>

Servo positioningServo;

void setup() {
  Serial.begin(9600);
  
  // Attach to Pin 11
  positioningServo.attach(11);
  
  Serial.println(F("================================="));
  Serial.println(F("SERVO 1 FULL SWEEP TEST"));
  Serial.println(F("Pin 11 - Positioning Servo"));
  Serial.println(F("================================="));
  Serial.println(F("Watch the servo carefully!"));
  Serial.println(F("It should sweep SLOWLY from 0° to 180°"));
  Serial.println();
  
  delay(2000);
}

void loop() {
  Serial.println(F("--- Starting at 0° ---"));
  positioningServo.write(0);
  delay(2000);
  
  Serial.println(F("--- Sweeping 0° to 180° (SLOW) ---"));
  
  // Very slow sweep with position feedback
  for (int angle = 0; angle <= 180; angle += 1) {
    positioningServo.write(angle);
    
    // Print every 15 degrees
    if (angle % 15 == 0) {
      Serial.print(F("Position: "));
      Serial.print(angle);
      Serial.println(F("°"));
    }
    
    delay(50);  // 50ms per degree = 9 seconds total
  }
  
  Serial.println(F("--- Reached 180° ---"));
  Serial.println(F("Holding at 180° for 3 seconds..."));
  positioningServo.write(180);
  delay(3000);
  
  Serial.println(F("--- Sweeping 180° to 0° (SLOW) ---"));
  
  // Sweep back slowly
  for (int angle = 180; angle >= 0; angle -= 1) {
    positioningServo.write(angle);
    
    // Print every 15 degrees
    if (angle % 15 == 0) {
      Serial.print(F("Position: "));
      Serial.print(angle);
      Serial.println(F("°"));
    }
    
    delay(50);  // 50ms per degree = 9 seconds total
  }
  
  Serial.println(F("--- Back to 0° ---"));
  Serial.println(F("Holding at 0° for 3 seconds..."));
  Serial.println();
  positioningServo.write(0);
  delay(3000);
  
  Serial.println(F("================================="));
  Serial.println(F("CYCLE COMPLETE - Repeating..."));
  Serial.println(F("================================="));
  Serial.println();
  delay(2000);
}
