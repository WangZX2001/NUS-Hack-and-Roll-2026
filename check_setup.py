#!/usr/bin/env python3
"""
Setup Verification Tool for AI Garbage Classification System
Run this to check if everything is properly installed and configured
"""

import sys
import platform
import subprocess
import importlib
import os
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def print_status(item, status, details=""):
    """Print status with emoji."""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {item}: {'OK' if status else 'FAILED'}")
    if details:
        print(f"   {details}")

def check_python_version():
    """Check Python version."""
    print_header("Python Version Check")
    
    version = sys.version_info
    required_major, required_minor = 3, 8
    
    is_valid = version.major >= required_major and version.minor >= required_minor
    
    print_status(
        f"Python {version.major}.{version.minor}.{version.micro}",
        is_valid,
        f"Required: Python {required_major}.{required_minor}+" if not is_valid else ""
    )
    
    if not is_valid:
        print(f"   💡 Please install Python {required_major}.{required_minor} or newer")
        print(f"   📥 Download from: https://python.org/downloads")
    
    return is_valid

def check_dependencies():
    """Check if all required Python packages are installed."""
    print_header("Python Dependencies Check")
    
    # Read requirements from file
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print_status("requirements.txt", False, "File not found")
        return False
    
    with open(requirements_file, 'r') as f:
        requirements = [line.strip().split('>=')[0].split('==')[0] 
                      for line in f if line.strip() and not line.startswith('#')]
    
    # Package name mappings for imports
    package_mappings = {
        'opencv-python': 'cv2',
        'pillow': 'PIL',
        'scikit-learn': 'sklearn',
        'ultralytics': 'ultralytics'
    }
    
    all_good = True
    missing_packages = []
    
    for package in requirements:
        import_name = package_mappings.get(package, package)
        
        try:
            importlib.import_module(import_name)
            print_status(package, True)
        except ImportError:
            print_status(package, False, "Not installed")
            missing_packages.append(package)
            all_good = False
    
    if missing_packages:
        print(f"\n💡 To install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        print(f"   or")
        print(f"   pip install -r requirements.txt")
    
    return all_good

def check_project_files():
    """Check if essential project files exist."""
    print_header("Project Files Check")
    
    essential_files = [
        "webapp_5class.py",
        "templates/index_5class.html", 
        "arduino_dual_servo_controller/arduino_dual_servo_controller.ino",
        "requirements.txt"
    ]
    
    all_good = True
    
    for file_path in essential_files:
        exists = Path(file_path).exists()
        print_status(file_path, exists)
        if not exists:
            all_good = False
    
    return all_good

def check_model_files():
    """Check if AI model files exist."""
    print_header("AI Model Files Check")
    
    model_paths = [
        "runs/classify/runs/classify/5class_model/weights/best.pt",
        "runs/classify/5class_model/weights/best.pt",
        "runs/classify/train2/weights/best.pt"
    ]
    
    model_found = False
    
    for model_path in model_paths:
        exists = Path(model_path).exists()
        if exists:
            print_status(f"5-class model", True, f"Found at {model_path}")
            model_found = True
            break
    
    if not model_found:
        print_status("5-class model", False, "No trained model found")
        print("   💡 Run: python3 create_5_class_dataset.py")
        print("   💡 This will create and train the 5-class model")
    
    # Check for detection model (auto-downloaded)
    yolo_model = Path("yolov8n.pt")
    print_status("Detection model", yolo_model.exists(), 
                "Will be auto-downloaded on first run" if not yolo_model.exists() else "")
    
    return model_found

def check_arduino_connection():
    """Check Arduino connection capability."""
    print_header("Arduino Connection Check")
    
    try:
        import serial.tools.list_ports
        
        ports = list(serial.tools.list_ports.comports())
        print_status(f"Serial ports detected", len(ports) > 0, f"Found {len(ports)} ports")
        
        arduino_ports = []
        for port in ports:
            arduino_keywords = ['arduino', 'ch340', 'cp210', 'ftdi', 'usb', 'usbmodem', 'usbserial']
            is_arduino_like = any(keyword in port.description.lower() for keyword in arduino_keywords)
            is_arduino_like = is_arduino_like or any(keyword in port.device.lower() for keyword in arduino_keywords)
            
            if is_arduino_like:
                arduino_ports.append(port)
                print_status(f"Arduino-like device", True, f"{port.device}: {port.description}")
        
        if not arduino_ports:
            print_status("Arduino device", False, "No Arduino detected")
            print("   💡 Make sure Arduino is connected via USB")
            print("   💡 Try a different USB cable (data cable, not power-only)")
            print("   💡 Install Arduino IDE for drivers")
        
        return len(arduino_ports) > 0
        
    except ImportError:
        print_status("pyserial", False, "Required for Arduino communication")
        return False

def check_camera_access():
    """Check camera access."""
    print_header("Camera Access Check")
    
    try:
        import cv2
        
        # Try to open default camera
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                print_status("Camera access", True, "Default camera working")
                return True
            else:
                print_status("Camera access", False, "Camera detected but can't read frames")
        else:
            print_status("Camera access", False, "No camera detected")
            
        print("   💡 Make sure camera is connected and not used by other apps")
        print("   💡 Check camera permissions in system settings")
        return False
        
    except ImportError:
        print_status("OpenCV", False, "Required for camera access")
        return False

def check_system_requirements():
    """Check system-specific requirements."""
    print_header("System Requirements Check")
    
    system = platform.system()
    print_status(f"Operating System", True, f"{system} {platform.release()}")
    
    # Check available memory (rough estimate)
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        memory_ok = memory_gb >= 4
        print_status(f"RAM", memory_ok, f"{memory_gb:.1f}GB {'(recommended: 8GB+)' if memory_gb < 8 else ''}")
    except ImportError:
        print_status("RAM check", False, "psutil not available")
    
    # Check disk space
    try:
        import shutil
        free_space_gb = shutil.disk_usage('.').free / (1024**3)
        space_ok = free_space_gb >= 2
        print_status(f"Disk space", space_ok, f"{free_space_gb:.1f}GB free")
    except:
        print_status("Disk space check", False, "Could not check")
    
    return True

def provide_next_steps(results):
    """Provide next steps based on check results."""
    print_header("Next Steps")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("🎉 All checks passed! Your system is ready.")
        print("\n🚀 To start the application:")
        print("   python3 start_auto_arduino.py")
        print("\n🌐 Then open your browser to:")
        print("   http://localhost:5001")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\n🔧 Common solutions:")
        
        if not results.get('python_version'):
            print("   • Install Python 3.8+ from python.org")
            
        if not results.get('dependencies'):
            print("   • Run: pip install -r requirements.txt")
            
        if not results.get('model'):
            print("   • Run: python3 create_5_class_dataset.py")
            
        if not results.get('arduino'):
            print("   • Connect Arduino via USB (data cable)")
            print("   • Install Arduino IDE for drivers")
            
        if not results.get('camera'):
            print("   • Connect camera and check permissions")
            print("   • Close other apps using camera")
        
        print("\n🆘 For detailed help:")
        print("   • Read SETUP_GUIDE.md")
        print("   • Run: python3 arduino_diagnostic.py (full diagnostic)")
        print("   • Run: python3 check_arduino_connection.py (real-time monitor)")

def main():
    """Run all checks."""
    print("🔧 AI Garbage Classification System - Setup Verification")
    print("This tool will check if your system is ready to run the application.")
    
    # Run all checks
    results = {
        'python_version': check_python_version(),
        'dependencies': check_dependencies(),
        'project_files': check_project_files(),
        'model': check_model_files(),
        'arduino': check_arduino_connection(),
        'camera': check_camera_access(),
        'system': check_system_requirements()
    }
    
    # Provide guidance
    provide_next_steps(results)
    
    # Summary
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n📊 Summary: {passed}/{total} checks passed")
    
    if passed == total:
        print("✅ System ready! You can start using the application.")
        return 0
    else:
        print("❌ Please fix the issues above before proceeding.")
        return 1

if __name__ == "__main__":
    exit(main())