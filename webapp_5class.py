#!/usr/bin/env python3
"""
Web-based garbage classification system with 5 classes.
Separates glass from other materials for better sorting.
Now includes object detection with green bounding boxes.
"""

from flask import Flask, render_template, Response, jsonify, request
import cv2
import json
import time
from ultralytics import YOLO
from pathlib import Path
import threading
import base64
import numpy as np
import serial
import serial.tools.list_ports

app = Flask(__name__)

class GarbageClassifier5Class:
    def __init__(self):
        self.model = None
        self.detection_model = None  # For object detection
        self.camera = None
        self.camera_index = 0
        self.is_running = False
        self.last_prediction = None
        self.confidence_threshold = 0.5
        self.detection_enabled = False  # Start with detection disabled for better performance
        self.current_frame_with_boxes = None
        self.frame_skip_counter = 0
        self.detection_frame_skip = 3  # Only run detection every 3rd frame
        
        # Arduino serial connection
        self.arduino = None
        self.arduino_port = None
        self.arduino_connected = False
        
        # 5-class system with separate glass
        self.classes = ["paper", "metal", "plastic", "glass", "trash"]
        self.colors = {
            "paper": "#00FF00",    # Green
            "metal": "#FF0000",    # Red
            "plastic": "#FFA500",  # Orange
            "glass": "#00BFFF",    # Deep Sky Blue
            "trash": "#8B4513"     # Saddle Brown
        }
        self.cmd_map = {
            "paper": "P", 
            "metal": "M", 
            "plastic": "L", 
            "glass": "G", 
            "trash": "T"
        }
        
        # Servo angles for each material (for reference)
        self.servo_angles = {
            "paper": 0,     # Paper bin
            "metal": 45,    # Metal bin
            "plastic": 90,  # Plastic bin
            "glass": 135,   # Glass bin
            "trash": 180    # Trash bin
        }
        
        # Dual servo sequence description
        self.servo_sequence = {
            "paper": "Position to 0° → Open flap → Close flap → Return center",
            "metal": "Position to 45° → Open flap → Close flap → Return center",
            "plastic": "Position to 90° → Open flap → Close flap → Return center",
            "glass": "Position to 135° → Open flap → Close flap → Return center",
            "trash": "Position to 180° → Open flap → Close flap → Return center"
        }
        
        # Load models
        self.load_model()
        self.load_detection_model()
        self.connect_arduino()
    
    def load_detection_model(self):
        """Load YOLO detection model for drawing bounding boxes."""
        try:
            # Use YOLOv8 detection model for general object detection
            self.detection_model = YOLO('yolov8n.pt')  # This will download if not present
            print("✅ Detection model loaded for bounding boxes")
            print("   Detection starts disabled for better performance")
            return True
        except Exception as e:
            print(f"⚠️  Detection model not loaded: {e}")
            print("   Continuing without bounding boxes...")
            self.detection_enabled = False
            return False
    
    def get_available_arduino_ports(self):
        """Get list of available serial ports for Arduino."""
        ports = []
        for port in serial.tools.list_ports.comports():
            # Look for Arduino-like devices
            if any(keyword in port.description.lower() for keyword in ['arduino', 'ch340', 'cp210', 'ftdi', 'usb']):
                ports.append({
                    'port': port.device,
                    'description': port.description,
                    'manufacturer': getattr(port, 'manufacturer', 'Unknown')
                })
        return ports
    
    def connect_arduino(self, port=None):
        """Connect to Arduino via serial."""
        try:
            # Close existing connection
            if self.arduino and self.arduino.is_open:
                self.arduino.close()
                time.sleep(1)  # Give port time to close
            
            if port is None:
                # Auto-detect Arduino port
                available_ports = self.get_available_arduino_ports()
                if not available_ports:
                    print("⚠️  No Arduino ports found")
                    return False
                port = available_ports[0]['port']
            
            print(f"🔌 Attempting to connect to Arduino on {port}...")
            
            # Try to connect with multiple attempts
            for attempt in range(3):
                try:
                    self.arduino = serial.Serial(port, 9600, timeout=3)
                    break
                except serial.SerialException as e:
                    if attempt < 2:
                        print(f"   Attempt {attempt + 1} failed, retrying...")
                        time.sleep(2)
                    else:
                        raise e
            
            # Wait for Arduino to initialize
            print("   Waiting for Arduino to initialize...")
            time.sleep(3)  # Increased wait time
            
            # Test connection
            if self.arduino.is_open:
                self.arduino_port = port
                self.arduino_connected = True
                print(f"✅ Arduino connected on {port}")
                
                # Clear any initial messages and send test
                try:
                    # Clear input buffer
                    self.arduino.reset_input_buffer()
                    
                    # Send a test command to verify communication
                    print("   Testing communication...")
                    self.arduino.write(b'P')  # Test with Paper command
                    time.sleep(1)
                    
                    # Read any responses
                    responses = []
                    while self.arduino.in_waiting > 0:
                        try:
                            message = self.arduino.readline().decode().strip()
                            if message:
                                responses.append(message)
                                print(f"   Arduino: {message}")
                        except:
                            break
                    
                    if responses:
                        print("✅ Arduino communication test successful!")
                    else:
                        print("⚠️  No response from Arduino, but connection established")
                    
                except Exception as comm_error:
                    print(f"⚠️  Communication test failed: {comm_error}")
                    # Don't fail connection for communication test failure
                
                return True
            else:
                print(f"❌ Failed to open Arduino port {port}")
                return False
                
        except serial.SerialException as e:
            print(f"❌ Arduino connection error: {e}")
            if "Access is denied" in str(e) or "PermissionError" in str(e):
                print("   💡 This usually means:")
                print("   - Arduino IDE Serial Monitor is still open")
                print("   - Another program is using the port")
                print("   - Try closing Arduino IDE completely and wait 10 seconds")
            self.arduino_connected = False
            return False
        except Exception as e:
            print(f"❌ Unexpected Arduino error: {e}")
            self.arduino_connected = False
            return False
    
    def send_arduino_command(self, command):
        """Send command to Arduino for dual servo sequence."""
        if not self.arduino_connected or not self.arduino:
            print(f"⚠️  Arduino not connected, command '{command}' not sent")
            return False
        
        try:
            print(f"📡 Sending dual servo command '{command}' to Arduino...")
            print("   Sequence: Position → Drop flap → Close flap → Return center")
            
            # Clear any pending input
            self.arduino.reset_input_buffer()
            
            # Send command
            self.arduino.write(command.encode())
            self.arduino.flush()  # Ensure command is sent immediately
            
            # Wait for Arduino to process the full sequence
            time.sleep(0.5)
            
            # Read all responses from Arduino during sequence
            responses = []
            timeout = time.time() + 5  # 5 second timeout for full sequence
            
            while time.time() < timeout:
                if self.arduino.in_waiting > 0:
                    try:
                        response = self.arduino.readline().decode().strip()
                        if response:
                            responses.append(response)
                            print(f"✅ Arduino: {response}")
                    except Exception as decode_error:
                        print(f"⚠️  Error reading Arduino response: {decode_error}")
                        break
                time.sleep(0.1)
            
            if responses:
                print(f"✅ Dual servo sequence completed with {len(responses)} status updates")
            else:
                print(f"⚠️  No responses from Arduino for dual servo sequence")
            
            return True
            
        except serial.SerialException as e:
            print(f"❌ Serial error sending dual servo command: {e}")
            self.arduino_connected = False
            return False
        except Exception as e:
            print(f"❌ Error sending dual servo command: {e}")
            return False
    
    def disconnect_arduino(self):
        """Disconnect from Arduino."""
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            self.arduino_connected = False
            print("🔌 Arduino disconnected")
    
    def load_model(self):
        """Load the trained model."""
        # Try 5-class model first, then fall back to 4-class
        model_paths = [
            "runs/classify/runs/classify/5class_model/weights/best.pt",  # Actual 5-class model location
            "runs/classify/5class_model/weights/best.pt",  # Expected location
            "runs/classify/improved_model/weights/best.pt",
            "runs/classify/train2/weights/best.pt"
        ]
        
        for model_path in model_paths:
            if Path(model_path).exists():
                try:
                    self.model = YOLO(model_path)
                    print(f"✅ Model loaded from {model_path}")
                    
                    # Check if model supports 5 classes
                    if hasattr(self.model, 'names') and len(self.model.names) == 5:
                        print("🎯 Using 5-class model (with separate glass)")
                    elif len(self.model.names) == 4:
                        print("⚠️  Using 4-class model (glass grouped with 'other')")
                        # Adjust classes for 4-class model
                        self.classes = ["paper", "metal", "plastic", "other"]
                        self.colors["other"] = "#8B4513"
                        self.cmd_map["other"] = "T"
                        del self.colors["glass"]
                        del self.colors["trash"]
                        del self.cmd_map["glass"]
                        del self.cmd_map["trash"]
                    
                    return True
                except Exception as e:
                    print(f"❌ Error loading model from {model_path}: {e}")
                    continue
        
        print("❌ No working model found")
        return False
    
    def get_available_cameras(self):
        """Get list of available cameras."""
        cameras = []
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                ret, _ = cap.read()
                status = "Working" if ret else "Not working"
                cameras.append({
                    'index': i,
                    'resolution': f"{width}x{height}",
                    'status': status,
                    'working': ret
                })
                cap.release()
        return cameras
    
    def start_camera(self, camera_index=0):
        """Start the camera."""
        if self.camera:
            self.camera.release()
        
        self.camera = cv2.VideoCapture(camera_index)
        if self.camera.isOpened():
            self.camera_index = camera_index
            self.is_running = True
            print(f"✅ Camera {camera_index} started")
            return True
        else:
            print(f"❌ Failed to start camera {camera_index}")
            return False
    
    def stop_camera(self):
        """Stop the camera."""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
        print("🛑 Camera stopped")
    
    def get_frame(self):
        """Get current camera frame."""
        if not self.camera or not self.is_running:
            return None
        
        ret, frame = self.camera.read()
        if ret:
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Add detection boxes if enabled (with frame skipping for performance)
            if self.detection_enabled and self.detection_model:
                self.frame_skip_counter += 1
                if self.frame_skip_counter >= self.detection_frame_skip:
                    frame = self.add_detection_boxes(frame)
                    self.frame_skip_counter = 0
            
            self.current_frame_with_boxes = frame.copy()
            return frame
        return None
    
    def add_detection_boxes(self, frame):
        """Add green detection boxes around detected objects."""
        try:
            # Resize frame for faster detection, then scale back
            height, width = frame.shape[:2]
            detection_size = 416  # Smaller size for faster detection
            scale = min(detection_size / width, detection_size / height)
            
            if scale < 1.0:
                new_width = int(width * scale)
                new_height = int(height * scale)
                small_frame = cv2.resize(frame, (new_width, new_height))
            else:
                small_frame = frame
                scale = 1.0
            
            # Run detection on smaller frame
            results = self.detection_model(small_frame, verbose=False, conf=0.4)
            
            if len(results) > 0 and results[0].boxes is not None:
                boxes = results[0].boxes
                
                for box in boxes:
                    # Get box coordinates and scale back to original size
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    confidence = box.conf[0].cpu().numpy()
                    
                    # Scale coordinates back to original frame size
                    if scale < 1.0:
                        x1, y1, x2, y2 = int(x1/scale), int(y1/scale), int(x2/scale), int(y2/scale)
                    
                    # Only draw boxes for objects with reasonable confidence
                    if confidence > 0.4:
                        # Draw green bounding box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        # Add simple confidence text (smaller font for performance)
                        label = f"{confidence:.1f}"
                        cv2.putText(frame, label, (x1, y1 - 5), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        except Exception as e:
            print(f"Detection error: {e}")
        
        return frame
    
    def classify_frame(self, frame):
        """Classify the current frame."""
        if not self.model:
            return None, 0.0
        
        try:
            # Use the original frame without detection boxes for classification
            original_frame = cv2.flip(self.camera.read()[1], 1) if self.camera else frame
            
            results = self.model(original_frame, verbose=False)
            if len(results) > 0 and results[0].probs is not None:
                pred_class = results[0].names[results[0].probs.top1]
                confidence = results[0].probs.top1conf.item()
                return pred_class, confidence
        except Exception as e:
            print(f"Classification error: {e}")
        
        return None, 0.0

# Global classifier instance
classifier = GarbageClassifier5Class()

@app.route('/')
def index():
    """Main page."""
    return render_template('index_5class.html')

@app.route('/api/cameras')
def get_cameras():
    """Get available cameras."""
    cameras = classifier.get_available_cameras()
    return jsonify(cameras)

@app.route('/api/start_camera', methods=['POST'])
def start_camera():
    """Start camera with specified index."""
    data = request.get_json()
    camera_index = data.get('camera_index', 0)
    
    success = classifier.start_camera(camera_index)
    return jsonify({'success': success, 'camera_index': camera_index})

@app.route('/api/stop_camera', methods=['POST'])
def stop_camera():
    """Stop the camera."""
    classifier.stop_camera()
    return jsonify({'success': True})

@app.route('/api/classify', methods=['POST'])
def classify():
    """Classify current frame and optionally send Arduino command with delay."""
    frame = classifier.get_frame()
    if frame is None:
        return jsonify({'error': 'No camera frame available'})
    
    pred_class, confidence = classifier.classify_frame(frame)
    
    if pred_class and confidence > classifier.confidence_threshold:
        arduino_cmd = classifier.cmd_map.get(pred_class, 'T')
        
        # Create result immediately (before Arduino command)
        result = {
            'success': True,
            'class': pred_class,
            'confidence': round(confidence, 3),
            'arduino_cmd': arduino_cmd,
            'arduino_sent': False,  # Will be updated after delay
            'servo_angle': classifier.servo_angles.get(pred_class, 90),
            'color': classifier.colors.get(pred_class, '#FFFFFF')
        }
        
        # Store result for status updates
        classifier.last_prediction = result
        
        # Send Arduino command after a shorter delay (if connected)
        if classifier.arduino_connected:
            # Use threading to send command after delay without blocking response
            import threading
            def delayed_arduino_command():
                time.sleep(1.0)  # 1 second delay for results to display first
                arduino_success = classifier.send_arduino_command(arduino_cmd)
                # Update the stored result
                if hasattr(classifier, 'last_prediction') and classifier.last_prediction:
                    classifier.last_prediction['arduino_sent'] = arduino_success
            
            # Start delayed command in background
            threading.Thread(target=delayed_arduino_command, daemon=True).start()
        
        return jsonify(result)
    else:
        result = {
            'success': False,
            'message': f'Low confidence: {confidence:.3f}' if pred_class else 'No detection'
        }
        return jsonify(result)

@app.route('/api/status')
def get_status():
    """Get current system status."""
    return jsonify({
        'camera_running': classifier.is_running,
        'camera_index': classifier.camera_index,
        'model_loaded': classifier.model is not None,
        'detection_enabled': classifier.detection_enabled,
        'detection_model_loaded': classifier.detection_model is not None,
        'arduino_connected': classifier.arduino_connected,
        'arduino_port': classifier.arduino_port,
        'last_prediction': classifier.last_prediction,
        'confidence_threshold': classifier.confidence_threshold,
        'num_classes': len(classifier.classes),
        'classes': classifier.classes
    })

@app.route('/api/arduino/ports')
def get_arduino_ports():
    """Get available Arduino ports."""
    ports = classifier.get_available_arduino_ports()
    return jsonify(ports)

@app.route('/api/arduino/connect', methods=['POST'])
def connect_arduino():
    """Connect to Arduino."""
    data = request.get_json()
    port = data.get('port', None)
    
    success = classifier.connect_arduino(port)
    return jsonify({
        'success': success,
        'connected': classifier.arduino_connected,
        'port': classifier.arduino_port
    })

@app.route('/api/arduino/disconnect', methods=['POST'])
def disconnect_arduino():
    """Disconnect from Arduino."""
    classifier.disconnect_arduino()
    return jsonify({'success': True, 'connected': False})

@app.route('/api/arduino/test', methods=['POST'])
def test_arduino():
    """Test Arduino connection by sending a command."""
    data = request.get_json()
    command = data.get('command', 'P')
    
    success = classifier.send_arduino_command(command)
    return jsonify({'success': success, 'command_sent': command})

@app.route('/api/toggle_detection', methods=['POST'])
def toggle_detection():
    """Toggle object detection boxes."""
    data = request.get_json()
    enabled = data.get('enabled', True)
    
    if classifier.detection_model is not None:
        classifier.detection_enabled = enabled
        return jsonify({'success': True, 'detection_enabled': classifier.detection_enabled})
    else:
        return jsonify({'success': False, 'message': 'Detection model not available'})

@app.route('/api/set_confidence', methods=['POST'])
def set_confidence():
    """Set confidence threshold."""
    data = request.get_json()
    threshold = data.get('threshold', 0.5)
    classifier.confidence_threshold = max(0.1, min(1.0, threshold))
    return jsonify({'success': True, 'threshold': classifier.confidence_threshold})

def generate_frames():
    """Generate video frames for streaming."""
    while True:
        if classifier.is_running:
            frame = classifier.get_frame()
            if frame is not None:
                # Reduce frame size for streaming to improve performance
                height, width = frame.shape[:2]
                if width > 640:  # Limit max width for streaming
                    scale = 640 / width
                    new_width = 640
                    new_height = int(height * scale)
                    frame = cv2.resize(frame, (new_width, new_height))
                
                # Encode frame as JPEG with lower quality for better performance
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 75]  # Reduced quality
                ret, buffer = cv2.imencode('.jpg', frame, encode_param)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.05)  # Reduced to ~20 FPS for better performance

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("🌐 Starting 5-Class Garbage Classification Web App...")
    print("📱 Open your browser and go to: http://localhost:5001")
    print("git 🗂️  Classes: paper, metal, plastic, glass, trash")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        classifier.stop_camera()