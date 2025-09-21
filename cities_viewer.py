import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import Point
from matplotlib.patches import Rectangle

# --- DANE: wygodniej jako lista słowników z nazwą i lat/lon ---
miasta = [
    {"miasto": "Warszawa",        "lat": 52.2297, "lon": 21.0122},
    {"miasto": "Kraków",          "lat": 50.0647, "lon": 19.9450},
    {"miasto": "Gdańsk",          "lat": 54.3520, "lon": 18.6466},
    {"miasto": "Szczecin",        "lat": 53.4285, "lon": 14.5528},
    {"miasto": "Ustrzyki Dolne",  "lat": 49.4300, "lon": 22.5900},
]


# --- GeoDataFrame w WGS84 (EPSG:4326) ---
gdf = gpd.GeoDataFrame(
    miasta,
    geometry=gpd.points_from_xy([m["lon"] for m in miasta],
                                [m["lat"] for m in miasta]),
    crs="EPSG:4326"
)

# --- Rzutowanie do Web Mercator (metry) ---
gdf = gdf.to_crs(epsg=3857)

# --- USTAWIENIA WYJŚCIA A3 ---
# A3: 297 x 420 mm → w calach (1 cal = 25.4 mm)
A3_PORTRAIT = (11.69, 16.54)   # (szerokość, wysokość) w calach
A3_LANDSCAPE = (16.54, 11.69)

DPI = 300  # rozdzielczość druku
fig, ax = plt.subplots(figsize=A3_LANDSCAPE, dpi=DPI)

# --- RYSOWANIE PUNKTÓW (opcjonalnie) ---
# markersize jest w punktach^2 (większa liczba = większa kropka)
gdf.plot(ax=ax, color="red", markersize=60, zorder=6)

# --- PROSTOKĄTY-PLACEHOLDERY WOKÓŁ PUNKTÓW ---
# EPSG:3857 → jednostki ~metry. Tu np. 40 km x 30 km wokół miasta.
half_width_m  = 20000   # połowa szerokości  (20 km)
half_height_m = 15000   # połowa wysokości   (15 km)

for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf["miasto"]):
    # lewy-dolny róg + wymiary
    rect = Rectangle(
        (x - half_width_m, y - half_height_m),
        2 * half_width_m,
        2 * half_height_m,
        linewidth=2,
        edgecolor="red",
        facecolor="none",
        zorder=7
    )
    ax.add_patch(rect)
    # podpis nad prostokątem
    ax.text(x, y + half_height_m + 5000, label, ha="center", va="bottom",
            fontsize=12, color="red", zorder=8)

# --- TŁO Z INTERNETU ---
# Podajemy crs, a zoom dobieramy do skali (większy = więcej detalu).
# Dla mapy PL typowo 6–8; dla miasta 12–15. Spróbuj 7.
import contextily as ctx

from pyproj import Transformer

# transformacja z lat/lon (EPSG:4326) -> Web Mercator (EPSG:3857)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

# granice PL w stopniach (mniej więcej)
lon_min, lon_max = 13.0, 24.2
lat_min, lat_max = 48.9, 55.1

minx, miny = transformer.transform(lon_min, lat_min)
maxx, maxy = transformer.transform(lon_max, lat_max)

# # pobranie kafelków dla granic Polski
# img, ext = ctx.bounds2img(minx, miny, maxx, maxy,
#                           zoom=7,
#                           source=ctx.providers.OpenStreetMap.Mapnik)
#
# ax.imshow(img, extent=ext, interpolation='bilinear')
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)
#
#
# Estetyka
ax.set_axis_off()

# --- ZAPIS A3 ---
# PNG do druku
plt.savefig("mapa_A3_300dpi.png", dpi=DPI, bbox_inches="tight")
# PDF (wektorowy kontur + rastrowe kafelki; dobry do druku)
plt.savefig("mapa_A3_300dpi.pdf", bbox_inches="tight")
plt.close(fig)
