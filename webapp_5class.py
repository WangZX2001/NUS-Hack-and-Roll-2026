#!/usr/bin/env python3
"""
Web-based garbage classification system with 5 classes.
Separates glass from other materials for better sorting.
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
        self.camera = None
        self.camera_index = 0
        self.is_running = False
        self.last_prediction = None
        self.confidence_threshold = 0.5
        
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
        
        # Load model
        self.load_model()
    
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
            return frame
        return None
    
    def classify_frame(self, frame):
        """Classify the current frame."""
        if not self.model:
            return None, 0.0
        
        try:
            results = self.model(frame, verbose=False)
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
        'last_prediction': classifier.last_prediction,
        'confidence_threshold': classifier.confidence_threshold,
        'num_classes': len(classifier.classes),
        'classes': classifier.classes
    })

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
                # Encode frame as JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.033)  # ~30 FPS

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