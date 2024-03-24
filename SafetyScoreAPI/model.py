import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv('data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M')


df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['day_of_month'] = df['timestamp'].dt.day
df['month'] = df['timestamp'].dt.month
df['year'] = df['timestamp'].dt.year

X = df[['latitude', 'longitude', 'hour', 'day_of_week', 'day_of_month', 'month', 'year']]
y = df[['act379','act13','act279','act323','act363','act302']]

from sklearn.model_selection import train_test_split
X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=0.2,random_state=42)

classifier = {}
for act in y.columns:
    rc = RandomForestClassifier(n_estimators=100,random_state=42)
    rc.fit(X_train , y_train[act])
    classifier[act] = rc

predictions = {}
for act,rc in classifier.items():
    predictions[act] = rc.predict(X_test)

joblib.dump(classifier, 'ml.joblib')
    

