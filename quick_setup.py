#!/usr/bin/env python3
"""
Quick setup script for hackathon demo.
Sets up everything needed in one command.
"""

import subprocess
import sys
import os
from pathlib import Path
import time

def run_command(command, description):
    """Run a command and show progress."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def check_requirements():
    """Install dependencies from requirements.txt using the active Python."""
    print("📦 Checking Requirements...")

    req_file = Path("requirements.txt")

    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False

    # Upgrade pip first (safe & recommended)
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )

    # Install from requirements.txt
    success = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing dependencies from requirements.txt"
    )

    if not success:
        print("❌ Dependency installation failed")
        return False

    print("✅ All requirements installed")
    return True


def check_model():
    """Check if the trained model exists."""
    model_paths = [
        "runs/classify/runs/classify/5class_model/weights/best.pt",
        "runs/classify/5class_model/weights/best.pt",
        "runs/classify/train2/weights/best.pt"
    ]
    
    for path in model_paths:
        if Path(path).exists():
            print(f"✅ Found trained model: {path}")
            return True
    
    print("❌ No trained model found")
    print("💡 You need to train the model first:")
    print("   python3 create_5_class_dataset.py")
    return False

def setup_arduino_code():
    """Create Arduino code if it doesn't exist."""
    arduino_files = [
        "arduino_servo_controller_fast.ino",
        "arduino_servo_ultra_fast.ino",
        "hackathon_arduino_controller.ino"
    ]
    
    arduino_exists = any(Path(f).exists() for f in arduino_files)
    
    if not arduino_exists:
        print("🔧 Creating Arduino controller code...")
        
        arduino_code = '''/*
  Quick Setup Arduino Controller
  Simple servo control for garbage sorting
*/

#include <Servo.h>

Servo sortingServo;
const int servoPin = 9;

// Positions for each material
const int PAPER_POS = 30;
const int METAL_POS = 60;
const int PLASTIC_POS = 90;
const int GLASS_POS = 120;
const int TRASH_POS = 150;

void setup() {
  Serial.begin(9600);
  sortingServo.attach(servoPin);
  sortingServo.write(90); // Center position
  
  Serial.println("Arduino Garbage Sorter Ready");
  Serial.println("Commands: P(paper) M(metal) L(plastic) G(glass) T(trash)");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    switch (command) {
      case 'P':
        sortingServo.write(PAPER_POS);
        Serial.println("Sorted to PAPER bin");
        break;
      case 'M':
        sortingServo.write(METAL_POS);
        Serial.println("Sorted to METAL bin");
        break;
      case 'L':
        sortingServo.write(PLASTIC_POS);
        Serial.println("Sorted to PLASTIC bin");
        break;
      case 'G':
        sortingServo.write(GLASS_POS);
        Serial.println("Sorted to GLASS bin");
        break;
      case 'T':
        sortingServo.write(TRASH_POS);
        Serial.println("Sorted to TRASH bin");
        break;
      default:
        Serial.println("Unknown command");
        break;
    }
    
    delay(1000); // Wait for servo to move
    sortingServo.write(90); // Return to center
  }
}'''
        
        with open("quick_arduino_controller.ino", "w") as f:
            f.write(arduino_code)
        
        print("✅ Arduino code created: quick_arduino_controller.ino")
    else:
        print("✅ Arduino code already exists")

