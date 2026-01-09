# 🗑️ AI Trash Sorting System

An AI-powered vision system that automatically classifies and sorts waste into **paper, metal, plastic, and other** using a camera and a trained deep learning model.
The model runs locally on a laptop and sends commands to an **Arduino** to control physical sorting hardware.

Built for **Hacker-and-Roll 2026**.

## 🚀 What this project does

1. Captures an image of a waste item
2. Uses a trained AI model to classify it as:

   * `paper`
   * `metal`
   * `plastic`
   * `other`
3. Applies confidence-based safety logic
4. Sends a one-letter command to an Arduino to activate the correct bin

## 🧠 Trained AI Model

The model was trained using **YOLOv8 Nano (classification)** on real garbage images.

Your trained model is stored here:

```
runs/classify/train2/weights/best.pt
```

This file contains all the learned visual features for recognizing trash types.
It is the **core AI brain** of the system.

## 📁 Project Structure

```
Hacker-and-Roll-2026/
│
├── prepare_dataset.py        # Converts raw garbage dataset into 4-class format
├── train.py                  # Trains the classifier
├── trash_logic.py            # Confidence + ambiguity decision logic
├── test_images_runner.py     # Runs the model on real images
├── runs/
│   └── classify/train2/weights/best.pt   # Trained AI model
└── README.md
```

## 🧪 How the AI decides

For each image, the model outputs probabilities for the 4 classes.

Two safety rules are applied:

* **Low confidence** → send to `other`
* **Ambiguous result** → send to `other`

This prevents incorrect or unsafe sorting.

## 📸 Test on real images

To test the trained model on real photos:

```bash
yolo classify predict model=runs/classify/train2/weights/best.pt source=dataset/val
```

Or run the Python test pipeline:

```bash
python test_images_runner.py
```

This prints:

* predicted class
* confidence
* decision reason

## 🔌 Arduino control

The laptop sends one-character commands via serial:

| Waste Type | Arduino Signal |
| ---------- | -------------- |
| paper      | `P`            |
| metal      | `M`            |
| plastic    | `L`            |
| other      | `X`            |

The Arduino moves a gate or servo based on this signal to drop the item into the correct bin.

## 🛠 How the model was trained

Raw dataset:

```
Garbage classification/
  cardboard/
  glass/
  metal/
  plastic/
  trash/
```

Mapping:

* `cardboard` → `paper`
* `metal` → `metal`
* `plastic` → `plastic`
* `glass` + `trash` → `other`

Converted into:

```
dataset/train/
dataset/val/
```

Training command:

```bash
yolo classify train model=yolov8n-cls.pt data=dataset epochs=30 imgsz=224
```

