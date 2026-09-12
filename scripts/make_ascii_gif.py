#!/usr/bin/env python3
"""
Generates an animated GIF terminal photo/ASCII module for the GitHub Profile README.
Outputs to assets/ascii-profile.gif.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_ascii_module_gif(output_path):
    width, height = 350, 320
    bg_color = (13, 17, 23) # #0d1117
    border_color = (48, 54, 61) # #30363d
    title_bar_color = (22, 27, 34) # #161b22

    try:
        font_main = ImageFont.truetype("consola.ttf", 11)
        font_bold = ImageFont.truetype("consolab.ttf", 11)
    except IOError:
        font_main = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    prepped_image = os.path.join(os.path.dirname(output_path), "source-prepped.png")
    
    frames = []

    def draw_base():
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, width - 1, height - 1], outline=border_color, width=1)
        draw.rectangle([1, 1, width - 2, 24], fill=title_bar_color)
        draw.ellipse([14, 8, 22, 16], fill=(255, 95, 86))
        draw.ellipse([26, 8, 34, 16], fill=(255, 189, 46))
        draw.ellipse([38, 8, 46, 16], fill=(27, 201, 63))
        draw.text((54, 5), "photo-module.sh", fill=(139, 148, 158), font=font_main)
        return img, draw

    if os.path.exists(prepped_image):
        # Convert prepped photo to animated ASCII typewriter GIF
        img_photo = Image.open(prepped_image).convert("L")
        target_cols = 42
        aspect_ratio = 0.55
        target_rows = int((img_photo.height / img_photo.width) * target_cols * aspect_ratio)
        img_resized = img_photo.resize((target_cols, min(target_rows, 24)))
        pixels = img_resized.load()

        RAMP = " .`:-=+*cs#%@"
        ramp_len = len(RAMP)
        ascii_lines = []
        for y in range(img_resized.height):
            row_chars = []
            for x in range(img_resized.width):
                val = pixels[x, y]
                char = RAMP[int((val / 255.0) * (ramp_len - 1))]
                row_chars.append(char)
            ascii_lines.append("".join(row_chars))

        # Typewriter reveal rows
        for row_count in range(1, len(ascii_lines) + 1):
            img_frame, draw = draw_base()
            for r_idx in range(row_count):
                draw.text((20, 36 + r_idx * 10), ascii_lines[r_idx], fill=(57, 211, 83), font=font_main)
            frames.append(img_frame)

        # Hold state
        for blink in range(10):
            img_frame, draw = draw_base()
            for r_idx, line in enumerate(ascii_lines):
                draw.text((20, 36 + r_idx * 10), line, fill=(57, 211, 83), font=font_main)
            if blink % 2 == 0:
                cx = 20 + font_main.getbbox(ascii_lines[-1])[2]
                draw.rectangle([cx, 36 + (len(ascii_lines)-1)*10, cx+6, 46 + (len(ascii_lines)-1)*10], fill=(57, 211, 83))
            frames.append(img_frame)

    else:
        # Placeholder terminal module with animated matrix scanner bar
        scanner_width = 24
        
        # Build 20 scanner position frames
        for frame_num in range(24):
            img_frame, draw = draw_base()
            
            # Position of scanner dot
            pos = frame_num % scanner_width
            if (frame_num // scanner_width) % 2 == 1:
                pos = scanner_width - 1 - pos

            bar_chars = ["="] * scanner_width
            bar_chars[pos] = "█"
            bar_str = "[" + "".join(bar_chars) + "]"

            lines = [
                ("┌────────────────────────────────────────┐", (79, 192, 255)),
                ("│  [ PHOTO_MODULE ]                      │", (57, 211, 83)),
                ("│  status : awaiting_input               │", (57, 211, 83)),
                ("│  mode   : ascii_vision_v2              │", (139, 148, 158)),
                (f"│  scan   : {bar_str}   │", (88, 166, 255)),
                ("├────────────────────────────────────────┤", (79, 192, 255)),
                ("│                                        │", (139, 148, 158)),
                ("│   1. Add photo to assets/              │", (201, 209, 217)),
                ("│   2. Run python scripts/prep_photo.py  │", (201, 209, 217)),
                ("│   3. Run make_ascii_gif.py             │", (201, 209, 217)),
                ("│                                        │", (139, 148, 158)),
                ("└────────────────────────────────────────┘", (79, 192, 255)),
            ]

            start_y = 42
            for idx, (text_line, color) in enumerate(lines):
                draw.text((18, start_y + idx * 21), text_line, fill=color, font=font_main)

            frames.append(img_frame)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0
    )
    print(f"Generated animated ASCII profile GIF at: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    output_path = os.path.join(project_root, "assets", "ascii-profile.gif")
    create_ascii_module_gif(output_path)

if __name__ == "__main__":
    main()
