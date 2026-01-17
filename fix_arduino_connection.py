#!/usr/bin/env python3
"""
Arduino Connection Troubleshooter
Helps diagnose and fix Arduino connection issues
"""

import serial
import serial.tools.list_ports
import time
import psutil
import subprocess
import sys

def check_processes_using_port():
    """Check if any processes are using serial ports."""
    print("🔍 Checking for processes using serial ports...")
    
    arduino_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'arduino' in proc.info['name'].lower():
                arduino_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    if arduino_processes:
        print("⚠️  Found Arduino-related processes:")
        for proc in arduino_processes:
            print(f"   PID {proc['pid']}: {proc['name']}")
        print("   Consider closing Arduino IDE completely")
    else:
        print("✅ No Arduino IDE processes found")

def find_arduino_ports():
    """Find all potential Arduino ports."""
    print("\n🔍 Scanning for Arduino ports...")
    
    all_ports = serial.tools.list_ports.comports()
    arduino_ports = []
    
    for port in all_ports:
        description = port.description.lower()
        if any(keyword in description for keyword in ['arduino', 'ch340', 'cp210', 'ftdi', 'usb']):
            arduino_ports.append(port)
            print(f"✅ Found Arduino-like device:")
            print(f"   Port: {port.device}")
            print(f"   Description: {port.description}")
            print(f"   Manufacturer: {getattr(port, 'manufacturer', 'Unknown')}")
            print()
    
    if not arduino_ports:
        print("❌ No Arduino ports found!")
        print("   Check:")
        print("   - Arduino is connected via USB")
        print("   - USB cable is working (try different cable)")
        print("   - Arduino drivers are installed")
        return []
    
    return arduino_ports

def test_port_access(port_device):
    """Test if we can access a specific port."""
    print(f"\n🔌 Testing access to {port_device}...")
    
    try:
        # Try to open the port briefly
        test_serial = serial.Serial(port_device, 9600, timeout=1)
        test_serial.close()
        print(f"✅ Port {port_device} is accessible")
        return True
    except serial.SerialException as e:
        print(f"❌ Cannot access {port_device}: {e}")
        if "Access is denied" in str(e):
            print("   💡 Port is likely being used by another program")
        elif "does not exist" in str(e):
            print("   💡 Port doesn't exist or device disconnected")
        return False
    except Exception as e:
        print(f"❌ Unexpected error accessing {port_device}: {e}")
        return False

def test_arduino_communication(port_device):
    """Test full communication with Arduino."""
    print(f"\n📡 Testing communication with Arduino on {port_device}...")
    
    try:
        arduino = serial.Serial(port_device, 9600, timeout=3)
        print("✅ Serial connection opened")
        
        # Wait for Arduino to initialize
        print("⏳ Waiting for Arduino to initialize...")
        time.sleep(3)
        
        # Clear any startup messages
        while arduino.in_waiting > 0:
            try:
                msg = arduino.readline().decode().strip()
                if msg:
                    print(f"   Arduino startup: {msg}")
            except:
                break
        
        # Send test command
        print("📤 Sending test command 'P'...")
        arduino.write(b'P')
        arduino.flush()
        
        # Wait for response
        time.sleep(2)
        response_received = False
        
        if arduino.in_waiting > 0:
            try:
                response = arduino.readline().decode().strip()
                if response:
                    print(f"✅ Arduino responded: {response}")
                    response_received = True
            except Exception as e:
                print(f"⚠️  Error reading response: {e}")
        
        if not response_received:
            print("⚠️  No response from Arduino")
            print("   This might be normal if Arduino code isn't loaded")
        
        arduino.close()
        print("✅ Communication test completed")
        return True
        
    except Exception as e:
        print(f"❌ Communication test failed: {e}")
        return False

def main():
    print("🔧 Arduino Connection Troubleshooter")
    print("=" * 50)
    
    # Step 1: Check for conflicting processes
    check_processes_using_port()
    
    # Step 2: Find Arduino ports
    arduino_ports = find_arduino_ports()
    if not arduino_ports:
        print("\n❌ No Arduino found. Check hardware connection.")
        return
    
    # Step 3: Test each port
    working_ports = []
    for port in arduino_ports:
        if test_port_access(port.device):
            working_ports.append(port)
    
    if not working_ports:
        print("\n❌ No accessible Arduino ports found!")
        print("\n🔧 Try these steps:")
        print("1. Close Arduino IDE completely")
        print("2. Unplug and replug Arduino USB cable")
        print("3. Wait 10 seconds")
        print("4. Run this script again")
        return
    
    # Step 4: Test communication
    print(f"\n✅ Found {len(working_ports)} accessible port(s)")
    
    for port in working_ports:
        success = test_arduino_communication(port.device)
        if success:
            print(f"\n🎉 Arduino on {port.device} is ready for web app!")
            print(f"   Use this port in your web application")
            break
    
    print("\n📋 Summary:")
    print("If communication test passed:")
    print("  ✅ Your Arduino is ready")
    print("  ✅ Start the web app: python webapp_5class.py")
    print("  ✅ Use the Arduino Control panel to connect")
    print()
    print("If communication test failed:")
    print("  🔄 Upload arduino_servo_controller.ino to Arduino")
    print("  🔄 Make sure servo is connected to pin 9")
    print("  🔄 Check wiring: Red->5V, Brown->GND, Orange->Pin9")

if __name__ == "__main__":
    main()