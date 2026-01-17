# 🗑️ AI Garbage Classification System

An AI-powered vision system that automatically classifies and sorts waste into **5 material types** using a camera and a trained deep learning model. The system runs through a web interface and can send commands to an **Arduino** for physical sorting hardware.

Built for **Hacker-and-Roll 2026**.

## 🚀 What this project does

1. **Web Interface**: Easy-to-use browser-based camera interface
2. **5-Class Classification**: Identifies waste as:
   * 📄 `paper` (including cardboard)
   * 🔩 `metal` 
   * 🥤 `plastic`
   * 🍶 `glass`
   * 🗑️ `trash`
3. **Real-time Processing**: Live camera feed with instant classification
4. **Arduino Integration**: Automatically controls servo motor to sort waste into bins
5. **High Accuracy**: 97.5% accuracy with proper glass separation

## 🌐 Web Interface

The system features a modern web interface with:
- **Live camera feed** with multiple camera support
- **Optional object detection boxes** with green bounding boxes around detected items
- **Performance optimization** - detection can be toggled on/off for smooth video
- **One-click classification** with visual results
- **Arduino control panel** with port selection and servo testing
- **Automatic servo control** - servo moves to correct bin after classification
- **Confidence threshold adjustment** for optimal performance
- **Color-coded results** for each material type
- **Real-time status monitoring** for camera, Arduino, and AI models
- **Smart frame processing** with automatic quality adjustment

## 🧠 Trained AI Model

The model uses **YOLOv8 Nano (classification)** trained on 2,527 real garbage images with proper 5-class separation. Additionally, **YOLOv8 Nano (detection)** is used for drawing green bounding boxes around detected objects in the camera feed.

**Current model location:**
```
runs/classify/runs/classify/5class_model/weights/best.pt  # Classification model
yolov8n.pt                                               # Detection model (auto-downloaded)
```

**Performance:**
- Overall Accuracy: **97.5%**
- Glass Detection: **100%** ✅
- Metal Detection: **100%** ✅  
- Paper Detection: **100%** ✅
- Trash Detection: **100%** ✅
- Plastic Detection: **87.5%** ✅

## 📁 Project Structure

