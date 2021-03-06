from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import joblib
import pandas as pd
import numpy as np

app = FastAPI()

"""
CORS or "Cross-Origin Resource Sharing" refers to the situations
when a frontend running in a browser has JavaScript code
that communicates with a backend, and the backend is in a different "origin"
than the frontend.
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define a root '/' endpoint
@app.get("/")
def index():
    return {"greeting": "Hello world"}


# # Define a root '/' endpoint
# @app.get("/testpredict")
# def testpredict(surface, pieces, arrondissement, type_local):


#     # dependency = 0
#     # surface_terrain = 0
#     # arrondissements = np.zeros(16, 'int')
#     # index = (arrondissement + 7) % 16 - 1
#     # arrondissements[index] = 1  #vector of appartement presence concatenated
#     # if type_local=='Maison':
#     #     local=np.array([0,1])
# #     # else:
# #     #     local=np.array([1,0])

# #     # data_to_predict = np.concatenate(
# #     #     (np.array([surface]), np.array([pieces]), np.array([surface_terrain]),
# #     #      np.array([dependency]), arrondissements, local))
# #     # X_pred = pd.DataFrame(data_to_predict).T


# #     return print("arrondissement")


# @app.get("/predict")
# => Step to do when we have our predict function
# def predict(surface, pieces, arrondissement,
#             type_local):  # add parameters to execute the function

#     dependency = 0
#     surface_terrain = 0
#     arrondissements = np.zeros(16, 'int')
#     index = (arrondissement + 7) % 16 - 1
#     arrondissements[index] = 1  #vector of appartement presence concatenated

#     if type_local == 'Maison':
#         local = np.array([0, 1])
#     else:
#         local = np.array([1, 0])

#         #vector of appartement presence concatenated
#     """Enter the parameters used to execute the predict API,
#     to return the price per squared meter"""

#     data_to_predict = np.concatenate(
#         (np.array([surface]), np.array([pieces]), np.array([surface_terrain]),
#          np.array([dependency]), arrondissements, local))
#     # X_pred = pd.DataFrame(data_to_predict).T

#     # model_pred = joblib.load("../RandomForest.joblib")
#     # # test_scal = joblib.load('../robustscaler.joblib')
#     # # X_scaled = test_scal.transform(X_pred)
#     # reestimodel = model_pred.predict(X_pred)
#     X_pred = pd.DataFrame(data_to_predict)
#     model_pred = joblib.load("../RandomForest.joblib")
#     reestimodel= model_pred.predict(X_pred)

#     return dict(reestimodel=reestimodel[0])


# @app.get("/predict")
def predict(surface, pieces, arrondissement,
            type_local):  # add parameters to execute the function
    """Enter the parameters used to execute the predict API,
    to return the price per squared meter"""

    dependancy = 0
    surface_terrain = 0
    arrondissements = np.zeros(16, 'int')
    index = (arrondissement + 7) % 16 - 1
    arrondissements[index] = 1  #vector of appartement presence concatenated

    if type_local == 'Maison':
        local = np.array([0, 1])
    else:
        local = np.array([1, 0])

    data_to_predict = np.concatenate(
        (np.array([surface]), np.array([pieces]), np.array([surface_terrain]),
         np.array([dependancy]), arrondissements, local))
    X_pred = pd.DataFrame(data_to_predict).T
    # param_dict = {
    #     "surface_reelle_bati": [int(surface)],
    #     "nombre_pieces_principales": [int(pieces)],
    #     "surface_terrain": [int(surface_terrain)],
    #     "Dependency": [int(dependancy)],
    #     "Marseille 10e Arrondissement": [int(Arrondissement10)],
    #     "Marseille 11e Arrondissement": [int(Arrondissement11)],
    #     "Marseille 12e Arrondissement": [int(Arrondissement12)],
    #     "Marseille 13e Arrondissement": [int(Arrondissement13)],
    #     "Marseille 14e Arrondissement": [int(Arrondissement14)],
    #     "Marseille 15e Arrondissement": [int(Arrondissement15)],
    #     "Marseille 16e Arrondissement": [int(Arrondissement16)],
    #     "Marseille 1er Arrondissement": [int(Arrondissement1)],
    #     "Marseille 2e Arrondissement": [int(Arrondissement2)],
    #     "Marseille 3e Arrondissement": [int(Arrondissement3)],
    #     "Marseille 4e Arrondissement": [int(Arrondissement4)],
    #     "Marseille 5e Arrondissement": [int(Arrondissement5)],
    #     "Marseille 6e Arrondissement": [int(Arrondissement6)],
    #     "Marseille 7e Arrondissement": [int(Arrondissement7)],
    #     "Marseille 8e Arrondissement": [int(Arrondissement8)],
    #     "Marseille 9e Arrondissement": [int(Arrondissement9)],
    #     "Appartement": [int(is_house)],
    #     "Maison": [int(is_appart)]
    # }
    # X_pred = pd.DataFrame(param_dict)

    print(X_pred)
    model = joblib.load('XGBoost.joblib')
    test_scal = joblib.load('robustscaler.joblib')
    X_scaled = test_scal.transform(X_pred)
    y_pred = model.predict(X_scaled)
    # model_pred = joblib.load("../RandomForest.joblib")
    # y_pred = dict(reestimodel=reestimodel[0])
    # reesscore = model_pred.score(X_pred, y_pred)

    # return dict(y_pred[0])
    return {"prediction":y_pred[0]}

if __name__ == "__main__":
    from xgboost.sklearn import XGBRegressor
    # uvicorn.run("fast:app", host="0.0.0.0", port=2809)
    # y_pred = predict(50, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                  0, 0, 1)
    y_pred = predict(50, 2, 3,'Maison')
    print(y_pred)
