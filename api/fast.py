
import pandas as pd
import joblib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"Doodle Recognition API": "OK"}


@app.get("/predict/")
def predict():

    # build X ⚠️ beware to the order of the parameters ⚠️
    # X = pd.DataFrame(dict())

    # ⚠️ TODO: get model from GCP

    # pipeline = get_model_from_gcp()
    # pipeline = joblib.load('model.joblib')

    # make prediction
    # results = pipeline.predict(X)

    # convert response from numpy to python type
    # pred = float(results[0])

    # return dict(prediction=pred)
    return {"Prediction": "It's a cat !!!"}