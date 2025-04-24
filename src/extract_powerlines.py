"""
extract_powerlines.py
Description: Extract power lines from OpenStreetMap data for Paradise, CA. The extracted data will be saved in GeoJSON format to the specified directory.

Author: Raneem Samman
Date: 15-04-2025
"""

# Import necessary libraries
import osmnx as ox
import geopandas as gpd
import os

# Define bounding box around Paradise, CA
north, south, east, west = 39.80, 39.75, -121.55, -121.65

# Query for power lines in the area
tags = {"power": "line"}
gdf = ox.geometries_from_bbox(north, south, east, west, tags)

# Save to GeoJSON
os.makedirs("data/raw", exist_ok=True)
gdf.to_file("data/raw/powerlines.geojson", driver="GeoJSON")

print("Powerlines saved to data/raw/powerlines.geojson")
