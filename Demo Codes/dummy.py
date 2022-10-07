import folium
from selenium import webdriver
import pandas as pd
import numpy as np
district_wise_census = pd.read_csv(r"C:\Users\Admin\Desktop\Corona Prophecy\CSVFiles\district wise population and centroids.csv")
district_wise_census.head()
state_wise_centroid = pd.read_csv(r"C:\Users\Admin\Desktop\Corona Prophecy\CSVFiles\state wise centroids_2011.csv")
state_wise_census = district_wise_census.groupby(by="State").sum()[["Population in 2001","Population in 2011"]].reset_index()
state_wise_census = state_wise_centroid.merge(state_wise_census, left_on="State", right_on="State")
state_wise_census.head()
surat_city_long = district_wise_census[district_wise_census["District"] == "Surat"].Longitude.values[0]
surat_city_lat = district_wise_census[district_wise_census["District"] == "Surat"].Latitude.values[0]
center_lat = state_wise_census.mean().Latitude
center_long = state_wise_census.mean().Longitude

m = folium.Map(location=[center_lat, center_long], tiles="Stamen Terrain")
folium.FitBounds([(center_lat-10,center_long-8), (center_lat+10,center_long+8)]).add_to(m)
for state in state_wise_census["State"].unique():
    state_census = state_wise_census[state_wise_census["State"]==state]
    folium.CircleMarker(
        location=[state_census.Latitude.values[0], state_census.Longitude.values[0]],
        radius = float(state_census["Population in 2011"].values[0]/8e6),
        popup="Population 2011 : %s"%state_census["Population in 2011"].values[0],
        tooltip = state_census.State.values[0],
        color="black",
        fill_color="black"
    ).add_to(m)
m.save(r"C:\Users\Admin\Desktop\map.html")

#Open a browser window...
browser = webdriver.Firefox()
#..that displays the map...
browser.get(r"C:\Users\Admin\Desktop\map.html")
#Give the map tiles some time to load
time.sleep(5)
#Grab the screenshot
browser.save_screenshot(r"C:\Users\Admin\Desktop\map.png")
#Close the browser
browser.quit()
