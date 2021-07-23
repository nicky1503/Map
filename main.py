import folium
import pandas

# Determine the colours of the countries depending on their population
def country_color(population):
    if population < 50000000:
        return "green"
    elif 50000000 <= population < 100000000:
        return "#f3ff08"
    elif 100000000 <= population < 1000000000:
        return "orange"
    else:
        return "darkred"


map_1 = folium.Map([43.796639, 24.987949], zoom_start=4, tiles="CartoDB Positron")

# Loading values into lists from the capital_cities.csv file
data = pandas.read_csv("capital_cities.csv")
longitude = list(data["lng"])
latitude = list(data["lat"])
population = list(data["population"])
city_name = list(data["city"])

# Create feature group layer for the markers of the capital cities
fg_capitals = folium.FeatureGroup(name="Capitals")
# Adding Markers to the feature group layer
for lat, lon, pop, name in zip(latitude, longitude, population, city_name):
    fg_capitals.add_child(folium.CircleMarker(radius=8, location=(lat, lon),
                                              popup=f"{name} Population: {pop}",
                                              color="#3b3b3b",
                                              fill=True,
                                              fill_color="orange",
                                              fill_opacity=0.6))
# Creating feature group layer for coloring countries by there population
fg_color_by_population = folium.FeatureGroup(name="Countries coloured by population")
fg_color_by_population.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
                                                style_function=lambda x: {'fillColor': country_color(x["properties"]["POP2005"]),
                                                         "color": "black", "weight": 2,}))
# Adding the feature group layers to the map
map_1.add_child(fg_color_by_population)
map_1.add_child(fg_capitals)
map_1.add_child(folium.LayerControl())

map_1.save("map_1.html")