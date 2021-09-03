import streamlit as st
import sqlalchemy
import pymysql
import requests
import folium
#Importing our Packages: Analytics
import pandas as pd
import numpy as np

#Viz libaries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd # library for data analysis
from geopy.geocoders import Nominatim 

# convert an address into latitude and longitude values
import requests # library to handle requests
import folium # map rendering library
import streamlit as st #creating an app
#from streamlit_folium import folium_static 

#Web App Libraries
from streamlit_folium import folium_static

#Group Paris, Marseille, Lyon by arrondissement
def transform_string(string, separator):
    L = string.split(separator)
    return L[0] if L[0] in ['Paris', 'Marseille', 'Lyon'] else L[0]

#Get data from Mysql on Gcloud
df2 = pd.read_csv('final_data.csv', dtype={'Code département':'object'})
url = 'https://raw.githubusercontent.com/gmanchon/streamlit/master/data/departements.json'
response = requests.get(url).json()
df_gv = df2[df2['Code département'].isin(['13','75','69'])]
df2.Nom de commune = df2.Nom de commune.apply(lambda x: transform_string(x, ' '))

#Progress Bar
latest_iteration = st.empty()
bar = st.progress(0)
import time
for i in range(100):
    #Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.01)

#Filters
type_bati = st.sidebar.selectbox(
    'Type de batiment',
    ('Maison', 'Appartement')
)

#Slider
df2.Année = df2.Année.astype('int')
values = st.slider(
    'Select a range of values',
     2016, 2020, (2016, 2020))
st.write('Values:', values)

param = st.sidebar.selectbox(
    'Metrics',
    ('Prix moyen m2', 'Transactions', 'Surface moyenne', 'Nbre pièces principales', 'Valeur totale', 'Surface du terrain'))

# Add a selectbox to the sidebar:
selectbox_city = st.sidebar.selectbox(
    'Ville',
    ('Paris', 'Marseille', 'Lyon'))

if st.checkbox('Sans Metropoles Majeures ?'):
    df2= df2[~df2['Nom de commune'].isin(['Paris','Marseille','Lyon'])]

#Filter Final Dataframe
df2= df2[df2['Type du local']== type_bati]
df2= df2[df2['Année'].between(values[0],values[1])]

# Create Final Sum Checkbox
if st.checkbox('Somme?'):
    df2 = df2.groupby(['Code département','Type du local'])[f"{param}"].sum().reset_index(drop=False)

df2 = df2.groupby(['Code département','Type du local'])[f"{param}"].mean().reset_index(drop=False)

#Filter Departements in the Final DF 
df2.Code département = df2.Code département.astype('str')
geodf = df2[['Code département',f'{param}']]

#Center the Map around the Point of Interest
def center(ville):
   address = f'{ville}, FR'
   geolocator = Nominatim(user_agent="id_explorer")
   location = geolocator.geocode(address)
   latitude = location.latitude
   longitude = location.longitude
   return latitude, longitude

# initialize the first map and store it in a m object
m = folium.Map(location=center('Paris'), zoom_start=5)


def threshold(data, param):
        threshold_scale = np.linspace(geodf[param].min(),
                                      geodf[param].max(),
                                      15, dtype=int)
        # change the numpy array to a list
        threshold_scale = threshold_scale.tolist() 
        threshold_scale[-1] = threshold_scale[-1]
        return threshold_scale


def show_maps(data, threshold_scale):
            folium.Choropleth(geo_data=response,
                  name="choropleth",
                  data=geodf,
                  columns=["Code département", f"{param}"],
                  key_on="feature.properties.Code commune",
                  fill_color="YlOrRd",
                  fill_opacity=0.8,
                  line_opacity=.2,
                  legend_name=f"{param} par commune par departement ",
                  nan_fill_color='white').add_to(m)

    
            folium_static(m)


show_maps(geodf, threshold(geodf, param))

folium.LayerControl().add_to(m)
'''
# Distribution des parametres clefs sur les villes principales de France
'''

# Format second map dataframe
df_gv= df_gv[df_gv['Type du local']== type_bati]
df_gv= df_gv[df_gv['Année'].between(values[0],values[1])]
df_gv = df_gv.groupby(['Code commune','Type du local'])[f"{param}"].mean().reset_index(drop=False)
df_gv.Code commune = df_gv.Code commune.astype('str')
geodf2 = df_gv[['Code commune',f'{param}']]

import requests
url2 = 'https://raw.githubusercontent.com/Jehadel/reestimator/JulienVis/notebooks/Julien/arrondissements-millesimes0.geojson'
response2 =  requests.get(url2).json()


#Display the second map
m2 = folium.Map(location=center(f'{selectbox_city}'), zoom_start=11)
def show_maps2(data, threshold_scale):
            folium.Choropleth(geo_data=response2,
                  name="choropleth",
                  data=geodf2,
                  columns=["Code commune", f"{param}"],
                  key_on="feature.properties.code_insee",
                  fill_color="YlOrRd",
                  fill_opacity=0.8,
                  line_opacity=.3,
                  legend_name=f"{param} par commune par departement ",
                  nan_fill_color='white').add_to(m2)
    
            folium_static(m2)

#                threshold_scale=[-10, 60, 70, 80, 90, 100]
show_maps2(geodf2, threshold(geodf2, param))
folium.LayerControl().add_to(m2)


st.markdown('''# Distribution des biens Fonciers à Marseille''')

# Show Marseille Images
from PIL import Image
image = Image.open('boxplot_appartements_Marseille.png')
st.image(image)


image2 = Image.open('boxplot_maisons_Marseille.png')
st.image(image2)

'''
# PREDICTION
'''
st.markdown('''## Prix/m² en fonction du type de logement
''')
# Minimal necessary data to run our "predict API"

surface = st.slider('Surface en m² du bien à estimer?', 0, 130, 25)
pieces = st.slider('Nombre de pièces principales', 0, 1, 8)
value = list(range(1, 17))
Arrondissement = st.selectbox("Arrondissement",
                     value)
st.button('Prix') 
param_dict = {
    "type_local": type_bati,
    "surface": int(surface),
    "pieces/Nbre pièces principales": pieces,
    "Arrondissement/Code commune": int(Arrondissement),
}
st.markdown("""# This is a header
## This is a sub header
This is text""")
# -------------------------
# #  request json
# -------------------------
# url = 'predict API url'
#if st.button('Prix'):
#     response = requests.get(url, params=param_dict).json()
#     # print is visible in server output, not in the page
#     st.write('Prix au m² est', response['prediction'])
#    col1, col2 = st.columns(2)
#    col1.metric("Prix", response['prediction'], "1.2 °F")
#    col2.metric("Score", response['score'], "-8%")