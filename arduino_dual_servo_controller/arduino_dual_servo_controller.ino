/*
 * Arduino Dual Servo Controller for Garbage Classification System
 * Servo 1: Positioning arm (swings to correct bin)
 * Servo 2: Drop-down flap (opens to release rubbish) - FULL 180° MOTION
 * 
 * Hardware Setup:
 * - Servo 1 (positioning) connected to pin 11 (CHANGED from pin 9)
 * - Servo 2 (drop flap) connected to pin 10 - moves 0° to 180° (full range)
 * - Power: 5V and GND for both servos
 * - Signals: Digital pins 11 and 10
 * 
 * Commands from Python:
 * P = Paper (0°)
 * M = Metal (45°)
 * L = Plastic (90°)
 * G = Glass (135°)
 * T = Trash (180°)
 * 
 * Flap Motion: Smooth sweep from 0° (closed) to 180° (fully open) and back
 */

#include <Servo.h>

// Create servo objects
Servo positioningServo;  // Servo 1 - positions to correct bin
Servo dropFlapServo;     // Servo 2 - opens flap to drop rubbish

// Servo 1 positions for each material type
const int PAPER_ANGLE = 0;     // Paper bin
const int METAL_ANGLE = 45;    // Metal bin  
const int PLASTIC_ANGLE = 90;  // Plastic bin
const int GLASS_ANGLE = 135;   // Glass bin
const int TRASH_ANGLE = 180;   // Trash bin

// Servo 2 positions for drop flap
const int FLAP_CLOSED = 0;     // Flap closed (holding rubbish)
const int FLAP_OPEN = 180;     // Flap open (dropping rubbish)

// LED pin for status indication
const int LED_PIN = 13;

// Timing constants
const int POSITION_DELAY = 800;  // Time to wait after positioning (ms) - increased for full motion
const int DROP_DELAY = 1500;     // Time to keep flap open (ms) - increased for full 180° motion
const int RETURN_DELAY = 800;    // Time to wait before returning to center (ms) - increased

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Attach servos to pins
  positioningServo.attach(11);  // Servo 1 on pin 11 (changed from 9)
  dropFlapServo.attach(10);     // Servo 2 on pin 10
  
  // Initialize LED pin
  pinMode(LED_PIN, OUTPUT);
  
  // Initialize servo positions
  Serial.println("Initializing servos...");
  Serial.println("  Setting positioning servo to 0° (start position)");
  positioningServo.write(0);    // Start at 0 degrees instead of center
  Serial.println("  Setting flap servo to 0° (closed)");
  dropFlapServo.write(FLAP_CLOSED);  // Flap closed
  delay(1000);
  
  // Quick LED blink to indicate ready
  digitalWrite(LED_PIN, HIGH);
  delay(200);
  digitalWrite(LED_PIN, LOW);
  
  Serial.println(F("Arduino Dual Servo Controller Ready!"));
  Serial.println(F("Servo 1 (Pin 11): Positioning arm"));
  Serial.println(F("Servo 2 (Pin 10): Drop flap (0° to 180°)"));
  Serial.println(F("Commands: P(Paper), M(Metal), L(Plastic), G(Glass), T(Trash)"));
  Serial.println(F("Special: R(Reset), F(Test Flap), S(Test Positioning), D(Detach/Reattach)"));
  Serial.println(F("Sequence: Position → Drop → Return"));
}

void loop() {
  // Check for incoming serial commands
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // Convert to uppercase for consistency
    command = toupper(command);
    
    // Process command and execute dual servo sequence
    switch(command) {
      case 'P':  // Paper
        executeSortingSequence(PAPER_ANGLE, "Paper");
        break;
        
      case 'M':  // Metal
        executeSortingSequence(METAL_ANGLE, "Metal");
        break;
        
      case 'L':  // Plastic
        executeSortingSequence(PLASTIC_ANGLE, "Plastic");
        break;
        
      case 'G':  // Glass
        executeSortingSequence(GLASS_ANGLE, "Glass");
        break;
        
      case 'T':  // Trash
        executeSortingSequence(TRASH_ANGLE, "Trash");
        break;
        
      case 'R':  // Reset to center (manual command)
        resetToCenter();
        break;
        
      case 'F':  // Test FULL flap motion (0° to 180° and back)
        testFullFlapMotion();
        break;
        
      case 'S':  // Test positioning Servo (Servo 1)
        testPositioningServo();
        break;
        
      case 'D':  // Detach and reattach positioning servo
        detachReattachServo();
        break;
        
      default:
        Serial.print("Unknown command: ");
        Serial.println(command);
        break;
    }
  }
}

