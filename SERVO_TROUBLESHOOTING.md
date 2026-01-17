# 🔧 Servo 2 Troubleshooting Guide

## 🚨 **Problem: Second Servo Not Turning**

Let's systematically diagnose and fix the issue with Servo 2 (Pin 10).

## 🔍 **Step 1: Upload Test Code**

1. **Upload the test code**: `arduino_servo_test_individual.ino`
2. **Open Serial Monitor** (9600 baud)
3. **Test each servo individually**

### **Test Commands:**
```
1  ← Test Servo 1 (Pin 9) only
2  ← Test Servo 2 (Pin 10) only
B  ← Test both servos together
S  ← Sweep test for both servos
R  ← Reset both to start position
```

## 🔧 **Step 2: Hardware Checks**

### **Check Servo 2 Wiring:**
```
Servo 2 (Pin 10):
├── Red Wire    → Arduino 5V     ✓ Check connection
├── Brown Wire  → Arduino GND    ✓ Check connection
└── Orange Wire → Arduino Pin 10 ✓ Check connection
```

### **Power Supply Check:**
- **Single Servo Test**: Disconnect Servo 1, test only Servo 2
- **Power Capacity**: Two servos might need external 5V supply
- **Voltage Check**: Measure 5V pin with multimeter

### **Physical Check:**
- **Servo Horn**: Is it attached properly?
- **Mechanical Binding**: Can you move the servo by hand?
- **Servo Health**: Try swapping Servo 1 and Servo 2 positions

## 🔧 **Step 3: Common Issues & Solutions**

### **Issue 1: No Movement at All**
**Possible Causes:**
- Wiring problem (most common)
- Dead servo
- Insufficient power

**Test with minimal code:**
```cpp
#include <Servo.h>
Servo testServo;

void setup() {
  Serial.begin(9600);
  testServo.attach(10);
  Serial.println("Testing Servo 2 on Pin 10");
}

void loop() {
  Serial.println("Moving to 0°");
  testServo.write(0);
  delay(2000);
  
  Serial.println("Moving to 90°");
  testServo.write(90);
  delay(2000);
}
```

### **Issue 2: Servo 1 Works, Servo 2 Doesn't**
**Possible Causes:**
- Pin 10 problem
- Power insufficient for two servos
- Code issue

**Solutions:**
1. **Try different pin**: Change Servo 2 to pin 11
2. **External power**: Use external 5V supply for servos
3. **Test pin**: Use LED on pin 10 to verify pin works

### **Issue 3: Jittery or Weak Movement**
**Possible Causes:**
- Power supply too weak
- Interference between servos

**Solutions:**
1. **External 5V supply** (recommended for dual servos)
2. **Separate power rails**
3. **Add capacitors** (100µF across power lines)

## ⚡ **Step 4: Power Supply Solutions**

### **Option 1: External 5V Supply (Recommended)**
```
External 5V Power Supply (2A or more)
├── +5V → Both servo red wires
├── GND → Both servo brown wires + Arduino GND
└── Arduino pins 9,10 → Servo signal wires only
```

### **Option 2: USB Power Bank**
- Use 5V USB power bank (2A output)
- Cut USB cable or use USB breakout
- More current capacity than Arduino's 5V pin

### **Option 3: Battery Pack**
- 4x AA batteries (6V) with 5V voltage regulator
- Or 3x AA rechargeable (4.8V) direct connection

## 🔧 **Step 5: Alternative Pin Configuration**

If Pin 10 doesn't work, modify the code to use Pin 11:

```cpp
// In arduino_dual_servo_controller.ino, change:
dropFlapServo.attach(11);  // Instead of pin 10

// Update wiring:
// Servo 2 Orange Wire → Arduino Pin 11
```

## 🔧 **Step 6: Quick Diagnostic Tests**

### **Test A: Pin 10 with LED**
```cpp
void setup() {
  pinMode(10, OUTPUT);
}

void loop() {
  digitalWrite(10, HIGH);
  delay(500);
  digitalWrite(10, LOW);
  delay(500);
}
```
**Expected**: LED should blink on pin 10

### **Test B: Servo Swap**
1. **Disconnect both servos**
2. **Connect Servo 2 to Pin 9** (where Servo 1 was)
3. **Test with Servo 1 commands**
4. **If Servo 2 works on Pin 9**: Pin 10 is the problem
5. **If Servo 2 doesn't work on Pin 9**: Servo 2 is broken

### **Test C: Power Consumption**
```cpp
void setup() {
  Serial.begin(9600);
  // Test one servo at a time
}

void loop() {
  Serial.println("Testing power draw...");
  // Monitor if Arduino resets when both servos move
}
```

## 🚨 **Most Likely Solutions**

### **90% of cases: Power Issue**
- **Arduino 5V pin**: Limited to ~500mA
- **Two servos**: Can draw 1000mA+ when moving
- **Solution**: External 5V power supply

### **Hardware Wiring:**
```
External 5V Supply (2A):
┌─────────────┐
│ 5V Power    │
│ Supply      │
└─────────────┘
      │
      ├── +5V ──┬── Servo 1 Red
      │         └── Servo 2 Red
      │
      └── GND ──┬── Servo 1 Brown
                ├── Servo 2 Brown
                └── Arduino GND

Arduino:
├── Pin 9  ──── Servo 1 Orange
└── Pin 10 ──── Servo 2 Orange
```

## ✅ **Testing Checklist**

- [ ] Upload individual servo test code
- [ ] Test Servo 2 alone with command "2"
- [ ] Check all wiring connections
- [ ] Try external 5V power supply
- [ ] Test Servo 2 on different pin (11)
- [ ] Swap servos to test if Servo 2 is broken
- [ ] Check for mechanical binding
- [ ] Verify Arduino pin 10 works with LED test

## 🎯 **Expected Results**

After fixing the issue:
- **Command "2"**: Servo 2 should move 0° → 45° → 90° → 0°
- **Command "B"**: Both servos should work together
- **Full sequence**: Position → Drop → Close → Return

Most servo issues are **power-related**. An external 5V supply usually solves the problem! 🔋