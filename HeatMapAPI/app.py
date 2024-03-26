from fastapi import FastAPI
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Model API"}

@app.get("/predict/")
async def predict():
    df = pd.read_csv('data.csv')

    X = df[['latitude', 'longitude', 'act379', 'act13', 'act279', 'act323', 'act363', 'act302']]
    y = df[['latitude', 'longitude']]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    rf_regressor = RandomForestRegressor(n_estimators=10, random_state=5)
    rf_regressor.fit(X_scaled, y)

    predicted_coordinates = {}

    for act_no in df.columns[2:]:
        act_data = df[df[act_no] == 1]
        act_coordinates = act_data[['latitude', 'longitude']].values.tolist()

        act_coordinates_formatted = [{"lat": lat, "lng": lng} for lat, lng in act_coordinates]

        predicted_coordinates[act_no] = act_coordinates_formatted

    return predicted_coordinates

