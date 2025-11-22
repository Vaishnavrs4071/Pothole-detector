# Real-Time Video Detection Feature

## Overview

Added **live video detection** capability that allows users to use their phone camera to detect potholes in real-time while recording.

## New Features

### 📹 Live Camera Feed
- Automatically uses **rear camera** on mobile devices
- Continuous video stream with real-time detection
- Works on both desktop and mobile browsers

### 🎯 Real-Time Detection
- Processes frames at **~5 FPS** for smooth performance
- Draws bounding boxes directly on video feed
- Shows confidence scores for each detection
- Updates detection count in real-time

### 📊 Live Statistics
- **Pothole Count**: Number of potholes currently detected
- **FPS Counter**: Actual frames processed per second
- **Recording Timer**: Duration of live detection session

### 🎨 Visual Feedback
- Green bounding boxes around detected potholes
- Confidence percentage labels
- Pulsing red recording indicator
- Overlay stats on video feed

## How It Works

### Frontend (JavaScript)
1. **Camera Access**: Requests camera with rear-facing preference
2. **Frame Capture**: Captures video frames every 200ms
3. **Send to Backend**: Converts frame to base64 and sends via AJAX
4. **Draw Results**: Receives detections and draws bounding boxes on canvas overlay

### Backend (Python/Flask)
1. **Receive Frame**: Gets base64 encoded frame
2. **Decode Image**: Converts to numpy array
3. **Run YOLO**: Processes frame with trained model
4. **Return Detections**: Sends back bounding boxes and confidence scores

## Usage

### On Mobile Phones
1. Open the website on your phone
2. Click "Start Live Detection"
3. Allow camera access (will use rear camera)
4. Point camera at road
5. See real-time pothole detection with bounding boxes
6. Click "Stop Detection" when done

### On Desktop
1. Click "Start Live Detection"
2. Allow webcam access
3. Show road images to webcam
4. See real-time detection

## Technical Details

### Performance Optimization
- **Frame Rate**: 5 FPS (200ms interval) balances accuracy and performance
- **Image Quality**: JPEG compression at 80% reduces data transfer
- **Async Processing**: Non-blocking detection prevents frame skipping
- **Canvas Overlay**: Hardware-accelerated drawing for smooth visuals

### Mobile Optimizations
- `facingMode: 'environment'` - Prefers rear camera
- `playsinline` attribute - Prevents fullscreen on iOS
- Responsive canvas sizing - Matches video dimensions
- Touch-friendly controls - Large stop button

### Browser Compatibility
- ✅ Chrome/Edge (Desktop & Mobile)
- ✅ Safari (iOS & macOS)
- ✅ Firefox (Desktop & Mobile)
- ⚠️ Requires HTTPS or localhost for camera access

## Code Changes

### Files Modified

1. **app.py** - Added `/detect_frame` endpoint for real-time processing
2. **index.html** - Added video section with canvas overlay
3. **style.css** - Added video container, stats, and recording indicator styles
4. **script.js** - Implemented camera access, frame capture, and detection loop

### New API Endpoint

```python
@app.route('/detect_frame', methods=['POST'])
def detect_frame():
    # Receives base64 frame
    # Runs YOLO detection
    # Returns bounding boxes and confidence scores
```

### Key JavaScript Functions

- `startDetectionLoop()` - Main detection loop (5 FPS)
- `drawDetections()` - Draws bounding boxes on canvas
- `stopVideoDetection()` - Cleans up camera and intervals

## Performance Metrics

- **Latency**: ~200-500ms per frame (depending on model and hardware)
- **Frame Rate**: 3-5 FPS typical
- **Bandwidth**: ~50-100 KB per frame
- **CPU Usage**: Moderate (YOLO inference is main bottleneck)

## Future Enhancements

Possible improvements:
- Video recording with detections
- Save detection snapshots
- Adjust detection threshold in real-time
- Show detection history/heatmap
- Add sound alerts for potholes
- Batch processing for better FPS

## Testing

### To Test on Phone
1. Make sure Flask app is accessible on network: `python app.py` (already set to `0.0.0.0`)
2. Find your computer's IP address
3. On phone, navigate to `http://<your-ip>:5000`
4. Click "Start Live Detection"
5. Point camera at road (or test images)

### To Test on Desktop
1. Run `python app.py`
2. Open `http://localhost:5000`
3. Click "Start Live Detection"
4. Allow webcam access
5. Show road images to webcam

---

**The system now supports both static image analysis AND real-time video detection!** 🎉
