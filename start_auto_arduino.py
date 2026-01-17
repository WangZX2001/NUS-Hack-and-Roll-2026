#!/usr/bin/env python3
"""
Enhanced startup script for garbage classification with automatic Arduino connection.
This script ensures clean startup and automatic Arduino connection.
"""

import subprocess
import sys
import time
import os

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def kill_existing_processes():
    """Kill any existing webapp processes."""
    print("🔍 Checking for existing webapp processes...")
    try:
        import psutil
        killed_count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    if cmdline and any('webapp_5class.py' in str(cmd) for cmd in cmdline):
                        print(f"   Terminating existing webapp PID {proc.info['pid']}")
                        proc.terminate()
                        proc.wait(timeout=3)
                        killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if killed_count > 0:
            print(f"✅ Terminated {killed_count} existing processes")
            time.sleep(2)
        else:
            print("✅ No existing processes found")
            
    except ImportError:
        print("⚠️  psutil not available, skipping process cleanup")

def start_webapp():
    """Start the webapp with automatic Arduino connection."""
    print("🚀 Starting garbage classification webapp...")
    print("🤖 Arduino auto-connection: ENABLED")
    print("📱 Web interface will be available at: http://localhost:5001")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        # Start the webapp
        subprocess.run([sys.executable, "webapp_5class.py"])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error starting webapp: {e}")

def main():
    print("🗑️  AI Garbage Classification - Auto Arduino Startup")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not os.path.exists("webapp_5class.py"):
        print("❌ webapp_5class.py not found in current directory")
        print("   Please run this script from the project root directory")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Kill existing processes
    kill_existing_processes()
    
    # Start webapp
    start_webapp()
    
    return True

if __name__ == "__main__":
    main()