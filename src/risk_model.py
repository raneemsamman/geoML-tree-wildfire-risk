""" 
risk_model.py
Description: Train a basic binary classifier to predict wildfire risk based on NDVI and distance to powerlines 

Author: Raneem Samman
Date: 20-04-2025
"""

# import necessary libraries
import pandas as pd
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
from shapely.geometry import Point
from scipy.ndimage import distance_transform_edt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# ------------------ Load NDVI Raster ------------------
ndvi_path = "outputs/ndvi_paradise.tif"
with rasterio.open(ndvi_path) as src:
    ndvi_data = src.read(1)
    ndvi_transform = src.transform
    ndvi_crs = src.crs
    ndvi_shape = src.shape

# ------------------ Load Powerlines ------------------
powerline_path = "data/raw/powerlines.geojson"
powerlines = gpd.read_file(powerline_path).to_crs(ndvi_crs) 

# ------------------ Create Distance Raster ------------------
# Rasterize powerlines into a mask that matches the NDVI raster to compute distance 
powerline_mask = geometry_mask(
    [geom for geom in powerlines.geometry],
    out_shape=ndvi_shape,
    transform=ndvi_transform,
    invert=True
)

# Compute distance transform: distance to nearest powerline (in pixels)
distance_pixels = distance_transform_edt(~powerline_mask) 
distance_meters = distance_pixels * abs(ndvi_transform[0])  # convert pixels to meters so we can use the transform value

# ------------------ Sample NDVI + Distance Features ------------------
sample_idx = np.random.choice(np.arange(ndvi_data.size), size=1000, replace=False) # randomly sample 1000 pixels
rows, cols = np.unravel_index(sample_idx, ndvi_data.shape) # convert to row/col indices 

ndvi_values = ndvi_data[rows, cols] # get NDVI values at sampled indices
distance_values = distance_meters[rows, cols] # get distance values at sampled indices

# Create DataFrame
features = pd.DataFrame({
    "ndvi": ndvi_values,
    "distance_to_powerline": distance_values
})

# Clean data (remove nodata or NaN)
features = features.replace([-9999, np.nan], np.nan).dropna()

# Simulate risk label: risky if low NDVI & close to powerline (It assumes NDVI < 0.3 = unhealthy/stressed vegetation. It then labels those areas as "risky" if they're also close to powerlines)
features["risk"] = ((features["ndvi"] < 0.3) & (features["distance_to_powerline"] < 100)).astype(int) # 1 = risky, 0 = not risky

# ------------------ Train Model ------------------
X = features[["ndvi", "distance_to_powerline"]] # features
y = features["risk"] # target variable/label

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# ------------------ Evaluation ------------------
y_pred = clf.predict(X_test)
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ------------------ Visualization ------------------
plt.figure(figsize=(6, 4))
sns.scatterplot(data=features, x="ndvi", y="distance_to_powerline", hue="risk", palette="coolwarm")
plt.title("NDVI vs. Distance to Powerline\nLabeled Risk Zones")
plt.xlabel("NDVI")
plt.ylabel("Distance to Powerline (m)")
plt.tight_layout()
plt.savefig("outputs/risk_visualization.png")
plt.show()

# ----------------- SAVE MODEL ------------------
os.makedirs("models", exist_ok=True)
joblib.dump(clf, "models/risk_classifier.pkl")
print("Model saved to models/risk_classifier.pkl")
