#!/usr/bin/env python3
"""
Dependency Installation Script for AI Garbage Classification System
Automatically installs all required dependencies with error handling
"""

import sys
import subprocess
import platform
import os
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print(f"{'='*60}")

def print_status(message, success=True):
    """Print status message with emoji."""
    emoji = "✅" if success else "❌"
    print(f"{emoji} {message}")

def run_command(command, description, shell=False):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    
    try:
        if shell:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status(f"{description} completed successfully")
            return True
        else:
            print_status(f"{description} failed", False)
            print(f"   Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print_status(f"{description} failed", False)
        print(f"   Exception: {e}")
        return False

def check_python_version():
    """Check if Python version is adequate."""
    print_header("Python Version Check")
    
    version = sys.version_info
    required_major, required_minor = 3, 8
    
    is_valid = version.major >= required_major and version.minor >= required_minor
    
    if is_valid:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Compatible")
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Too old", False)
        print(f"   💡 Please install Python {required_major}.{required_minor}+ from https://python.org")
        return False
    
    return True

def upgrade_pip():
    """Upgrade pip to latest version."""
    print_header("Upgrading pip")
    
    python_cmd = "python3" if platform.system() != "Windows" else "python"
    
    return run_command([python_cmd, "-m", "pip", "install", "--upgrade", "pip"], 
                      "Upgrading pip")

def install_requirements():
    """Install requirements from requirements.txt."""
    print_header("Installing Python Dependencies")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print_status("requirements.txt not found", False)
        return False
    
    python_cmd = "python3" if platform.system() != "Windows" else "python"
    
    # Try regular install first
    success = run_command([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"], 
                         "Installing requirements")
    
    if not success:
        print("🔄 Trying alternative installation methods...")
        
        # Try with --user flag
        success = run_command([python_cmd, "-m", "pip", "install", "--user", "-r", "requirements.txt"], 
                             "Installing requirements (user mode)")
        
        if not success and platform.system() != "Windows":
            # Try with pip3 directly
            success = run_command(["pip3", "install", "-r", "requirements.txt"], 
                                 "Installing requirements (pip3)")
    
    return success

def install_pytorch_separately():
    """Install PyTorch separately with CPU-only version for better compatibility."""
    print_header("Installing PyTorch (CPU version)")
    
    python_cmd = "python3" if platform.system() != "Windows" else "python"
    
    # Install CPU-only PyTorch for better compatibility
    pytorch_cmd = [
        python_cmd, "-m", "pip", "install", 
        "torch", "torchvision", "torchaudio", 
        "--index-url", "https://download.pytorch.org/whl/cpu"
    ]
    
    return run_command(pytorch_cmd, "Installing PyTorch CPU version")

def verify_installation():
    """Verify that key packages can be imported."""
    print_header("Verifying Installation")
    
    test_imports = [
        ("torch", "PyTorch"),
        ("cv2", "OpenCV"),
        ("flask", "Flask"),
        ("serial", "PySerial"),
        ("ultralytics", "Ultralytics YOLO"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy"),
        ("psutil", "psutil")
    ]
    
    all_good = True
    
    for module, name in test_imports:
        try:
            __import__(module)
            print_status(f"{name} import successful")
        except ImportError:
            print_status(f"{name} import failed", False)
            all_good = False
    
    return all_good

def install_system_dependencies():
    """Install system-level dependencies if needed."""
    print_header("System Dependencies Check")
    
    system = platform.system()
    
    if system == "Linux":
        print("🐧 Linux detected - checking for system dependencies...")
        
        # Common packages needed for OpenCV and other libraries
        packages_to_check = [
            "python3-dev",
            "python3-pip", 
            "libgl1-mesa-glx",
            "libglib2.0-0",
            "libsm6",
            "libxext6",
            "libxrender-dev",
            "libgomp1"
        ]
        
        print("💡 If installation fails, you may need to install system packages:")
        print(f"   sudo apt update")
        print(f"   sudo apt install {' '.join(packages_to_check)}")
        
    elif system == "Darwin":  # macOS
        print("🍎 macOS detected")
        print("💡 If you encounter issues, consider installing Xcode Command Line Tools:")
        print("   xcode-select --install")
        
    elif system == "Windows":
        print("🪟 Windows detected")
        print("💡 If you encounter build errors, install Microsoft C++ Build Tools:")
        print("   https://visualstudio.microsoft.com/visual-cpp-build-tools/")
    
    return True

def create_startup_script():
    """Create a simple startup script for users."""
    print_header("Creating Startup Script")
    
    system = platform.system()
    
    if system == "Windows":
        script_content = """@echo off
echo Starting AI Garbage Classification System...
python webapp_5class.py
pause
"""
        script_name = "start_system.bat"
    else:
        script_content = """#!/bin/bash
echo "Starting AI Garbage Classification System..."
python3 webapp_5class.py
"""
        script_name = "start_system.sh"
    
    try:
        with open(script_name, 'w') as f:
            f.write(script_content)
        
        if system != "Windows":
            os.chmod(script_name, 0o755)  # Make executable
        
        print_status(f"Created {script_name}")
        print(f"   💡 You can now run: ./{script_name}")
        return True
        
    except Exception as e:
        print_status(f"Failed to create {script_name}", False)
        print(f"   Error: {e}")
        return False

def main():
    """Main installation process."""
    print("🚀 AI Garbage Classification System - Dependency Installer")
    print("This script will install all required dependencies automatically.")
    print("\n⏱️  This may take 10-15 minutes depending on your internet connection.")
    
    input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    # Check Python version first
    if not check_python_version():
        print("\n❌ Python version too old. Please upgrade Python first.")
        return 1
    
    # Install system dependencies info
    install_system_dependencies()
    
    # Upgrade pip
    if not upgrade_pip():
        print("⚠️  pip upgrade failed, but continuing...")
    
    # Try PyTorch separately first (often causes issues)
    pytorch_success = install_pytorch_separately()
    if not pytorch_success:
        print("⚠️  PyTorch installation failed, trying with requirements.txt...")
    
    # Install main requirements
    if not install_requirements():
        print("\n❌ Failed to install requirements. Please check errors above.")
        print("\n🆘 Common solutions:")
        print("   • Run as administrator/sudo")
        print("   • Install Microsoft C++ Build Tools (Windows)")
        print("   • Install Xcode Command Line Tools (macOS)")
        print("   • Install python3-dev packages (Linux)")
        return 1
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️  Some packages failed to import. The system may still work.")
        print("   Run 'python3 check_setup.py' for detailed diagnostics.")
    else:
        print("\n✅ All packages installed and verified successfully!")
    
    # Create startup script
    create_startup_script()
    
    # Final instructions
    print_header("Installation Complete!")
    print("🎉 Dependencies installed successfully!")
    print("\n🚀 Next steps:")
    print("   1. Connect your Arduino via USB")
    print("   2. Upload the Arduino code using Arduino IDE")
    print("   3. Run: python3 start_auto_arduino.py")
    print("   4. Open browser to: http://localhost:5001")
    print("\n🔍 To verify everything is working:")
    print("   python3 check_setup.py")
    print("\n📚 For detailed setup instructions:")
    print("   Read SETUP_GUIDE.md")
    
    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled by user.")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("🆘 Please report this issue or try manual installation.")
        exit(1)