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
    return {"greeting": "Hello world"}

@app.get("/predict") # => Step to do when we have our predict function
def predict(): # add parameters to execute the function
    """Enter the parameters used to execute the predict API,
    to return the price per squared meter"""
    # param_dict = {
    #     "parameters": parameters # ex parameters : number of room, surface, name of municipality7
    # }
    # X_pred=pd.DataFrame(param_dict)
    # model_pred = joblib.load("../model.joblib")
    # reestimodel= model_pred.predict(X_pred)

    # return dict(reestimodel=reestimodel[0])


if __name__ == "__main__":
    uvicorn.run("fast:app", host="0.0.0.0", port=2809)
