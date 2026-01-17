#!/usr/bin/env python3
"""
Create a 5-class dataset separating glass from other materials.
Classes: paper, metal, plastic, glass, trash
"""

import os
import shutil
from pathlib import Path
import random

def create_5_class_dataset():
    """Create dataset with 5 distinct classes including separate glass."""
    print("🔄 Creating 5-class dataset (paper, metal, plastic, glass, trash)...")
    
    src_dir = Path("Garbage classification")
    dst_dir = Path("dataset_5class")
    
    # Remove old dataset if exists
    if dst_dir.exists():
        shutil.rmtree(dst_dir)
        print("🗑️  Removed old dataset")
    
    # Create new structure with 5 classes
    classes = ['paper', 'metal', 'plastic', 'glass', 'trash']
    for split in ['train', 'val']:
        for class_name in classes:
            (dst_dir / split / class_name).mkdir(parents=True, exist_ok=True)
    
    # New mapping - separate glass from trash
    class_mapping = {
        'cardboard': 'paper',    # Cardboard goes to paper
        'paper': 'paper',        # Paper stays paper
        'metal': 'metal',        # Metal stays metal
        'plastic': 'plastic',    # Plastic stays plastic
        'glass': 'glass',        # Glass gets its own class
        'trash': 'trash'         # Trash gets its own class
    }
    
    # Copy files with 75/25 split for better training data
    random.seed(42)
    total_files = 0
    
    print("\n📊 Processing classes:")
    for original_class, new_class in class_mapping.items():
        class_dir = src_dir / original_class
        if not class_dir.exists():
            print(f"⚠️  {original_class} directory not found")
            continue
            
        # Get all image files
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png']:
            image_files.extend(list(class_dir.glob(ext)))
        
        if not image_files:
            print(f"⚠️  No images found in {original_class}")
            continue
        
        # Shuffle and split (75% train, 25% val)
        random.shuffle(image_files)
        split_idx = int(len(image_files) * 0.75)
        
        train_files = image_files[:split_idx]
        val_files = image_files[split_idx:]
        
        # Copy training files
        for img_file in train_files:
            dst_path = dst_dir / 'train' / new_class / img_file.name
            shutil.copy2(img_file, dst_path)
        
        # Copy validation files  
        for img_file in val_files:
            dst_path = dst_dir / 'val' / new_class / img_file.name
            shutil.copy2(img_file, dst_path)
        
        total_files += len(image_files)
        print(f"✅ {original_class:>9} -> {new_class:>7}: {len(train_files):>3} train, {len(val_files):>3} val")
    
    print(f"\n📈 Dataset Summary:")
    print(f"   Total images: {total_files}")
    print(f"   Classes: {len(classes)}")
    print(f"   Location: {dst_dir}")
    
    # Show final class distribution
    print(f"\n📊 Final class distribution:")
    for split in ['train', 'val']:
        print(f"  {split.upper()}:")
        for class_name in classes:
            class_dir = dst_dir / split / class_name
            if class_dir.exists():
                count = len(list(class_dir.glob('*.jpg')))
                print(f"    {class_name:>7}: {count:>3} images")
    
    return dst_dir

def train_5_class_yolo_model(dataset_path):
    """Train YOLO model with 5 classes."""
    print("\n🤖 Training 5-class YOLO model...")
    
    try:
        from ultralytics import YOLO
        
        # Load YOLOv8 nano model
        model = YOLO('yolov8n-cls.pt')
        
        # Training parameters optimized for 5 classes
        results = model.train(
            data=str(dataset_path),
            epochs=40,
            imgsz=224,
            batch=32,
            lr0=0.001,
            weight_decay=0.0005,
            warmup_epochs=5,
            patience=15,
            
            # Data augmentation
            hsv_h=0.015,
            hsv_s=0.6,
            hsv_v=0.4,
            degrees=15,
            translate=0.1,
            scale=0.2,
            fliplr=0.5,
            flipud=0.0,
            mixup=0.05,  # Light mixup
            
            # Project settings
            project='runs/classify',
            name='5class_model',
            verbose=True
        )
        
        print("✅ YOLO training completed!")
        return results
        
    except ImportError:
        print("❌ Ultralytics not installed. Install with: pip install ultralytics")
        return None

