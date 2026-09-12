#!/usr/bin/env python3
"""
Generates an animated GIF terminal header for the GitHub Profile README.
Output: assets/header-animation.gif
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_header_gif(output_path):
    width, height = 860, 90
    bg_color = (13, 17, 23) # #0d1117
    border_color = (48, 54, 61) # #30363d
    title_bar_color = (22, 27, 34) # #161b22
    
    # Text colors
    green_color = (57, 211, 83) # #39d353
    at_color = (139, 148, 158) # #8b949e
    host_color = (88, 166, 255) # #58a6ff
    text_color = (201, 209, 217) # #c9d1d9
    sub_color = (165, 214, 255) # #a5d6ff

    try:
        font_cmd = ImageFont.truetype("consola.ttf", 13)
        font_text = ImageFont.truetype("consola.ttf", 12)
    except IOError:
        font_cmd = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # Story steps to animate
    cmd1_user = "tarushi"
    cmd1_rest = "@github:~$ whoami"
    out1_text = "> Tarushi12-ux (Computer Vision & AI Developer)"
    cmd2_user = "tarushi"
    cmd2_rest = "@github:~$ status"
    out2_text = "> Building real-time vision pipelines ⚡"

    frames = []

    def draw_base_frame():
        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        # Outer border
        draw.rectangle([0, 0, width - 1, height - 1], outline=border_color, width=1)
        # Title bar
        draw.rectangle([1, 1, width - 2, 24], fill=title_bar_color)
        # Dots
        draw.ellipse([14, 8, 22, 16], fill=(255, 95, 86))
        draw.ellipse([26, 8, 34, 16], fill=(255, 189, 46))
        draw.ellipse([38, 8, 46, 16], fill=(27, 201, 63))
        # Title
        draw.text((58, 5), "tarushi@github:~", fill=(139, 148, 158), font=font_text)
        return img, draw

    # Animation script
    full_sequence = [
        # (cmd1_typed, out1_typed, cmd2_typed, out2_typed, cursor_on)
    ]

    # Type command 1
    for i in range(1, len(cmd1_rest) + 1):
        full_sequence.append((cmd1_rest[:i], "", "", "", True))

    # Output 1 typing
    for i in range(1, len(out1_text) + 1):
        full_sequence.append((cmd1_rest, out1_text[:i], "", "", True))

    # Type command 2
    for i in range(1, len(cmd2_rest) + 1):
        full_sequence.append((cmd1_rest, out1_text, cmd2_rest[:i], "", True))

    # Output 2 typing
    for i in range(1, len(out2_text) + 1):
        full_sequence.append((cmd1_rest, out1_text, cmd2_rest, out2_text[:i], True))

    # Hold state with blinking cursor
    for blink in range(10):
        full_sequence.append((cmd1_rest, out1_text, cmd2_rest, out2_text, blink % 2 == 0))

    # Render frames
    for cmd1_str, out1_str, cmd2_str, out2_str, cursor in full_sequence:
        img, draw = draw_base_frame()
        
        # Line 1: tarushi@github:~$ whoami
        if cmd1_str:
            draw.text((20, 34), cmd1_user, fill=green_color, font=font_cmd)
            # Calculate position for rest of command
            u_bbox = font_cmd.getbbox(cmd1_user)
            u_width = u_bbox[2] - u_bbox[0]
            draw.text((20 + u_width, 34), cmd1_str, fill=text_color, font=font_cmd)

        # Line 2: Output 1
        if out1_str:
            draw.text((20, 52), out1_str, fill=sub_color, font=font_text)
            if not cmd2_str and cursor:
                o_bbox = font_text.getbbox(out1_str)
                o_width = o_bbox[2] - o_bbox[0]
                draw.rectangle([22 + o_width, 53, 29 + o_width, 64], fill=green_color)
        elif cmd1_str == cmd1_rest and cursor:
            c_bbox = font_cmd.getbbox(cmd1_user + cmd1_rest)
            c_width = c_bbox[2] - c_bbox[0]
            draw.rectangle([22 + c_width, 35, 29 + c_width, 46], fill=green_color)

        # Line 3: tarushi@github:~$ status (if out1 finished)
        if cmd2_str:
            draw.text((450, 34), cmd2_user, fill=green_color, font=font_cmd)
            u_bbox = font_cmd.getbbox(cmd2_user)
            u_width = u_bbox[2] - u_bbox[0]
            draw.text((450 + u_width, 34), cmd2_str, fill=text_color, font=font_cmd)

        # Line 4: Output 2
        if out2_str:
            draw.text((450, 52), out2_str, fill=green_color, font=font_text)
            if cursor:
                o_bbox = font_text.getbbox(out2_str)
                o_width = o_bbox[2] - o_bbox[0]
                draw.rectangle([452 + o_width, 53, 459 + o_width, 64], fill=green_color)

        frames.append(img)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Save as animated GIF
    durations = [80] * (len(frames) - 10) + [400] * 10
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0
    )
    print(f"Generated animated header GIF at: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    output_path = os.path.join(project_root, "assets", "header-animation.gif")
    create_header_gif(output_path)

if __name__ == "__main__":
    main()
