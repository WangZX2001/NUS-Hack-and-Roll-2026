/*
 * Arduino Servo Controller - ULTRA FAST VERSION
 * Fastest possible servo movement for garbage classification
 * 
 * Hardware Setup:
 * - Servo motor connected to pin 9
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

Servo sortingServo;  // Create servo object

// Servo positions for each material type
const int PAPER_ANGLE = 0;     // Paper bin
const int METAL_ANGLE = 45;    // Metal bin  
const int PLASTIC_ANGLE = 90;  // Plastic bin
const int GLASS_ANGLE = 135;   // Glass bin
const int TRASH_ANGLE = 180;   // Trash bin

// LED pin for status indication (optional)
const int LED_PIN = 13;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Attach servo to pin 9
  sortingServo.attach(9);
  
  // Initialize LED pin
  pinMode(LED_PIN, OUTPUT);
  
  // Move servo to center position on startup
  sortingServo.write(90);
  delay(500);  // Reduced startup delay
  
  // Quick LED blink to indicate ready
  digitalWrite(LED_PIN, HIGH);
  delay(100);
  digitalWrite(LED_PIN, LOW);
  
  Serial.println("Arduino ULTRA FAST Servo Controller Ready!");
  Serial.println("Commands: P(Paper), M(Metal), L(Plastic), G(Glass), T(Trash)");
  Serial.println("Ultra fast movement mode - minimal delays!");
}

void loop() {
  // Check for incoming serial commands
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // Convert to uppercase for consistency
    command = toupper(command);
    
    // Process command and move servo IMMEDIATELY
    switch(command) {
      case 'P':  // Paper
        moveServoUltraFast(PAPER_ANGLE, "Paper");
        break;
        
      case 'M':  // Metal
        moveServoUltraFast(METAL_ANGLE, "Metal");
        break;
        
      case 'L':  // Plastic (L for pLastic to avoid confusion with Paper)
        moveServoUltraFast(PLASTIC_ANGLE, "Plastic");
        break;
        
      case 'G':  // Glass
        moveServoUltraFast(GLASS_ANGLE, "Glass");
        break;
        
      case 'T':  // Trash
        moveServoUltraFast(TRASH_ANGLE, "Trash");
        break;
        
      default:
        Serial.print("Unknown command: ");
        Serial.println(command);
        // No error blink to save time
        break;
    }
  }
}

void moveServoUltraFast(int angle, String material) {
  // LED on immediately
  digitalWrite(LED_PIN, HIGH);
  
  // Move servo IMMEDIATELY - no delays
  sortingServo.write(angle);
  
  // Send confirmation immediately
  Serial.print("Servo moved to ");
  Serial.print(angle);
  Serial.print("° for ");
  Serial.println(material);
  
  // Minimal delay just to ensure servo starts moving
  delay(100);  // Absolute minimum delay
  
  // LED off
  digitalWrite(LED_PIN, LOW);
}