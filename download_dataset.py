"""
Download and prepare the pothole detection dataset from Kaggle using kagglehub.

This script uses kagglehub which doesn't require API credentials!
Just run: python download_dataset.py

The dataset will be automatically downloaded and organized.
"""

import os
import zipfile
import shutil
from pathlib import Path


def download_dataset():
    """Download the pothole dataset from Kaggle using kagglehub."""
    
    try:
        import kagglehub
        
        print("\n[*] Downloading pothole dataset from Kaggle...")
        print("Dataset: andrewmvd/pothole-detection")
        print("This is a YOLO-format dataset for pothole detection")
        print("Download size: ~200MB")
        print("\nUsing kagglehub - no API credentials needed!")
        print("This may take a few minutes...\n")
        
        # Download dataset using kagglehub
        # This automatically downloads to ~/.cache/kagglehub/
        dataset_path = kagglehub.dataset_download('andrewmvd/pothole-detection')
        
        print(f"\n[+] Dataset downloaded successfully!")
        print(f"Location: {dataset_path}")
        
        # Create a symlink or copy to our data directory
        from pathlib import Path
        import shutil
        
        data_dir = Path('data')
        data_dir.mkdir(exist_ok=True)
        
        source = Path(dataset_path)
        
        # Copy dataset contents to our data directory
        print("\n[*] Organizing dataset...")
        for item in source.iterdir():
            dest = data_dir / item.name
            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                print(f"  [+] Copied: {item.name}")
            else:
                shutil.copy2(item, dest)
                print(f"  [+] Copied: {item.name}")
        
        # Verify dataset structure
        print("\n[*] Checking dataset structure...")
        
        # Look for common YOLO dataset folders
        train_dir = None
        valid_dir = None
        
        for item in data_dir.rglob('*'):
            if item.is_dir():
                if 'train' in item.name.lower():
                    train_dir = item
                if 'valid' in item.name.lower() or 'val' in item.name.lower():
                    valid_dir = item
        
        if train_dir:
            print(f"[+] Found training directory: {train_dir.relative_to(data_dir)}")
        if valid_dir:
            print(f"[+] Found validation directory: {valid_dir.relative_to(data_dir)}")
        
        # Check for YAML config files
        yaml_files = list(data_dir.rglob('*.yaml'))
        if yaml_files:
            print(f"\n[+] Found YOLO config file: {yaml_files[0].name}")
            return True
        else:
            print("\n[!] Warning: No YAML config file found.")
            print("The training script will create one automatically.")
            return True
            
    except ImportError:
        print("\n[-] Error: kagglehub is not installed!")
        print("\nPlease install it:")
        print("  pip install kagglehub")
        return False
        
    except Exception as e:
        print(f"\n[-] Error downloading dataset: {e}")
        print("\nTroubleshooting:")
        print("- Check your internet connection")
        print("- Make sure kagglehub is installed: pip install kagglehub")
        print("- Visit: https://www.kaggle.com/datasets/andrewmvd/pothole-detection")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Pothole Detection Dataset Downloader")
    print("=" * 60)
    
    success = download_dataset()
    
    if success:
        print("\n" + "=" * 60)
        print("[+] Setup complete! You can now run train.py")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("[-] Setup failed. Please fix the errors above.")
        print("=" * 60)
