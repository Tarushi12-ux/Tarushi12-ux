#!/usr/bin/env python3
"""
Converts assets/source-prepped.png into a monochrome animated ASCII SVG portrait.
If no prepped image is found, generates a clean terminal placeholder SVG displaying "ADD YOUR PHOTO".
Output: ascii-profile.svg
"""

import sys
import os

RAMP = " .`:-=+*cs#%@" # Bright (sparse space) -> Dark (dense char)

def generate_ascii_from_image(image_path, svg_output_path):
    try:
        from PIL import Image
    except ImportError:
        print("PIL/Pillow not installed. Cannot process image.")
        return False

    img = Image.open(image_path).convert("L")
    
    # Target grid resolution (~65 cols x ~45 rows for 370x370 SVG)
    target_cols = 64
    aspect_ratio = 0.55 # Font aspect ratio (height is ~1.8x width)
    width, height = img.size
    target_rows = int((height / width) * target_cols * aspect_ratio)

    img_resized = img.resize((target_cols, target_rows))
    pixels = img_resized.load()

    lines = []
    ramp_len = len(RAMP)
    for y in range(target_rows):
        line_chars = []
        for x in range(target_cols):
            val = pixels[x, y]
            char_idx = int((val / 255.0) * (ramp_len - 1))
            char = RAMP[char_idx]
            # Replace spaces with non-breaking space for XML preserving whitespace
            line_chars.append("&#160;" if char == " " else char)
        lines.append("".join(line_chars))

    render_ascii_svg(lines, svg_output_path, is_placeholder=False)
    return True

def generate_placeholder_svg(svg_output_path):
    # ASCII box art placeholder
    placeholder_ascii = [
        "+-----------------------------------------+",
        "|                                         |",
        "|           [ PROFILE PORTRAIT ]          |",
        "|                                         |",
        "|             ADD YOUR PHOTO              |",
        "|                                         |",
        "|     1. Add photo to assets/             |",
        "|     2. Run python scripts/prep_photo.py |",
        "|     3. Run make_ascii_svg.py            |",
        "|                                         |",
        "+-----------------------------------------+"
    ]
    render_ascii_svg(placeholder_ascii, svg_output_path, is_placeholder=True)

def render_ascii_svg(lines, output_path, is_placeholder=False):
    width = 370
    height = 370

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('<defs>')
    svg_lines.append('''
        <style>
            .bg { fill: #0d1117; rx: 8px; ry: 8px; }
            .card-border { stroke: #30363d; stroke-width: 1px; fill: none; rx: 8px; ry: 8px; }
            .title-bar { fill: #161b22; rx: 8px; ry: 8px; }
            .dot-red { fill: #ff5f56; }
            .dot-yellow { fill: #ffbd2e; }
            .dot-green { fill: #27c93f; }
            .title-text { font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 11px; fill: #8b949e; }
            .ascii-text {
                font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
                font-size: 8px;
                fill: #58a6ff;
                white-space: pre;
                letter-spacing: 1px;
            }
            .placeholder-text {
                font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
                font-size: 11px;
                fill: #8b949e;
                white-space: pre;
            }
            .highlight-line { fill: #39d353; font-weight: bold; }
            .row { opacity: 0; animation: rowFadeIn 0.3s ease-out forwards; }
            @keyframes rowFadeIn {
                from { opacity: 0; transform: translateY(2px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    ''')
    svg_lines.append('</defs>')

    # Background card
    svg_lines.append(f'<rect class="bg" width="{width}" height="{height}" />')
    svg_lines.append(f'<rect class="card-border" width="{width - 1}" height="{height - 1}" x="0.5" y="0.5" />')

    # Top Terminal Window Header
    svg_lines.append(f'<rect class="title-bar" width="{width}" height="28" />')
    svg_lines.append('<circle cx="16" cy="14" r="4.5" class="dot-red" />')
    svg_lines.append('<circle cx="28" cy="14" r="4.5" class="dot-yellow" />')
    svg_lines.append('<circle cx="40" cy="14" r="4.5" class="dot-green" />')
    
    title = "ascii-art.sh" if not is_placeholder else "portrait.ascii (no photo)"
    svg_lines.append(f'<text x="54" y="18" class="title-text">{title}</text>')

    start_y = 52
    line_height = 12 if is_placeholder else 7

    for idx, line in enumerate(lines):
        delay = round(0.05 + idx * 0.04, 2)
        y_pos = start_y + idx * line_height
        
        css_class = "placeholder-text" if is_placeholder else "ascii-text"
        if is_placeholder and "ADD YOUR PHOTO" in line:
            css_class += " highlight-line"
            
        svg_lines.append(
            f'<text x="20" y="{y_pos}" class="{css_class} row" style="animation-delay: {delay}s;">{line}</text>'
        )

    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"Generated ASCII profile SVG at: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    prepped_image = os.path.join(project_root, "assets", "source-prepped.png")
    svg_output = os.path.join(project_root, "ascii-profile.svg")

    if os.path.exists(prepped_image):
        print(f"Found prepped image at {prepped_image}. Converting to ASCII SVG...")
        success = generate_ascii_from_image(prepped_image, svg_output)
        if not success:
            generate_placeholder_svg(svg_output)
    else:
        print("No prepped photo found in assets/source-prepped.png.")
        print("Generating terminal placeholder SVG ('ADD YOUR PHOTO').")
        generate_placeholder_svg(svg_output)

if __name__ == "__main__":
    main()
