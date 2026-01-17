# 🤖 Arduino Setup Guide for Garbage Classification System

This guide will help you set up the Arduino Uno with a servo motor to work with the garbage classification system.

## 📋 Required Components

- **Arduino Uno** (or compatible board)
- **Servo Motor** (SG90 or similar)
- **Jumper Wires** (3 wires minimum)
- **USB Cable** (to connect Arduino to computer)
- **Breadboard** (optional, for cleaner connections)

## 🔌 Hardware Connections

### Servo Motor Wiring:
```
Servo Motor    →    Arduino Uno
─────────────────────────────────
Red Wire       →    5V
Brown/Black    →    GND  
Orange/Yellow  →    Digital Pin 9
```

### Connection Diagram:
```
Arduino Uno
┌─────────────────┐
│                 │
│  [5V]  ●────────┼──── Red (Power)
│  [GND] ●────────┼──── Brown (Ground)  
│  [D9]  ●────────┼──── Orange (Signal)
│                 │
└─────────────────┘
        │
        │ USB Cable
        │
    Computer
```

## 💻 Arduino Code Setup

### 1. Install Arduino IDE
- Download from: https://www.arduino.cc/en/software
- Install and open Arduino IDE

### 2. Upload the Code
1. Open `arduino_servo_controller.ino` in Arduino IDE
2. Connect Arduino to computer via USB
3. Select correct board: **Tools → Board → Arduino Uno**
4. Select correct port: **Tools → Port → COM# (Arduino Uno)**
5. Click **Upload** button (→)

### 3. Verify Installation
- Open **Serial Monitor** (Tools → Serial Monitor)
- Set baud rate to **9600**
- You should see: `"Arduino Servo Controller Ready!"`

## 🎯 Servo Positions

The servo will move to these angles based on classification:

| Material | Command | Angle | Position |
|----------|---------|-------|----------|
| 📄 Paper | `P` | 0° | Far Left |
| 🔩 Metal | `M` | 45° | Left |
| 🥤 Plastic | `L` | 90° | Center |
| 🍶 Glass | `G` | 135° | Right |
| 🗑️ Trash | `T` | 180° | Far Right |

## 🔧 Testing the Setup

### Manual Testing (Arduino IDE):
1. Open Serial Monitor
2. Type commands: `P`, `M`, `L`, `G`, or `T`
3. Press Enter
4. Servo should move to corresponding position

### Web Interface Testing:
1. Run the Python webapp: `python webapp_5class.py`
2. Open browser: http://localhost:5000
3. Go to **Arduino Control** section
4. Click **Refresh Ports** to find your Arduino
5. Select the Arduino port and click **Connect**
6. Use **Test Servo Positions** buttons to verify movement

## 🚨 Troubleshooting

### Arduino Not Detected:
- Check USB cable connection
- Install Arduino drivers if needed
- Try different USB port
- Check Device Manager (Windows) for COM ports

### Servo Not Moving:
- Verify wiring connections
- Check power supply (5V and GND)
- Ensure signal wire is on pin 9
- Test with different servo motor

### Serial Communication Issues:
- Close Arduino IDE Serial Monitor before running Python app
- Check correct COM port selection
- Verify baud rate is 9600
- Restart Arduino (unplug/replug USB)

### Permission Errors:
- **Windows**: Run as Administrator
- **Linux/Mac**: Add user to dialout group:
  ```bash
  sudo usermod -a -G dialout $USER
  ```

## 🎛️ Physical Bin Setup

For a complete sorting system, position bins at these servo angles:

```
    0°        45°       90°      135°     180°
    📄        🔩        🥤       🍶       🗑️
  [Paper]   [Metal]  [Plastic] [Glass]  [Trash]
```

## 🔄 Integration with Classification

Once everything is connected:

1. **Start Camera** in web interface
2. **Connect Arduino** using the Arduino Control panel
3. **Point camera** at waste item
4. **Click "Classify Material"**
5. **Servo automatically moves** to correct bin position

The system will:
- Classify the material using AI
- Send command to Arduino
- Move servo to appropriate angle
- Display confirmation in web interface

## 📝 Code Customization

### Changing Servo Angles:
Edit these values in `arduino_servo_controller.ino`:
```cpp
const int PAPER_ANGLE = 0;     // Change as needed
const int METAL_ANGLE = 45;    // Change as needed
const int PLASTIC_ANGLE = 90;  // Change as needed
const int GLASS_ANGLE = 135;   // Change as needed
const int TRASH_ANGLE = 180;   // Change as needed
```

### Adding LED Indicator:
The code includes LED support on pin 13 (built-in LED):
- **Solid**: Arduino ready
- **Blinking**: Processing command
- **Rapid blink**: Error

## ✅ Success Checklist

- [ ] Arduino IDE installed
- [ ] Servo connected to correct pins
- [ ] Arduino code uploaded successfully
- [ ] Serial monitor shows "Ready" message
- [ ] Python webapp detects Arduino port
- [ ] Connection established in web interface
- [ ] Servo test buttons work
- [ ] Classification triggers servo movement
- [ ] All 5 positions work correctly

## 🎉 You're Ready!

Your Arduino servo controller is now integrated with the AI garbage classification system. The servo will automatically sort waste into the correct bins based on the AI's classification results!