```
Hacker-and-Roll-2026/
│
├── webapp_5class.py                    # Main web application
├── arduino_servo_controller.ino       # Arduino servo control code
├── ARDUINO_SETUP.md                   # Arduino setup guide
├── create_5_class_dataset.py           # Dataset creation tool
├── test_5class_model.py               # Model testing utility
├── requirements.txt                    # Python dependencies
├── templates/
│   └── index_5class.html              # Web interface template
├── Garbage classification/             # Original source images (6 classes)
│   ├── cardboard/
│   ├── paper/
│   ├── metal/
│   ├── plastic/
│   ├── glass/
│   └── trash/
├── dataset_5class/                     # Processed ML dataset
│   ├── train/                         # Training images (75%)
│   └── val/                           # Validation images (25%)
└── runs/classify/runs/classify/5class_model/
    └── weights/best.pt                # Trained 5-class model
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application
```bash
python webapp_5class.py
```

### 3. Open Your Browser
Navigate to: **http://localhost:5001**

### 4. Use the Interface
1. **Select Camera**: Choose your external webcam
2. **Connect Arduino**: Select Arduino port and connect (see [Arduino Setup Guide](ARDUINO_SETUP.md))
3. **Start Camera**: Begin live video feed (detection boxes disabled by default for performance)
4. **Optional Detection**: Enable bounding boxes if desired (may reduce video smoothness)
5. **Classify**: Point camera at waste item and click "Classify Material"
6. **Automatic Sorting**: Servo motor automatically moves to correct bin position
7. **View Results**: See classification, confidence, Arduino command, and servo angle

## 🎯 Classification System

### Material Classes & Arduino Commands

| Material | Description | Arduino Command | Color Code |
|----------|-------------|-----------------|------------|
| 📄 Paper | Paper + Cardboard | `P` | Green |
| 🔩 Metal | All metal items | `M` | Red |
| 🥤 Plastic | Plastic containers/items | `L` | Orange |
| 🍶 Glass | Glass bottles/containers | `G` | Blue |
| 🗑️ Trash | Non-recyclable waste | `T` | Brown |

### Confidence System
- **High Confidence** (>0.5): Classification displayed with Arduino command
- **Low Confidence** (<0.5): "Low confidence" message, adjustable threshold
- **Real-time Adjustment**: Confidence slider in web interface

## 🔌 Arduino Integration

The system automatically controls a servo motor to sort waste into physical bins.

### Hardware Setup
- **Arduino Uno** with servo motor on pin 9
- **5 bins** positioned at different servo angles
- **USB connection** to computer running the webapp

### Servo Positions & Commands

| Material | Arduino Command | Servo Angle | Bin Position |
|----------|----------------|-------------|--------------|
| 📄 Paper | `P` | 0° | Far Left |
| 🔩 Metal | `M` | 45° | Left |
| 🥤 Plastic | `L` | 90° | Center |
| 🍶 Glass | `G` | 135° | Right |
| 🗑️ Trash | `T` | 180° | Far Right |

### Setup Instructions
See detailed [Arduino Setup Guide](ARDUINO_SETUP.md) for:
- Hardware wiring diagrams
- Arduino code installation
- Troubleshooting tips
- Physical bin positioning

### Web Interface Features
- **Port Detection**: Automatically finds connected Arduino
- **Connection Status**: Real-time Arduino connection monitoring
- **Servo Testing**: Manual servo position testing buttons
- **Automatic Control**: Servo moves automatically after classification

## 🛠 Dataset & Training

### Original Data Structure
```
Garbage classification/          # Source images (2,527 total)
├── cardboard/    (403 images)
├── paper/        (594 images)  
├── metal/        (410 images)
├── plastic/      (482 images)
├── glass/        (501 images)
└── trash/        (137 images)
```

### Processed Dataset
```
dataset_5class/                  # ML-ready dataset
├── train/        (1,892 images, 75%)
│   ├── paper/    (697 images)   # cardboard + paper combined
│   ├── metal/    (307 images)
│   ├── plastic/  (361 images)
│   ├── glass/    (376 images)
│   └── trash/    (103 images)
└── val/          (635 images, 25%)
    ├── paper/    (300 images)
    ├── metal/    (103 images)
    ├── plastic/  (121 images)
    ├── glass/    (125 images)
    └── trash/    (34 images)
```

### Training Process
1. **Data Preparation**: `python create_5_class_dataset.py`
2. **Model Training**: Automatic YOLO training with data augmentation
3. **Validation**: Built-in accuracy testing and confusion matrix
4. **Optimization**: 40 epochs with early stopping and regularization

## 🧪 Testing & Validation

### Test Current Model
```bash
python test_5class_model.py
```

### Create New Dataset
```bash
python create_5_class_dataset.py
```

## 🎯 Key Features

### ✅ Advantages Over 4-Class System
- **Glass Separation**: Glass no longer confused with trash
- **Better Accuracy**: 97.5% vs previous lower accuracy
- **Cleaner Classification**: Each material gets proper recognition
- **Real-world Performance**: Tested on diverse lighting conditions

### 🌐 Web Interface Benefits
- **No Command Line**: Everything through browser
- **Live Preview**: See camera feed in real-time
- **Easy Camera Selection**: Visual camera picker
- **Instant Results**: One-click classification
- **Mobile Friendly**: Works on phones and tablets

### 🔧 Technical Features
- **Multiple Camera Support**: Automatically detects available cameras
- **Optional Object Detection**: Green bounding boxes with performance optimization
- **Smart Frame Processing**: Automatic resolution and quality adjustment
- **Confidence Adjustment**: Real-time threshold tuning
- **Status Monitoring**: Live system health indicators
- **Error Handling**: Graceful failure recovery
- **Performance Optimized**: ~20 FPS video streaming with frame skipping
- **Detection Toggle**: Enable/disable bounding boxes for optimal performance

## 🎉 Results

The 5-class system successfully separates glass from other materials, achieving:
- **Perfect glass detection** (100% accuracy)
- **Excellent overall performance** (97.5% accuracy)
- **Real-world usability** through web interface
- **Arduino-ready commands** for physical sorting

This represents a significant improvement over traditional 4-class systems that group glass with "other" materials.

