# Quick Setup Guide

## 🚀 Getting Started (Step-by-Step)

### Step 1: Install Dependencies
```bash
cd pothole-detector
pip install -r requirements.txt
```

### Step 2: Setup Kaggle API

1. Create a Kaggle account at https://www.kaggle.com
2. Go to https://www.kaggle.com/settings/account
3. Scroll to "API" section
4. Click "Create New API Token"
5. This downloads `kaggle.json`
6. Move it to:
   - **Windows**: `C:\Users\<YourUsername>\.kaggle\kaggle.json`
   - **Linux/Mac**: `~/.kaggle/kaggle.json`

### Step 3: Download Dataset
```bash
python download_dataset.py
```

This will download ~500MB of pothole images from Kaggle.

### Step 4: Train the Model
```bash
python train.py
```

**Note**: This takes 15-30 minutes. You'll see:
- Training progress with loss metrics
- Validation results
- Model saved to `runs/detect/pothole_detector/weights/best.pt`

### Step 5: Run the Web App
```bash
python app.py
```

Open your browser to: **http://localhost:5000**

---

## 🧪 Quick Test (Without Training)

Want to test the interface before training?

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. The app will use a pretrained YOLOv8 model (won't detect potholes specifically, but shows the interface works)

---

## 📸 Testing the Detection

### Option 1: Use Sample Images
```bash
python generate_samples.py
```
This creates test images in `test_images/` folder.

### Option 2: Use Real Images
Find pothole images online or take photos of roads.

### Option 3: Command Line Testing
```bash
python detect.py --image path/to/image.jpg
```

---

## ⚡ Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `pip install -r requirements.txt` | Install all dependencies |
| `python download_dataset.py` | Download training data |
| `python train.py` | Train the model |
| `python app.py` | Start web server |
| `python detect.py --image <path>` | Detect potholes in image |
| `python generate_samples.py` | Create test images |

---

## 🎯 Expected Results

After training, you should see:
- **mAP50**: ~0.7-0.9 (70-90% accuracy)
- **Detection**: Bounding boxes around potholes
- **Confidence**: 0.25-1.0 (25-100%)

---

## 💡 Tips

- **GPU Training**: Much faster if you have NVIDIA GPU with CUDA
- **CPU Training**: Works but takes longer (30-60 minutes)
- **Batch Size**: Reduce if you get memory errors (edit `train.py`)
- **Epochs**: Increase for better accuracy (edit `train.py`)

---

## 🐛 Common Issues

**"Model not found"**
→ Run `python train.py` first

**"Kaggle API error"**
→ Check kaggle.json location and permissions

**"Out of memory"**
→ Reduce batch size in `train.py` (try batch=8 or batch=4)

**Camera not working**
→ Use HTTPS or localhost, check browser permissions

---

## 📱 Using the Web Interface

1. **Upload Image**: Drag & drop or click browse
2. **Use Camera**: Click "Use Camera" button
3. **Analyze**: Click "Analyze Image"
4. **View Results**: See bounding boxes and statistics
5. **New Analysis**: Click "New Analysis" to try another image

---

**Ready to detect potholes! 🚗💨**
