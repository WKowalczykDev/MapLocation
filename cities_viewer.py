import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import transforms, image as mpimg
from matplotlib.patches import Rectangle
import json
from functions.map_scale import map_scale
from functions.mm_to_inch import mm_to_inch
from functions.scale_mm_to_DPI import scale_mm_to_DPI

from constants import A2_width, A2_height

with open("cities_data.json", "r", encoding="utf-8") as f:
    miasta = json.load(f)

miasta = miasta[:20]


# --- GeoDataFrame w WGS84 (EPSG:4326) ---
gdf = gpd.GeoDataFrame(
    miasta,
    geometry=gpd.points_from_xy([m["lon"] for m in miasta],
                                [m["lat"] for m in miasta]),
    crs="EPSG:4326"
)

minx, maxx = 14.0, 24.2
miny, maxy = 48.9, 55.1

max_min_gdf = gpd.GeoDataFrame(
    geometry=gpd.points_from_xy([minx, maxx],[miny, maxy])
    ,crs="EPSG:4326"
)


# --- Rzutowanie do Web Mercator (metry) ---
gdf = gdf.to_crs(epsg=3857)
max_min_gdf = max_min_gdf.to_crs(epsg=3857)

from shapely.geometry import Point

dx = max_min_gdf.geometry.x[0]
dy = max_min_gdf.geometry.y[0]

# zmiana na rzutowanie względne - względem określonego w max_min_gdf w metrach
end_gdf_m = gpd.GeoDataFrame(
    miasta,
    geometry=[Point(x - dx, y - dy) for x, y in zip(gdf.geometry.x, gdf.geometry.y)],
    crs="EPSG:3857"
)


# szerokość i wysokość w metrach
end_width = max_min_gdf.geometry.x[1] - max_min_gdf.geometry.x[0]
end_height = max_min_gdf.geometry.y[1] - max_min_gdf.geometry.y[0]

# rozmiar A3
A2_PORTRAIT = (mm_to_inch(A2_width), mm_to_inch(A2_height))   # (szerokość, wysokość) w calach
A2_LANDSCAPE = (mm_to_inch(A2_height), mm_to_inch(A2_width))

# tworzenie skali z metrów na mm
scale_mm = map_scale(end_width, A2_width)
end_gdf_mm = gpd.GeoDataFrame(
    miasta,
    geometry=[Point(p.x*1000 / scale_mm, p.y*1000 / scale_mm) for p in end_gdf_m.geometry],
    crs=end_gdf_m.crs
)

DPI = 300  # rozdzielczość druku
fig, ax = plt.subplots(figsize=A2_PORTRAIT, dpi=DPI)

mm_w, mm_h = 30,40  # szerokość i wysokość w mm
width_dots = scale_mm_to_DPI(mm_w,DPI)
height_dots = scale_mm_to_DPI(mm_h,DPI)
print(width_dots, height_dots)


tlo_img = mpimg.imread("./map/wyciety_obraz.png")  # podaj ścieżkę do obrazu

wysokosc, szerokosc = tlo_img.shape[:2]  # [:2] bo może być kanał koloru

print("Szerokość:", szerokosc)
print("Wysokość:", wysokosc)
ratio = wysokosc/szerokosc

ax.imshow(
    tlo_img,
    extent=[0, A2_width, 0, A2_width*ratio],  # rozciągnięcie obrazu na całą powierzchnię figury w mm
    aspect='auto',
    zorder=0  # najniższy z-order, tło
)

#tutaj stworze funkcje ktora bedzie szukala miejsce na wszystkie pasujace

# zmiana rozmieszczenia punktów, tak żeby znajdowały się na mapie w milimetrach
for x, y, label in zip(end_gdf_mm.geometry.x, end_gdf_mm.geometry.y, gdf["miasto"]):
    ax.scatter(x, y, color="blue", s=10, zorder=10)
    rect = Rectangle(
        (x-mm_w/2, y-mm_h/2),
        mm_w,      # szerokość w mm
        mm_h,      # wysokość w mm
        linewidth=1,
        edgecolor="red",
        facecolor="none",
        zorder=7
    )
    ax.add_patch(rect)
    ax.text(x, y + 5, label,
            ha="center", va="bottom", fontsize=8, color="red")

ax.set_xlim(0, A2_width)
ax.set_ylim(0, A2_height)
ax.axis('off')


# zapis do pliku PNG
fig.savefig("./results/map_A2.png", dpi=DPI, bbox_inches="tight")

# zapis do pliku PDF
fig.savefig("./results/map_A2.pdf", bbox_inches="tight")
plt.show()
