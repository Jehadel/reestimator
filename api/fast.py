from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import joblib
import pandas as pd


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
    return {"greeting": "Hell world"}

@app.get("/predict") # => Step to do when we have our predict function
def predict(surface, pieces, surface_terrain, dependancy, Arrondissement10, Arrondissement11,
            Arrondissement12, Arrondissement13, Arrondissement14,
            Arrondissement15, Arrondissement16, Arrondissement1,
            Arrondissement2, Arrondissement3, Arrondissement4, Arrondissement5,
            Arrondissement6, Arrondissement7, Arrondissement8, Arrondissement9,
            is_house,
            is_appart):  # add parameters to execute the function
    """Enter the parameters used to execute the predict API,
    to return the price per squared meter"""
    param_dict = {
        "surface_reelle_bati":  [int(surface)],
        "nombre_pieces_principales": [int(pieces)],
        "surface_terrain": [int(surface_terrain)],
        "Dependency": [int(dependancy)],
        "Marseille 10e Arrondissement": [int(Arrondissement10)],
        "Marseille 11e Arrondissement": [int(Arrondissement11)],
        "Marseille 12e Arrondissement": [int(Arrondissement12)],
        "Marseille 13e Arrondissement": [int(Arrondissement13)],
        "Marseille 14e Arrondissement": [int(Arrondissement14)],
        "Marseille 15e Arrondissement": [int(Arrondissement15)],
        "Marseille 16e Arrondissement": [int(Arrondissement16)],
        "Marseille 1er Arrondissement": [int(Arrondissement1)],
        "Marseille 2e Arrondissement": [int(Arrondissement2)],
        "Marseille 3e Arrondissement": [int(Arrondissement3)],
        "Marseille 4e Arrondissement": [int(Arrondissement4)],
        "Marseille 5e Arrondissement": [int(Arrondissement5)],
        "Marseille 6e Arrondissement": [int(Arrondissement6)],
        "Marseille 7e Arrondissement": [int(Arrondissement7)],
        "Marseille 8e Arrondissement": [int(Arrondissement8)],
        "Marseille 9e Arrondissement": [int(Arrondissement9)],
        "Appartement": [int(is_house)],
        "Maison": [int(is_appart)]
    }
    X_pred=pd.DataFrame(param_dict)
    model_pred = joblib.load("../RandomForest.joblib")
    reestimodel= model_pred.predict(X_pred)
    y_pred = dict(reestimodel=reestimodel[0])
    reesscore = model_pred.score(X_pred, y_pred)

    return dict(reestimodel=reestimodel[0])
    # return y_pred, reesscore


if __name__ == "__main__":
    uvicorn.run("fast:app", host="0.0.0.0", port=2809)
