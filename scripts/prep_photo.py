#!/usr/bin/env python3
"""
Prepares the user's actual photo for ASCII conversion.
Crops around the portrait subject, enhances contrast, and converts to grayscale.
Saves result to assets/source-prepped.png.
"""

import sys
import os
from PIL import Image, ImageOps, ImageEnhance

DEFAULT_PHOTO = r"C:\Users\tarus\OneDrive\Desktop\WhatsApp Image 2026-09-12 at 1.41.30 PM.jpeg"

def prep_photo(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Photo file not found at: {input_path}")
        sys.exit(1)

    print(f"Processing source photo: {input_path}...")
    img = Image.open(input_path).convert("RGB")
    w, h = img.size

    # Intelligent portrait crop around the subject
    # Crop central region to focus on face/upper body
    if w > h:
        crop_w = int(h * 0.85)
        left = max(0, int((w - crop_w) / 2))
        right = min(w, left + crop_w)
        crop_box = (left, 0, right, h)
        img = img.crop(crop_box)

    # Convert to grayscale
    gray = ImageOps.grayscale(img)

    # Enhance contrast to define features cleanly for ASCII shading
    enhancer = ImageEnhance.Contrast(gray)
    high_contrast = enhancer.enhance(1.6)
    
    # Sharpness enhancement
    sharpener = ImageEnhance.Sharpness(high_contrast)
    sharp = sharpener.enhance(1.4)

    final_img = ImageOps.autocontrast(sharp, cutoff=1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_img.save(output_path)
    print(f"Prepped photo successfully saved to: {output_path} (Size: {final_img.size})")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    output_path = os.path.join(project_root, "assets", "source-prepped.png")

    input_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PHOTO
    prep_photo(input_path, output_path)

if __name__ == "__main__":
    main()