void executeSortingSequence(int targetAngle, String material) {
  Serial.print(F("Sorting: "));
  Serial.println(material);
  
  digitalWrite(LED_PIN, HIGH);
  
  // Step 1: Position the arm
  Serial.print(F("Position to "));
  Serial.print(targetAngle);
  Serial.println(F("°"));
  
  positioningServo.write(targetAngle);
  delay(POSITION_DELAY);
  
  Serial.println(F("Positioned"));
  
  // Step 2: Open flap (0° to 180°)
  Serial.println(F("Opening flap"));
  
  for (int angle = FLAP_CLOSED; angle <= FLAP_OPEN; angle += 2) {
    dropFlapServo.write(angle);
    delay(10);
  }
  dropFlapServo.write(FLAP_OPEN);
  
  delay(DROP_DELAY);
  
  Serial.println(F("Dropped"));
  
  // Step 3: Close flap (180° to 0°)
  Serial.println(F("Closing flap"));
  
  for (int angle = FLAP_OPEN; angle >= FLAP_CLOSED; angle -= 2) {
    dropFlapServo.write(angle);
    delay(10);
  }
  dropFlapServo.write(FLAP_CLOSED);
  
  delay(RETURN_DELAY);
  
  Serial.println(F("Closed"));
  
  // Step 4: Return to center
  Serial.println(F("Return center"));
  
  positioningServo.write(90);
  delay(RETURN_DELAY);
  
  digitalWrite(LED_PIN, LOW);
  
  Serial.println(F("Complete"));
  Serial.println();
}

void resetToCenter() {
  Serial.println(F("Reset"));
  
  digitalWrite(LED_PIN, HIGH);
  
  positioningServo.write(90);
  dropFlapServo.write(FLAP_CLOSED);
  
  delay(500);
  
  digitalWrite(LED_PIN, LOW);
  
  Serial.println(F("Ready"));
}

void testFullFlapMotion() {
  Serial.println(F("=== FLAP TEST ==="));
  
  digitalWrite(LED_PIN, HIGH);
  
  Serial.println(F("Start: 0°"));
  dropFlapServo.write(0);
  delay(1000);
  
  Serial.println(F("Sweep to 180°"));
  for (int angle = 0; angle <= 180; angle += 5) {
    dropFlapServo.write(angle);
    if (angle % 30 == 0) {
      Serial.print(angle);
      Serial.println(F("°"));
    }
    delay(30);
  }
  
  dropFlapServo.write(180);
  Serial.println(F("At 180° - hold 2s"));
  delay(2000);
  
  Serial.println(F("Return to 0°"));
  for (int angle = 180; angle >= 0; angle -= 5) {
    dropFlapServo.write(angle);
    delay(30);
  }
  
  dropFlapServo.write(0);
  Serial.println(F("Back to 0°"));
  
  digitalWrite(LED_PIN, LOW);
  Serial.println(F("=== TEST DONE ==="));
}


void testPositioningServo() {
  Serial.println(F("=== POSITION TEST ==="));
  
  digitalWrite(LED_PIN, HIGH);
  
  Serial.println(F("Unstick: rapid moves"));
  for (int i = 0; i < 5; i++) {
    positioningServo.write(0);
    delay(200);
    positioningServo.write(180);
    delay(200);
  }
  
  Serial.println(F("Test positions"));
  delay(1000);
  
  int pos[] = {0, 45, 90, 135, 180};
  const char* labels[] = {"Paper", "Metal", "Plastic", "Glass", "Trash"};
  
  for (int i = 0; i < 5; i++) {
    Serial.print(labels[i]);
    Serial.print(F(" "));
    Serial.println(pos[i]);
    positioningServo.write(pos[i]);
    delay(2000);
  }
  
  Serial.println(F("Center 90°"));
  positioningServo.write(90);
  delay(1000);
  
  digitalWrite(LED_PIN, LOW);
  Serial.println(F("=== TEST DONE ==="));
}


void detachReattachServo() {
  Serial.println(F("=== DETACH/REATTACH ==="));
  
  digitalWrite(LED_PIN, HIGH);
  
  Serial.println(F("Detaching..."));
  positioningServo.detach();
  delay(1000);
  Serial.println(F("Move servo manually!"));
  
  Serial.println(F("Wait 3s..."));
  delay(3000);
  
  Serial.println(F("Reattaching..."));
  positioningServo.attach(11);  // Changed to pin 11
  delay(500);
  
  Serial.println(F("Center 90°"));
  positioningServo.write(90);
  delay(1000);
  
  Serial.println(F("Test 0°"));
  positioningServo.write(0);
  delay(1500);
  
  Serial.println(F("Test 180°"));
  positioningServo.write(180);
  delay(1500);
  
  Serial.println(F("Back to 90°"));
  positioningServo.write(90);
  delay(1000);
  
  digitalWrite(LED_PIN, LOW);
  Serial.println(F("=== DONE ==="));
}
