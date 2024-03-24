from fastapi import FastAPI,Query
import joblib
import numpy as np
import pandas as pd
from typing import List
import csv


app = FastAPI()

model = joblib.load('ml.joblib')

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML Model API"}

@app.post("/predict/")
def predict(data: dict):

    latitude = data['latitude']
    longitude = data['longitude']
    timestamp = pd.to_datetime(data['timestamp'], format='%d-%m-%Y %H:%M')

    input_data = np.array([[latitude, longitude, timestamp.hour, timestamp.dayofweek,
                            timestamp.day, timestamp.month, timestamp.year]])

    predictions = {}
    for act, rc in model.items():
        pred = rc.predict(input_data)[0]
        predictions[act] = pred

    return {"predictions": predictions}

def fetch_data(latitude: float, longitude: float) -> List[dict]:
    data = []
    with open('data.csv', newline='') as csvfile:  
        reader = csv.DictReader(csvfile)
        for row in reader:
            if float(row['latitude']) == latitude and float(row['longitude']) == longitude:
                data.append(row)
    return data

@app.get("/data/{latitude}/{longitude}")
async def get_data(latitude: float, longitude: float):
    return fetch_data(latitude, longitude)
