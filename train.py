"""
Train YOLOv8 model for pothole detection.
"""

from ultralytics import YOLO
import os
from pathlib import Path

def train_model():
    """Train YOLOv8 model on pothole dataset."""
    
    print("=" * 60)
    print("YOLOv8 Pothole Detection Training")
    print("=" * 60)
    
    # Check if dataset exists
    yolo_dataset_dir = Path('yolo_dataset')
    data_dir = Path('data')
    
    if not yolo_dataset_dir.exists() and not data_dir.exists():
        print("❌ Dataset not found! Please run download_dataset.py first.")
        return
    
    # Find the YAML config file
    yaml_files = list(yolo_dataset_dir.rglob('*.yaml')) if yolo_dataset_dir.exists() else list(data_dir.rglob('*.yaml'))
    
    if not yaml_files:
        print("❌ No YAML config file found!")
        print("Please run convert_dataset.py to convert the dataset to YOLO format.")
        return
    
    yaml_path = yaml_files[0]
    print(f"✓ Found config: {yaml_path}")
    
    # Initialize YOLOv8 model
    print("\n📦 Loading YOLOv8 model...")
    model = YOLO('yolov8n.pt')  # Use nano model for faster training
    
    # Training parameters
    print("\n🎯 Training configuration:")
    print(f"  Model: YOLOv8n (nano)")
    print(f"  Epochs: 50")
    print(f"  Image size: 640x640")
    print(f"  Batch size: 16")
    print(f"  Device: CPU (training will be slower)")
    print(f"  Expected time: 30-60 minutes on CPU")
    
    # Train the model
    print("\n🚀 Starting training...")
    print("This may take 15-30 minutes depending on your hardware.\n")
    
    try:
        results = model.train(
            data=str(yaml_path),
            epochs=50,
            imgsz=640,
            batch=16,
            name='pothole_detector',
            patience=10,  # Early stopping
            save=True,
            plots=True,
            device='cpu'  # Use CPU (change to '0' if you have GPU)
        )
        
        print("\n" + "=" * 60)
        print("✓ Training completed successfully!")
        print("=" * 60)
        print(f"\nModel saved to: runs/detect/pothole_detector/weights/best.pt")
        print(f"Training plots saved to: runs/detect/pothole_detector/")
        
        # Validate the model
        print("\n📊 Running validation...")
        metrics = model.val()
        
        print(f"\nValidation Results:")
        print(f"  mAP50: {metrics.box.map50:.3f}")
        print(f"  mAP50-95: {metrics.box.map:.3f}")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        print("\nTroubleshooting:")
        print("- Check that the dataset is properly downloaded")
        print("- Verify the YAML config file paths are correct")
        print("- Make sure you have enough disk space")

if __name__ == "__main__":
    train_model()
