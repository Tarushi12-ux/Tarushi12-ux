#!/usr/bin/env python3
"""
Fetch public GitHub contribution calendar without API token.
Extracts daily contribution counts and derives statistics, saving to data/contributions.json.
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta, timezone
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    print(f"Fetching contribution calendar from {url}...")
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Map element IDs to tooltip text
    tooltips = {}
    for tt in soup.find_all("tool-tip"):
        for_id = tt.get("for")
        if for_id:
            tooltips[for_id] = tt.get_text(strip=True)
            
    days_data = []
    day_elements = soup.find_all(attrs={"data-date": True})
    
    for el in day_elements:
        date_str = el.get("data-date")
        if not date_str:
            continue
            
        level = int(el.get("data-level", 0))
        el_id = el.get("id", "")
        
        count = 0
        tooltip_text = tooltips.get(el_id, "")
        
        # Also check title or aria-label attribute if present
        if not tooltip_text:
            tooltip_text = el.get("aria-label", "") or el.get("title", "")
            
        if tooltip_text:
            match = re.search(r"(\d+)\s+contribution", tooltip_text, re.IGNORECASE)
            if match:
                count = int(match.group(1))
            elif "no contribution" in tooltip_text.lower():
                count = 0
            else:
                # Fallback to level heuristic if text doesn't match standard pattern
                count = level
        else:
            count = level

        days_data.append({
            "date": date_str,
            "count": count,
            "level": level
        })
        
    # Sort chronologically
    days_data.sort(key=lambda x: x["date"])
    
    # Calculate derived stats
    total_contributions = sum(d["count"] for d in days_data)
    
    # Best day
    best_day = {"date": None, "count": 0}
    for d in days_data:
        if d["count"] > best_day["count"]:
            best_day = {"date": d["date"], "count": d["count"]}
            
    # Monthly totals
    monthly_totals = {}
    for d in days_data:
        month_key = d["date"][:7] # YYYY-MM
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + d["count"]
        
    # Streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    for d in days_data:
        if d["count"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Current streak looking backwards from most recent entry
    for d in reversed(days_data):
        if d["count"] > 0:
            current_streak += 1
        else:
            if d == days_data[-1]:
                continue
            break
            
    result = {
        "username": username,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly_totals,
        "contributions": days_data
    }
    
    return result

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else "Tarushi12-ux"
    data = fetch_contributions(username)
    
    # Determine script path and output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, "contributions.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully saved contribution data for '{username}' to {output_path}")
    print(f"Total Contributions: {data['total_contributions']}")
    print(f"Current Streak: {data['current_streak']} days")
    print(f"Longest Streak: {data['longest_streak']} days")

if __name__ == "__main__":
    main()
