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
        
        # Load models
        self.load_model()
        self.load_detection_model()
    
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
    """Classify current frame."""
    frame = classifier.get_frame()
    if frame is None:
        return jsonify({'error': 'No camera frame available'})
    
    pred_class, confidence = classifier.classify_frame(frame)
    
    if pred_class and confidence > classifier.confidence_threshold:
        result = {
            'success': True,
            'class': pred_class,
            'confidence': round(confidence, 3),
            'arduino_cmd': classifier.cmd_map.get(pred_class, 'T'),
            'color': classifier.colors.get(pred_class, '#FFFFFF')
        }
        classifier.last_prediction = result
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
        'last_prediction': classifier.last_prediction,
        'confidence_threshold': classifier.confidence_threshold,
        'num_classes': len(classifier.classes),
        'classes': classifier.classes
    })

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
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🗂️  Classes: paper, metal, plastic, glass, trash")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        classifier.stop_camera()