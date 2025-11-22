"""
Flask web application for pothole detection.
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import uuid
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO
from depth_estimator import get_depth_estimator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# Create necessary directories
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path(app.config['RESULTS_FOLDER']).mkdir(exist_ok=True)

# Load model (will be loaded on first request)
model = None
MODEL_PATH = 'runs/detect/pothole_detector2/weights/best.pt'

# Depth estimator (will be loaded on first request)
depth_estimator = None
# Enable depth estimation for local use
USE_DEPTH_ESTIMATION = True

def load_model():
    """Load the trained YOLO model."""
    global model
    if model is None:
        model_file = Path(MODEL_PATH)
        if model_file.exists():
            print(f"Loading trained model from {MODEL_PATH}...")
            model = YOLO(MODEL_PATH)
            print("Trained model loaded successfully!")
        else:
            print(f"Trained model not found at {MODEL_PATH}")
            print("Using pretrained YOLOv8n model for general object detection")
            print("Note: This model is not specifically trained for potholes")
            model = YOLO('yolov8n.pt')  # Use pretrained model
            print("Pretrained model loaded successfully!")
    return model

def detect_potholes_in_image(image_path):
    """
    Run pothole detection on an image.
    
    Returns:
        dict: Detection results with severity classification
    """
    global depth_estimator
    
    model = load_model()
    
    # Run inference
    results = model.predict(
        source=image_path,
        conf=0.25,  # Normal threshold for trained model
        iou=0.45,
        verbose=False
    )
    
    result = results[0]
    
    # Load original image for depth estimation
    original_img = cv2.imread(str(image_path))
    
    # Get annotated image
    annotated_img = result.plot()
    
    # Convert to PIL Image
    annotated_img_rgb = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(annotated_img_rgb)
    
    # Save annotated image
    result_filename = f"result_{uuid.uuid4().hex[:8]}.jpg"
    result_path = Path(app.config['RESULTS_FOLDER']) / result_filename
    pil_img.save(result_path)
    
    # Get detection info
    boxes = result.boxes
    detections = []
    
    # Initialize depth estimator if enabled
    if USE_DEPTH_ESTIMATION and depth_estimator is None:
        try:
            print("Loading depth estimator...")
            depth_estimator = get_depth_estimator()
        except Exception as e:
            print(f"Warning: Could not load depth estimator: {e}")
            print("Continuing without severity classification.")
    
    for box in boxes:
        bbox = box.xyxy[0].cpu().numpy().tolist()
        detection = {
            'confidence': float(box.conf[0]),
            'class': int(box.cls[0]),
            'bbox': bbox
        }
        
        # Add severity classification if depth estimator is available
        if USE_DEPTH_ESTIMATION and depth_estimator is not None:
            try:
                severity_info = depth_estimator.classify_pothole_severity(original_img, bbox)
                detection['severity'] = severity_info['severity']
                detection['depth_score'] = severity_info['depth_score']
                detection['severity_color'] = severity_info['color']
                detection['severity_emoji'] = severity_info['emoji']
            except Exception as e:
                print(f"Warning: Depth estimation failed for detection: {e}")
                detection['severity'] = 'Unknown'
        
        detections.append(detection)
    
    return {
        'count': len(boxes),
        'detections': detections,
        'result_image': result_filename
    }

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    """Handle image upload and run detection."""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Save uploaded file
        filename = secure_filename(f"{uuid.uuid4().hex[:8]}_{file.filename}")
        filepath = Path(app.config['UPLOAD_FOLDER']) / filename
        file.save(filepath)
        
        # Run detection
        results = detect_potholes_in_image(str(filepath))
        
        return jsonify({
            'success': True,
            'count': results['count'],
            'detections': results['detections'],
            'result_image': f'/results/{results["result_image"]}'
        })
    
    except Exception as e:
        print(f"Error during detection: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/detect_frame', methods=['POST'])
def detect_frame():
    """Handle real-time video frame detection."""
    try:
        # Get base64 encoded frame from request
        data = request.get_json()
        if not data or 'frame' not in data:
            return jsonify({'error': 'No frame provided'}), 400
        
        # Decode base64 image
        import base64
        frame_data = data['frame'].split(',')[1]  # Remove data:image/jpeg;base64, prefix
        frame_bytes = base64.b64decode(frame_data)
        
        # Convert to numpy array
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Load model
        model = load_model()
        
        # Run inference
        results = model.predict(
            source=frame,
            conf=0.30,  # Slightly higher threshold for video
            iou=0.45,
            verbose=False
        )
        
        result = results[0]
        boxes = result.boxes
        
        # Prepare detection data
        detections = []
        for box in boxes:
            bbox = box.xyxy[0].cpu().numpy().tolist()
            detections.append({
                'bbox': bbox,  # [x1, y1, x2, y2]
                'confidence': float(box.conf[0]),
                'class': int(box.cls[0])
            })
        
        return jsonify({
            'success': True,
            'count': len(boxes),
            'detections': detections
        })
    
    except Exception as e:
        print(f"Error during frame detection: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/results/<filename>')
def serve_result(filename):
    """Serve result images."""
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded images."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    print("=" * 60)
    print("Pothole Detection Web App")
    print("=" * 60)
    print("\nStarting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
