#!/usr/bin/env python3
"""Generate interactive Folium maps for active roadbooks."""

import re
import os
import folium

BASE = "/opt/data/voyages-wiki/docs"
VOYAGES = [
    "italie",
]

def extract_coords(filepath):
    """Extract GPS coordinates from the Traces GPS section of a markdown file."""
    with open(filepath, 'r') as f:
        content = f.read()

    gps_section = re.search(r'Traces GPS complètes.*?(\|\s*#.*?\|.*?)(.*?)(?:\n\n|\n---|</details>)', content, re.DOTALL)
    if not gps_section:
        gps_section = re.search(r'Traces GPS.*?(\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?)(.*?)(?:\n\n|\n---)', content, re.DOTALL)
    if not gps_section:
        print(f"  No GPS trace section found in {filepath}")
        return []

    table_text = gps_section.group(0)
    coords = []

    pattern = r'\|\s*\d+\s*\|\s*[^|]*\|\s*\[([0-9.-]+),\s*([0-9.-]+)\]'
    matches = re.findall(pattern, table_text)
    for lat, lng in matches:
        coords.append((float(lat), float(lng)))

    print(f"  Extracted {len(coords)} GPS points")
    return coords

def generate_map(voyage_name, coords):
    """Generate a Folium interactive map from GPS coordinates."""
    if not coords:
        print(f"  Skipping {voyage_name} — no coordinates")
        return

    mid_lat = sum(c[0] for c in coords) / len(coords)
    mid_lng = sum(c[1] for c in coords) / len(coords)

    m = folium.Map(location=[mid_lat, mid_lng], zoom_start=8,
                   tiles="OpenStreetMap", control_scale=True)

    folium.PolyLine(coords, color="blue", weight=3, opacity=0.7).add_to(m)

    folium.Marker(
        coords[0],
        popup="Départ",
        icon=folium.Icon(color="green", icon="play", prefix="fa"),
    ).add_to(m)

    folium.Marker(
        coords[-1],
        popup="Arrivée",
        icon=folium.Icon(color="red", icon="flag-checkered", prefix="fa"),
    ).add_to(m)

    out_path = os.path.join(BASE, voyage_name, "map.html")
    m.save(out_path)
    print(f"  → Saved {out_path}")

def main():
    for voyage in VOYAGES:
        filepath = os.path.join(BASE, voyage, "index.md")
        print(f"\n📌 {voyage}")
        if not os.path.exists(filepath):
            print(f"  File not found: {filepath}")
            continue
        coords = extract_coords(filepath)
        generate_map(voyage, coords)

if __name__ == "__main__":
    main()
