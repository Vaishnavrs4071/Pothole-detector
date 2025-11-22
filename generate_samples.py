"""
Generate sample road images for testing (optional).
This creates synthetic test images if you want to test the web interface
before training the model.
"""

from PIL import Image, ImageDraw, ImageFilter
import random
import os

def create_sample_road_image(filename, has_pothole=True):
    """Create a simple synthetic road image for testing."""
    
    # Create base image (road)
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(60, 60, 65))
    draw = ImageDraw.Draw(img)
    
    # Add road texture
    for _ in range(1000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(1, 3)
        color = (
            random.randint(50, 70),
            random.randint(50, 70),
            random.randint(55, 75)
        )
        draw.ellipse([x, y, x+size, y+size], fill=color)
    
    # Add lane markings
    for i in range(0, width, 60):
        draw.rectangle([i, height//2-2, i+30, height//2+2], fill=(200, 200, 200))
    
    if has_pothole:
        # Add potholes
        num_potholes = random.randint(1, 3)
        for _ in range(num_potholes):
            x = random.randint(100, width-100)
            y = random.randint(100, height-100)
            size = random.randint(40, 80)
            
            # Draw irregular pothole shape
            draw.ellipse([x, y, x+size, y+size*0.7], fill=(30, 30, 35))
            draw.ellipse([x+5, y+5, x+size-5, y+size*0.7-5], fill=(20, 20, 25))
    
    # Apply slight blur for realism
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Save
    os.makedirs('test_images', exist_ok=True)
    filepath = os.path.join('test_images', filename)
    img.save(filepath)
    print(f"✓ Created: {filepath}")
    
    return filepath

if __name__ == "__main__":
    print("=" * 60)
    print("Sample Image Generator")
    print("=" * 60)
    print("\nGenerating test images...\n")
    
    # Create sample images
    create_sample_road_image('road_with_pothole_1.jpg', has_pothole=True)
    create_sample_road_image('road_with_pothole_2.jpg', has_pothole=True)
    create_sample_road_image('good_road.jpg', has_pothole=False)
    
    print("\n" + "=" * 60)
    print("✓ Sample images created in 'test_images/' folder")
    print("=" * 60)
