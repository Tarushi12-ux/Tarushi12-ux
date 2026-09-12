#!/usr/bin/env python3
"""
Converts assets/source-prepped.png (the user's actual photo) into a recognizable,
animated ASCII terminal portrait GIF for the GitHub profile README.
Output: assets/ascii-profile.gif
"""

import sys
import os
from PIL import Image, ImageDraw, ImageFont

# Detailed character ramp from bright (space) to dark (dense char)
RAMP = " .':;!~+*e#%@"

def create_ascii_portrait_gif(prepped_image_path, output_path):
    if not os.path.exists(prepped_image_path):
        print(f"Error: Prepped image not found at {prepped_image_path}")
        sys.exit(1)

    print(f"Loading prepped photo from: {prepped_image_path}")
    img_photo = Image.open(prepped_image_path).convert("L")

    # Grid size for 370x350 canvas: 52 cols x 22 rows
    target_cols = 52
    target_rows = 22

    img_resized = img_photo.resize((target_cols, target_rows), Image.Resampling.LANCZOS)
    pixels = img_resized.load()

    ramp_len = len(RAMP)
    ascii_lines = []
    for y in range(target_rows):
        row_chars = []
        for x in range(target_cols):
            val = pixels[x, y]
            # Map pixel brightness (0=black/dark, 255=white/bright)
            char_idx = int((val / 255.0) * (ramp_len - 1))
            char = RAMP[char_idx]
            row_chars.append(char)
        ascii_lines.append("".join(row_chars))

    # Rendering setup
    width, height = 370, 350
    bg_color = (13, 17, 23)      # #0d1117
    border_color = (48, 54, 61)  # #30363d
    title_bar_color = (22, 27, 34) # #161b22
    green_accent = (57, 211, 83) # #39d353
    cyan_accent = (88, 166, 255) # #58a6ff
    text_dim = (139, 148, 158)   # #8b949e

    try:
        font_ascii = ImageFont.truetype("consola.ttf", 9)
        font_text = ImageFont.truetype("consola.ttf", 11)
        font_bold = ImageFont.truetype("consolab.ttf", 11)
    except IOError:
        font_ascii = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_bold = ImageFont.load_default()

    frames = []

    def draw_base_frame():
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, width - 1, height - 1], outline=border_color, width=1)
        draw.rectangle([1, 1, width - 2, 24], fill=title_bar_color)
        draw.ellipse([14, 8, 22, 16], fill=(255, 95, 86))
        draw.ellipse([26, 8, 34, 16], fill=(255, 189, 46))
        draw.ellipse([38, 8, 46, 16], fill=(27, 201, 63))
        draw.text((54, 5), "PROFILE.EXE --ascii-renderer", fill=text_dim, font=font_text)
        return img, draw

    # Step 1: Typewriter reveal of ASCII face portrait
    for reveal_rows in range(1, target_rows + 1):
        img_frame, draw = draw_base_frame()
        for r_idx in range(reveal_rows):
            line = ascii_lines[r_idx]
            draw.text((18, 34 + r_idx * 9), line, fill=green_accent, font=font_ascii)
        frames.append(img_frame)

    # Step 2: Matrix Scanner Line sweeping over face
    for scan_y in range(target_rows):
        img_frame, draw = draw_base_frame()
        for r_idx, line in enumerate(ascii_lines):
            color = cyan_accent if r_idx == scan_y else green_accent
            draw.text((18, 34 + r_idx * 9), line, fill=color, font=font_ascii)
        # Highlight bar line
        scan_pixel_y = 34 + scan_y * 9 + 4
        draw.line([18, scan_pixel_y, width - 18, scan_pixel_y], fill=(126, 231, 135), width=1)
        frames.append(img_frame)

    # Step 3: Typewriter bottom profile details
    info_fields = [
        ("USER", "Tarushi12-ux", green_accent),
        ("MODE", "Computer Vision", cyan_accent),
        ("STATUS", "ONLINE 🟢", (126, 231, 135))
    ]

    base_y_info = 34 + target_rows * 9 + 8

    for f_idx in range(1, len(info_fields) + 1):
        for c_idx in range(1, len(info_fields[f_idx - 1][1]) + 1):
            img_frame, draw = draw_base_frame()
            # Draw ASCII face
            for r_idx, line in enumerate(ascii_lines):
                draw.text((18, 34 + r_idx * 9), line, fill=green_accent, font=font_ascii)
            
            # Separator line
            draw.line([18, base_y_info - 4, width - 18, base_y_info - 4], fill=border_color, width=1)

            # Draw typed info lines
            for i in range(f_idx):
                k, v, col = info_fields[i]
                y_p = base_y_info + i * 18
                key_str = f"{k:<7}: "
                draw.text((20, y_p), key_str, fill=cyan_accent, font=font_bold)
                k_w = font_bold.getbbox(key_str)[2] - font_bold.getbbox(key_str)[0]
                
                v_str = v[:c_idx] if i == (f_idx - 1) else v
                draw.text((20 + k_w, y_p), v_str, fill=col, font=font_text)
                
                # Cursor at active typing line
                if i == (f_idx - 1):
                    v_w = font_text.getbbox(v_str)[2] - font_text.getbbox(v_str)[0]
                    cx = 22 + k_w + v_w
                    draw.rectangle([cx, y_p + 1, cx + 6, y_p + 11], fill=green_accent)

            frames.append(img_frame)

    # Hold state with blinking cursor
    for blink in range(10):
        img_frame, draw = draw_base_frame()
        for r_idx, line in enumerate(ascii_lines):
            draw.text((18, 34 + r_idx * 9), line, fill=green_accent, font=font_ascii)
        draw.line([18, base_y_info - 4, width - 18, base_y_info - 4], fill=border_color, width=1)

        for i, (k, v, col) in enumerate(info_fields):
            y_p = base_y_info + i * 18
            key_str = f"{k:<7}: "
            draw.text((20, y_p), key_str, fill=cyan_accent, font=font_bold)
            k_w = font_bold.getbbox(key_str)[2] - font_bold.getbbox(key_str)[0]
            draw.text((20 + k_w, y_p), v, fill=col, font=font_text)

        if blink % 2 == 0:
            last_v = info_fields[-1][1]
            last_w = font_text.getbbox(last_v)[2] - font_text.getbbox(last_v)[0]
            k_w = font_bold.getbbox("STATUS : ")[2] - font_bold.getbbox("STATUS : ")[0]
            cx = 22 + k_w + last_w
            draw.rectangle([cx, base_y_info + 2 * 18 + 1, cx + 6, base_y_info + 2 * 18 + 11], fill=green_accent)

        frames.append(img_frame)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    durations = [60] * (len(frames) - 10) + [400] * 10
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0
    )
    print(f"Successfully generated ASCII portrait GIF from user photo at: {output_path}")
    print(f"Total Frames: {len(frames)}, File Size: {os.path.getsize(output_path) / 1024:.1f} KB")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    prepped_image = os.path.join(project_root, "assets", "source-prepped.png")
    output_path = os.path.join(project_root, "assets", "ascii-profile.gif")

    create_ascii_portrait_gif(prepped_image, output_path)

if __name__ == "__main__":
    main()
