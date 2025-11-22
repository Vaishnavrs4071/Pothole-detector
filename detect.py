"""
Run pothole detection on images using trained YOLOv8 model.
"""

import argparse
from pathlib import Path
from ultralytics import YOLO
import cv2

def detect_potholes(image_path, model_path='runs/detect/pothole_detector/weights/best.pt', save_dir='results'):
    """
    Detect potholes in an image.
    
    Args:
        image_path: Path to input image
        model_path: Path to trained model weights
        save_dir: Directory to save results
    
    Returns:
        dict: Detection results with count, confidence scores, and annotated image path
    """
    
    # Check if model exists
    model_file = Path(model_path)
    if not model_file.exists():
        print(f"❌ Model not found at {model_path}")
        print("Please train the model first by running: python train.py")
        return None
    
    # Load model
    print(f"📦 Loading model from {model_path}...")
    model = YOLO(model_path)
    
    # Run inference
    print(f"🔍 Detecting potholes in {image_path}...")
    results = model.predict(
        source=image_path,
        save=True,
        save_dir=save_dir,
        conf=0.25,  # Confidence threshold
        iou=0.45,   # NMS IoU threshold
        show_labels=True,
        show_conf=True,
        line_width=2
    )
    
    # Process results
    result = results[0]
    boxes = result.boxes
    
    detection_info = {
        'count': len(boxes),
        'confidences': boxes.conf.cpu().numpy().tolist() if len(boxes) > 0 else [],
        'image_path': str(result.path),
        'save_path': str(result.save_dir)
    }
    
    # Print results
    print("\n" + "=" * 60)
    print("Detection Results")
    print("=" * 60)
    print(f"Potholes detected: {detection_info['count']}")
    
    if detection_info['count'] > 0:
        print(f"Confidence scores: {[f'{c:.2f}' for c in detection_info['confidences']]}")
        print(f"Annotated image saved to: {detection_info['save_path']}")
    else:
        print("No potholes detected in this image.")
    
    print("=" * 60)
    
    return detection_info

def main():
    parser = argparse.ArgumentParser(description='Detect potholes in images')
    parser.add_argument('--image', type=str, required=True, help='Path to input image')
    parser.add_argument('--model', type=str, default='runs/detect/pothole_detector/weights/best.pt',
                        help='Path to trained model weights')
    parser.add_argument('--save-dir', type=str, default='results',
                        help='Directory to save results')
    
    args = parser.parse_args()
    
    detect_potholes(args.image, args.model, args.save_dir)

if __name__ == "__main__":
    main()
