import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import geopandas as gpd
from prettytable import PrettyTable

#######################################################################################3

def showmap(show_data):
    #function to display map with the given data.. parameters: list with columns "Sr.No", "States/UT","Active","Recovered","Deceased","Total"
    map_data = gpd.read_file(r'C:\Users\Admin\Desktop\Corona Prophecy\Indian_States.shp')
    map_data.plot()
    map_data.rename(columns = {'st_nm':'States/UT'}, inplace = True)

    map_data['States/UT'] = map_data['States/UT'].str.replace('&','and')
    map_data['States/UT'].replace('Arunanchal Pradesh',
                                  'Arunachal Pradesh', inplace = True)
    map_data['States/UT'].replace('Telangana', 
                                  'Telengana', inplace = True)
    map_data['States/UT'].replace('NCT of Delhi', 
                                  'Delhi', inplace = True)
    map_data['States/UT'].replace('Andaman and Nicobar Island', 
                                  'Andaman and Nicobar Islands', 
                                   inplace = True)

    show_data['Active'] = show_data['Active'].map(int)

    merged = pd.merge(map_data, show_data, on='States/UT')
    merged.drop('Sr.No', axis = 1, inplace = True)
    merged.head()

    fig, ax = plt.subplots(1, figsize=(20, 12))
    ax.axis('off')

    ax.set_title('Coronavirus Active cases in India', fontsize=25)
    merged.plot(column = 'Active',cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend = True)

    fig.show()
    #function ends
    #######################################################################################


url = 'https://www.mohfw.gov.in/'
# make a GET request to fetch the raw HTML content
web_content = requests.get(url).content
# parse the html content
soup = BeautifulSoup(web_content, "html.parser")
# remove any newlines and extra spaces from left and right
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
# find all table rows and data cells within
stats = [] 
all_rows = soup.find_all('tr')
for row in all_rows:
    stat = extract_contents(row.find_all('td')) 
    # notice that the data that we require is now a list of length 6
    if len(stat) == 6:
        stats.append(stat)
#now convert the data into a pandas dataframe for further processing
new_cols = ["Sr.No", "States/UT","Active","Recovered","Deceased","Total"]
state_data = pd.DataFrame(data = stats, columns = new_cols)
state_data.head()



showmap(state_data)
