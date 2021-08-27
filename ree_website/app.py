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

#Web App Libraries
from streamlit_folium import folium_static

engine = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username='Estimators',  # e.g. "my-database-user"
        password='Estimator2021',  # e.g. "my-database-password"
        host='34.77.88.127',  # e.g. "127.0.0.1"
        port=3306,  # e.g. 3306
        database='Housing_France',  # e.g. "my-database-name"
    ))
conn = engine.connect().execution_options(stream_results=True)


def get_data(querystring, chunk):
    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username='Estimators',  #
            password='Estimator2021',  # e.g. "my-database-password"
            host='34.77.88.127',  # e.g. "127.0.0.1"
            port=3306,  # e.g. 3306
            database='Housing_France',  # e.g. "my-database-name"
        ))
    conn = engine.connect().execution_options(stream_results=True)
    frame = pd.DataFrame()
    for chunk_dataframe in pd.read_sql(querystring, conn, chunksize=chunk):
        #print(f"Got dataframe w/{len(chunk_dataframe)} rows")
        frame = frame.append(chunk_dataframe)
        # ... do something with dataframe ...
    return frame


#Create String for data creation
querystring = """SELECT dwu.code_commune AS code,
dwu.type_local AS type,
dwu.nom_commune AS commune,
dwu.code_postal AS Code_post,
ROUND(AVG(dwu.valeur_fonciere/dwu.surface_reelle_bati),0) AS Prixm2,
ROUND(AVG(dwu.valeur_fonciere),0) AS Price,
ROUND(AVG(dwu.surface_reelle_bati),0) AS Avg_sqm,
COUNT(dwu.id_mutation) AS transactions,
MAX(dwu.latitude) AS lat,
MAX(dwu.longitude) AS lon
FROM data_working_update dwu
WHERE dwu.type_local IN('Appartement', 'Maison')
GROUP BY code_commune, Code_post, nom_commune, dwu.type_local;
"""
#Get data from Mysql on Gcloud
df = get_data(querystring, 100000)

url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/communes-version-simplifiee.geojson'
response = requests.get(url).json()

df2 = df[df['type'] == 'Appartement']
geodf = df2[['commune', 'transactions']]


#Group Paris, Marseille, Lyon by arrondissement
def transform_string(string, separator):
    L = string.split(separator)
    return L[0] if L[0] in ['Paris', 'Marseille', 'Lyon'] else L[0]


geodf.commune = geodf.commune.apply(lambda x: transform_string(x, ' '))
geodf = geodf.groupby(geodf.commune).sum().reset_index(drop=False)

# import the folium library
import folium

# initialize the map and store it in a m object
m = folium.Map(location=[46.514783, 6.163627], zoom_start=4)

# show the map
folium.Choropleth(geo_data=response,
                  name="choropleth",
                  data=geodf,
                  columns=["commune", "transactions"],
                  key_on="feature.properties.nom",
                  fill_color="OrRd",
                  fill_opacity=0.8,
                  line_opacity=.01,
                  legend_name="transaction par commune",
                  nan_fill_color='white').add_to(m)

folium.LayerControl().add_to(m)

folium_static(m)
'''
# Reestimator front
'''

st.markdown('''# Prix/m² en fonction du type de logement
## A compléter
''')
# Minimal necessary data to run our "predict API"
type_local = st.text_input('Maison ou Appartement')
st.write(type_local)
type_local = type_local

surface = st.number_input('Surface en m² du bien à estimer')
st.write(surface)
surface = surface

code_commune = st.number_input('Code commune ou Code postal')
st.write(f'Vous cherchez le prix au m² sur la {code_commune}')
code_commune = code_commune

# Create a dictionnary with necessary parameters for predict API
param_dict = {
    "type_local": type_local,
    "surface": int(surface),
    "code_commune": int(code_commune),
}
# -------------------------
# #  request json
# -------------------------
# url = 'predict API url'

# if st.button('click me'):
#     response = requests.get(url, params=param_dict).json()

#     # print is visible in server output, not in the page
#     st.write('Prix au m² est', response['prediction'])

# -------------------------
# #  map code
# -------------------------
