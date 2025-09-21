from scrapper.cities_scrapper import get_all_polish_cities

cities = get_all_polish_cities()
for city in cities:
    print(city)
