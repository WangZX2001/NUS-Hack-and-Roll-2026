#!/usr/bin/env python3
"""
Arduino Connection Diagnostic Tool
Helps identify why Arduino connection might be failing
"""

import sys
import platform
import subprocess
import time
import os

def check_system_info():
    """Check basic system information."""
    print("🖥️  SYSTEM INFORMATION")
    print("=" * 50)
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version}")
    print(f"Architecture: {platform.machine()}")
    print()

def check_python_dependencies():
    """Check if required Python packages are installed."""
    print("🐍 PYTHON DEPENDENCIES")
    print("=" * 50)
    
    required_packages = [
        'pyserial',
        'psutil',
        'flask'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}: Installed")
        except ImportError:
            print(f"❌ {package}: Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print(f"Install with: pip install {' '.join(missing_packages)}")
    else:
        print("✅ All required packages are installed")
    
    print()
    return len(missing_packages) == 0

def check_serial_ports():
    """Check available serial ports."""
    print("🔌 SERIAL PORTS DETECTION")
    print("=" * 50)
    
    try:
        import serial.tools.list_ports
        
        ports = list(serial.tools.list_ports.comports())
        
        if not ports:
            print("❌ No serial ports detected")
            print("💡 Possible causes:")
            print("   - Arduino not connected")
            print("   - USB cable is power-only (not data)")
            print("   - Driver issues")
            print("   - Permission issues")
        else:
            print(f"✅ Found {len(ports)} serial port(s):")
            for port in ports:
                print(f"   📍 {port.device}")
                print(f"      Description: {port.description}")
                print(f"      Manufacturer: {getattr(port, 'manufacturer', 'Unknown')}")
                print(f"      VID:PID: {port.vid}:{port.pid}" if port.vid and port.pid else "      VID:PID: Unknown")
                
                # Check if it looks like Arduino
                arduino_keywords = ['arduino', 'ch340', 'cp210', 'ftdi', 'usb']
                is_arduino_like = any(keyword in port.description.lower() for keyword in arduino_keywords)
                print(f"      Arduino-like: {'✅ Yes' if is_arduino_like else '❌ No'}")
                print()
        
        return ports
        
    except ImportError:
        print("❌ pyserial not installed")
        return []

def check_permissions():
    """Check file permissions for serial ports (Linux/macOS)."""
    print("🔐 PERMISSIONS CHECK")
    print("=" * 50)
    
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("📱 macOS detected")
        # Check if user is in dialout group (not typically needed on macOS)
        try:
            import grp
            groups = [g.gr_name for g in grp.getgrall() if os.getlogin() in g.gr_mem]
            print(f"User groups: {', '.join(groups)}")
        except:
            print("Could not check user groups")
        
        # Check for common serial device permissions
        serial_devices = ['/dev/cu.usbmodem*', '/dev/cu.usbserial*', '/dev/tty.usbmodem*', '/dev/tty.usbserial*']
        found_devices = []
        
        for pattern in serial_devices:
            try:
                import glob
                devices = glob.glob(pattern)
                found_devices.extend(devices)
            except:
                pass
        
        if found_devices:
            print("✅ Found potential Arduino devices:")
            for device in found_devices:
                print(f"   {device}")
        else:
            print("⚠️  No Arduino-like devices found in /dev/")
            
    elif system == "Linux":
        print("🐧 Linux detected")
        # Check if user is in dialout group
        try:
            import grp
            dialout_group = grp.getgrnam('dialout')
            user_groups = [g.gr_name for g in grp.getgrall() if os.getlogin() in g.gr_mem]
            
            if 'dialout' in user_groups:
                print("✅ User is in dialout group")
            else:
                print("❌ User is NOT in dialout group")
                print("💡 Fix with: sudo usermod -a -G dialout $USER")
                print("   Then logout and login again")
        except:
            print("Could not check dialout group membership")
            
    elif system == "Windows":
        print("🪟 Windows detected")
        print("💡 Windows usually doesn't have permission issues")
        print("   If connection fails, check:")
        print("   - Arduino IDE is closed")
        print("   - No other programs using the port")
        print("   - Driver installation")
    
    print()

def test_serial_connection(ports):
    """Test actual serial connection to detected ports."""
    print("🧪 SERIAL CONNECTION TEST")
    print("=" * 50)
    
    if not ports:
        print("❌ No ports to test")
        return
    
    try:
        import serial
        
        for port in ports:
            print(f"Testing {port.device}...")
            
            try:
                # Try to open the port
                ser = serial.Serial(port.device, 9600, timeout=2)
                print(f"✅ Successfully opened {port.device}")
                
                # Try to write/read
                time.sleep(2)  # Wait for Arduino to initialize
                ser.write(b'R')  # Send reset command
                ser.flush()
                
                # Try to read response
                time.sleep(1)
                if ser.in_waiting > 0:
                    response = ser.readline().decode().strip()
                    print(f"✅ Arduino responded: '{response}'")
                else:
                    print("⚠️  No response from Arduino (might be normal)")
                
                ser.close()
                print(f"✅ Successfully closed {port.device}")
                
            except serial.SerialException as e:
                print(f"❌ Failed to connect to {port.device}: {e}")
                
                if "Permission denied" in str(e):
                    print("💡 Permission issue - check user groups")
                elif "Access is denied" in str(e):
                    print("💡 Port in use - close Arduino IDE or other programs")
                elif "Device not found" in str(e):
                    print("💡 Device disconnected or driver issue")
                    
            except Exception as e:
                print(f"❌ Unexpected error with {port.device}: {e}")
            
            print()
            
    except ImportError:
        print("❌ pyserial not available for testing")

def check_running_processes():
    """Check for processes that might block Arduino connection."""
    print("🔍 PROCESS CHECK")
    print("=" * 50)
    
    try:
        import psutil
        
        blocking_processes = []
        arduino_keywords = ['arduino', 'serial', 'tty', 'com']
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and any(keyword in proc.info['name'].lower() for keyword in arduino_keywords):
                    blocking_processes.append(proc.info)
                elif proc.info['cmdline']:
                    cmdline_str = ' '.join(proc.info['cmdline']).lower()
                    if any(keyword in cmdline_str for keyword in arduino_keywords):
                        blocking_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if blocking_processes:
            print("⚠️  Found potentially blocking processes:")
            for proc in blocking_processes:
                print(f"   PID {proc['pid']}: {proc['name']}")
        else:
            print("✅ No obvious blocking processes found")
            
    except ImportError:
        print("❌ psutil not available for process checking")
    
    print()

def provide_solutions():
    """Provide common solutions based on system."""
    print("💡 COMMON SOLUTIONS")
    print("=" * 50)
    
    system = platform.system()
    
    print("1. 🔌 Hardware Check:")
    print("   - Try a different USB cable (data cable, not power-only)")
    print("   - Try a different USB port")
    print("   - Check Arduino power LED is on")
    print("   - Press Arduino reset button")
    print()
    
    print("2. 🖥️  Software Check:")
    print("   - Close Arduino IDE completely")
    print("   - Close any serial monitor programs")
    print("   - Restart your computer")
    print()
    
    if system == "Darwin":  # macOS
        print("3. 🍎 macOS Specific:")
        print("   - Install Arduino IDE to get drivers")
        print("   - Check System Preferences > Security for blocked software")
        print("   - Try: brew install arduino-cli")
        print()
        
    elif system == "Linux":
        print("3. 🐧 Linux Specific:")
        print("   - Add user to dialout group: sudo usermod -a -G dialout $USER")
        print("   - Logout and login again")
        print("   - Install Arduino IDE for drivers")
        print("   - Check: ls -la /dev/ttyUSB* /dev/ttyACM*")
        print()
        
    elif system == "Windows":
        print("3. 🪟 Windows Specific:")
        print("   - Install Arduino IDE for drivers")
        print("   - Check Device Manager for unknown devices")
        print("   - Try different COM port in Device Manager")
        print("   - Run as Administrator")
        print()
    
    print("4. 🔧 Driver Issues:")
    print("   - Install CH340/CH341 drivers for cheap Arduino clones")
    print("   - Install FTDI drivers for FTDI-based boards")
    print("   - Reinstall Arduino IDE")
    print()
    
    print("5. 🐍 Python Issues:")
    print("   - pip install --upgrade pyserial")
    print("   - pip install --upgrade psutil")
    print("   - Try running with sudo/admin privileges")
    print()

def main():
    """Run complete diagnostic."""
    print("🔧 ARDUINO CONNECTION DIAGNOSTIC")
    print("=" * 50)
    print("This tool will help diagnose Arduino connection issues")
    print()
    
    # Run all checks
    check_system_info()
    deps_ok = check_python_dependencies()
    ports = check_serial_ports()
    check_permissions()
    
    if deps_ok and ports:
        test_serial_connection(ports)
    
    check_running_processes()
    provide_solutions()
    
    print("🎯 SUMMARY")
    print("=" * 50)
    if not deps_ok:
        print("❌ Missing Python dependencies - install them first")
    elif not ports:
        print("❌ No serial ports detected - check hardware connection")
    else:
        print("✅ Basic setup looks good - try the solutions above")
    
    print("\n💬 If issues persist:")
    print("   - Compare this output with your friend's laptop")
    print("   - Try the same Arduino on your friend's laptop")
    print("   - Check if it's a hardware vs software issue")

if __name__ == "__main__":
    main()