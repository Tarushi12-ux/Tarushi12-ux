#!/usr/bin/env python3
"""
Generates a modern, compact neofetch-style terminal info card SVG.
Output: info-card.svg
"""

import sys
import os

# ==============================================================================
# CONFIGURATION - STRICTLY AUTHENTIC PROFILE DETAILS ONLY
# ==============================================================================
CONFIG = {
    "USER": "Tarushi12-ux",
    "FOCUS": "Computer Vision & AI Development",
    "STACK": "Python • PyTorch • OpenCV • JavaScript • React",
    "PROJECTS": "Campus Object Detection • Air Script AI • Falco",
    "BUILDING": "Real-Time Object Detection & Vision Pipelines"
}
# ==============================================================================

def generate_info_card(config, output_path):
    width = 490
    height = 320

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
            .title-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11px; fill: #8b949e; }
            
            .prompt-user { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12.5px; font-weight: bold; fill: #39d353; }
            .prompt-at { fill: #8b949e; }
            .prompt-host { fill: #58a6ff; }
            .prompt-cmd { fill: #c9d1d9; }
            .separator { stroke: #30363d; stroke-width: 1px; }

            .key-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11.5px; font-weight: bold; fill: #58a6ff; }
            .val-text { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 11.5px; fill: #c9d1d9; }
            .val-highlight { fill: #7ee787; font-weight: 500; }
            .val-accent { fill: #79c0ff; }
            
            /* CRITICAL FIX: opacity defaults to 1 so SVG renders instantly on GitHub */
            .row-line { opacity: 1; animation: lineSlideIn 0.4s ease-out; }
            @keyframes lineSlideIn {
                from { opacity: 0.3; transform: translateX(-6px); }
                to { opacity: 1; transform: translateX(0); }
            }
        </style>
    ''')
    svg_lines.append('</defs>')

    # Background card
    svg_lines.append(f'<rect class="bg" width="{width}" height="{height}" />')
    svg_lines.append(f'<rect class="card-border" width="{width - 1}" height="{height - 1}" x="0.5" y="0.5" />')

    # Top Terminal Header
    svg_lines.append(f'<rect class="title-bar" width="{width}" height="28" />')
    svg_lines.append('<circle cx="16" cy="14" r="4.5" class="dot-red" />')
    svg_lines.append('<circle cx="28" cy="14" r="4.5" class="dot-yellow" />')
    svg_lines.append('<circle cx="40" cy="14" r="4.5" class="dot-green" />')
    svg_lines.append(f'<text x="54" y="18" class="title-text">neofetch --user {config["USER"]}</text>')

    # Terminal Command Line
    svg_lines.append(
        '<text x="20" y="52" class="prompt-user row-line" style="animation-delay: 0.05s;">'
        f'{config["USER"]}<tspan class="prompt-at">@</tspan><tspan class="prompt-host">github</tspan> '
        '<tspan class="prompt-cmd">:~$ neofetch</tspan>'
        '</text>'
    )
    
    # Separator Line
    svg_lines.append('<line x1="20" y1="62" x2="470" y2="62" class="separator row-line" style="animation-delay: 0.1s;" />')

    # Info Fields
    fields = [
        ("USER", config["USER"], "val-highlight"),
        ("FOCUS", config["FOCUS"], "val-text"),
        ("STACK", config["STACK"], "val-accent"),
        ("PROJECTS", config["PROJECTS"], "val-text"),
        ("BUILDING", config["BUILDING"], "val-highlight"),
    ]

    start_y = 92
    line_spacing = 34

    for idx, (key, val, val_class) in enumerate(fields):
        y_pos = start_y + idx * line_spacing
        delay = round(0.12 + idx * 0.05, 2)
        key_str = f"{key:<10}:"
        
        svg_lines.append(
            f'<text x="20" y="{y_pos}" class="row-line" style="animation-delay: {delay}s;">'
            f'<tspan class="key-text">{key_str}</tspan> '
            f'<tspan class="{val_class}">{val}</tspan>'
            '</text>'
        )

    # Accent Dots Footer
    dot_y = start_y + len(fields) * line_spacing + 12
    colors = ["#161b22", "#ff5f56", "#27c93f", "#ffbd2e", "#58a6ff", "#bc8cff", "#39d353", "#c9d1d9"]
    
    svg_lines.append(f'<g class="row-line" style="animation-delay: {round(0.12 + len(fields) * 0.05, 2)}s;">')
    for i, col in enumerate(colors):
        cx = 20 + i * 20
        svg_lines.append(f'<rect x="{cx}" y="{dot_y}" width="14" height="10" fill="{col}" rx="2" />')
    svg_lines.append('</g>')

    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"Generated info card SVG at: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    output_path = os.path.join(project_root, "info-card.svg")

    generate_info_card(CONFIG, output_path)

if __name__ == "__main__":
    main()
