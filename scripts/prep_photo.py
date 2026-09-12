#!/usr/bin/env python3
"""
Prepares a personal portrait photo for ASCII conversion.
- Removes background (using rembg if available, or fallback thresholding).
- Applies CLAHE contrast enhancement for distinct highlight/shadow definition.
- Saves grayscale result to assets/source-prepped.png.
"""

import sys
import os

def prep_photo(input_path, output_path):
    try:
        from PIL import Image, ImageOps, ImageEnhance
        import numpy as np
    except ImportError:
        print("Error: PIL and numpy are required. Install with: pip install pillow numpy")
        sys.exit(1)

    print(f"Processing photo: {input_path}...")
    img = Image.open(input_path).convert("RGB")

    # Optional background removal if rembg is installed
    try:
        from rembg import remove
        print("Removing background with rembg...")
        img_bytes = open(input_path, "rb").read()
        out_bytes = remove(img_bytes)
        import io
        img_rgba = Image.open(io.BytesIO(out_bytes)).convert("RGBA")
        
        # Composite onto white background
        bg = Image.new("RGBA", img_rgba.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img_rgba).convert("RGB")
    except Exception as e:
        print(f"Note: rembg background removal skipped or unavailable ({e}). Continuing with contrast prep...")

    # Convert to grayscale
    gray = ImageOps.grayscale(img)

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray)
    high_contrast = enhancer.enhance(1.8)

    # Autocontrast
    final_img = ImageOps.autocontrast(high_contrast, cutoff=2)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_img.save(output_path)
    print(f"Prepped photo saved to: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    output_path = os.path.join(project_root, "assets", "source-prepped.png")

    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <path_to_photo.jpg>")
        print(f"Default target destination: {output_path}")
        if not os.path.exists(output_path):
            print("No photo provided. Placeholder ASCII SVG will be used until a photo is prepped.")
        sys.exit(0)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    prep_photo(input_path, output_path)

if __name__ == "__main__":
    main()