def create_demo_script():
    """Create a simple demo script."""
    demo_script = '''#!/usr/bin/env python3
"""
Quick demo script - simplified version for immediate testing.
"""

import cv2
from ultralytics import YOLO
import serial
import serial.tools.list_ports
import time
from pathlib import Path

class QuickDemo:
    def __init__(self):
        self.model = None
        self.camera = None
        self.arduino = None
        self.load_model()
        self.setup_camera()
        self.setup_arduino()
    
    def load_model(self):
        """Load the best available model."""
        model_paths = [
            "runs/classify/runs/classify/5class_model/weights/best.pt",
            "runs/classify/5class_model/weights/best.pt",
            "runs/classify/train2/weights/best.pt",
            "yolov8n-cls.pt"
        ]
        
        for path in model_paths:
            if Path(path).exists():
                try:
                    self.model = YOLO(path)
                    print(f"✅ Model loaded: {path}")
                    return
                except:
                    continue
        
        print("❌ No model found!")
    
    def setup_camera(self):
        """Setup camera."""
        self.camera = cv2.VideoCapture(0)
        if self.camera.isOpened():
            print("✅ Camera ready")
        else:
            print("❌ Camera not found")
    
    def setup_arduino(self):
        """Setup Arduino connection."""
        try:
            ports = serial.tools.list_ports.comports()
            arduino_ports = [p for p in ports if 'arduino' in p.description.lower() or 'ch340' in p.description.lower()]
            
            if arduino_ports:
                self.arduino = serial.Serial(arduino_ports[0].device, 9600, timeout=2)
                time.sleep(2)
                print(f"✅ Arduino connected: {arduino_ports[0].device}")
            else:
                print("⚠️  No Arduino found - demo mode")
        except:
            print("⚠️  Arduino connection failed - demo mode")
    
    def classify_and_sort(self, frame):
        """Classify frame and send Arduino command."""
        if not self.model:
            return None, 0
        
        try:
            results = self.model(frame, verbose=False)
            if results and results[0].probs:
                pred_class = results[0].names[results[0].probs.top1]
                confidence = results[0].probs.top1conf.item()
                
                if confidence > 0.5:  # Confidence threshold
                    # Send Arduino command
                    commands = {'paper': 'P', 'metal': 'M', 'plastic': 'L', 'glass': 'G', 'trash': 'T'}
                    
                    if self.arduino and pred_class in commands:
                        try:
                            self.arduino.write(commands[pred_class].encode())
                            print(f"📡 Sent: {commands[pred_class]} for {pred_class}")
                        except:
                            print(f"🔧 [Demo] Sort {pred_class}")
                    else:
                        print(f"🔧 [Demo] Sort {pred_class}")
                    
                    return pred_class, confidence
        except Exception as e:
            print(f"Error: {e}")
        
        return None, 0
    
    def run_demo(self):
        """Run the demo."""
        print("\\n🚀 Quick Demo Started")
        print("Point camera at waste items")
        print("Press SPACE to classify, Q to quit")
        
        last_classification = 0
        
        while True:
            if self.camera:
                ret, frame = self.camera.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    
                    # Auto-classify every 3 seconds
                    current_time = time.time()
                    if current_time - last_classification > 3:
                        pred_class, confidence = self.classify_and_sort(frame)
                        if pred_class:
                            last_classification = current_time
                    
                    # Show frame
                    cv2.imshow('Quick Garbage Sorting Demo', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):  # Manual classify
                last_classification = 0
        
        # Cleanup
        if self.camera:
            self.camera.release()
        if self.arduino:
            self.arduino.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    demo = QuickDemo()
    demo.run_demo()
'''
    
    with open("quick_demo.py", "w") as f:
        f.write(demo_script)
    
    print("✅ Demo script created: quick_demo.py")

def main():
    print("🎯 QUICK SETUP")
    print("=" * 30)
    print("Setting up everything for your demo...")
    
    # Step 1: Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        return
    
    # Step 2: Check model
    model_exists = check_model()
    
    # Step 3: Setup Arduino code
    setup_arduino_code()
    
    # Step 4: Create demo script
    create_demo_script()
    
    # Step 5: Run optimization if enhanced files exist
    if Path("optimize_system.py").exists():
        print("🔄 Running system optimization...")
        run_command("python3 optimize_system.py", "System optimization")
    
    print("\n🎉 QUICK SETUP COMPLETE!")
    print("=" * 30)
    
    if model_exists:
        print("✅ System ready for demo!")
        print("\\n🚀 Quick Start Options:")
        print("1. Simple demo:     python3 quick_demo.py")
        print("2. Web interface:   python3 webapp_5class.py")
        
        if Path("enhanced_webapp.py").exists():
            print("3. Enhanced demo:   python3 enhanced_webapp.py")
        
        if Path("start_optimized.py").exists():
            print("4. Optimized demo:  python3 start_optimized.py")
        
        print("\\n🔧 Arduino Setup:")
        print("1. Upload quick_arduino_controller.ino to your Arduino")
        print("2. Connect servo to pin 9")
        print("3. Power Arduino via USB")
        
    else:
        print("⚠️  Model not found!")
        print("\\n📚 First-time setup:")
        print("1. python3 create_5_class_dataset.py")
        print("2. Train the model when prompted")
        print("3. Run this setup script again")
    
    print("\\n📖 Files created:")
    print("- quick_arduino_controller.ino")
    print("- quick_demo.py")
    
    if Path("optimized_config.json").exists():
        print("- optimized_config.json")

if __name__ == "__main__":
    main()