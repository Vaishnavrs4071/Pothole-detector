// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const cameraBtn = document.getElementById('cameraBtn');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const analyzeBtn = document.getElementById('analyzeBtn');
const videoSection = document.getElementById('videoSection');
const videoFeed = document.getElementById('videoFeed');
const detectionCanvas = document.getElementById('detectionCanvas');
const stopVideoBtn = document.getElementById('stopVideoBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingOverlay = document.getElementById('loadingOverlay');
const potholeCount = document.getElementById('potholeCount');
const avgConfidence = document.getElementById('avgConfidence');
const originalImage = document.getElementById('originalImage');
const resultImage = document.getElementById('resultImage');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const liveCount = document.getElementById('liveCount');
const fpsDisplay = document.getElementById('fps');
const recordingTime = document.getElementById('recordingTime');

let selectedFile = null;
let videoStream = null;
let detectionInterval = null;
let startTime = null;
let frameCount = 0;
let lastFrameTime = Date.now();

// GPS and Report Generation (Live Detection Only)
let currentLocation = null;
let liveDetections = [];  // Store detections for report
let watchId = null;  // GPS watch ID

// Upload Area Click
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

browseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
});

// File Input Change
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
});

// Drag and Drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFile(file);
    }
});

// Camera Button - Start Live Detection
cameraBtn.addEventListener('click', async () => {
    try {
        // Request camera access with rear camera preference for mobile
        const constraints = {
            video: {
                facingMode: { ideal: 'environment' }, // Prefer rear camera
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        };

        videoStream = await navigator.mediaDevices.getUserMedia(constraints);
        videoFeed.srcObject = videoStream;

        // Show video section, hide others
        document.querySelector('.upload-section').style.display = 'none';
        previewSection.style.display = 'none';
        resultsSection.style.display = 'none';
        videoSection.style.display = 'block';

        // Wait for video to be ready
        videoFeed.onloadedmetadata = () => {
            // Set canvas size to match video
            detectionCanvas.width = videoFeed.videoWidth;
            detectionCanvas.height = videoFeed.videoHeight;

            // Start detection loop
            startTime = Date.now();
            liveDetections = [];  // Reset detections for new session
            startGPSTracking();  // Start GPS tracking for live detection
            startDetectionLoop();
        };

        // Scroll to video
        videoSection.scrollIntoView({ behavior: 'smooth', block: 'center' });

    } catch (error) {
        alert('Camera access denied or not available. Please allow camera access and try again.');
        console.error('Camera error:', error);
    }
});

// Stop Video Button
stopVideoBtn.addEventListener('click', () => {
    stopVideoDetection();

    // Show upload section again
    document.querySelector('.upload-section').style.display = 'block';
    videoSection.style.display = 'none';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Start Detection Loop
function startDetectionLoop() {
    let isProcessing = false;

    detectionInterval = setInterval(async () => {
        if (isProcessing) return;

        isProcessing = true;

        try {
            // Capture frame from video
            const canvas = document.createElement('canvas');
            canvas.width = videoFeed.videoWidth;
            canvas.height = videoFeed.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(videoFeed, 0, 0);

            // Convert to base64
            const frameData = canvas.toDataURL('image/jpeg', 0.8);

            // Send to backend for detection
            // Clear previous drawings
            ctx.clearRect(0, 0, detectionCanvas.width, detectionCanvas.height);

            // Draw each detection
            detections.forEach(detection => {
                const [x1, y1, x2, y2] = detection.bbox;
                const confidence = detection.confidence;

                // Scale coordinates to canvas size
                const scaleX = detectionCanvas.width / videoFeed.videoWidth;
                const scaleY = detectionCanvas.height / videoFeed.videoHeight;

                const sx1 = x1 * scaleX;
                const sy1 = y1 * scaleY;
                const sx2 = x2 * scaleX;
                const sy2 = y2 * scaleY;

                // Draw bounding box
                ctx.strokeStyle = '#10b981'; // Green color
                ctx.lineWidth = 3;
                ctx.strokeRect(sx1, sy1, sx2 - sx1, sy2 - sy1);

                // Draw label background
                const label = `Pothole ${(confidence * 100).toFixed(0)}%`;
                ctx.font = 'bold 16px Inter, sans-serif';
                const textWidth = ctx.measureText(label).width;

                ctx.fillStyle = '#10b981';
                ctx.fillRect(sx1, sy1 - 25, textWidth + 10, 25);

                // Draw label text
                ctx.fillStyle = '#ffffff';
                ctx.fillText(label, sx1 + 5, sy1 - 7);
            });
        }

// Stop Video Detection
function stopVideoDetection() {
            if (detectionInterval) {
                clearInterval(detectionInterval);
                detectionInterval = null;
            }

            if (videoStream) {
                videoStream.getTracks().forEach(track => track.stop());
                videoStream = null;
            }

            // Clear canvas
            if (detectionCanvas) {
                const ctx = detectionCanvas.getContext('2d');
                ctx.clearRect(0, 0, detectionCanvas.width, detectionCanvas.height);
            }

            // Reset counters
            frameCount = 0;
            startTime = null;
        }

        // Handle File
        function handleFile(file) {
            selectedFile = file;

            // Show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                previewSection.style.display = 'block';

                // Scroll to preview
                previewSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            };
            reader.readAsDataURL(file);
        }

        // Analyze Button
        analyzeBtn.addEventListener('click', async () => {
            if (!selectedFile) return;

            // Show loading
            loadingOverlay.style.display = 'flex';

            try {
                // Create form data
                const formData = new FormData();
                formData.append('image', selectedFile);

                // Send to backend
                const response = await fetch('/detect', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (data.success) {
                    // Update stats
                    potholeCount.textContent = data.count;

                    // Calculate average confidence
                    if (data.detections.length > 0) {
                        const avgConf = data.detections.reduce((sum, d) => sum + d.confidence, 0) / data.detections.length;
                        avgConfidence.textContent = `${(avgConf * 100).toFixed(1)}%`;
                    } else {
                        avgConfidence.textContent = '0%';
                    }

                    // Show images
                    originalImage.src = previewImage.src;
                    resultImage.src = data.result_image;

                    // Display severity information if available
                    const severitySection = document.getElementById('severitySection');
                    const severityList = document.getElementById('severityList');

                    if (data.detections.length > 0 && data.detections[0].severity) {
                        severityList.innerHTML = '';
                        data.detections.forEach((detection, index) => {
                            const severityItem = document.createElement('div');
                            severityItem.className = 'severity-item';
                            severityItem.innerHTML = `
                        <div class="severity-badge" style="background-color: ${detection.severity_color}20; border-color: ${detection.severity_color};">
                            <span class="severity-emoji">${detection.severity_emoji}</span>
                            <span class="severity-level">${detection.severity}</span>
                        </div>
                        <div class="severity-details">
                            <span>Pothole #${index + 1}</span>
                            <span class="severity-confidence">${(detection.confidence * 100).toFixed(1)}% confidence</span>
                        </div>
                    `;
                            severityList.appendChild(severityItem);
                        });
                        severitySection.style.display = 'block';
                    } else {
                        severitySection.style.display = 'none';
                    }

                    // Show results
                    resultsSection.style.display = 'block';
                    previewSection.style.display = 'none';

                    // Scroll to results
                    setTimeout(() => {
                        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100);

                } else {
                    alert('Error: ' + (data.error || 'Detection failed'));
                }

            } catch (error) {
                console.error('Error:', error);
                alert('Failed to analyze image. Please try again.');
            } finally {
                loadingOverlay.style.display = 'none';
            }
        });

        // New Analysis Button
        newAnalysisBtn.addEventListener('click', () => {
            // Reset everything
            selectedFile = null;
            fileInput.value = '';
            previewSection.style.display = 'none';
            resultsSection.style.display = 'none';

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // Clean up on page unload
        window.addEventListener('beforeunload', () => {
            stopVideoDetection();
            stopGPSTracking();
        });

        // Add smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';

        // ========== GPS TRACKING AND REPORT GENERATION ==========

        function startGPSTracking() {
            if (!navigator.geolocation) {
                console.warn('Geolocation not supported');
                return;
            }

            // Request GPS permission and start watching position
            watchId = navigator.geolocation.watchPosition(
                (position) => {
                    currentLocation = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    };
                    console.log('GPS location updated:', currentLocation);
                },
                (error) => {
                    console.warn('GPS error:', error.message);
                    currentLocation = null;
                },
                {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 0
                }
            );
        }

        function stopGPSTracking() {
            if (watchId !== null) {
                navigator.geolocation.clearWatch(watchId);
                watchId = null;
            }
        }

        // Modified stopVideoDetection to include report prompt
        const originalStopVideoDetection = stopVideoDetection;
        function stopVideoDetection() {
            originalStopVideoDetection();
            stopGPSTracking();

            // If detections were made, ask if user wants a report
            if (liveDetections.length > 0) {
                setTimeout(() => {
                    if (confirm(`${liveDetections.length} pothole(s) detected! Would you like to download a report with GPS location?`)) {
                        generateReport();
                    }
                }, 500);
            }

            // Reset detections
            liveDetections = [];
        }

        async function generateReport() {
            try {
                // Capture current frame from video
                const canvas = document.createElement('canvas');
                canvas.width = videoFeed.videoWidth || 640;
                canvas.height = videoFeed.videoHeight || 480;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(videoFeed, 0, 0);
                const imageData = canvas.toDataURL('image/jpeg', 0.8);

                // Prepare report data
                const reportData = {
                    detections: liveDetections,
                    location: currentLocation,
                    image: imageData
                };

                // Show loading
                loadingOverlay.style.display = 'flex';
                loadingOverlay.querySelector('p').textContent = 'Generating report...';

                // Send request to generate PDF
                const response = await fetch('/generate_report', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(reportData)
                });

                if (response.ok) {
                    // Download the PDF
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `pothole_report_${new Date().getTime()}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);

                    alert('Report downloaded successfully!');
                } else {
                    alert('Failed to generate report. Please try again.');
                }

            } catch (error) {
                console.error('Report generation error:', error);
                alert('Error generating report: ' + error.message);
            } finally {
                loadingOverlay.style.display = 'none';
                loadingOverlay.querySelector('p').textContent = 'Analyzing image with AI...';
            }
        }

        // Store detections from live feed (modify existing detection handling)
        // This will be called when detections are received
        function storeDetection(detection) {
            // Add timestamp
            detection.timestamp = new Date().toISOString();
            liveDetections.push(detection);

            // Keep only last 50 detections to avoid memory issues
            if (liveDetections.length > 50) {
                liveDetections.shift();
            }
        }
