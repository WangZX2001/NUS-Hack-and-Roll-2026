#!/usr/bin/env python3
"""
Test script to verify the flap servo moves through full 180° range.
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

def test_flap_motion():
    """Test the full flap servo motion."""
    print("🔍 Finding Arduino...")
    
    port = find_arduino()
    if not port:
        print("❌ No Arduino found!")
        print("   Make sure Arduino is connected via USB")
        return False
    
    print(f"✅ Found Arduino on {port}")
    print("🔌 Connecting...")
    
    try:
        arduino = serial.Serial(port, 9600, timeout=5)
        time.sleep(3)  # Wait for Arduino to initialize
        
        # Clear any initial messages
        arduino.reset_input_buffer()
        
        print("✅ Connected!")
        print("\n" + "="*50)
        print("🧪 TESTING FULL FLAP SERVO MOTION (0° to 180°)")
        print("="*50)
        print("\n📤 Sending 'F' command to test full flap motion...")
        print("   Watch your servo - it should move from 0° to 180°\n")
        
        # Send test command
        arduino.write(b'F')
        arduino.flush()
        
        # Read all responses
        print("📥 Arduino output:")
        print("-" * 50)
        
        timeout = time.time() + 15  # 15 second timeout
        while time.time() < timeout:
            if arduino.in_waiting > 0:
                try:
                    line = arduino.readline().decode().strip()
                    if line:
                        print(line)
                except:
                    pass
            time.sleep(0.1)
        
        print("-" * 50)
        print("\n✅ Test complete!")
        print("\n🔍 TROUBLESHOOTING:")
        print("   If servo only moved 90°:")
        print("   1. ⚠️  You might have a 90° servo (not 180°)")
        print("   2. 🔧 Check if servo is mechanically limited")
        print("   3. ⚡ Ensure adequate power supply (5V, sufficient current)")
        print("   4. 📤 Make sure you uploaded the NEW Arduino code")
        print("\n💡 To upload new code:")
        print("   1. Open Arduino IDE")
        print("   2. Open: arduino_dual_servo_controller/arduino_dual_servo_controller.ino")
        print("   3. Click Upload button")
        print("   4. Run this test again")
        
        arduino.close()
        return True
        
    except serial.SerialException as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_flap_motion()
