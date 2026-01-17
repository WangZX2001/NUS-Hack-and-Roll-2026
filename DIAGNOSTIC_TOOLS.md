# 🔧 Diagnostic Tools Reference

This project includes several diagnostic tools to help troubleshoot setup and connection issues. Here's when to use each one:

## 🔍 **check_setup.py** - Complete System Verification
**When to use:** Before starting the application for the first time

```bash
python3 check_setup.py
```

**What it checks:**
- ✅ Python version compatibility
- ✅ All Python dependencies installed
- ✅ Essential project files present
- ✅ AI model files available
- ✅ Arduino connection capability
- ✅ Camera access
- ✅ System requirements (RAM, disk space)

**Output:** Pass/fail for each component with specific guidance

---

## 🤖 **arduino_diagnostic.py** - Comprehensive Arduino Analysis
**When to use:** When Arduino connection issues occur

```bash
python3 arduino_diagnostic.py
```

**What it checks:**
- 🖥️ System information and compatibility
- 🐍 Python dependencies (pyserial, psutil, flask)
- 🔌 Serial port detection and analysis
- 🔐 Permissions and user groups
- 🧪 Actual serial connection testing
- 🔍 Process conflicts that might block Arduino
- 💡 Platform-specific solutions and drivers

**Output:** Detailed diagnostic report with specific solutions

---

## ⚡ **check_arduino_connection.py** - Real-time Connection Monitor
**When to use:** To see if Arduino is being detected while connecting/disconnecting

```bash
python3 check_arduino_connection.py
```

**What it does:**
- 🔍 Monitors serial ports in real-time
- ⚡ Shows Arduino detection instantly
- 🧪 Tests actual communication with detected Arduino
- 💡 Perfect for hardware troubleshooting

**Usage:** Run this script, then plug/unplug your Arduino to see if it appears

---

## 🔧 **install_dependencies.py** - Automated Installation
**When to use:** First-time setup or when dependencies are missing

```bash
python3 install_dependencies.py
```

**What it does:**
- 🔄 Upgrades pip to latest version
- 📦 Installs all required Python packages
- 🧪 Verifies installation by testing imports
- 🚀 Creates startup scripts for easy launching
- 💡 Provides fallback installation methods

---

## 🚀 **start_auto_arduino.py** - One-Command Launcher
**When to use:** To start the complete system automatically

```bash
python3 start_auto_arduino.py
```

**What it does:**
- 🔄 Kills any conflicting processes
- 🤖 Starts webapp with auto-Arduino connection
- 🌐 Opens web interface automatically
- 📊 Provides real-time status updates

---

## 📊 **Troubleshooting Workflow**

### **For New Users:**
1. `python3 install_dependencies.py` - Install everything
2. `python3 check_setup.py` - Verify installation
3. `python3 start_auto_arduino.py` - Start the system

### **For Arduino Issues:**
1. `python3 check_arduino_connection.py` - Monitor while connecting
2. `python3 arduino_diagnostic.py` - Full diagnostic if not detected
3. Follow the specific solutions provided

### **For General Issues:**
1. `python3 check_setup.py` - Check overall system health
2. Read `SETUP_GUIDE.md` for detailed instructions
3. Check specific error messages in diagnostic outputs

---

## 🎯 **Quick Reference**

| Problem | Tool to Use | Command |
|---------|-------------|---------|
| First-time setup | install_dependencies.py | `python3 install_dependencies.py` |
| System verification | check_setup.py | `python3 check_setup.py` |
| Arduino not detected | check_arduino_connection.py | `python3 check_arduino_connection.py` |
| Arduino connection fails | arduino_diagnostic.py | `python3 arduino_diagnostic.py` |
| Start the system | start_auto_arduino.py | `python3 start_auto_arduino.py` |

---

## 💡 **Pro Tips**

1. **Always run `check_setup.py` first** - it gives you a complete overview
2. **Use `check_arduino_connection.py` while physically connecting Arduino** - you'll see exactly when it's detected
3. **The diagnostic tools provide copy-paste solutions** - follow their specific recommendations
4. **Each tool is designed for different scenarios** - use the right tool for your specific issue
5. **All tools work on Windows, macOS, and Linux** - they automatically detect your platform

---

## 🆘 **Still Having Issues?**

If the diagnostic tools don't solve your problem:

1. **Check the output carefully** - they provide specific solutions
2. **Try the suggested commands** - copy-paste the recommended fixes
3. **Read SETUP_GUIDE.md** - comprehensive setup instructions
4. **Compare with a working system** - run diagnostics on both
5. **Create a GitHub issue** - include diagnostic output for help

**Remember: Most Arduino issues are hardware-related (USB cable, drivers, or port conflicts) rather than software issues!**