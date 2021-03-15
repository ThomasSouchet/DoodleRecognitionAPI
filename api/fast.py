
import pandas as pd
import numpy as np
import joblib
import os
import time
import shutil
import json
import operator
from api.CacheModel import CacheModel
from PIL import Image
from pylab import array
from fastapi import FastAPI, Response, Request, Header, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import tensorflow_addons as tfa

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
    img = img.resize((28,28), Image.ANTIALIAS)
    img = np.expand_dims(array(img), axis=(0, -1))
    img = img / 255
    return img

# @app.on_event("startup")
# async def startup_event():
#     '''
#     On api startup, load and store models in mem  
#     '''
#     print("load model ...")
#     dirname = os.path.dirname(os.path.dirname(__file__))
#     model_path = os.path.join(dirname,'models','my_model1')
#     model = load_model(model_path)
#     CacheModel.getInstance().setModel(model)
#     print("model is ready ...")

@app.get("/")
def index():
    return {"Doodle Recognition API": "OK"}

@app.post("/predict/")
def predict(response : Response, modelName: str = Form(...), numClass: int = Form(...), inputImage : UploadFile = File(...)):

    print(modelName)
    print(numClass)
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
    #pred = CacheModel.getInstance().getModel().predict(img)
    dirname = os.path.dirname(os.path.dirname(__file__))
    model_path = os.path.join(dirname,'models',modelName)
    model = load_model(model_path)
    pred = model.predict(img)

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
        classes = params['classes'][:numClass]
        
    predict = [int(pred*100) for pred in pred[0]]

    prediction = {}
    cpt = 0
    for val in predict:
        if val > 0:
            prediction[classes[cpt]] = predict[cpt]
        cpt += 1
    
    prediction = dict(sorted(prediction.items(), key=operator.itemgetter(1), reverse=True))
    
    final_prediction = {}
    cpt = 0
    for key, value in prediction.items():
        if cpt < 5:
            final_prediction[key] = str(value)
        else:
            break
        cpt += 1
        
    response_prediction = {"prediction" : final_prediction}
    response.status_code = 200 
    response.headers["Content-Type"] = "application/json"
    return response_prediction
