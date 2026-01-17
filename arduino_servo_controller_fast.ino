/*
 * Arduino Servo Controller for Garbage Classification System - FAST VERSION
 * Controls servo motor to sort waste into different bins with faster movement
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
  delay(1000);
  
  // Blink LED to indicate ready
  for(int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
  
  Serial.println("Arduino Fast Servo Controller Ready!");
  Serial.println("Commands: P(Paper), M(Metal), L(Plastic), G(Glass), T(Trash)");
  Serial.println("Fast movement mode enabled!");
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
        moveServoToFast(PAPER_ANGLE, "Paper");
        break;
        
      case 'M':  // Metal
        moveServoToFast(METAL_ANGLE, "Metal");
        break;
        
      case 'L':  // Plastic (L for pLastic to avoid confusion with Paper)
        moveServoToFast(PLASTIC_ANGLE, "Plastic");
        break;
        
      case 'G':  // Glass
        moveServoToFast(GLASS_ANGLE, "Glass");
        break;
        
      case 'T':  // Trash
        moveServoToFast(TRASH_ANGLE, "Trash");
        break;
        
      default:
        Serial.print("Unknown command: ");
        Serial.println(command);
        blinkError();
        break;
    }
  }
}

void moveServoToFast(int angle, String material) {
  // Indicate activity
  digitalWrite(LED_PIN, HIGH);
  
  // Send immediate confirmation that command was received
  Serial.print("Moving servo to ");
  Serial.print(angle);
  Serial.print("° for ");
  Serial.println(material);
  
  // Move servo directly to target angle (FAST movement)
  sortingServo.write(angle);
  
  // Short delay to ensure servo starts moving
  delay(300);  // Reduced from 15ms per degree - much faster!
  
  // Confirm movement completion
  Serial.print("Servo moved to ");
  Serial.print(angle);
  Serial.print("° for ");
  Serial.println(material);
  
  // Turn off LED
  digitalWrite(LED_PIN, LOW);
}

void blinkError() {
  // Blink LED rapidly to indicate error
  for(int i = 0; i < 5; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
    delay(100);
  }
}