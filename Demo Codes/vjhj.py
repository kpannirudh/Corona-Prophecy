import plotly.express as px
import pandas as pd
import json
import geopandas as gpd
geodf = gpd.read_file(r'C:\Users\Admin\Desktop\Indian_States.shp')
geodf.rename(columns = {'st_nm':'States/UT'}, inplace = True)
geodf['States/UT'] = geodf['States/UT'].str.replace('&','and')
geodf['States/UT'].replace('Arunanchal Pradesh','Arunachal Pradesh', inplace = True)
geodf['States/UT'].replace('Telangana', 'Telengana', inplace = True)
geodf['States/UT'].replace('NCT of Delhi', 'Delhi', inplace = True)
geodf['States/UT'].replace('Andaman and Nicobar Island','Andaman and Nicobar Islands',inplace = True)
geodf.to_file(r'C:\Users\Admin\Desktop\Indian_States.json', driver = "GeoJSON")
with open(r'C:\Users\Admin\Desktop\Indian_States.json') as geofile:
    j_file = json.load(geofile)
# ----------- Step 1 ------------
URL_DATASET = r'C:\Users\Admin\Desktop\Corona Prophecy\CSVFiles\StatewiseTestingDetails.csv'
df1 = pd.read_csv(URL_DATASET)
# print(df1.head) # Uncomment to see what the dataframe is like
# ----------- Step 2 ------------
"""list_countries = df1['Country'].unique().tolist()
# print(list_countries) # Uncomment to see list of countries
d_country_code = {}  # To hold the country names and their ISO
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        # country_data is a list of objects of class pycountry.db.Country
        # The first item  ie at index 0 of list is best fit
        # object of class Country have an alpha_3 attribute
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        # If could not find country, make ISO code ' '
        d_country_code.update({country: ' '})

# print(d_country_code) # Uncomment to check dictionary  

# create a new column iso_alpha in the df
# and fill it with appropriate iso 3 code
for k, v in d_country_code.items():
    df1.loc[(df1.Country == k), 'iso_alpha'] = v
"""
# print(df1.head)  # Uncomment to confirm that ISO codes added
# ----------- Step 3 ------------

fig = px.choropleth(data_frame = df1,
                    geojson=j_file,
                    locations= "States/UT",
                    color= "TotalSamples",  # value in column 'Confirmed' determines color
                    hover_name= "States/UT",
                    color_continuous_scale= 'RdYlGn',  #  color scale red, yellow green
                    animation_frame= "Date")

fig.show()
