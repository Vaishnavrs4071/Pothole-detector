# 🚗 AI Pothole Detector

An advanced AI-powered pothole detection system using **YOLOv8** deep learning model. Upload road images or use your camera to instantly detect and locate potholes with bounding boxes and confidence scores.

![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)

## ✨ Features

- 🎯 **Real-time Detection**: Powered by YOLOv8 for accurate pothole detection
- 📹 **Live Video Mode**: Use your phone camera for continuous real-time detection
- 📸 **Image Upload**: Drag-and-drop or browse for single image analysis
- 🖼️ **Camera Support**: Capture photos or start live video detection
- 📊 **Visual Results**: Bounding boxes with confidence scores
- 🎨 **Modern UI**: Glassmorphism design with smooth animations
- 📱 **Mobile Optimized**: Rear camera support for phones
- 💨 **Fast Processing**: ~5 FPS real-time detection

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Kaggle account (for dataset download)
- GPU recommended for training (CPU works but slower)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd pothole-detector
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup Kaggle API** (for dataset download)
   - Go to https://www.kaggle.com/settings/account
   - Click "Create New API Token" under API section
   - Move the downloaded `kaggle.json` to:
     - **Windows**: `C:\Users\<username>\.kaggle\kaggle.json`
     - **Linux/Mac**: `~/.kaggle/kaggle.json`
   - Set permissions (Linux/Mac only): `chmod 600 ~/.kaggle/kaggle.json`

4. **Download the dataset**
```bash
python download_dataset.py
```

5. **Train the model** (15-30 minutes depending on hardware)
```bash
python train.py
```

6. **Run the web application**
```bash
python app.py
```

7. **Open your browser** and go to: `http://localhost:5000`

## 📖 Usage

### Web Interface

1. Open the web app at `http://localhost:5000`
2. Upload an image by:
   - Dragging and dropping an image
   - Clicking "Browse Files"
   - Using the "Use Camera" button
3. Click "Analyze Image"
4. View detection results with bounding boxes and statistics

### Command Line Detection

```bash
python detect.py --image path/to/image.jpg
```

Options:
- `--image`: Path to input image (required)
- `--model`: Path to trained model weights (default: `runs/detect/pothole_detector/weights/best.pt`)
- `--save-dir`: Directory to save results (default: `results`)

## 🏗️ Project Structure

```
pothole-detector/
├── app.py                  # Flask web application
├── train.py                # Model training script
├── detect.py               # Detection script
├── download_dataset.py     # Kaggle dataset downloader
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web interface
├── static/
│   ├── style.css          # Styles
│   └── script.js          # Frontend logic
├── data/                  # Dataset (created after download)
├── runs/                  # Training outputs and models
├── uploads/               # Uploaded images
└── results/               # Detection results
```

## 🧠 Model Details

- **Architecture**: YOLOv8n (nano) - optimized for speed and accuracy
- **Input Size**: 640x640 pixels
- **Training**: 50 epochs with early stopping
- **Dataset**: Kaggle pothole detection dataset
  - 1,581 training images
  - 396 validation images
  - Diverse conditions (day/night, wet/dry roads)

## 📊 Training Metrics

After training, you can find:
- Training plots: `runs/detect/pothole_detector/`
- Best model weights: `runs/detect/pothole_detector/weights/best.pt`
- Validation metrics: mAP50, mAP50-95, precision, recall

## 🎨 Web Interface Features

- **Glassmorphism Design**: Modern, premium UI with blur effects
- **Dark Mode**: Easy on the eyes with vibrant accent colors
- **Smooth Animations**: Micro-interactions for better UX
- **Before/After View**: Compare original and detected images
- **Statistics Dashboard**: Detection count and confidence scores
- **Responsive Layout**: Works on all screen sizes

## 🔧 Customization

### Adjust Detection Threshold

Edit `app.py` or `detect.py`:
```python
results = model.predict(
    source=image_path,
    conf=0.25,  # Change confidence threshold (0-1)
    iou=0.45,   # Change IoU threshold for NMS
)
```

### Train with Different Parameters

Edit `train.py`:
```python
results = model.train(
    epochs=50,      # Number of training epochs
    imgsz=640,      # Image size
    batch=16,       # Batch size
    patience=10,    # Early stopping patience
)
```

## 🐛 Troubleshooting

**Model not found error**
- Make sure you've run `python train.py` first
- Check that `runs/detect/pothole_detector/weights/best.pt` exists

**Kaggle API error**
- Verify `kaggle.json` is in the correct location
- Accept the dataset terms on Kaggle website
- Check internet connection

**Camera not working**
- Ensure browser has camera permissions
- Use HTTPS or localhost (required for camera access)
- Try a different browser

**Low detection accuracy**
- Train for more epochs
- Use a larger YOLO model (yolov8s, yolov8m)
- Collect more training data

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- **Ultralytics** for YOLOv8
- **Kaggle** for the pothole detection dataset
- **Flask** for the web framework

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📧 Support

For issues or questions, please check the troubleshooting section or create an issue in the repository.

---

**Built with ❤️ using YOLOv8, Flask, and Modern Web Technologies**
