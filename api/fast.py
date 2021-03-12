
import pandas as pd
import numpy as np
import joblib
import os
import time
import shutil
import json
from api.CacheModel import CacheModel
from PIL import Image
from pylab import array
from fastapi import FastAPI, Response, Request, Header, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def read_imagefile(file) -> Image.Image :
    img = Image.open(file)
    img = img.convert('1') # convert image to black and white
    img = img.resize((28,28), Image.ANTIALIAS)
    img = np.expand_dims(array(img), axis=-1)
    img = img / 255
    img = np.expand_dims(array(img), axis=0)
    return array(img)

@app.on_event("startup")
async def startup_event():
    '''
    On api startup, load and store models in mem  
    '''
    print("load model ...")
    dirname = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(dirname,'models','my_model1')
    model = load_model(model_path)
    CacheModel.getInstance().setModel(model)
    print("model is ready ...")

@app.get("/")
def index():
    return {"Doodle Recognition API": "OK"}


@app.post("/predict/")
def predict(response : Response, inputImage : UploadFile = File(...)):

    ''' 
    Temp image
    '''
    temp_image = f'{str(int(time.time()))}-{inputImage.filename}'
    with open(temp_image, "wb") as buffer:
        shutil.copyfileobj(inputImage.file, buffer)
 
    '''
    Prediction worker
    '''
    # Extraction image
    img = read_imagefile(temp_image)

    # prediction
    pred = CacheModel.getInstance().getModel().predict(img)

    '''
    Delete temp image
    '''
    if os.path.exists(temp_image):
        os.remove(temp_image)

    '''
    Build response
    '''
    classes = []
    with open('./api/params.json', 'rb') as f:
        params = json.load(f)
        nb_classes = params['number_of_classes']
        classes = params['classes'][:nb_classes]

    predict10 = (pred[0] > 0.1)

    prediction = {}
    cpt = 0
    for bool in predict10:
        if bool:
            prediction[classes[cpt]] = str(round(pred[0][cpt]*100, 2))
        cpt += 1
    
    response_prediction = {"prediction" : prediction}
    response.status_code = 200 
    response.headers["Content-Type"] = "application/json"
    return response_prediction
