"""
Convert Pascal VOC XML annotations to YOLO format and reorganize dataset.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import random

def convert_voc_to_yolo(xml_file, img_width, img_height):
    """Convert Pascal VOC XML annotation to YOLO format."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    yolo_annotations = []
    
    for obj in root.findall('object'):
        # Get bounding box
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        
        # Convert to YOLO format (normalized center x, center y, width, height)
        x_center = ((xmin + xmax) / 2) / img_width
        y_center = ((ymin + ymax) / 2) / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height
        
        # Class 0 for pothole
        yolo_annotations.append(f"0 {x_center} {y_center} {width} {height}")
    
    return yolo_annotations

def organize_dataset():
    """Organize dataset into YOLO format."""
    
    print("[*] Converting dataset to YOLO format...")
    
    data_dir = Path('data')
    images_dir = data_dir / 'images'
    annotations_dir = data_dir / 'annotations'
    
    # Create YOLO directory structure
    yolo_dir = Path('yolo_dataset')
    train_images = yolo_dir / 'train' / 'images'
    train_labels = yolo_dir / 'train' / 'labels'
    valid_images = yolo_dir / 'valid' / 'images'
    valid_labels = yolo_dir / 'valid' / 'labels'
    
    for dir_path in [train_images, train_labels, valid_images, valid_labels]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Get all image files
    image_files = list(images_dir.glob('*.png')) + list(images_dir.glob('*.jpg'))
    
    print(f"[+] Found {len(image_files)} images")
    
    # Shuffle and split (80% train, 20% valid)
    random.shuffle(image_files)
    split_idx = int(len(image_files) * 0.8)
    train_files = image_files[:split_idx]
    valid_files = image_files[split_idx:]
    
    print(f"[+] Train: {len(train_files)}, Valid: {len(valid_files)}")
    
    # Process training set
    print("\n[*] Processing training set...")
    for img_file in train_files:
        # Get corresponding XML file
        xml_file = annotations_dir / f"{img_file.stem}.xml"
        
        if not xml_file.exists():
            continue
        
        # Get image dimensions from XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        img_width = int(size.find('width').text)
        img_height = int(size.find('height').text)
        
        # Convert annotations
        yolo_annotations = convert_voc_to_yolo(xml_file, img_width, img_height)
        
        if yolo_annotations:  # Only copy if there are annotations
            # Copy image
            shutil.copy(img_file, train_images / img_file.name)
            
            # Save YOLO annotations
            txt_file = train_labels / f"{img_file.stem}.txt"
            txt_file.write_text('\n'.join(yolo_annotations))
    
    # Process validation set
    print("[*] Processing validation set...")
    for img_file in valid_files:
        # Get corresponding XML file
        xml_file = annotations_dir / f"{img_file.stem}.xml"
        
        if not xml_file.exists():
            continue
        
        # Get image dimensions from XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        img_width = int(size.find('width').text)
        img_height = int(size.find('height').text)
        
        # Convert annotations
        yolo_annotations = convert_voc_to_yolo(xml_file, img_width, img_height)
        
        if yolo_annotations:  # Only copy if there are annotations
            # Copy image
            shutil.copy(img_file, valid_images / img_file.name)
            
            # Save YOLO annotations
            txt_file = valid_labels / f"{img_file.stem}.txt"
            txt_file.write_text('\n'.join(yolo_annotations))
    
    # Create data.yaml
    yaml_content = f"""# Pothole Detection Dataset
path: {yolo_dir.absolute()}
train: train/images
val: valid/images

# Classes
names:
  0: pothole
"""
    
    yaml_file = yolo_dir / 'data.yaml'
    yaml_file.write_text(yaml_content)
    
    print(f"\n[+] Dataset converted successfully!")
    print(f"[+] Location: {yolo_dir.absolute()}")
    print(f"[+] Config file: {yaml_file}")
    print(f"[+] Train images: {len(list(train_images.glob('*')))}")
    print(f"[+] Valid images: {len(list(valid_images.glob('*')))}")
    
    return yaml_file

if __name__ == "__main__":
    print("=" * 60)
    print("Dataset Converter: Pascal VOC to YOLO")
    print("=" * 60)
    
    yaml_file = organize_dataset()
    
    print("\n" + "=" * 60)
    print("[+] Conversion complete!")
    print(f"[+] Use this config for training: {yaml_file}")
    print("=" * 60)
