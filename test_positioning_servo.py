#!/usr/bin/env python3
"""
Test script specifically for the positioning servo (Servo 1 on Pin 9).
"""

import serial
import serial.tools.list_ports
import time

def find_arduino():
    """Find Arduino port automatically."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if any(keyword in port.description.lower() for keyword in ['arduino', 'ch340', 'cp210', 'ftdi', 'usb']):
            return port.device
    return None

def main():
    print("🔧 POSITIONING SERVO TEST (Servo 1 - Pin 9)")
    print("="*60)
    
    print("\n🔍 Finding Arduino...")
    port = find_arduino()
    
    if not port:
        print("❌ No Arduino found!")
        return False
    
    print(f"✅ Found Arduino on {port}")
    print("🔌 Connecting...")
    
    try:
        arduino = serial.Serial(port, 9600, timeout=5)
        time.sleep(3)
        
        # Clear buffer
        while arduino.in_waiting > 0:
            arduino.read()
        
        print("✅ Connected!\n")
        print("="*60)
        print("🧪 Sending 'S' command to test positioning servo")
        print("="*60)
        print("\n👀 WATCH SERVO 1 (Pin 9) - It should move through:")
        print("   0° → 45° → 90° → 135° → 180° → 90° (center)")
        print("\n📤 Sending command...\n")
        
        # Send test command
        arduino.write(b'S')
        arduino.flush()
        
        # Read responses
        print("📥 Arduino output:")
        print("-"*60)
        
        timeout = time.time() + 15
        last_activity = time.time()
        
        while time.time() < timeout:
            if arduino.in_waiting > 0:
                try:
                    line = arduino.readline().decode().strip()
                    if line:
                        print(line)
                        last_activity = time.time()
                except:
                    pass
            else:
                if time.time() - last_activity > 2:
                    break
            time.sleep(0.05)
        
        print("-"*60)
        print("\n" + "="*60)
        print("🔍 DIAGNOSIS:")
        print("="*60)
        
        response = input("\nDid Servo 1 (Pin 9) move? (y/n): ").strip().lower()
        
        if response == 'y':
            print("\n✅ GREAT! Servo 1 is working!")
            print("   The positioning servo hardware is functional.")
            print("   If it doesn't work during classification, there might be")
            print("   a timing or power issue when both servos run together.")
        else:
            print("\n❌ Servo 1 NOT moving. Possible issues:")
            print("\n🔧 Hardware Checks:")
            print("   1. ⚠️  Is servo connected to Pin 9? (Check wiring)")
            print("   2. ⚡ Does servo have power? (5V and GND connected)")
            print("   3. 📍 Is signal wire in Pin 9? (Orange/Yellow wire)")
            print("   4. 🔋 Is power supply adequate? (Both servos need power)")
            print("\n🧪 Quick Test:")
            print("   - Swap the two servos (swap their pins)")
            print("   - If Servo 2 position now works, Pin 9 might be damaged")
            print("   - If Servo 1 still doesn't work, the servo itself might be faulty")
            print("\n💡 Alternative:")
            print("   - Try using a different Arduino pin (e.g., Pin 11)")
            print("   - Update the code: positioningServo.attach(11);")
        
        arduino.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()
