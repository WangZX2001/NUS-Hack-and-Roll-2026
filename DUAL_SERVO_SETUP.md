# 🤖 Dual Servo Setup Guide - Position + Drop Flap System

## 🎯 **System Overview**

Your garbage classification system now uses **two servos** for reliable sorting:

1. **Servo 1 (Pin 9)**: **Positioning Arm** - Swings to correct bin position
2. **Servo 2 (Pin 10)**: **Drop Flap** - Opens to release rubbish into bin

## 🔧 **Hardware Setup**

### **Wiring Connections:**
```
Servo 1 (Positioning Arm):
├── Red Wire    → Arduino 5V
├── Brown Wire  → Arduino GND
└── Orange Wire → Arduino Pin 9

Servo 2 (Drop Flap):
├── Red Wire    → Arduino 5V
├── Brown Wire  → Arduino GND
└── Orange Wire → Arduino Pin 10

Power Supply:
├── Both servos share 5V and GND
└── Consider external 5V supply if servos draw too much current
```

### **Physical Setup:**
```
[Positioning Arm Servo] ──┐
                          │
                    [Drop Flap Servo]
                          │
                    [Rubbish Holder]
                          │
                    [Bin Selection Area]
                     /  |  |  |  \
                   📄  🔩 🥤 🍶 🗑️
                Paper Metal Plastic Glass Trash
```

## 🚀 **Operation Sequence**

### **4-Step Sorting Process:**

```
1. 📍 POSITION: Arm swings to correct bin (0°, 45°, 90°, 135°, or 180°)
   ↓ (0.5 second wait)
2. 📂 DROP: Flap opens 90° to release rubbish
   ↓ (1 second wait for rubbish to fall)
3. 📁 CLOSE: Flap closes back to 0° (ready for next item)
   ↓ (0.3 second wait)
4. 🔄 RETURN: Arm returns to center position (90°)
```

**Total sequence time: ~2.3 seconds**

## 💻 **Arduino Code Setup**

### **Step 1: Upload Dual Servo Code**
1. **Open Arduino IDE**
2. **Load**: `arduino_dual_servo_controller.ino`
3. **Upload to Arduino**
4. **Open Serial Monitor** (9600 baud)

### **Step 2: Test Individual Commands**
Type these commands in Serial Monitor:

```
P  ← Paper sequence (0° → drop → close → center)
M  ← Metal sequence (45° → drop → close → center)
L  ← Plastic sequence (90° → drop → close → center)
G  ← Glass sequence (135° → drop → close → center)
T  ← Trash sequence (180° → drop → close → center)
R  ← Reset both servos to ready position
```

### **Expected Serial Output:**
```
Starting sorting sequence for Plastic
Step 1: Positioning arm to 90° for Plastic
Step 1 complete: Arm positioned
Step 2: Opening drop flap
Step 2 complete: Rubbish dropped
Step 3: Closing drop flap
Step 3 complete: Flap closed
Step 4: Returning arm to center
Step 4 complete: Arm centered
Sorting sequence complete for Plastic
Ready for next item
```

## 🌐 **Web Interface Integration**

### **Start Web Application:**
```bash
python webapp_5class.py
```

### **New User Experience:**
1. **Click "Classify Material"**
2. **See results immediately**: "plastic, Confidence: 0.89"
3. **Watch countdown**: "Dual servo sequence starts in 1 second..."
4. **See sequence**: "Executing: Position → Drop → Close → Return"
5. **Get confirmation**: "Dual servo sequence complete! Rubbish sorted ✅"

### **Manual Control (Backup):**
- Keep Arduino Serial Monitor open
- Type commands when web interface shows results
- Watch full 4-step sequence execute

## ⚡ **Performance & Timing**

| Phase | Duration | Description |
|-------|----------|-------------|
| **Results Display** | 0s | Immediate classification results |
| **Countdown** | 1s | "Sequence starts in 1 second..." |
| **Step 1: Position** | 0.5s | Arm moves to target bin |
| **Step 2: Drop** | 1s | Flap opens, rubbish falls |
| **Step 3: Close** | 0.3s | Flap closes |
| **Step 4: Return** | 0.5s | Arm returns to center |
| **Total Time** | **3.3s** | Complete operation |

## 🎯 **Servo Positions Reference**

### **Positioning Servo (Pin 9):**
- **Paper**: 0° (Far Left)
- **Metal**: 45° (Left)
- **Plastic**: 90° (Center)
- **Glass**: 135° (Right)
- **Trash**: 180° (Far Right)

### **Drop Flap Servo (Pin 10):**
- **Closed**: 0° (Holding rubbish)
- **Open**: 90° (Releasing rubbish)

## 🔧 **Customization Options**

### **Adjust Timing in Arduino Code:**
```cpp
const int POSITION_DELAY = 500;  // Time after positioning (ms)
const int DROP_DELAY = 1000;     // Time flap stays open (ms)
const int RETURN_DELAY = 300;    // Time before returning (ms)
```

### **Adjust Servo Angles:**
```cpp
// Positioning angles
const int PAPER_ANGLE = 10;    // Adjust if needed
const int METAL_ANGLE = 50;    // Adjust if needed
// etc.

// Flap angles
const int FLAP_CLOSED = 0;     // Adjust if needed
const int FLAP_OPEN = 90;      // Adjust if needed
```

## ✅ **Testing Checklist**

### **Hardware Test:**
- [ ] Both servos connected and powered
- [ ] Servo 1 moves to all 5 positions (0°, 45°, 90°, 135°, 180°)
- [ ] Servo 2 opens and closes flap (0° ↔ 90°)
- [ ] No mechanical interference between servos
- [ ] Adequate power supply for both servos

### **Software Test:**
- [ ] Arduino code uploads successfully
- [ ] Serial Monitor shows sequence messages
- [ ] All commands (P, M, L, G, T, R) work
- [ ] Web interface shows dual servo status
- [ ] Manual and automatic control both work

### **Integration Test:**
- [ ] Classification triggers full sequence
- [ ] Positioning happens before flap opens
- [ ] Flap stays open long enough for rubbish to drop
- [ ] System returns to ready state after each operation
- [ ] Multiple classifications work in sequence

## 🚨 **Troubleshooting**

### **Servo 1 doesn't move:**
- Check wiring to pin 9
- Verify power connections
- Test with manual commands

### **Servo 2 doesn't move:**
- Check wiring to pin 10
- Verify power connections
- Test flap mechanism isn't stuck

### **Sequence doesn't complete:**
- Check Serial Monitor for error messages
- Verify both servos are responding
- Check power supply capacity

### **Timing issues:**
- Adjust delay constants in Arduino code
- Ensure mechanical system can keep up
- Check for binding or interference

## 🎉 **Benefits of Dual Servo System**

1. **Reliable Sorting**: Flap ensures rubbish actually drops into bin
2. **Precise Control**: Separate control of positioning and dropping
3. **Consistent Operation**: Same sequence every time
4. **Visual Feedback**: Clear status updates throughout process
5. **Fail-Safe Design**: Manual control always available

Your garbage classification system now has professional-grade mechanical sorting with the dual servo setup! 🚀