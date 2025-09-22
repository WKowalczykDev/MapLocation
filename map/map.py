import matplotlib.pyplot as plt
import contextily as cx
import geopandas as gpd
from shapely.geometry import box

# bounding box
minx, maxx = 14.0, 24.2
miny, maxy = 48.9, 55.1
geom = box(minx, miny, maxx, maxy)
gdf = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326").to_crs(epsg=3857)

# wymiar w calach (A2 ≈ 16.5 x 23.4 inch)
fig, ax = plt.subplots(figsize=(23.4, 16.5))  # szer x wys
gdf.boundary.plot(ax=ax, edgecolor='red', linewidth=2)

# wysokie dpi
cx.add_basemap(ax, source=cx.providers.CartoDB.VoyagerNoLabels, zoom=8)  # wyższy zoom
plt.axis('off')
plt.savefig("mapa_A2.png", dpi=300, bbox_inches='tight')
plt.show()