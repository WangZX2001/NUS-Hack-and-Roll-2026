#!/usr/bin/env python3
"""
Simple Arduino connection checker
Run this while connecting/disconnecting Arduino to see if it's detected
"""

import serial.tools.list_ports
import time

def check_arduino_ports():
    """Check for Arduino-like ports."""
    ports = list(serial.tools.list_ports.comports())
    arduino_ports = []
    
    print(f"Found {len(ports)} total ports:")
    for port in ports:
        print(f"  {port.device}: {port.description}")
        
        # Check if it looks like Arduino
        arduino_keywords = ['arduino', 'ch340', 'cp210', 'ftdi', 'usb', 'usbmodem', 'usbserial']
        is_arduino_like = any(keyword in port.description.lower() for keyword in arduino_keywords)
        is_arduino_like = is_arduino_like or any(keyword in port.device.lower() for keyword in arduino_keywords)
        
        if is_arduino_like:
            arduino_ports.append(port)
            print(f"    ✅ ARDUINO-LIKE PORT DETECTED!")
        else:
            print(f"    ❌ Not Arduino-like")
    
    return arduino_ports

def main():
    print("🔍 Arduino Connection Monitor")
    print("=" * 40)
    print("Connect your Arduino now and watch for changes...")
    print("Press Ctrl+C to stop")
    print()
    
    last_ports = set()
    
    try:
        while True:
            arduino_ports = check_arduino_ports()
            current_ports = set(p.device for p in arduino_ports)
            
            if current_ports != last_ports:
                if current_ports:
                    print(f"\n🎉 ARDUINO DETECTED: {', '.join(current_ports)}")
                    
                    # Try to connect to first Arduino port
                    for port in arduino_ports:
                        print(f"\n🧪 Testing connection to {port.device}...")
                        try:
                            import serial
                            ser = serial.Serial(port.device, 9600, timeout=2)
                            print(f"✅ Successfully opened {port.device}")
                            time.sleep(2)
                            ser.write(b'R')  # Send reset command
                            ser.flush()
                            time.sleep(1)
                            if ser.in_waiting > 0:
                                response = ser.readline().decode().strip()
                                print(f"✅ Arduino responded: '{response}'")
                            else:
                                print("⚠️  No response (normal for some Arduinos)")
                            ser.close()
                            print(f"✅ Connection test successful!")
                            break
                        except Exception as e:
                            print(f"❌ Connection failed: {e}")
                else:
                    print(f"\n❌ No Arduino detected")
                
                last_ports = current_ports
            
            print(".", end="", flush=True)
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n\n👋 Monitoring stopped")

if __name__ == "__main__":
    main()