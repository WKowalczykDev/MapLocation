import re
from time import sleep
from geopy.geocoders import Nominatim

# inicjalizacja geolokatora
geolocator = Nominatim(user_agent="geo_scraper")

def get_coordinates(city):
    try:
        location = geolocator.geocode(f"{city}, Polska")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Błąd podczas geokodowania miasta {city}: {e}")
        return None, None

def get_all_polish_cities():
    with open("dataToScrap.js", encoding="utf-8") as f:
        js_text = f.read()

    city_matches = re.findall(r"<a href='[^']+'>([^<]+)</a>", js_text)

    cities = []
    i = 0
    while i < len(city_matches):
        cities.append(city_matches[i])
        i += 3  # co 3 pojawia się powiat i województwo

    print(f"Znaleziono {len(cities)} miast")
    return cities

# Pobieranie współrzędnych dla każdego miasta
cities_data = []
cities = get_all_polish_cities()
for city in cities:
    print(f"Pobieram dane dla: {city}")
    lat, lon = get_coordinates(city)
    if lat and lon:
        cities_data.append({
            "miasto": city,
            "lat": lat,
            "lon": lon
        })
    sleep(1)  # uniknięcie limitów Nominatim

print(cities_data)
import json

# zapis do pliku JSON
with open("../cities_data.json", "w", encoding="utf-8") as f:
    json.dump(cities_data, f, ensure_ascii=False, indent=4)

print("Dane zapisane do cities_data.json")

