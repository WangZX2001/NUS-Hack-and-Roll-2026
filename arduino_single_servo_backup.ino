/*
 * Single Servo Backup - Use while troubleshooting Servo 2
 * Only uses Servo 1 for positioning
 * 
 * Hardware Setup:
 * - Servo 1 (positioning) connected to pin 9 only
 * - Power: 5V and GND
 * - Signal: Digital pin 9
 * 
 * Commands from Python:
 * P = Paper (0°)
 * M = Metal (45°)
 * L = Plastic (90°)
 * G = Glass (135°)
 * T = Trash (180°)
 */

#include <Servo.h>

Servo positioningServo;  // Only Servo 1

// Servo positions for each material type
const int PAPER_ANGLE = 0;     // Paper bin
const int METAL_ANGLE = 45;    // Metal bin  
const int PLASTIC_ANGLE = 90;  // Plastic bin
const int GLASS_ANGLE = 135;   // Glass bin
const int TRASH_ANGLE = 180;   // Trash bin

// LED pin for status indication
const int LED_PIN = 13;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Attach servo to pin 9 only
  positioningServo.attach(9);
  
  // Initialize LED pin
  pinMode(LED_PIN, OUTPUT);
  
  // Move servo to center position on startup
  positioningServo.write(90);
  delay(1000);
  
  // Quick LED blink to indicate ready
  digitalWrite(LED_PIN, HIGH);
  delay(200);
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("Arduino Single Servo Controller Ready!");
  Serial.println("Servo 1 (Pin 9): Positioning arm only");
  Serial.println("Commands: P(Paper), M(Metal), L(Plastic), G(Glass), T(Trash)");
  Serial.println("Note: Using single servo while troubleshooting Servo 2");
}

void loop() {
  // Check for incoming serial commands
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // Convert to uppercase for consistency
    command = toupper(command);
    
    // Process command and move servo
    switch(command) {
      case 'P':  // Paper
        moveServoTo(PAPER_ANGLE, "Paper");
        break;
        
      case 'M':  // Metal
        moveServoTo(METAL_ANGLE, "Metal");
        break;
        
      case 'L':  // Plastic
        moveServoTo(PLASTIC_ANGLE, "Plastic");
        break;
        
      case 'G':  // Glass
        moveServoTo(GLASS_ANGLE, "Glass");
        break;
        
      case 'T':  // Trash
        moveServoTo(TRASH_ANGLE, "Trash");
        break;
        
      case 'R':  // Reset to center
        resetToCenter();
        break;
        
      default:
        Serial.print("Unknown command: ");
        Serial.println(command);
        break;
    }
  }
}

void moveServoTo(int angle, String material) {
  // Turn on LED
  digitalWrite(LED_PIN, HIGH);
  
  Serial.print("Moving servo to ");
  Serial.print(angle);
  Serial.print("° for ");
  Serial.println(material);
  
  // Move servo to position
  positioningServo.write(angle);
  delay(500);  // Wait for movement
  
  Serial.print("Servo positioned at ");
  Serial.print(angle);
  Serial.print("° for ");
  Serial.println(material);
  
  // Note about manual drop
  Serial.println("Note: Manually drop rubbish while Servo 2 is being fixed");
  
  // Return to center after 2 seconds
  delay(2000);
  positioningServo.write(90);
  delay(300);
  
  Serial.println("Servo returned to center - Ready for next item");
  
  // Turn off LED
  digitalWrite(LED_PIN, LOW);
}

void resetToCenter() {
  Serial.println("Resetting to center position");
  
  digitalWrite(LED_PIN, HIGH);
  positioningServo.write(90);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("Reset complete - Ready for sorting");
}