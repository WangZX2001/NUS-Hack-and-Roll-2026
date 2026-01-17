/*
 * Individual Servo Test - Troubleshoot Servo Issues
 * Tests each servo separately to identify problems
 * 
 * Commands:
 * 1 = Test Servo 1 (Pin 9) only
 * 2 = Test Servo 2 (Pin 10) only
 * B = Test Both servos together
 * S = Sweep test for both servos
 */

#include <Servo.h>

Servo servo1;  // Pin 9
Servo servo2;  // Pin 10

const int LED_PIN = 13;

void setup() {
  Serial.begin(9600);
  
  // Attach servos
  servo1.attach(9);
  servo2.attach(10);
  
  pinMode(LED_PIN, OUTPUT);
  
  // Initialize positions
  servo1.write(90);
  servo2.write(0);
  delay(1000);
  
  Serial.println("=== Individual Servo Test ===");
  Serial.println("Servo 1: Pin 9 (Positioning)");
  Serial.println("Servo 2: Pin 10 (Drop Flap)");
  Serial.println();
  Serial.println("Commands:");
  Serial.println("1 = Test Servo 1 only");
  Serial.println("2 = Test Servo 2 only");
  Serial.println("B = Test Both servos");
  Serial.println("S = Sweep test");
  Serial.println("R = Reset both to start position");
  Serial.println();
  Serial.println("Ready for testing!");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    command = toupper(command);
    
    digitalWrite(LED_PIN, HIGH);
    
    switch(command) {
      case '1':
        testServo1Only();
        break;
        
      case '2':
        testServo2Only();
        break;
        
      case 'B':
        testBothServos();
        break;
        
      case 'S':
        sweepTest();
        break;
        
      case 'R':
        resetServos();
        break;
        
      default:
        Serial.print("Unknown command: ");
        Serial.println(command);
        break;
    }
    
    digitalWrite(LED_PIN, LOW);
  }
}

void testServo1Only() {
  Serial.println("=== Testing Servo 1 (Pin 9) Only ===");
  
  int positions[] = {0, 45, 90, 135, 180, 90};
  String names[] = {"0°", "45°", "90°", "135°", "180°", "Center"};
  
  for(int i = 0; i < 6; i++) {
    Serial.print("Moving Servo 1 to ");
    Serial.println(names[i]);
    
    servo1.write(positions[i]);
    delay(1000);
    
    Serial.print("Servo 1 position: ");
    Serial.println(servo1.read());
  }
  
  Serial.println("Servo 1 test complete!");
  Serial.println();
}

void testServo2Only() {
  Serial.println("=== Testing Servo 2 (Pin 10) Only ===");
  
  Serial.println("Moving Servo 2 to 0° (Closed)");
  servo2.write(0);
  delay(1000);
  Serial.print("Servo 2 position: ");
  Serial.println(servo2.read());
  
  Serial.println("Moving Servo 2 to 45° (Half Open)");
  servo2.write(45);
  delay(1000);
  Serial.print("Servo 2 position: ");
  Serial.println(servo2.read());
  
  Serial.println("Moving Servo 2 to 90° (Full Open)");
  servo2.write(90);
  delay(1000);
  Serial.print("Servo 2 position: ");
  Serial.println(servo2.read());
  
  Serial.println("Moving Servo 2 back to 0° (Closed)");
  servo2.write(0);
  delay(1000);
  Serial.print("Servo 2 position: ");
  Serial.println(servo2.read());
  
  Serial.println("Servo 2 test complete!");
  Serial.println();
}

void testBothServos() {
  Serial.println("=== Testing Both Servos Together ===");
  
  Serial.println("Step 1: Position Servo 1 to 90°, Servo 2 to 0°");
  servo1.write(90);
  servo2.write(0);
  delay(1000);
  
  Serial.println("Step 2: Open Servo 2 to 90°");
  servo2.write(90);
  delay(1000);
  
  Serial.println("Step 3: Close Servo 2 to 0°");
  servo2.write(0);
  delay(1000);
  
  Serial.println("Both servos test complete!");
  Serial.println();
}

void sweepTest() {
  Serial.println("=== Sweep Test ===");
  
  Serial.println("Sweeping Servo 1 (0° to 180°)");
  for(int pos = 0; pos <= 180; pos += 10) {
    servo1.write(pos);
    delay(100);
  }
  
  Serial.println("Sweeping Servo 2 (0° to 90°)");
  for(int pos = 0; pos <= 90; pos += 10) {
    servo2.write(pos);
    delay(100);
  }
  
  Serial.println("Returning to start positions");
  servo1.write(90);
  servo2.write(0);
  delay(500);
  
  Serial.println("Sweep test complete!");
  Serial.println();
}

void resetServos() {
  Serial.println("=== Resetting Servos ===");
  
  Serial.println("Servo 1 to 90° (Center)");
  servo1.write(90);
  
  Serial.println("Servo 2 to 0° (Closed)");
  servo2.write(0);
  
  delay(1000);
  
  Serial.println("Reset complete!");
  Serial.println();
}