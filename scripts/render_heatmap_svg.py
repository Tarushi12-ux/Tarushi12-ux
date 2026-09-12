#!/usr/bin/env python3
"""
Reads data/contributions.json and renders a sleek, animated SVG contribution heatmap.
Outputs to contrib-heatmap.svg.
"""

import sys
import os
import json
from datetime import datetime

PALETTE = [
    "#161b22", # Level 0 - None
    "#0e4429", # Level 1 - Low
    "#006d32", # Level 2 - Medium-Low
    "#26a641", # Level 3 - Medium-High
    "#39d353", # Level 4 - High
]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_LABELS = ["", "Mon", "", "Wed", "", "Fri", ""]

def render_svg(data, output_path):
    contributions = data.get("contributions", [])
    total = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    username = data.get("username", "developer")

    if not contributions:
        print("No contribution data found to render.")
        return

    # Parse dates and organize into weeks (Sunday=0 to Saturday=6)
    parsed_days = []
    for d in contributions:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        parsed_days.append({
            "date": d["date"],
            "dt": dt,
            "count": d["count"],
            "level": min(max(d["level"], 0), 4)
        })

    parsed_days.sort(key=lambda x: x["dt"])

    # Group into weeks
    weeks = []
    current_week = []
    
    # Align the first week
    first_dt = parsed_days[0]["dt"]
    # wday: Mon=0 .. Sun=6 in python, convert to Sun=0..Sat=6
    first_wday = (first_dt.weekday() + 1) % 7
    
    # Pad beginning of first week if necessary
    for _ in range(first_wday):
        current_week.append(None)

    for day in parsed_days:
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []

    if current_week:
        # Pad remaining days of last week
        while len(current_week) < 7:
            current_week.append(None)
        weeks.append(current_week)

    # Keep at most 53 weeks
    weeks = weeks[-53:]

    # SVG layout parameters
    svg_width = 860
    svg_height = 200

    padding_x = 35
    padding_y = 55
    cell_size = 11
    cell_gap = 3
    cell_step = cell_size + cell_gap # 14px

    start_x = padding_x + 30 # Offset for weekday labels
    start_y = padding_y + 20 # Offset for month labels

    # Month label positioning
    month_labels = []
    last_month = -1
    for w_idx, week in enumerate(weeks):
        for day in week:
            if day and day["dt"].day <= 7:
                m = day["dt"].month
                if m != last_month:
                    last_month = m
                    x_pos = start_x + w_idx * cell_step
                    month_labels.append((MONTH_NAMES[m - 1], x_pos))
                    break

    # Build SVG content
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_lines.append('<defs>')
    svg_lines.append('''
        <style>
            .bg { fill: #0d1117; rx: 8px; ry: 8px; }
            .card-border { stroke: #30363d; stroke-width: 1px; fill: none; rx: 8px; ry: 8px; }
            .header-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; fill: #58a6ff; }
            .sub-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; fill: #8b949e; }
            .label-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10px; fill: #8b949e; }
            .cell { rx: 2px; ry: 2px; opacity: 0; animation: fadeInCell 0.4s ease-out forwards; }
            .legend-cell { rx: 2px; ry: 2px; }

            @keyframes fadeInCell {
                0% { opacity: 0; transform: scale(0.4); }
                100% { opacity: 1; transform: scale(1); }
            }
        </style>
    ''')
    svg_lines.append('</defs>')

    # Background card
    svg_lines.append(f'<rect class="bg" width="{svg_width}" height="{svg_height}" />')
    svg_lines.append(f'<rect class="card-border" width="{svg_width - 1}" height="{svg_height - 1}" x="0.5" y="0.5" />')

    # Top Terminal / Header
    header_title = f"{username}@github ~ $ ./contributions.sh"
    summary_text = f"{total:,} contributions in the last year • Streak: {current_streak}d (max: {longest_streak}d)"
    
    svg_lines.append(f'<text x="{padding_x}" y="28" class="header-text">&gt; {header_title}</text>')
    svg_lines.append(f'<text x="{svg_width - padding_x}" y="28" class="sub-text" text-anchor="end">{summary_text}</text>')
    
    # Divider line
    svg_lines.append(f'<line x1="{padding_x}" y1="38" x2="{svg_width - padding_x}" y2="38" stroke="#21262d" stroke-width="1" />')

    # Month Labels
    for name, x_pos in month_labels:
        svg_lines.append(f'<text x="{x_pos}" y="{start_y - 6}" class="label-text">{name}</text>')

    # Day of Week Labels
    for d_idx, label in enumerate(DAY_LABELS):
        if label:
            y_pos = start_y + d_idx * cell_step + 9
            svg_lines.append(f'<text x="{start_x - 8}" y="{y_pos}" class="label-text" text-anchor="end">{label}</text>')

    # Grid Cells
    for w_idx, week in enumerate(weeks):
        for d_idx, day in enumerate(week):
            if day is None:
                continue
            x_pos = start_x + w_idx * cell_step
            y_pos = start_y + d_idx * cell_step
            color = PALETTE[day["level"]]
            
            # Staggered animation delay based on diagonal position
            delay = round((w_idx * 0.01 + d_idx * 0.02), 3)
            
            # Cell rect with title tooltip
            cell_svg = (
                f'<rect class="cell" x="{x_pos}" y="{y_pos}" width="{cell_size}" height="{cell_size}" '
                f'fill="{color}" style="animation-delay: {delay}s; transform-origin: {x_pos + 5}px {y_pos + 5}px;">'
                f'<title>{day["count"]} contributions on {day["date"]}</title></rect>'
            )
            svg_lines.append(cell_svg)

    # Legend Footer (Bottom Right)
    legend_x = svg_width - padding_x - 140
    legend_y = svg_height - 18
    
    svg_lines.append(f'<text x="{legend_x - 28}" y="{legend_y + 9}" class="label-text">Less</text>')
    for i, color in enumerate(PALETTE):
        lx = legend_x + i * (cell_size + 3)
        svg_lines.append(f'<rect class="legend-cell" x="{lx}" y="{legend_y}" width="{cell_size}" height="{cell_size}" fill="{color}" />')
    svg_lines.append(f'<text x="{legend_x + len(PALETTE) * (cell_size + 3) + 4}" y="{legend_y + 9}" class="label-text">More</text>')

    svg_lines.append('</svg>')

    # Save output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"Successfully generated heatmap SVG at: {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    json_path = os.path.join(project_root, "data", "contributions.json")
    output_path = os.path.join(project_root, "contrib-heatmap.svg")

    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist. Run fetch_contributions.py first.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    render_svg(data, output_path)

if __name__ == "__main__":
    main()
