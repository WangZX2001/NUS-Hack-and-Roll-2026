# 🚀 Complete Setup Guide for New Users

Welcome! This guide will help you set up the AI Garbage Classification System from scratch, even if you're new to Python or Arduino projects.

## 📋 Prerequisites Check

Before starting, make sure you have:

### 🖥️ **System Requirements**
- **Operating System**: Windows 10+, macOS 10.14+, or Linux Ubuntu 18.04+
- **RAM**: At least 4GB (8GB recommended)
- **Storage**: 2GB free space
- **USB Port**: For Arduino connection
- **Camera**: Built-in webcam or external USB camera

### 🛠️ **Hardware Requirements**
- **Arduino Uno** (or compatible board)
- **2x Servo Motors** (SG90 or similar)
- **USB Cable** (Arduino to computer - **must be data cable, not power-only**)
- **Jumper Wires** for servo connections
- **Breadboard** (optional, for cleaner connections)

---

## 🐍 Step 1: Install Python

### **Windows:**
1. Go to [python.org/downloads](https://python.org/downloads)
2. Download Python 3.8 or newer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

### **macOS:**
1. **Option A - Official Installer:**
   - Go to [python.org/downloads](https://python.org/downloads)
   - Download and install Python 3.8+
   
2. **Option B - Homebrew (Recommended):**
   ```bash
   # Install Homebrew first if you don't have it
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python
   brew install python
   ```

3. Verify installation:
   ```bash
   python3 --version
   pip3 --version
   ```

### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

---

## 📁 Step 2: Download the Project

### **Option A - Download ZIP (Easiest):**
1. Go to the project GitHub page
2. Click green "Code" button → "Download ZIP"
3. Extract to a folder like `Desktop/garbage-classifier`

### **Option B - Git Clone:**
```bash
git clone <repository-url>
cd <project-folder>
```

---

## 🔧 Step 3: Install Dependencies

Open terminal/command prompt in the project folder and run:

### **Windows:**
```cmd
# Navigate to project folder
cd path\to\your\project

# Install dependencies
pip install -r requirements.txt
```

### **macOS/Linux:**
```bash
# Navigate to project folder
cd path/to/your/project

# Install dependencies
pip3 install -r requirements.txt
```

### 🚨 **Common Installation Issues & Solutions:**

#### **Issue: "pip not found" or "python not found"**
- **Windows**: Reinstall Python with "Add to PATH" checked
- **macOS**: Use `python3` and `pip3` instead of `python` and `pip`
- **Linux**: Install with `sudo apt install python3-pip`

#### **Issue: Permission denied**
- **Windows**: Run Command Prompt as Administrator
- **macOS/Linux**: Use `pip3 install --user -r requirements.txt`

#### **Issue: "Microsoft Visual C++ required" (Windows)**
- Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Or install [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/)

#### **Issue: Long installation time**
- This is normal! The AI libraries (PyTorch, OpenCV) are large
- Wait 10-15 minutes for complete installation

---

## 🤖 Step 4: Arduino Setup

### **4.1 Install Arduino IDE**

#### **Windows:**
1. Go to [arduino.cc/software](https://arduino.cc/software)
2. Download and install Arduino IDE
3. This installs necessary USB drivers

#### **macOS:**
```bash
# Using Homebrew (recommended)
brew install --cask arduino-ide

# Or download from arduino.cc/software
```

#### **Linux:**
```bash
# Ubuntu/Debian
sudo apt install arduino

# Or download from arduino.cc/software
```

### **4.2 Upload Arduino Code**

1. **Connect Arduino** to computer via USB
2. **Open Arduino IDE**
3. **Open the sketch**: `arduino_dual_servo_controller/arduino_dual_servo_controller.ino`
4. **Select Board**: Tools → Board → Arduino Uno
5. **Select Port**: Tools → Port → (select your Arduino port)
6. **Upload**: Click upload button (→)

### **4.3 Hardware Wiring**

Connect servos to Arduino:
```
Servo 1 (Position):     Servo 2 (Drop Flap):
- Red → 5V             - Red → 5V  
- Brown → GND          - Brown → GND
- Orange → Pin 9       - Orange → Pin 10
```

### **🚨 Arduino Troubleshooting:**

#### **Issue: Arduino not detected**
- **Check USB cable**: Must be data cable, not power-only
- **Try different USB port**
- **Real-time monitoring**: Run `python3 check_arduino_connection.py` while connecting Arduino
- **Install drivers**: 
  - Windows: Arduino IDE installs them automatically
  - macOS: May need [CH340 drivers](https://www.wch.cn/downloads/CH341SER_MAC_ZIP.html) for clones
  - Linux: Add user to dialout group: `sudo usermod -a -G dialout $USER`

#### **Issue: Upload failed**
- **Close Serial Monitor** if open
- **Press Arduino reset button** before upload
- **Check board and port selection** in Arduino IDE

#### **Issue: Permission denied (Linux/macOS)**
```bash
# Linux
sudo usermod -a -G dialout $USER
# Then logout and login again

# macOS - usually no permission issues
```

---

## 🎯 Step 5: Run the System

### **5.1 Quick Start (Recommended)**

Run the automatic setup script:

#### **Windows:**
```cmd
python start_auto_arduino.py
```

#### **macOS/Linux:**
```bash
python3 start_auto_arduino.py
```

This will:
- ✅ Check all dependencies
- ✅ Kill any conflicting processes  
- ✅ Start the web application
- ✅ Automatically connect to Arduino
- ✅ Open your browser to the interface

### **5.2 Manual Start**

If you prefer manual control:

#### **Windows:**
```cmd
python webapp_5class.py
```

#### **macOS/Linux:**
```bash
python3 webapp_5class.py
```

Then open your browser to: **http://localhost:5001**

---

## 🌐 Step 6: Using the Web Interface

1. **Check Status**: Look for green indicators showing:
   - ✅ Model: Ready
   - ✅ Arduino: Connected
   - ✅ Classes: 5 (with glass)

2. **Select Camera**: 
   - Click "Refresh Cameras"
   - Select your camera from the list
   - Click "Start Camera"

3. **Test Classification**:
   - Point camera at a piece of waste
   - Click "Classify Material"
   - Watch Arduino automatically sort the item!

4. **Adjust Settings**:
   - Use confidence slider for sensitivity
   - Toggle detection boxes on/off
   - Test individual servo positions

---

## 🔍 Step 7: Troubleshooting

### **Run Diagnostics**

If something isn't working, we have two diagnostic tools:

#### **Full System Diagnostic:**
```bash
python3 arduino_diagnostic.py
```
This comprehensive tool checks:
- ✅ Python dependencies
- ✅ Arduino connection
- ✅ Serial ports
- ✅ Permissions
- ✅ Common issues
- ✅ Provides specific solutions

#### **Real-time Connection Monitor:**
```bash
python3 check_arduino_connection.py
```
This tool monitors Arduino connection in real-time:
- 🔍 Shows all serial ports as they appear/disappear
- ⚡ Detects Arduino connection instantly
- 🧪 Tests actual communication with Arduino
- 💡 Perfect for troubleshooting connection issues

**Use the connection monitor while plugging/unplugging Arduino to see if it's being detected!**

### **Common Issues & Solutions**

#### **🚨 "No module named 'torch'"**
```bash
# Reinstall PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### **🚨 "Camera not found"**
- Check camera permissions in system settings
- Try different camera index in web interface
- Restart browser/application

#### **🚨 "Arduino not connecting"**
- Run `python3 check_arduino_connection.py` while connecting Arduino
- Run `python3 arduino_diagnostic.py` for full system check
- Try different USB cable (data cable, not power-only)
- Check Arduino IDE can connect to same port

#### **🚨 "Port already in use"**
- Close Arduino IDE Serial Monitor
- Kill other Python processes: `pkill -f python`
- Restart computer if needed

#### **🚨 Web interface won't load**
- Check if port 5001 is free: `lsof -i :5001` (macOS/Linux)
- Try different port: edit `webapp_5class.py` and change `port=5001`
- Check firewall settings

---

## 📚 Additional Resources

### **Learning Resources**
- [Python Basics](https://python.org/about/gettingstarted/)
- [Arduino Getting Started](https://arduino.cc/en/Guide)
- [OpenCV Python Tutorial](https://opencv-python-tutroals.readthedocs.io/)

### **Hardware Suppliers**
- **Arduino Uno**: [Arduino Store](https://store.arduino.cc/), Amazon, local electronics stores
- **Servo Motors**: SG90 micro servos work great
- **USB Cables**: Make sure they're data cables, not power-only

### **Community Support**
- Create GitHub issues for bugs
- Check existing issues for solutions
- Join our Discord/Slack for real-time help

---

## ✅ Success Checklist

Before considering setup complete, verify:

- [ ] Python 3.8+ installed and working
- [ ] All dependencies installed without errors
- [ ] Arduino IDE installed and can connect to Arduino
- [ ] Arduino code uploaded successfully
- [ ] Servos connected and moving during test
- [ ] Web application starts without errors
- [ ] Camera detected and working in web interface
- [ ] Arduino auto-connects (green status indicator)
- [ ] Classification works and Arduino responds
- [ ] All 5 material types recognized correctly

---

## 🎉 You're Ready!

Congratulations! Your AI Garbage Classification System is now set up and ready to use. 

### **Next Steps:**
1. **Test with different materials** to see the 5-class classification
2. **Adjust confidence threshold** for optimal performance  
3. **Position your bins** according to servo angles
4. **Show off your project** at the hackathon! 🏆

### **Need Help?**
- Run `python3 arduino_diagnostic.py` for automated troubleshooting
- Check the main `README.md` for detailed technical information
- Create an issue on GitHub if you find bugs

**Happy Hacking! 🚀**