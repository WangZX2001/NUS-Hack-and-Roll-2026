#!/usr/bin/env python3
"""
Test the 5-class model that was actually trained.
"""

from ultralytics import YOLO
from pathlib import Path
import random

def test_5class_model():
    """Test the 5-class model with correct path."""
    
    # Correct path where the model was actually saved
    model_path = "runs/classify/runs/classify/5class_model/weights/best.pt"
    
    if not Path(model_path).exists():
        print(f"❌ Model not found at {model_path}")
        return False
    
    print(f"✅ Found 5-class model at: {model_path}")
    
    try:
        model = YOLO(model_path)
        print(f"🤖 Model loaded successfully")
        print(f"📊 Model classes: {model.names}")
        print(f"🔢 Number of classes: {len(model.names)}")
        
        # Test on validation images
        val_dir = Path("dataset_5class/val")
        if not val_dir.exists():
            print("⚠️  Validation dataset not found")
            return True  # Model loads, just no test data
        
        classes = ['paper', 'metal', 'plastic', 'glass', 'trash']
        overall_results = {}
        
        print(f"\n🧪 Testing model on validation data:")
        print("=" * 50)
        
        for class_name in classes:
            class_dir = val_dir / class_name
            if not class_dir.exists():
                print(f"⚠️  {class_name} directory not found")
                continue
                
            image_files = list(class_dir.glob('*.jpg'))[:8]  # Test 8 per class
            
            if not image_files:
                print(f"⚠️  No images in {class_name}")
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
            
            # Check if glass is working better
            if 'glass' in overall_results:
                glass_acc = overall_results['glass']['accuracy']
                print(f"\n🍶 Glass Classification:")
                if glass_acc >= 80:
                    print(f"   ✅ Excellent glass detection: {glass_acc:.1f}%")
                elif glass_acc >= 60:
                    print(f"   ✅ Good glass detection: {glass_acc:.1f}%")
                else:
                    print(f"   ⚠️  Glass detection needs improvement: {glass_acc:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def update_webapp_paths():
    """Update webapp to use correct model path."""
    print(f"\n🔧 WEBAPP UPDATE:")
    print("=" * 50)
    
    correct_path = "runs/classify/runs/classify/5class_model/weights/best.pt"
    
    print(f"✅ Your 5-class model is at:")
    print(f"   {correct_path}")
    
    print(f"\n📝 Update webapp_5class.py:")
    print(f"   Change the model_paths list to:")
    print(f'   model_paths = [')
    print(f'       "{correct_path}",')
    print(f'       "runs/classify/train2/weights/best.pt"  # fallback')
    print(f'   ]')
    
    print(f"\n🚀 Then run:")
    print(f"   python webapp_5class.py")

def main():
    print("🔍 5-CLASS MODEL TESTER")
    print("=" * 50)
    
    success = test_5class_model()
    
    if success:
        update_webapp_paths()
        
        print(f"\n🎯 SUMMARY:")
        print(f"✅ 5-class model trained successfully")
        print(f"✅ Model can be loaded and used")
        print(f"📁 Model location: runs/classify/runs/classify/5class_model/weights/best.pt")
        print(f"\n🌐 Next: Update webapp_5class.py with correct path and test!")
    else:
        print(f"\n❌ Model testing failed")

if __name__ == "__main__":
    main()