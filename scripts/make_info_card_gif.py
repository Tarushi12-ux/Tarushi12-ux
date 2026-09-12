#!/usr/bin/env python3
"""
Generates an animated GIF neofetch terminal info card for the GitHub Profile README.
Output: assets/info-card.gif
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Strictly authentic details only
FIELDS = [
    ("USER", "Tarushi12-ux", (126, 231, 135)),      # Green
    ("FOCUS", "Computer Vision & AI", (201, 209, 217)), # Text
    ("STACK", "Python • PyTorch • OpenCV • React", (121, 192, 255)), # Cyan
    ("PROJECTS", "Campus Object Detection • Air Script AI • Falco", (201, 209, 217)),
    ("BUILDING", "Real-Time Object Detection Pipelines", (126, 231, 135)),
    ("STATUS", "ONLINE 🟢", (57, 211, 83))           # Active Green
]

def create_info_card_gif(output_path):
    width, height = 490, 320
    bg_color = (13, 17, 23) # #0d1117
    border_color = (48, 54, 61) # #30363d
    title_bar_color = (22, 27, 34) # #161b22

    try:
        font_main = ImageFont.truetype("consola.ttf", 12)
        font_key = ImageFont.truetype("consolab.ttf", 12)
    except IOError:
        font_main = ImageFont.load_default()
        font_key = ImageFont.load_default()

    frames = []

    def draw_base_frame():
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, width - 1, height - 1], outline=border_color, width=1)
        draw.rectangle([1, 1, width - 2, 24], fill=title_bar_color)
        draw.ellipse([14, 8, 22, 16], fill=(255, 95, 86))
        draw.ellipse([26, 8, 34, 16], fill=(255, 189, 46))
        draw.ellipse([38, 8, 46, 16], fill=(27, 201, 63))
        draw.text((54, 5), "neofetch --user Tarushi12-ux", fill=(139, 148, 158), font=font_main)
        
        # Command line prompt
        draw.text((20, 36), "tarushi", fill=(57, 211, 83), font=font_key)
        u_width = font_key.getbbox("tarushi")[2] - font_key.getbbox("tarushi")[0]
        draw.text((20 + u_width, 36), "@github:~$ neofetch", fill=(201, 209, 217), font=font_main)
        draw.line([20, 56, width - 20, 56], fill=(48, 54, 61), width=1)
        return img, draw

    # Build typing frame steps
    steps = []
    # Step 1..N: Lines reveal one by one
    for line_idx in range(1, len(FIELDS) + 1):
        for char_idx in range(1, len(FIELDS[line_idx - 1][1]) + 1):
            steps.append((line_idx - 1, char_idx, False))

    # Hold state with blinking cursor / status pulse
    for blink in range(12):
        steps.append((len(FIELDS) - 1, len(FIELDS[-1][1]), blink % 2 == 0))

    start_y = 74
    line_spacing = 34

    for max_line, partial_chars, cursor_on in steps:
        img, draw = draw_base_frame()
        
        for idx in range(max_line + 1):
            key, val, val_color = FIELDS[idx]
            y_pos = start_y + idx * line_spacing
            
            # Format key (padded)
            key_str = f"{key:<10}: "
            draw.text((20, y_pos), key_str, fill=(88, 166, 255), font=font_key)
            k_width = font_key.getbbox(key_str)[2] - font_key.getbbox(key_str)[0]
            
            # Partial or full text
            current_val = val[:partial_chars] if idx == max_line else val
            draw.text((20 + k_width, y_pos), current_val, fill=val_color, font=font_main)

            # Cursor at current typing line
            if idx == max_line and cursor_on:
                v_width = font_main.getbbox(current_val)[2] - font_main.getbbox(current_val)[0]
                cx = 22 + k_width + v_width
                draw.rectangle([cx, y_pos + 1, cx + 7, y_pos + 13], fill=(57, 211, 83))

        # Bottom accent palette dots
        dot_y = start_y + len(FIELDS) * line_spacing + 10
        colors = [(22, 27, 34), (255, 95, 86), (39, 201, 63), (255, 189, 46), (88, 166, 255), (188, 140, 255), (57, 211, 83), (201, 209, 217)]
        for i, col in enumerate(colors):
            cx = 20 + i * 18
            draw.rectangle([cx, dot_y, cx + 12, dot_y + 8], fill=col)

        frames.append(img)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    durations = [50] * (len(frames) - 12) + [350] * 12
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0
    )
    print(f"Generated animated info card GIF at: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    output_path = os.path.join(project_root, "assets", "info-card.gif")
    create_info_card_gif(output_path)

if __name__ == "__main__":
    main()
