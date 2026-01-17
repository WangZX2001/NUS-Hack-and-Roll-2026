# 🎮 Manual Arduino Control Guide

Since the web interface can't connect to Arduino automatically, you can control it manually. This is actually a great way to test the system!

## 🔧 Setup

1. **Upload Arduino Code**:
   - Open Arduino IDE
   - Load `arduino_servo_controller.ino`
   - Upload to Arduino
   - Keep Arduino IDE open

2. **Open Serial Monitor**:
   - Tools → Serial Monitor
   - Set baud rate: **9600**
   - Should show: `"Arduino Servo Controller Ready!"`

## 🎯 Manual Operation Workflow

### Step 1: Start Web App (Camera Only)
```bash
python webapp_5class.py
```
- Open browser: http://localhost:5000
- Start camera
- **Ignore Arduino connection errors** - we'll control manually

### Step 2: Classify and Control
1. **Point camera at waste item**
2. **Click "Classify Material"**
3. **Look at the result** in web interface
4. **Send corresponding command** to Arduino Serial Monitor

## 📋 Command Reference

| Web App Shows | Arduino Command | Servo Position | Bin |
|---------------|-----------------|----------------|-----|
| **paper** | Type `P` + Enter | 0° | Paper bin |
| **metal** | Type `M` + Enter | 45° | Metal bin |
| **plastic** | Type `L` + Enter | 90° | Plastic bin |
| **glass** | Type `G` + Enter | 135° | Glass bin |
| **trash** | Type `T` + Enter | 180° | Trash bin |

## 🎮 Example Session

```
Web App Result: "Classification: plastic, Confidence: 0.89, Arduino Command: L"
↓
Arduino Serial Monitor: Type "L" and press Enter
↓
Arduino Response: "Servo moved to 90° for Plastic"
↓
Servo moves to plastic bin position!
```

## 🔄 Quick Test Sequence

Test all positions by typing these commands in Arduino Serial Monitor:

```
P  ← Paper (0°)
M  ← Metal (45°)
L  ← Plastic (90°)
G  ← Glass (135°)
T  ← Trash (180°)
```

Each command should:
- Move servo to correct position
- Show confirmation message
- Blink LED on Arduino

## 🎯 Benefits of Manual Control

- **No connection issues** - Arduino IDE handles the serial connection
- **Easy testing** - You can test any position anytime
- **Visual feedback** - See Arduino responses in real-time
- **Full control** - Send commands whenever you want
- **Debugging** - Easy to see if Arduino is responding

## 🚀 Advanced Manual Testing

### Test Specific Materials:
1. **Paper items**: newspaper, cardboard → Send `P`
2. **Metal items**: cans, foil → Send `M`
3. **Plastic items**: bottles, containers → Send `L`
4. **Glass items**: bottles, jars → Send `G`
5. **Trash items**: mixed waste → Send `T`

### Rapid Testing:
- Classify multiple items quickly
- Send commands in sequence
- Watch servo sort into different bins

## 🔧 Troubleshooting

### Servo doesn't move:
- Check wiring: Red→5V, Brown→GND, Orange→Pin9
- Try different servo
- Check power supply

### No Arduino response:
- Check Serial Monitor baud rate (9600)
- Re-upload Arduino code
- Check USB connection

### Wrong servo positions:
- Adjust angles in Arduino code:
```cpp
const int PAPER_ANGLE = 10;    // Instead of 0
const int METAL_ANGLE = 50;    // Instead of 45
// etc.
```

## ✅ Success Checklist

- [ ] Arduino code uploaded successfully
- [ ] Serial Monitor shows "Ready" message
- [ ] All 5 commands (P, M, L, G, T) move servo
- [ ] Web app classifies materials correctly
- [ ] Manual commands work for each classification
- [ ] Servo positions align with physical bins

This manual method gives you complete control and is perfect for testing and demonstrations!