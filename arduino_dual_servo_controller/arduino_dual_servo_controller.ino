/*
 * Arduino Dual Servo Controller for Garbage Classification System
 * Servo 1: Positioning arm (swings to correct bin)
 * Servo 2: Drop-down flap (opens to release rubbish) - FULL 180° MOTION
 * 
 * Hardware Setup:
 * - Servo 1 (positioning) connected to pin 9
 * - Servo 2 (drop flap) connected to pin 10 - moves 0° to 180° (full range)
 * - Power: 5V and GND for both servos
 * - Signals: Digital pins 9 and 10
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
  positioningServo.attach(9);   // Servo 1 on pin 9
  dropFlapServo.attach(10);     // Servo 2 on pin 10
  
  // Initialize LED pin
  pinMode(LED_PIN, OUTPUT);
  
  // Initialize servo positions
  positioningServo.write(90);    // Center position
  dropFlapServo.write(FLAP_CLOSED);  // Flap closed
  delay(1000);
  
  // Quick LED blink to indicate ready
  digitalWrite(LED_PIN, HIGH);
  delay(200);
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("Arduino Dual Servo Controller Ready!");
  Serial.println("Servo 1 (Pin 9): Positioning arm");
  Serial.println("Servo 2 (Pin 10): Drop flap");
  Serial.println("Commands: P(Paper), M(Metal), L(Plastic), G(Glass), T(Trash)");
  Serial.println("Sequence: Position → Drop → Return");
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
        
      default:
        Serial.print("Unknown command: ");
        Serial.println(command);
        break;
    }
  }
}

void executeSortingSequence(int targetAngle, String material) {
  Serial.print("Starting sorting sequence for ");
  Serial.println(material);
  
  // Turn on LED to indicate activity
  digitalWrite(LED_PIN, HIGH);
  
  // Step 1: Position the arm to correct bin
  Serial.print("Step 1: Positioning arm to ");
  Serial.print(targetAngle);
  Serial.print("° for ");
  Serial.println(material);
  
  positioningServo.write(targetAngle);
  delay(POSITION_DELAY);  // Wait for positioning to complete
  
  Serial.println("Step 1 complete: Arm positioned");
  
  // Step 2: Open drop flap to release rubbish - FULL 180° MOTION
  Serial.println("Step 2: Opening drop flap (0° → 180°)");
  
  // Smooth sweep from 0° to 180° for full motion
  for (int angle = FLAP_CLOSED; angle <= FLAP_OPEN; angle += 2) {
    dropFlapServo.write(angle);
    delay(10);  // Small delay for smooth motion
  }
  dropFlapServo.write(FLAP_OPEN);  // Ensure we reach exactly 180°
  
  delay(DROP_DELAY);  // Keep flap open for rubbish to drop
  
  Serial.println("Step 2 complete: Rubbish dropped (flap at 180°)");
  
  // Step 3: Close drop flap - FULL 180° RETURN MOTION
  Serial.println("Step 3: Closing drop flap (180° → 0°)");
  
  // Smooth sweep from 180° back to 0°
  for (int angle = FLAP_OPEN; angle >= FLAP_CLOSED; angle -= 2) {
    dropFlapServo.write(angle);
    delay(10);  // Small delay for smooth motion
  }
  dropFlapServo.write(FLAP_CLOSED);  // Ensure we reach exactly 0°
  
  delay(RETURN_DELAY);
  
  Serial.println("Step 3 complete: Flap closed (back to 0°)");
  
  // Step 4: Return positioning arm to center
  Serial.println("Step 4: Returning arm to center");
  
  positioningServo.write(90);  // Return to center
  delay(RETURN_DELAY);
  
  Serial.println("Step 4 complete: Arm centered");
  
  // Turn off LED
  digitalWrite(LED_PIN, LOW);
  
  Serial.print("Sorting sequence complete for ");
  Serial.println(material);
  Serial.println("Ready for next item");
  Serial.println();
}

void resetToCenter() {
  Serial.println("Manual reset to center position");
  
  digitalWrite(LED_PIN, HIGH);
  
  positioningServo.write(90);      // Center position
  dropFlapServo.write(FLAP_CLOSED); // Flap closed
  
  delay(500);
  
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("Reset complete - Ready for sorting");
}