def test_5_class_model():
    """Test the 5-class model."""
    model_path = "runs/classify/5class_model/weights/best.pt"
    
    if not Path(model_path).exists():
        print("❌ 5-class model not found")
        return
    
    print("\n🧪 Testing 5-class model...")
    
    try:
        from ultralytics import YOLO
        model = YOLO(model_path)
        
        # Test on validation images
        val_dir = Path("dataset_5class/val")
        classes = ['paper', 'metal', 'plastic', 'glass', 'trash']
        
        overall_results = {}
        
        for class_name in classes:
            class_dir = val_dir / class_name
            if not class_dir.exists():
                continue
                
            image_files = list(class_dir.glob('*.jpg'))[:10]  # Test 10 per class
            
            if not image_files:
                continue
            
            print(f"\n🔍 Testing {class_name} ({len(image_files)} images):")
            correct = 0
            confidences = []
            
            for img_path in image_files:
                try:
                    results = model(img_path, verbose=False)
                    if results and len(results) > 0:
                        pred_class = results[0].names[results[0].probs.top1]
                        confidence = results[0].probs.top1conf.item()
                        confidences.append(confidence)
                        
                        status = "✅" if pred_class == class_name else "❌"
                        if pred_class == class_name:
                            correct += 1
                        
                        print(f"   {status} {img_path.name}: {pred_class} ({confidence:.3f})")
                except Exception as e:
                    print(f"   ❌ Error: {e}")
            
            accuracy = correct / len(image_files) * 100 if image_files else 0
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            overall_results[class_name] = {
                'accuracy': accuracy,
                'confidence': avg_confidence,
                'tested': len(image_files),
                'correct': correct
            }
            
            print(f"   📊 {class_name} accuracy: {accuracy:.1f}% (avg conf: {avg_confidence:.3f})")
        
        # Overall summary
        if overall_results:
            total_correct = sum(r['correct'] for r in overall_results.values())
            total_tested = sum(r['tested'] for r in overall_results.values())
            overall_accuracy = total_correct / total_tested * 100 if total_tested > 0 else 0
            
            print(f"\n📈 OVERALL RESULTS:")
            print(f"   Total accuracy: {overall_accuracy:.1f}% ({total_correct}/{total_tested})")
            
            # Show per-class results
            for class_name, results in overall_results.items():
                print(f"   {class_name:>7}: {results['accuracy']:>5.1f}%")
        
        return overall_results
        
    except ImportError:
        print("❌ Ultralytics not installed")
        return None

def update_webapp_for_5_classes():
    """Show instructions to update webapp for 5 classes."""
    print("\n🌐 WEBAPP UPDATE INSTRUCTIONS:")
    print("=" * 50)
    
    print("1. Update webapp.py classes:")
    print('   classes = ["paper", "metal", "plastic", "glass", "trash"]')
    
    print("\n2. Update Arduino command mapping:")
    print('   cmd_map = {')
    print('       "paper": "P",')
    print('       "metal": "M",')
    print('       "plastic": "L",')
    print('       "glass": "G",')
    print('       "trash": "T"')
    print('   }')
    
    print("\n3. Update colors:")
    print('   colors = {')
    print('       "paper": "#00FF00",    # Green')
    print('       "metal": "#FF0000",    # Red')
    print('       "plastic": "#FFA500",  # Orange')
    print('       "glass": "#00BFFF",    # Deep Sky Blue')
    print('       "trash": "#8B4513"     # Saddle Brown')
    print('   }')
    
    print("\n4. Update model path in webapp.py:")
    print('   model_paths = [')
    print('       "runs/classify/5class_model/weights/best.pt",')
    print('       "runs/classify/train2/weights/best.pt"  # fallback')
    print('   ]')

def main():
    print("🗂️  5-CLASS GARBAGE CLASSIFICATION SETUP")
    print("=" * 50)
    print("Creating separate classes for: paper, metal, plastic, glass, trash")
    
    # Step 1: Create 5-class dataset
    dataset_path = create_5_class_dataset()
    
    # Step 2: Train YOLO model
    print(f"\n🤖 Ready to train 5-class model...")
    train_choice = input("Train YOLO model now? (y/n): ").lower().strip()
    
    if train_choice == 'y':
        results = train_5_class_yolo_model(dataset_path)
        
        if results:
            # Step 3: Test the model
            test_results = test_5_class_model()
            
            if test_results:
                # Step 4: Show webapp update instructions
                update_webapp_for_5_classes()
                
                print(f"\n🎯 SUCCESS!")
                print(f"✅ 5-class dataset created")
                print(f"✅ Model trained and tested")
                print(f"📁 Model location: runs/classify/5class_model/weights/best.pt")
                print(f"\n🚀 Next steps:")
                print(f"1. Update webapp.py with the code shown above")
                print(f"2. Run: python webapp.py")
                print(f"3. Test glass classification!")
            else:
                print("❌ Model testing failed")
        else:
            print("❌ Model training failed")
    else:
        print(f"\n📁 Dataset ready at: {dataset_path}")
        print(f"To train later, run:")
        print(f"python -c \"from ultralytics import YOLO; YOLO('yolov8n-cls.pt').train(data='{dataset_path}', epochs=40, project='runs/classify', name='5class_model')\"")

if __name__ == "__main__":
    main()