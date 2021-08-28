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


# Minimal necessary data to run our "predict API"
type_local = st.text_input('Maison ou Appartement')
st.write(type_local)
type_local = type_local

code_commune = st.number_input('Code commune ou Code postal')
st.write(f'Vous cherchez le prix au m² sur la {code_commune}')
code_commune = code_commune

df2 = df[df['type'] == str(type_local)]
geodf = df2[['commune', 'transactions']]
data = df[(df['code'] == code_commune)& (df['type'] == type_local)].reset_index(drop=True).to_dict(orient='records')[0]


#Group Paris, Marseille, Lyon by arrondissement
def transform_string(string, separator):
    L = string.split(separator)
    return L[0] if L[0] in ['Paris', 'Marseille', 'Lyon'] else L[0]

geodf.commune = geodf.commune.apply(lambda x: transform_string(x,' '))
geodf = geodf.groupby(geodf.commune).sum().reset_index(drop=False)


# import the folium library
import folium

# initialize the map and store it in a m object
m = folium.Map(location=[data['lat'], data['lon']], zoom_start=11)

# show the map
m
folium.Choropleth(
    geo_data=response,
    name="choropleth",
    data=geodf,
    columns=["commune", "transactions"],
    key_on= "feature.properties.nom",
    fill_color="OrRd",
    fill_opacity=0.8,
    line_opacity=.01,
    legend_name="transaction par commune",
    nan_fill_color='white'
).add_to(m)

folium.Marker(
    location=[data['lat'], data['lon']],
    popup=pd.DataFrame.from_dict(data, orient='index', columns=[data['commune']]),
    icon=folium.Icon(color="red", icon="accessible-icon"),
).add_to(m)

folium.LayerControl().add_to(m)

m

#House price and transactions evolution over years
query2 ="""SELECT dwu.code_commune AS code,
dwu.type_local AS type,  
year(dwu.date_mutation) AS 'Year', 
dwu.nom_commune AS commune,
ROUND(AVG(dwu.valeur_fonciere/dwu.surface_reelle_bati),0) AS Prixm2,
ROUND(AVG(dwu.valeur_fonciere),0) AS Price,
ROUND(AVG(dwu.surface_reelle_bati),0) AS Avg_sqm,
COUNT(dwu.id_mutation) AS transactions,
MAX(dwu.latitude) AS lat,
MAX(dwu.longitude) AS lon
FROM data_working_update dwu
WHERE dwu.type_local IN('Appartement', 'Maison')
GROUP BY code_commune, nom_commune, dwu.type_local, year(dwu.date_mutation)"""

#Get data from Mysql on Gcloud
df3 = get_data(query2, 100000)


#Create 
df_time = df3[['code','Year','commune', 'type','Prixm2','transactions']]
#df_time = df_time[df_time['type']==type_bati]
df_time = df_time[df_time['code']==code_commune]
df_time.commune = df_time.commune.apply(lambda x: transform_string(x,' '))
df_time =df_time.groupby(['commune','Year','type']).agg({
                                             'Prixm2':'mean',
                                             'transactions':'sum'}).reset_index(drop=False)
df_time.drop(columns='transactions')

fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,8))
sns.lineplot(data =df_time, x=df_time.Year.astype('str'), y='Prixm2', hue='type', ax=ax1)
ax1.title.set_text(f"Prixm2: {data['commune']}")
sns.lineplot(data =df_time, x=df_time.Year.astype('str'), y='transactions', hue='type', ax=ax2)
ax2.title.set_text(f"# Transactions: {data['commune']}")
plt.show()



'''
# Reestimator front
'''

st.markdown('''# Prix/m² en fonction du type de logement
## A compléter
''')


surface = st.number_input('Surface en m² du bien à estimer')
st.write(surface)
surface = surface



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
