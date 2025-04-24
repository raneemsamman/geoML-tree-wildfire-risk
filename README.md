# geoML-tree-wildfire-risk

![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Stars](https://img.shields.io/github/stars/raneemsamman/geoML-tree-wildfire-risk?style=social)
![Last Commit](https://img.shields.io/github/last-commit/raneemsamman/geoML-tree-wildfire-risk)
![License](https://img.shields.io/github/license/raneemsamman/geoML-tree-wildfire-risk)

NDVI-based wildfire risk analysis using Sentinel-2 imagery, OSM powerlines, and geospatial ML 

A lightweight geospatial machine learning project inspired by Overstory's mission: analyzing tree health and proximity to infrastructure to help mitigate wildfire risk. This pipeline uses OSM powerlines, and geospatial ML, and Sentinel-2 imagery to compute NDVI (Normalized Difference Vegetation Index) over Paradise, California — a region critically impacted by the 2018 Camp Fire.

---

## Project Goals
- Use real satellite data to compute and map tree health (via NDVI)
- Identify zones of high vegetation density near infrastructure
- Visualize overlaps with wildfire perimeters to assess risk

---

## Tech Stack

| Component        | Tools / Libraries                                    |
|------------------|-------------------------------------------------------|
| Geospatial       | `geopandas`, `shapely`, `rasterio`, `rioxarray`, `fiona` |
| Satellite Data   | `pystac-client`, `stackstac`, `planetary_computer`    |
| ML Ready         | `xarray`, `scikit-learn`, `matplotlib`, `folium`      |
| Deep Learning    | `pytorch`, `tensorflow` *(coming soon)*               |
| Infrastructure   | `osmnx` (for OpenStreetMap powerline data)           |

---


## How to Run This Project

### 1. Clone the Repo

### 2. Set Up Environment

### 3. Run the Scripts

## Data Sources
- [Microsoft Planetary Computer](https://planetarycomputer.microsoft.com/)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [USGS GeoMAC Fire Perimeters](https://data-nifc.opendata.arcgis.com/)

---

## Future Additions
- Overlay powerlines (from OpenStreetMap)
- Add a more advanced risk classification model

---

## Maintained by
**Raneem Samman**  
LinkedIn: [linkedin.com/in/raneemsamman](https://www.linkedin.com/in/raneemsamman)

---

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

