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
    return {"greeting": "Hel world"}

@app.get("/predict") # => Step to do when we have our predict function
def predict(surface, pieces, arrondissement, type_local):  # add parameters to execute the function

    dependency=0
    surface_terrain=0
    arrondissements = np.zeros(16,'int')
    index = (arrondissement + 7) % 16 - 1
    arrondissements[index] = 1 #vector of appartement presence concatenated

    if type_local=='Maison':
        local=np.array([0,1])
    else:
        local=np.array([1,0])



        #vector of appartement presence concatenated
    """Enter the parameters used to execute the predict API,
    to return the price per squared meter"""

    data_to_predict = np.concatenate((np.array([surface]), np.array([pieces]), np.array([surface_terrain]), np.array([dependency]), arrondissements, local))
    X_pred=pd.DataFrame(data_to_predict).T

    model_pred = joblib.load("model.joblib")
    test_scal = joblib.load('robustscaler.joblib')
    X_scaled = test_scal.transform(X_pred)
    reestimodel= model_pred.predict(X_scaled)


    return dict(reestimodel=reestimodel[0])


if __name__ == "__main__":
    uvicorn.run("fast:app", host="0.0.0.0", port=2809)
