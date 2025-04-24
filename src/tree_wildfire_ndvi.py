"""
NDVI Computation and Visualization for Wildfire Analysis

This script fetches Sentinel-2 imagery from Microsoft Planetary Computer,
computes NDVI over Paradise, CA (affected by the 2018 Camp Fire), and saves
results to raster and preview image outputs

Author: Raneem Samman
Date: 01-04-2025
"""

# Import necessary libraries
import pystac_client
import stackstac
import planetary_computer
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box
import xarray as xr
import rioxarray
import os

# --------------------- CONFIG ---------------------

# Define the area of interest (AOI) for Paradise, CA, this is the (lon, lat) coordinates
AOI = box(-121.6, 39.5, -121.4, 39.6)  # Bounding box coordinates, [min lon, min lat, max lon, max lat]
DATE_RANGE = "2021-07-01/2021-07-30"
NDVI_TIF = "outputs/ndvi_paradise.tif"
NDVI_PNG = "outputs/ndvi_preview.png"

# --------------------- HELPER FUNCTIONS ---------------------

def fetch_sentinel2_data(AOI, date_range):
    """
    Fetch Sentinel-2 data from Microsoft Planetary Computer for the given AOI and date range.
    """
    print("Connecting to Planetary Computer and fetching Sentinel-2 imagery...")
    catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1") # Connect to the Planetary Computer STAC API
    search = catalog.search( 
        collections=["sentinel-2-l2a"], # Collection name
        bbox=AOI, # Bounding box for the search
        datetime=date_range, # Date range for the search 
        query={"eo:cloud_cover": {"lt": 10}} # Cloud cover filter to reduce cloudiness
    )
    items = list(search.get_items()) # Fetch items from the search
    signed_items = [planetary_computer.sign(item) for item in items] # Sign the items for access
    return signed_items

def compute_ndvi_from_stack(items, AOI):
    """
    Compute NDVI from Sentinel-2 imagery stack.
    """
    print("Loading image stack and computing NDVI from Sentinel-2 imagery stack...")
    stack = stackstac.stack(items, assets=["B04", "B08"], resolution=10, bounds_latlon=AOI) # Stack the items
    b4 = stack.sel(band="B04").mean(dim="time") # Select band 4 (Red)
    b8 = stack.sel(band="B08").mean(dim="time") # Select band 8 (NIR)
    ndvi = (b8 - b4) / (b8 + b4) # Compute NDVI
    ndvi.name = "NDVI"
    return ndvi.clip(min=-1.0, max=1.0)

def save_ndvi_to_tif(ndvi, output_path):
    """
    Save NDVI data to a GeoTIFF file.
    """
    print(f"Saving NDVI data to {output_path}...")
    ndvi.rio.to_raster(output_path) # Save the NDVI data to a GeoTIFF file
    print("NDVI data saved successfully.")

# --------------------- MAIN ---------------------
if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    items = fetch_sentinel2_items(AOI, DATE_RANGE)
    ndvi = compute_ndvi_from_stack(items, AOI)
    save_ndvi(ndvi, NDVI_TIF, NDVI_PNG)
    print("NDVI processing complete.")