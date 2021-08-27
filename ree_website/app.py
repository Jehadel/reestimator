import streamlit as st
import requests

'''
# Reestimator front
'''

st.markdown('''# Prix/m² en focntion du type de logement
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
# @st.cache
# def get_map_data():
#     print('get_map_data called')
#     return pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#                         columns=['lat', 'lon'])

# if st.checkbox('Show map', False):
#     df = get_map_data()

#     st.map(df)
# else:
#     from PIL import Image
#     image = Image.open('images/map.png')
#     st.image(image, caption='map', use_column_width=False)

# data = pd.DataFrame({
#     'awesome cities': ['Chicago', 'Minneapolis', 'Louisville', 'Topeka'],
#     'lat': [41.868171, 44.979840, 38.257972, 39.030575],
#     'lon': [-87.667458, -93.272474, -85.765187, -95.702548]
# })

# # Adding code so we can have map default to the center of the data
# midpoint = (np.average(data['lat']), np.average(data['lon']))

# st.deck_gl_chart(viewport={
#     'latitude': midpoint[0],
#     'longitude': midpoint[1],
#     'zoom': 4
# },
#                  layers=[{
#                      'type': 'ScatterplotLayer',
#                      'data': data,
#                      'radiusScale': 250,
#                      'radiusMinPixels': 5,
#                      'getFillColor': [248, 24, 148],
#                  }])
