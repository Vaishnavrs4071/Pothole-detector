"""
Monocular Depth Estimation Module for Pothole Severity Classification.

Uses MiDaS (Monocular Depth Estimation) to estimate depth from RGB images
and classify pothole severity based on relative depth.
"""

import torch
import cv2
import numpy as np
from pathlib import Path

class DepthEstimator:
    """Estimates depth from RGB images using MiDaS model."""
    
    def __init__(self, model_type='MiDaS_small'):
        """
        Initialize the depth estimator.
        
        Args:
            model_type: Type of MiDaS model to use
                - 'MiDaS_small': Faster, smaller model (~100MB)
                - 'DPT_Large': More accurate, larger model (~1.3GB)
        """
        self.model_type = model_type
        self.model = None
        self.transform = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        print(f"Initializing depth estimator with {model_type} on {self.device}...")
        self._load_model()
    
    def _load_model(self):
        """Load the MiDaS model and transform."""
        try:
            # Load MiDaS model from torch hub
            self.model = torch.hub.load('intel-isl/MiDaS', self.model_type)
            self.model.to(self.device)
            self.model.eval()
            
            # Load transforms
            midas_transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
            
            if self.model_type == 'DPT_Large' or self.model_type == 'DPT_Hybrid':
                self.transform = midas_transforms.dpt_transform
            else:
                self.transform = midas_transforms.small_transform
            
            print("✓ Depth estimation model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading MiDaS model: {e}")
            print("Make sure you have internet connection for first-time model download.")
            raise
    
    def estimate_depth(self, image):
        """
        Estimate depth map from RGB image.
        
        Args:
            image: RGB image as numpy array (H, W, 3)
        
        Returns:
            depth_map: Depth map as numpy array (H, W)
        """
        # Convert BGR to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 3:
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = image
        
        # Apply transforms
        input_batch = self.transform(img_rgb).to(self.device)
        
        # Predict depth
        with torch.no_grad():
            prediction = self.model(input_batch)
            
            # Resize to original resolution
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img_rgb.shape[:2],
                mode='bicubic',
                align_corners=False,
            ).squeeze()
        
        depth_map = prediction.cpu().numpy()
        
        return depth_map
    
    def classify_pothole_severity(self, image, bbox):
        """
        Classify pothole severity based on estimated depth.
        
        Args:
            image: RGB image as numpy array
            bbox: Bounding box [x1, y1, x2, y2]
        
        Returns:
            dict: {
                'severity': 'Low'|'Medium'|'High',
                'depth_score': float,
                'color': str (hex color code)
            }
        """
        # Get depth map
        depth_map = self.estimate_depth(image)
        
        # Extract pothole region
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        
        # Ensure coordinates are within image bounds
        h, w = depth_map.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        if x2 <= x1 or y2 <= y1:
            return self._default_severity()
        
        pothole_region = depth_map[y1:y2, x1:x2]
        
        # Get surrounding context (expand bbox by 50%)
        margin_x = int((x2 - x1) * 0.5)
        margin_y = int((y2 - y1) * 0.5)
        
        ctx_x1 = max(0, x1 - margin_x)
        ctx_y1 = max(0, y1 - margin_y)
        ctx_x2 = min(w, x2 + margin_x)
        ctx_y2 = min(h, y2 + margin_y)
        
        # Create mask to exclude pothole from context
        context_region = depth_map[ctx_y1:ctx_y2, ctx_x1:ctx_x2].copy()
        
        # Calculate relative depth
        pothole_depth = np.mean(pothole_region)
        context_depth = np.mean(context_region)
        
        # Normalize depth score (higher = deeper pothole)
        # In depth maps, higher values = closer to camera
        # So potholes (farther) should have lower values
        depth_score = (context_depth - pothole_depth) / (context_depth + 1e-6)
        
        # Also consider depth variance (deeper holes have more variation)
        depth_variance = np.std(pothole_region)
        
        # Combined score
        combined_score = depth_score * 0.7 + (depth_variance / 100) * 0.3
        
        # Classify severity
        return self._classify_score(combined_score)
    
    def _classify_score(self, score):
        """Classify depth score into severity levels."""
        if score < 0.15:
            severity = 'Low'
            color = '#10b981'  # Green
            emoji = '🟢'
        elif score < 0.35:
            severity = 'Medium'
            color = '#f59e0b'  # Yellow/Orange
            emoji = '🟡'
        else:
            severity = 'High'
            color = '#ef4444'  # Red
            emoji = '🔴'
        
        return {
            'severity': severity,
            'depth_score': float(score),
            'color': color,
            'emoji': emoji
        }
    
    def _default_severity(self):
        """Return default severity when depth estimation fails."""
        return {
            'severity': 'Unknown',
            'depth_score': 0.0,
            'color': '#6b7280',  # Gray
            'emoji': '⚪'
        }

# Singleton instance
_depth_estimator = None

def get_depth_estimator(model_type='MiDaS_small'):
    """Get or create the depth estimator singleton."""
    global _depth_estimator
    if _depth_estimator is None:
        _depth_estimator = DepthEstimator(model_type)
    return _depth_estimator
